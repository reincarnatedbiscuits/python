'''
    return_word_frequency():
        Returns the number of occurrences of a word, default in alphabetical order
    
    Enhancements:
        By highest frequency, then by alphabetical order [done]
        Be able to choose (a) alphabetically or (b) highest frequency then alphabetically
        have an ignore words list -- start static at first [done]
            could be another file
        input a file dynamically through passed argument or through UI
        some kind of GUI (for input file, for output)

        long term: "grab some number of reqs" -> files -> parse all files in this folder/subfolder
        then return all occurrences (for file in os.dir(directory))
'''

import collections

def findOccurrences(s, ch):
    return [i for i, letter in enumerate(s) if (letter == ch) and ch.isalpha()]

def return_word_frequency(**kwargs):
    # Open a file, C:\temp\python\word_frequency\sample.txt in read mode 
    text = open("C:\\temp\\python\\word_frequency\\sample.txt", "r")

    # Create an empty dictionary
    d = dict() 

    # Loop through each line of the file
    for line in text: 
        # Strip leading spaces and newline
        line = line.strip()

        punctuation_list = [",", ";", ":", ".", "[", "]", "&", "(", ")"]
        for punctuation in punctuation_list:
            line = line.replace(punctuation, "")

        ignore_list = ["and", "as", "at", "or", "for", "a", "an", "be", "by", "do", "on", "of", "the", "to", "in", "with"]

        # convert everything to lowercase (avoids case mismatch)
        line = line.lower() 

        # Split the line into words 
        words = line.split(" ") 
                            

        # Iterate over each word in line 
        for word in words: 
            # Check if the word is already in dictionary 
            if (word in d) and (word not in ignore_list): 
                # Increment count of word by 1 
                d[word] = d[word] + 1
            elif (word not in ignore_list): 
                # Add the word to dictionary with count 1 
                d[word] = 1

    if kwargs.get('runtype')=="alphabetical":
        # put the dictionary into an OrderedDict (easier to read in alphabetical order)
        od = collections.OrderedDict(sorted(d.items()))

        # Print the contents of dictionary -- sorted by word in alphabetical order
        for key, value in od.items():
            print(key, ":", value) 
    elif kwargs.get('runtype')=="frequency":
        # sort by frequency descending, then word in alphabetical order: this results in a list of tuples  (word, frequency)
        # print(sorted(d.items(), key=lambda x: (-x[1], x[0])))

        l = sorted(d.items(), key=lambda x: (-x[1], x[0]))

        for item in l:
            print(item[0], ":", item[1])
        
return_word_frequency(runtype='alphabetical')

# if I want to get back in the dict certain items based on value: [k for k, v in dict1.items() if v == 4]
# for instance, the maximum is 4
