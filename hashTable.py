#Class used to create a hash table
class hashTable:
#Initialisation - Class is passed the size, row depth and title of the hash table
    def __init__(self, size, depth, title):
        print("\nCreating:", title)
        self.__size = size
        self.__depth = depth
        self.__table = [[[]for i in range(depth)] for i in range(size)]
#Adds the bucket to the end of the hash table
        self.__table.append([])
        self.__title = title
        print("Created!")

#Method used to apply the hashing function to the record (Number is Passed)
    def hashFunc(self, idNum):
        index = (idNum**2) % self.__size
#Returns the index for the row of the table the record needs to be added to
        return index

#Base Method - Used to add a record to the hash table (Passed the record and a boolean valeue user)
    def addMember(self, record, user):
#Takes the student number from the record, to be used in the hash function
        multer = record[0]
#Calls the hash function in order to determine the row at which the record should be input
        baseIndex = self.hashFunc(multer)
#Takes the row which the record is going to be added to
        comparator = self.__table[baseIndex]
        added = False
#Loops through the items in the row, looking for an empty slot
        for i in range(len(comparator)):
            if not added and not comparator[i]:
#Once an empty slot is found, the record is added
                comparator[i] = record
                added = True
#If the row is full, the record is added to the end of the bucket
        if not added:
            self.__table[-1].append(record)
#User indicates whether or not the record is being added as a part of Rehashing
#If not, a message is displayed to the user, telling them that the member has been added
        if user:
            print("\nMember", multer, "added to table")

#Method used to find the details of a member given the student id number
    def findMember(self, idNum):
#Uses the hash fucntion to determine the row in which the item would have been inserted
        baseIndex = self.hashFunc(idNum)
#Uses the baseIndex to retrieve that row from the hash table
        comparator = self.__table[baseIndex]
#Loops through each item in the row checking if the student number matches any of the records
        for i in range(len(comparator)):
            if comparator[i]:
                if comparator[i][0] == idNum:
#If the record is found, it is returned, and a message is output
                    print("\nMember", idNum, "Found - Table")
                    return comparator[i]
#If not, the method then performs a linear search on the bucket (HIGHLY INEFFICIENT) in order to check if the
        for item in self.__table[-1]:
            if item[0] == idNum:
                print ("\nMember", idNum, "Found - Bucket")
                return item
#If the item is not found in the bucket, a message is returned indicating that the member is not present in the table
        print("\nMember", idNum, "Not Found")

#Method used to remove a member from the table
    def removeMember(self, idNum):
        baseIndex = self.hashFunc(idNum)
        comparator = self.__table[baseIndex]
        removed = False
#Loops through each item in the row that the item should be found in
        for i in range(len(comparator)):
            if comparator[i]:
#If the item is found in the row
                if comparator[i][0] == idNum:
#The method used to remove an item from a row is called
                    self.removeHash(self.__table.index(comparator), i)
#And a suitable message is displayed
                    print("\nMember", idNum, "removed from table")
                    removed = True
#If the record has been removed from the row
        if removed:
#Each record in the bucket is checked to see if it could fill the now-empty slot
            i = 0
            while len(self.__table[-1]) > i:
                print(i)
                finish = self.hashFunc(self.__table[-1][i][0])
                if finish == baseIndex:
#If so, the record is added to the table again, and removed from the bucket
                    self.addMember(self.__table[-1][i], False)
                    del self.__table[-1][i]
                i += 1
        else:
#If the item has not been removed from the row, a linear search is applied to the bucket to see if the record exists
            for item in self.__table[-1]:
#If the record is found
                if item[0] == idNum:
#The built in pop function is used to remove the item from the bucket
                    self.__table[-1].pop(self.__table[-1].index(item))
#And a suitable message is displayed
                    print("\nMember", idNum, "removed from table")
                    removed = True
#If the record has still not been removed, then it does not exist
        if not removed:
#So a suitable message is displayed
            print("\nMember", idNum, "not found")

#Sub-method used to remove an item from a certain point in the table (Passed the row and column)
    def removeHash(self, row, column):
#Resets the table slot to []
        self.__table[row][column] = []
#Loops through the rest of the row, shifting any items backwards into the empty slots
        for i in range(column+1, 3):
            if self.__table[row][i]:
                self.__table[row][i-1] = self.__table[row][i]
                self.__table[row][i] = []

#Method used to carry out the main portion of the rehashing process
    def rehashFunc(self, tooFew):
        print("\nRehashing:", self.__title)
#Sets a list to contain all of the records already stored in the table
        newMembs = []
#Loops through every slot in the table
        for i in range(self.__size):
            for j in range(3):
#If the slot contains a record
                if self.__table[i][j]:
#The record is added to the newMembs list
                    newMembs.append(self.__table[i][j])
#Adds all of the items in the bucket to the newMembs list
        for item in self.__table[-1]:
            newMembs.append(item)
#If the rehashing requires the number of rows to be cut down
        if tooFew:
#The size of the table is halfed
            self.__size = self.__size // 2
#With the new size, the table is reset
            self.__table = [[[]for i in range(self.__depth)] for i in range(self.__size)]
            self.__table.append([])
#If the rehashing requires the number of rows to increase
        else:
#The size of the table is doubled
            self.__size = self.__size * 2
#With the new size, the table is reset
            self.__table = [[[]for i in range(self.__depth)] for i in range(self.__size)]
            self.__table.append([])
#Each item in the newMembs list is the re-added to the newly reset table
        for item in newMembs:
            self.addMember(item, False)
        print("Rehashed!")
#The table is printed using the printTable method
        self.printTable()

#Method used to carry out the UI portion of rehashing
    def rehash(self):
        rowsUsed = 0
#Loops through the table, determining how many rows contain records (Used to determine the load factor)
        for i in range(self.__size):
            if self.__table[i][0]:
                rowsUsed += 1
#Calculates the load factor as a percentage
        percentage = (rowsUsed / self.__size) * 100
#Rounds the percentage to make it more readable
        percentage = round(percentage, 2)
#If the load factor is above the recommended maximum (75%)
        if percentage > 75:
#A suitable message is displayed
            print("\nMore than 75% (", percentage, "% ) of rows used")
            print("Hash Table needs Rehashing")
#The table is rehashed
            self.rehashFunc(False)
#If the load factor is below the recommended minimum (25%)
        elif percentage < 25:
#A suitable message is displayed
            print("\nLess than 25% (", percentage, "% ) of rows used")
            print("Hash Table needs Rehashing")
#The table is rehashed
            self.rehashFunc(True)
#If the load factor is within the recommended range (25-75%)
        else:
#A suitable message is displayed
            print("\nAn appropriate number of rows used (", percentage, "% )")
            print("Hash Table does not need Rehashing")

#Method used to print the table (USED FOR TESTING)
    def printTable(self):
        print("\nHash Table:", self.__title)
#Prints each row on a new line
        for i in range(self.__size):
            print ("Row", i+1, ":", self.__table[i])
        print("Bucket:", self.__table[-1])



#TESTING
#Creates a hash table with title: Students, number of rows: 19, and row depth: 3
hash = hashTable(19, 3, "Students")

#List containing each of the student records (Provided Data Set)
members = [[123,"Robin","AB4"], [124,"Nguyen","HD12"], [125,"Jev","L18"], [126,"Will","OX5"], [127,"Lily","CH3"], [128,"Jonny","YO12"], [129,"Clara","BS1"], [130,"Callum","BA1"]]

#Adds each record to the hash table
for item in members:
    hash.addMember(item, True)

#Prints the hash Table
hash.printTable()

#Checks if the hash table needs rehashing
hash.rehash()

#Adds another member to the hash table
hash.addMember([131,"Kirsten","SE2"], True)

hash.printTable()

#Removes a member from the hash table
hash.removeMember(124)

hash.printTable()

hash.rehash()

#Testing for the rehashing method
smol = hashTable(5, 3, "Smol")
for i in range(10):
    smol.addMember([i, "Tom", "Dubai"], True)
smol.printTable()
smol.rehash()
smol.removeMember(1)
smol.printTable()
smol.rehash()
