from tkinter import N
import numpy as np
import timeit
import sys
import random

sys.setrecursionlimit(100000)


def count(n): #count the length of the collatz sequence
    count = 0
    while n != 1:
        if n % 2 == 0:
            n = n/2
        else:
            n = int(3*n + 1)
        count = count + 1
    return count

def find(threshold): # finds the longest sequence under a threshold
    temp = 0
    for n in range(2, threshold):
        k = count(n)
        if k <= temp:
            pass
        else:
            temp = k
            number = n

    return number

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
    
    return list


def coord(x):
    list = []
    while not x == 1:
        if x%8 == 0:
            list.append("N")
        if x%8 == 1:
            list.append("NE")
        if x%8 == 2:
            list.append("E")
        if x%8 == 3:
            list.append("SE")
        if x%8 == 4:
            list.append("S")
        if x%8 == 5:
            list.append("SW")
        if x%8 == 6:
            list.append("W")
        if x%8 == 7:
            list.append("NW")
        
        j = x % 2
        if j == 0:
            x=int(x/2)
        if j == 1:
            x = int((3*x)+1)
    
    return list

def coord_rand(length):
    list = []
    for time in range(0,length):
        x = random.randrange(1,9)
        if x == 8:
            list.append("N")
        if x == 7:
            list.append("NE")
        if x == 6:
            list.append("E")
        if x == 5:
            list.append("SE")
        if x == 4:
            list.append("S")
        if x == 3:
            list.append("SW")
        if x == 2:
            list.append("W")
        if x == 1:
            list.append("NW")
    return list



def test(n): #tests the time and size of the reduced biglist

    start = timeit.default_timer()

    k = find(n)
    print(k)  
    print(count(k))  
    stop = timeit.default_timer()
    
    print('The time for find() is ', stop - start, ".") 

#test(10000000)



