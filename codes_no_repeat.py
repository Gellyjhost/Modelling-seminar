import math
import numpy as np
import timeit
import sys
sys.setrecursionlimit(100000)
#Initial functions________________________________________________________________________________________________________________________________________
def findmax(tosort):  #finds the maximum of a list consisting of sequences of positive numbers
    maximum = 0
    for list in tosort:
        if list[0]>max:
            maximum = list[0]

    return maximum

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

def countingSort(arr,maximum,size):# python program for counting sort. The overall complexity of the algorithm is O(m+n)
    output = [0] * size
    # count array initialization
    count = [0] * maximum

    # storing the count of each element 
    for m in range(0, size):
        count[arr[m][0]] += 1

    # storing the cumulative count
    for m in range(1, maximum):
        count[m] += count[m - 1]

    # place the elements in output array after finding the index of each element of original array in count array
    m = size - 1
    while m >= 0:
        output[count[arr[m][0]] - 1] = arr[m]
        count[arr[m][0]] -= 1
        m = m- 1

    for m in range(0, size):
        arr[m] = output[m]

def sorted_set(n):#sorts a list of natural numbers from 1 to n by the length of their collatz sequence
    tosort = []
    maximum = 0
    for x in range(1,n+1):
        list = number_list(x)
        length = len(list)
        if length > maximum:
            maximum = length
        tosort.append([length,x])
    maximum = maximum + 1
    countingSort(tosort,maximum,n)
    tosort.reverse()
    nlist = []
    for element in tosort:
        nlist.append(element[1])
    return nlist

def condensed_set(nlist,biglist): #creates a non repeating list of sequences
    if nlist == []:
        return biglist
    else:
        list = number_list(nlist[0])
        biglist.append(list)
        del nlist[0]
        for item in list:
            if item in nlist:
                x = nlist.index(item)
                del nlist[x]
        return condensed_set(nlist,biglist)

def get_sequence(n): #creates a non repeating list of sequences for numbers from 1 to n
    nlist = sorted_set(n)
    biglist = []
    return condensed_set(nlist,biglist)

def test(n): #tests the time and size of the reduced biglist
    start = timeit.default_timer()
    
    sys.setrecursionlimit(100000)
    x = get_sequence(n)
    stop = timeit.default_timer()
    
    print("The time it takes to generate a set of non-repeating Collatz sequences for the first ",n, "natural numbers is ",stop - start, " seconds.")
    print('The size of the set is ', len(x), ".")  

    start = timeit.default_timer()

    sys.setrecursionlimit(100000)
    y = big_list(n)
    print(len(y))

    stop = timeit.default_timer()
    print("The time it takes to generate a set of Collatz sequences for the first ",n, "natural numbers is ",stop - start, " seconds.")
    print('The size of the set is ', len(y),".")  
