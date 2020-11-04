class TrieNode:

    # Trie node class
    def __init__(self):
        self.count = 0
        self.docCount = 0
        self.children = [None]*128
        self.documents = []

        # isEndOfWord is True if node represent the end of the word
        self.isEndOfWord = False

class Trie:

    # Trie data structure class
    def __init__(self):
        self.root = self.getNode()

    def getNode(self):

        # Returns new trie node (initialized to NULLs)
        return TrieNode()

    def _charToIndex(self,ch):

        # private helper function
        # Converts key current character into index
        # use only 'a' through 'z' and lower case

        return ord(ch)-ord('0')


    def insert(self,key, docID):

        # If not present, inserts key into trie
        # If the key is prefix of trie node,
        # just marks leaf node
        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self._charToIndex(key[level])

            # if current character is not present
            if not pCrawl.children[index]:
                pCrawl.children[index] = self.getNode()
            pCrawl = pCrawl.children[index]

        # mark last node as leaf
        pCrawl.count += 1
        if len(pCrawl.documents) == 0 or pCrawl.documents[len(pCrawl.documents) - 1] != docID:
            pCrawl.docCount += 1
            pCrawl.documents += [docID]
        pCrawl.isEndOfWord = True
        return True

    def search(self, key):

        # Search key in the trie
        # Returns true if key presents
        # in trie, else false
        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self._charToIndex(key[level])
            if not pCrawl.children[index]:
                return False
            pCrawl = pCrawl.children[index]
        return pCrawl
        #return pCrawl != None and pCrawl.isEndOfWord
