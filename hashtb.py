
class Word:
    def __init__(self, key, cnt, ID):
        self.key = key
        self.cnt = cnt
        self.ID = ID


def hashCalc2(key):
    # sdbm hash algorithm
    hVal = 0
    key = key.lower()
    for i in key:
        num = ord(i)
        hVal = num + (hVal << 6) + (hVal << 16) - hVal
    return hVal


def hashCalc(key):
    # djb2 hash algorithm
    hVal = 5381
    key = key.lower()
    for i in key:
        num = ord(i)
        hVal = ((hVal << 5) + hVal) + num  # hVal * 33 + char
    return hVal % 3010913

class HashTable:
    def __init__(self):
        self.table = [None] * 3010913

    def insert(self, key):
        hash_key = hashCalc(key)
        if self.table[hash_key] is None:  # if this is the first occurrence of this word
            self.table[hash_key] = []  # create a list at current index
            temp = Word(key, 1, hashCalc2(key))  # create a new word
            self.table[hash_key].append(temp)
        else:  # else if this a collision (wanted or not)
            wordID = hashCalc2(key)
            for i in range(0, len(self.table[hash_key])):
                # iterate through every index of word list at hash_key in table
                if wordID != self.table[hash_key][i].ID:
                    # id of current word and i'th word at hash_key do not match
                    # this is an unwanted collision
                    temp = Word(key, 1, hashCalc2(key))  # create a new word
                    self.table[hash_key].append(temp)
                    break
                else:
                    # word already exists in hash table
                    self.table[hash_key][i].cnt += 1  # increment count of word
                    break

    def getCount(self, key):
        # get the number of times a certain word appears in text
        hash_key = hashCalc(key)  # hash the word
        if self.table[hash_key] is not None:
            for word in self.table[hash_key]:  # iterate through word list at hash_key
                if key == word.key:
                    size = word.cnt  # return the count of the matching word
                    return size
        return 0  # word not found in hash table

    def getCounts(self):
        # get dictionary of counts and how many times each count exists
        Dict = {}
        for arr in self.table:  # iterate through hash table
            if arr is not None:
                for word in arr:   # iterate through list of nodes at hash table
                    if word.cnt in Dict.keys():   # if the count already exists as a key in the dict
                        Dict[word.cnt] += 1
                    else:                           # else if count is not yet a key in the dict
                        Dict[word.cnt] = 1
        return Dict  # return dict of all counts and number of repetitions of that count
