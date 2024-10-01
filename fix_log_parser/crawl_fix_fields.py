import requests
import re

# can be 4.2 or 4.4
fixversion = '4.4'

for counter in range(200, 957):
    url = f'https://www.onixs.biz/fix-dictionary/{fixversion}/tagNum_{counter}.html'

    response = requests.get(url)

    html_response = response.text

    skip_text = [r'See <a href=".*html">Appendix', 
                 r'As defined in the NYSE Stock and bond Symbol Directory and in the AMEX Fitch Directory']
    
    replaced_in_fix_43 = ['Deprecated in FIX 4.3', 'Removed in FIX 4.4', 'Replaced in FIX 4.3', 'Deprecated in FIX 4.4', 
                          'Replaced in FIX 4.4']
    
    # skip_tags = [8, 100, 205, 305, 308, 310, 347, 418, 421] # for FIX 4.2
    skip_tags = [8, 30, 100, 166, 201, 204, 205, 207, 219, 221, 239, 275, 305, 308, 347, 418, 421, 423, 456, 459, 462, 463] # for FIX 4.4

    # and skip fix tag 8

    # only do stuff if we find "Valid values:"
    if "Valid values:" in html_response and counter not in skip_tags:
        # processing here
        # only get the next <p> fields until non <p> field
        found_p_tag = False
        already_processed_section = False

        for text in replaced_in_fix_43:
            if re.search(text, html_response):
                already_processed_section = True
                print(f'Replaced in FIX 4.3 or 4.4: (check the {counter} tag)')

        # skip if "See Appendix"
        for text in skip_text:
            if re.search(text, html_response):
                already_processed_section = True
                print(f'Appendix desired (check the {counter} tag)')        
        
        remainder = html_response[html_response.index("Valid values:"):]

        while not already_processed_section:
            if not found_p_tag:
                print('\t\'' + str(counter) + '\': {')
            for line in remainder.split('\n'):
                if '=' in line and '<del>' not in line:
                     # need to find <p> tag
                    if "<p>" in line and not already_processed_section:
                        strip_p_tag = line.replace('<p>', '').strip()
                        strip_close_p_tag = strip_p_tag.replace('</p>', '').strip()
                        # get rid of <a href="anything">
                        strip_close_p_tag = re.sub(r'<a href=".*">', '', strip_close_p_tag)
                        # get rid of &lt;*&gt</a>
                        final_strip = re.sub(r'&lt;.*&gt;</a>', '', strip_close_p_tag.strip()).strip()
                        if len(final_strip.split('=')) == 2:
                            (fix_field, line_values) = final_strip.split('=')
                            print('\t\'' + fix_field.strip() + '\'' + ': \'' + line_values.strip() + '\',')
                        elif len(final_strip.split('=')) == 3:
                            (fix_field, line_values, another_line_value) = final_strip.split('=')
                            print('\t\'' + fix_field.strip() + '\'' + ': \'' + line_values.strip() + another_line_value.strip() + '\',')
                        else:
                            print(f'{counter} value is {final_strip}')
                        found_p_tag = True
                    elif found_p_tag and not "<p>" in line:
                        already_processed_section = True
        print('\t},')
