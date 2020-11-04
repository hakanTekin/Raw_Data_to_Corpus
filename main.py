import os
import io
import string

import myTrie


### PART ONE BEGINNING ###
# Normalization #

# Remove the punctiation marks from the given line
# Create a copy and do the operation on it


def RemovePunctions(line):
    x = line
    if line[0] != '<':
        for i in range(line.__len__()):
            if (ord(line[i]) > 32 and ord(line[i]) < 48) or (ord(line[i]) > 90 and ord(line[i]) < 97) or (ord(line[i]) > 57 and ord(line[i]) < 65):
                x = x.replace(line[i], ' ')
    return x


# Remove the extra spaces
# If the ending or beginning starts with a space, it is useless
# If there are 2 consecutive spaces, it is useless
# Create a copy of the line and operate on it then return it
def RemoveExtraSpaces(line):
    line.replace('  ', ' ')
    if (line[0] == ' '):
        line = line[1:]
    # TODO: Remove the last char if it is space too
    return line


# Convert the line to all uppercase
def ConvertToUppercase(line):
    return line.upper()


# Convert every turkish letter into its english counterpart
def ConvertToEnglish(line):
    x = line
    x = x.translate(str.maketrans("ğĞıİöÖüÜşŞçÇðýþÐÝÞ", "gGiIoOuUsScCgisGIS"))
    return x


# After each step is complete, remove the  remaining non ASCII characters
# If the resulting line is empty, then return None
def RemoveNonAscii(line):
    x = line
    for i in range(len(line)):
        if (ord(line[i]) > 127):
            x = x.replace(line[i], '')
    return x


# Step 1 - Normalizing the data
# - Remove punctiation mark
# - Remove EXTRA spaces (not word seperating ones :) )
# - Convert to upper case
# - Convert turkish characters to english

def NormalizeData(file):
    with open('temp_normalized_first.txt', 'w', encoding='cp1254', errors='replace') as new_file:
        try:
            # This line should read line by line
            for original_file_line in file:
                line = RemovePunctions(original_file_line);
                line = RemoveExtraSpaces(line)
                line = ConvertToUppercase(line)
                line = ConvertToEnglish(line)
                line = RemoveNonAscii(line)
                new_file.write(line)
            return new_file
        except Exception as e:
            print(e)
            return None

            ### PART ONE ENDING ###

            ### PART TWO BEGINNING ###
            # Lexicon #


# file should be named 'radikal.sorted.terms'


# Create a trie structure for generating the lexicon,
# The trie should have 2 values:
# - number of documents a word is found in
# - total number of occurence

# The results should be printed onto a text file in format => '%s\t%d\t%d'
def CreateLexicon(file):
    if file.closed:
        file = open(file.name, 'r')

    trie = myTrie.Trie()  # This is the trie data structure
    docID = 0
    docs_file = open('id.docs', 'w')
    for line in file:
        if line.__contains__("<INS"):
            docID+=1
            docs_file.write(f'{line[line.index("=")+1 : line.index(".HTML")]}\t{docID}\n')

        if line[0] != '<':
            line = line[:len(line) - 1] #Remove line terminator character
            x = line.split(' ')
            for word in x:
                try:
                    if(len(word) > 0):
                        vall = trie.insert(word, docID)
                except Exception as e:
                    print(e)

    y = trie.search("BURAYA")
    print(y.documents)
    print(y.count)
    print(len(y.documents))
    #Create a new file for writing lexicon
    #with open('radikal.sorted.terms', 'w+') as sorted_file:
        #Write each word to file using DFS
        #WriteTrie(sorted_file, trie.root)

def WriteTrie(file, root, word):
    for i in root.children:
        WriteTrie(file, i)

def TabSeperatedString(word, count, docCount):
    return f'{word}\t'
    ### PART TWO ENDING ###

    ### PART THREE BEGINNING ###
    ### PART THREE ENDING ###


if __name__ == '__main__':
    print(f'Hi, Hakan')  # Press Ctrl+F8 to toggle the breakpoint.
    if (os.path.exists('radikal.corpus')):
        with open('radikal.corpus', 'r', encoding='cp1254', errors='replace') as file:
            try:
                # Start the process if there is a file
                new_file = NormalizeData(file)
                if new_file is not None:
                    CreateLexicon(new_file)
            except Exception as e:
                # Handle errors
                print(e)