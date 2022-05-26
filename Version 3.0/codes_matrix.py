import math
import numpy as np
import sys

#Initial functions________________________________________________________________________________________________________________________________________

def findmax(biglist):  
    find_max = []
    for list in biglist:
        find_max.append(max(list))
    return max(find_max)

def number_list(x): #create a sequence of number using the collatz function that starts from x, then revserse it backwards.
    list = []
    list.append(x)
    while not x == 1:
        j = x % 2
        if j == 0:
            x=int(x/2)
        if j == 1:
            x = int((3*x)+1)
        list.append(x)
    
    list.reverse()
    return list


def big_list(n):#create a list of sequences found using the number_list function
    l = []
    for x in range(1,n+1):
        q = number_list(x)
        l.append(q)
    
    #final = []
    #for list in l:
        #intermediate = []
        #for element in list:
            #object = point()
            #object.number = element
            #intermediate.append(object)
        #final.append(intermediate)
    return l


def create_array(n): #create a nxn matrix of 0's(the most memory efficient).
    a = []
    for number in range(0,n+1):
        list = []
        for number in range(0,n+1):
            list.append(0)
        a.append(list)
    return a

def change_array(a, list,number): #increases the frequency of a certain sequence by 1 in the matrix.
    for index in range(len(list)-1):
        #a[list[index]][list[index+1]] = number
        a[list[index]][list[index+1]] = a[list[index]][list[index+1]] + 1
    return a


def create_array2(biglist,a): #creates a matrix containing information of a list of sequences. For each element in the matrix, n_xy = 1 if there is an edge from x to y, n_xy = 0 if there is no edge from x to y.
    for list in biglist:
        a = change_array(a,list,1)
    
    return a


def initialize_array(a): #finds all of the splits in the tree and increases the frequency of everything before the split.
    for rowindex in range(0,len(a)): #for each row in the matrix
        x = 0
        for item in a[rowindex]:
            if item == 1:
                x=x+1
        # count the number of elements in the row. This represents the split.
        
        if x > 1:
            numberlist = number_list(rowindex)
            for index in range(0,len(numberlist)-1):
                a[numberlist[index]][numberlist[index+1]] = a[numberlist[index]][numberlist[index+1]] + x-1

        # increases the frequency of the sequence before the split by 1.
    
    return a

def condense_list1(array,row,list): #recursion that finds one condensed sequence from the edge matrix
    count = True
    for index in range(0,len(array[row])):
        if array[row][index] != 0:
            count = False
            number = index
            break
    
    if  count:
        return list
    else : 
        array[row][number] = array[row][number]-1
        list.append(number)

        return condense_list1(array,number,list)


def condense_list2(array):
    time = array[1][2]
    list = []
    for i in range(0,time):
        l = [1]
        condense_list1(array,1,l)
        list.append(l)
    
    return list

def store_data(n): #creates a condensed list of sequences, storing all data
    n=n+1
    biglist = big_list(n)
    a = create_array(findmax(biglist))
    matrix1 = initialize_array(create_array2(biglist,a))
    list = condense_list2(matrix1)

    return list
  
def create_matrix(n): #creates a matrix storing edge data
    n=n+1
    biglist = big_list(n)
    a = create_array(findmax(biglist))
    #matrix1 = initialize_array(create_array2(biglist,a))
    matrix1 = create_array2(biglist,a)

    return matrix1

def change1(array,row,index,number,max):
    length = len(array)
    if number == 0:
        return array
    else:
        for i in range(1,number+1):
            if row-i > 0 and row-i < length:
                array[row-i][index] = array[row-i][index]+ number/max
                if index+i > 0 and index+i < length:
                    array[row-i][index+i] = array[row-i][index+i]+ number/max
                if index-i > 0 and index-i < length:
                    array[row-i][index-i] = array[row-i][index-i]+ number/max
            if row+i > 0 and row+i < length:
                array[row+i][index] = array[row+i][index]+ number/max
                if index+i > 0 and index+i < length:
                    array[row+i][index+i] = array[row+i][index+i]+ number/max
                if index-i > 0 and index-i < length:
                    array[row+i][index-i] = array[row+i][index-i]+ number/max
            if index+i > 0 and index+i < length:
                array[row][index+i] = array[row][index+i] + number/max
            if index-i > 0 and index-i < length:
                array[row][index-i] = array[row][index-i] + number/max
        number = number - 1
        return(array,row,index,number)



def crop(array):
    length = int(len(array) / 1.1)
    array = array[: len(array)- length]
    
    for rowindex in range(len(array)):
        array[rowindex] = array[rowindex][: len(array[rowindex])- length]

    return array



def filter(n):
    matrix = create_matrix(n)
    array = create_matrix(n)

    findmax = []

    for rowindex in range(len(matrix)):
        for columnindex in range(len(matrix)):
            if matrix[rowindex][columnindex] != 0:
                findmax.append(matrix[rowindex][columnindex])
    
    maximum = max(findmax)
    for rowindex in range(len(matrix)):
        for columnindex in range(len(matrix)):
            n = matrix[rowindex][columnindex]*10
            if matrix[rowindex][columnindex] != 0:
                array[rowindex][columnindex] =  n/maximum 
                change1(array,rowindex, columnindex, n ,maximum)

    return array



#print(crop(filter(5)))
#print(filter(5))