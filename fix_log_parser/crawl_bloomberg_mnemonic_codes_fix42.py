import requests
import re

url = f'https://www.onixs.biz/fix-dictionary/4.2/app_c.html'

response = requests.get(url)

html_response = response.text

# the first is Abidjian

first_location = html_response.index('fixTableBorder')
remaining1 = html_response[first_location:]
pare_down = remaining1.index('<tr class="tr1">')
ending_location = remaining1.index('<h4>Other (assinged numeric values):</h4>')
remaining = remaining1[pare_down:ending_location]
replace_new_lines = ''.join(remaining.splitlines())
replace_text = [r'<tr class=\"tr.\">', r'<tr>', r'<\/tr>', r'<\/td>', r'<br>',
                r'<td class=\"white\" valign=\"top\">',
                r'<table.*class=\"white\">',
                r'<tbody>', r'<\/tbody>', r'<\/table>']



# replace_with_newline = []

for text in replace_text:
    while re.search(text, replace_new_lines):
        replace_new_lines = re.sub(text, '', replace_new_lines)
    while re.search('&nbsp;', replace_new_lines):
        replace_new_lines = re.sub('&nbsp;', ' ', replace_new_lines)

# get rid of first <td>
proper = replace_new_lines[replace_new_lines.index('<td>')+4:]

exchange_names = []
exchange_codes = []
list_exchanges = proper.split('<td>')
counter = 0
for item in list_exchanges:
    counter += 1
    if counter % 2 == 1:
        exchange_names.append(item.strip())
    else:
        exchange_codes.append(item.strip())

# print(exchange_codes)

res = dict(zip(exchange_names, exchange_codes))
print(res)
