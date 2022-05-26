import math
import numpy as np
import timeit
import sys
from codes_matrix import filter,create_matrix
from codes_no_repeat import get_sequence 
from codes_randomwalk import coord
import random

sys.setrecursionlimit(100000)
tree = open("tree.txt","w")
#Initial functions________________________________________________________________________________________________________________________________________
def bounding_box (x,y): #change bounding box width and height to (x,y)
    a = str(x)
    b = str(y)
    c = "%%BoundingBox: 0 0 " + a + " " + b +"\n"
    tree.write(c)

def change_origin(x,y): # change origin to (x,y)
    a = str(x)
    b = str(y)
    c = a+" "+ b + " translate\n"
    tree.write(c)


def rotate_page(x): # rotation of the page by x degrees
    a = str(x)
    b = a + " rotate\n"
    tree.write(b)

def draw_line_up(x): 
    b = "0 "+ str(x) + " lineto\n"
    c = "0 0 moveto\n"
    tree.write("newpath\n")
    tree.write(c)
    tree.write(b)
    tree.write("stroke\n\n")

def lineto(x,y,oldx,oldy): #draw line from (oldx,oldy) to (x,y)
    a = str(oldx) +" " + str(oldy) + " moveto\n"
    b = str(x)+ " " + str(y) + " lineto\n"
    tree.write("newpath\n")
    tree.write(a)
    tree.write(b)
    tree.write("stroke\n\n")

def fill_square(x,y,length,grayvalue):
    grayscale(grayvalue)
    a = str(x) +" " + str(y) + " moveto\n"
    b = str(x+length)+ " " + str(y) + " lineto\n"
    c = str(x+length) + " " + str(y+length) + " lineto\n"
    d = str(x) + " " + str(y+length) + " lineto\n"
    e = "closepath\n"
    tree.write("newpath\n")
    tree.write(a)
    tree.write(b)
    tree.write(c)
    tree.write(d)
    tree.write(e)
    tree.write("fill\n")
    tree.write("stroke\n\n")
    

def line_setting(cap, width, join): #set line cap, width, and join
    cap = str(cap)
    width = str(width)
    join = str(join)
    a = cap + " setlinecap\n"
    tree.write(a)
    b= width + " setlinewidth\n"
    tree.write(b)
    c = join + " setlinejoin\n"
    tree.write(c)

def line_width(width): #set line witdth
    width = str(round(width,2))
    b= width + " setlinewidth\n"
    tree.write(b)

def change_RGB(amount,current): #change the current RGB color(input in set) by the amount(input in set).
    new = []
    for n in range(0,3):
        if not current[n] >= 0.99:
            n = current[n] + amount[n]
            new.append(n)
        else:
            new.append(current[n])
    return new

def RGB(set): #set the RGB color to a certain amount
    a = str(round(set[0],2))+" "+str(round(set[1],2))+ " " + str(round(set[2],2)) + " setrgbcolor\n"
    tree.write(a)

def grayscale(value):
    a = str(value) + " " + "setgray\n"
    tree.write(a)

def apoint(x,y,r): #draw a point at (x,y), with radius r
    a = str(x) + " " + str(y) +" " + str(r) + " 0 360 arc\n"
    tree.write("newpath\n")
    tree.write(a)
    tree.write("fill\n")

def findmax(tosort):  
    maximum = 0
    for list in tosort:
        if list[0]>max:
            maximum = list[0]
    return maximum

#Create class point()
class point:
    def __init__(self, x = None, y= None, number = None, freq = None):
        self.x = x
        self.y = y
        self.number = number
        self.freq = freq

# value assignement to each object()______________________________________________________________________________________________________________________________
def assign_coordinate(bigset, angle_even, angle_odd,length): #assign coordinate to each point object according to angle_even and angle_odd
    for set in bigset:
        x = 0
        y = 0
        rotation = 90
        leng = len(set)
        for index in range(0,leng-1):
            #length = length
            j = set[index].number % 2
            if j == 0:
                rotation = rotation + angle_even
                x = x+ round(length*math.cos(math.radians(rotation)), 2)
                y = y+ round(length*math.sin(math.radians(rotation)),2)
                set[index+1].x = x
                set[index+1].y = y
            if j == 1:
                rotation = rotation + angle_odd
                x = x+ round(length*math.cos(math.radians(rotation)),2)
                y = y+ round(length*math.sin(math.radians(rotation)),2)
                set[index+1].x = x
                set[index+1].y = y
        set[0].x = 0
        set[0].y = 0
    
    return bigset




def assign_freq(bigset, biglist0): # count the frequency of each number in each sequence among a large set of sequences, then assign the frequency back to the numbers.
    dictionary = {}
    for list in biglist0:
        for element in list:
            x = element
            if x in dictionary:
                dictionary[x] = dictionary[x]+1
            if not x in dictionary:
                new = {x:1}
                dictionary.update(new)
    for list in bigset:
        for element in list:
            element.freq = dictionary[element.number]
    
    return bigset


#different types of drawing defined on a list of points________________________________________________________________________________________________________________________________________________

def draw_line(biglist):
    compare = []
    for list in biglist:
        for element in list:
            compare.append(element.freq)
    m = 3/max(compare)
    for set in biglist:
        x = len(set)
        for index in range(0,x-1):
            width = m*set[index].freq
            line_width(width)
            lineto(set[index+1].x,set[index+1].y,set[index].x,set[index].y)

def draw_point(biglist):
    #compare = []
    #for list in biglist:
        #for element in list:
            #compare.append(element.freq)
    #m = 3/max(compare)
    for set in biglist:
        for element in set:
            apoint(element.x,element.y, round(math.log(element.freq),2))



#bounding box settings and prerun________________________________________________________________________________________________________________________________________________

def new_bounding_box(largeset): #Creates a fitting bounding box
    x_list = []
    y_list = []
    for list in largeset:
        for element in list:
            x_list.append(element.x)
            y_list.append(element.y)
    
    max_x = int(max(x_list)+30)
    max_y = int(max(y_list)+30)
    min_x = int(min(x_list)-30)
    min_y = int(min(y_list)-30)

    boundingbox_x = max_x - min_x
    boundingbox_y = max_y - min_y
    bounding_box(boundingbox_x,boundingbox_y)
    change_origin(-min_x, -min_y)

def run_dot(n,angle_even,angle_odd,length):
    biglist0 = get_sequence(n)
    biglist = []
    for list in biglist0:
        l = []
        for element in list:
            object = point()
            object.number = element
            l.append(object)
        biglist.append(l)
    assign_coordinate(biglist, angle_even, angle_odd,length)
    new_bounding_box(biglist)
    line_setting(1,1,1)
    assign_freq(biglist,biglist0) 
    draw_point(biglist)

def run_line(n,angle_even,angle_odd,length):
    biglist0 = get_sequence(n)
    biglist = []
    for list in biglist0:
        l = []
        for element in list:
            object = point()
            object.number = element
            l.append(object)
        biglist.append(l)
    assign_coordinate(biglist, angle_even, angle_odd,length)
    new_bounding_box(biglist)
    line_setting(1,1,1)
    assign_freq(biglist,biglist0) 
    draw_line(biglist)


def run_matrix(n):
    matrix = filter(n)
    #matrix = create_matrix(n)
    size = len(matrix)
    bounding_box(size*1,size*1)
    a = "0 "+ str(size*1) + " translate\n"
    tree.write(a)
    lastx = 0
    lasty = 0
    for xindex in range(0,size):
        x = xindex*10
        for yindex in range(0,size):
            if matrix[xindex][yindex] == 0:
                pass
            else:
                normalize = matrix[xindex][yindex]
                y = -yindex*10
                apoint(x,y,normalize)
                #lineto(x,y,lastx,lasty)
                #lastx = x
                #lasty = y


def run_rw(n,length):
    set = coord(n)
    k = len(set)*length/2
    bounding_box(k,k)
    change_origin(k/2,k/2)
    
    length = 2*length
    line_setting(1,2,1)
    for element in set:
        if element == "N":
            rotate_page(90)
            draw_line_up(length)
            change_origin(0,length)
        if element == "NE":
            rotate_page(45)
            draw_line_up(length)
            change_origin(0,length)
        if element == "E":
            rotate_page(0)
            draw_line_up(length)
            change_origin(0,length)
        if element == "SE":
            rotate_page(-45)
            draw_line_up(length)
            change_origin(0,length)
        if element == "S":
            rotate_page(-90)
            draw_line_up(length)
            change_origin(0,length)
        if element == "SW":
            rotate_page(225)
            draw_line_up(length)
            change_origin(0,length)
        if element == "W":
            rotate_page(180)
            draw_line_up(length)
            change_origin(0,length)
        if element == "NW":
            rotate_page(135)
            draw_line_up(length)
            change_origin(0,length)
        
        
def run_rand(n,length):
    list = ["N","NE","E","SE","S","SW","W","NW"]
    set = []
    for time in range(0,n):
        x = random.choice (list)
        set.append(x)

    k = len(set)*length
    bounding_box(k,k)
    change_origin(k/2,k/2)
    
    line_setting(1,2,1)
    for element in set:
        if element == "N":
            rotate_page(90)
            draw_line_up(length)
            change_origin(0,length)
        if element == "NE":
            rotate_page(45)
            draw_line_up(length)
            change_origin(0,length)
        if element == "E":
            rotate_page(0)
            draw_line_up(length)
            change_origin(0,length)
        if element == "SE":
            rotate_page(-45)
            draw_line_up(length)
            change_origin(0,length)
        if element == "S":
            rotate_page(-90)
            draw_line_up(length)
            change_origin(0,length)
        if element == "SW":
            rotate_page(225)
            draw_line_up(length)
            change_origin(0,length)
        if element == "W":
            rotate_page(180)
            draw_line_up(length)
            change_origin(0,length)
        if element == "NW":
            rotate_page(135)
            draw_line_up(length)
            change_origin(0,length)



#program________________________________________________________________________________________________________________________________________________

tree.write("%!PS-Adobe-3.0 EPSF-3.0\n")

run_rand(1000000,10)



tree.write("showpage\n")
tree.write("%EOF")
tree.close()
