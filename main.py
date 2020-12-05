
class HashTable:
    def _init_(self):
        self.list = [None]*10000000000
        self.max = 0


class Word:
    def _init2_(self):
        self.key = None
        self.count = 0
        self.id = 0


# def hashCalc(key):
#     # FNV-1a hash algorithm
#     hVal = 14695981039346656037
#     for i in key:
#         num = ord(i)
#         if num > 64 or num < 91:
#             num += 32
#         hVal ^= num
#         hVal *= 1099511628211
#     return hVal


def hashCalc2(key):
    # sdbm hash algorithm
    hVal = 0
    for i in key:
        num = ord(i)
        if num > 64 or num < 91:  # convert uppercase to lowercase
            num += 32
        hVal = num + (hVal << 6) + (hVal << 16) - hVal
    return hVal


def hashCalc(key):
    # djb2 hash algorithm
    hVal = 5381
    for i in key:
        num = ord(i)
        if num > 64 or num < 91:  # convert uppercase to lowercase
            num += 32
        hVal = ((hVal << 5) + hVal) + num  # hVal * 33 + char
    return hVal


def insert(self, key):
    hash_key = hashCalc(key)
    if self.list[hash_key] is None:    # if this is the first occurrence of this word
        self.list[hash_key] = []   # create a list at current index
        temp = Word()              # create a new word
        temp.key = key             # assign the key to the word
        temp.count = 1             # set count of word to 1
        temp.id = hashCalc2(key)
        self.list[hash_key].append(temp)
    else:               # else if this a collision (wanted or not)
        wordID = hashCalc2(key)
        for i in range(0, len(self.list[hash_key])):
            # iterate through every index of word list at hash_key in table
            if wordID is not self.list[hash_key][i].id:
                # id of current word and i'th word at hash_key do not match
                # this is an unwanted collision
                temp = Word()      # create a new word
                temp.key = key     # assign the key to the word
                temp.count = 1     # set count of word to 1
                temp.id = hashCalc2(key)
                self.list[hash_key].append(temp)
                break
            else:
                # word already exists in hash table
                self.list[hash_key].count += 1   # increment count of word
                break


def getCount(self, key):
    # get the number of times a certain word appears in text
    hash_key = hashCalc(key)   # hash the word
    if self.list[hash_key] is not None:
        for word in self.list[hash_key]:   # iterate through word list at hash_key
            if key == word.key:
                size = word.count          # return the count of the matching word
                return size
    return 0   # word not found in hash table


def getKMostFrequent(self, k):
    # find top k most used words
    freqList = []           # list to store tuples of all word and word counts
    for arr in self.list:
        if arr is not None:
            for word in arr:
                pair = (word.key, word.count)        # pair <string,int> (word, count)
                freqList.append(pair)
    freqList.sort(key=lambda x: x[1], reverse=True)  # sort list by word count
    return freqList[0:k]    # return list of k most used words

# Driver Code
# parse txt file
# insert each word from txt file into hash table
# 2 options:
#    getCount  (returns integer)
#    getKMostFrequent  (returns list of size k)
