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
            if (ord(line[i]) > 32 and ord(line[i]) < 48) or (ord(line[i]) > 90 and ord(line[i]) < 97) or (
                    ord(line[i]) > 57 and ord(line[i]) < 65):
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
    with open('temp_normalized_first.txt', 'w') as new_file:
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
trie = myTrie.Trie()  # This is the trie data structure


def CreateLexicon(file):
    if file.closed:
        file = open(file.name, 'r')

    docID = 0
    docs_file = open('id.docs', 'w')
    for line in file:
        if line.__contains__("<INS"):
            docID += 1
            docs_file.write(f'{line[line.index("=") + 1: line.index(".HTML")]}\t{docID}\n')

        if line[0] != '<':
            line = line[:len(line) - 1]  # Remove line terminator character
            x = line.split(' ')
            for word in x:
                try:
                    if (len(word) > 0):
                        vall = trie.insert(word, docID)
                except Exception as e:
                    print(e)

    # Create a new file for writing lexicon
    with open('radikal.sorted.terms', 'w+') as sorted_file:
        # Write each word to file using DFS
        WriteTrie(sorted_file, trie.root, "")


def WriteTrie(sf, root: myTrie.TrieNode, word, charIndex=-1):
    if root is None:
        return

    if charIndex > -1:
        c = trie.indexToChar(charIndex)
        word += c
        if root.isEndOfWord:
            v = [word, root.count, root.docCount]
            sf.write(TabSeperatedString(v))

    count = 0
    i: myTrie.TrieNode

    for i in root.children:
        WriteTrie(sf, i, word, count)
        count += 1
    word = word[:len(word) - 1]



def TabSeperatedString(pack):
   x = ''
   for i in pack:
       x+= str(i)
       x+='\t'

   x=x[:len(x)-1]
   x+='\n'
   return x
    ### PART TWO ENDING ###

    ### PART THREE BEGINNING ###


def CreateInvertedIndex(sf):
    WriteToInvertedFile(sf, trie.root, "")
    return sf

def WriteToInvertedFile(sf, root: myTrie.TrieNode, word, charIndex=-1):
    if root is None:
        return
    if charIndex > -1:
        c = trie.indexToChar(charIndex)
        word += c
        if root.isEndOfWord:
            v = []
            v.append(word)
            for x in root.documents:
                v.append(x)
            sf.write(TabSeperatedString(v))

    count = 0
    i: myTrie.TrieNode

    for i in root.children:
        WriteToInvertedFile(sf, i, word, count)
        count += 1
    word = word[:len(word) - 1]
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

        with open('inverted_index.list', 'w') as inverted_index_file:
            CreateInvertedIndex(inverted_index_file)
    else:
        print('File not found. Not doing anything.')
