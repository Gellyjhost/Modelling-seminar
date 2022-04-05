from decimal import MAX_EMAX
import math
from tkinter import Y
import random

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


def lineto(x,y,oldx,oldy): #draw line from (oldx,oldy) to (x,y)
    a = str(oldx) +" " + str(oldy) + " moveto\n"
    b = str(x)+ " " + str(y) + " lineto\n"
    tree.write("newpath\n")
    tree.write(a)
    tree.write(b)
    tree.write("stroke\n\n")

def number_list(x): #create a sequence of number using the collatz function that starts from x, then revserse it backwards.
    list = []
    list.append(x)
    while not x == 1:
        j = x % 2
        if j == 0:
            x=x/2
            x = int(x)
        if j == 1:
            x = (3*x)+1
            x = int(x)
        list.append(x)
    
    list.reverse()
    return list

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

def exp2(max): #find the biggest n such that 2^n is smaller than the input number (max)
    n = 0
    status = True
    while status:
        x = x = math.pow(2,n)
        n=n+1
        if x > max:
            status = False
            n = n -2
        if x == max:
            status = False
            n = n-1
    return n

def efficient_number(max): #create a set of number between 1 and the input number, excluding all the smaller exponents of 2.
    n = exp2(max)
    s = number_list(math.pow(2,n))
    set = []
    set.append(int(math.pow(2,n)))
    for number in range(1,max):
        if not number in s:
            set.append(number)
    return set


def apoint(x,y,r): #draw a point at (x,y), with radius r
    a = str(x) + " " + str(y) +" " + str(r) + " 0 360 arc\n "
    tree.write("newpath\n")
    tree.write(a)
    tree.write("fill\n")

def trial2(number,angle_even,angle_odd,segment): #(Old version) to draw a sequence of numbers. For each number in the sequence. If the number is even, rotate the segment counter clockwise by angle_even, and if the number is odd rotate clockwise by angle_odd.
    L = number_list(number)
    x = 0
    y = 0
    rotation = 0
    for item in L:
        j = item % 2
        if j == 0:
            apoint(x,y,3)
            rotation = rotation + angle_even
            newx = x+segment*math.cos(math.radians(rotation))
            newy = y+segment*math.sin(math.radians(rotation))
            lineto(newx,newy,x,y)
            x = newx 
            y = newy
        if j ==1:
            apoint(x,y,3)
            rotation = rotation + angle_odd
            newx = x+segment*math.cos(math.radians(rotation))
            newy = y+segment*math.sin(math.radians(rotation))
            lineto(newx,newy,x,y)
            x = newx 
            y = newy


def trial_color(number,angle_even,angle_odd,segment): # (Old version) same as trial 2, but draw with color.
    L = number_list(number)
    x = 0
    y = 0
    rotation = 0
    current_color = [0,1,0]
    shift_R = 1/(len(L))
    shift_B = 1/(2*len(L))
    shift=[shift_R,0,shift_B]
    for item in L:
        j = item % 2
        if j == 0:
            #point(x,y,3)
            rotation = rotation + angle_even
            newx = x+segment*math.cos(math.radians(rotation))
            newy = y+segment*math.sin(math.radians(rotation))
            current_color = change_RGB(shift,current_color)

            lineto(newx,newy,x,y)
            x = newx 
            y = newy
        if j ==1:
            #point(x,y,3)
            rotation = rotation + angle_odd
            newx = x+segment*math.cos(math.radians(rotation))
            newy = y+segment*math.sin(math.radians(rotation))

            current_color = change_RGB(shift,current_color)
            lineto(newx,newy,x,y)
            x = newx 
            y = newy


#define the class point to store data______________________________________________________________________________________________________________________________

class point: #creates a class point that has certain attributes
    
    def __init__(self, x = "x not defined",y = "y not defined",number = "number not assigned", color = "color not assigned", gray = "grayscale not assigned", width = "width not assigned"):
        self.x = x
        self.y = y
        self.number = number
        self.width = width
        self.gray = gray
        self.color = color

    def show(self): #print the setting of a point
        print("number: ", self.number)
        print("coordinates: (", self.x, " ,", self.y, ")")
        print("line width: ", self.width)
        print("color: ", self.color)
        print("grayscale: ", self.gray)

    def assign_coord(self,x,y): #assign coordinates to a point
        self.x = x
        self.y = y

    def assign_number(self,number): #assign number
        self.number = number

    def assign_width(self,width): #assign width
        self.width = width

    def assign_gray(self, gray): #assign gray scale
        self.gray = gray
    
    def assign_color(self, color):#assign RGB color
        self.color = color
        

class freq: # Creates a class that records the number in a sequence and its frequence
    def __init__(self, number = "number not assigned", frequency = 0):
        self.number = number
        self.frequency = frequency
    
    def show(self):
        print("Number: ", self.number)
        print("Frequency: ", self.frequency)


# value assignement to each point()______________________________________________________________________________________________________________________________

def point_sequence(set): #create a sequence of the class point having the value of the input value
    newset = []
    for number in set:
        object = point()
        number_object = freq()
        number_object.number = number
        object.assign_number(number_object)
        newset.append(object)
    return newset

def coordinate_point(set, angle_even, angle_odd,length): #assign coordinate to each point object according to angle_even and angle_odd
    x = 0
    y = 0
    rotation = 0
    leng = len(set)
    for index in range(0,leng-1):
        j = set[index].number.number % 2
        if j == 0:
            rotation = rotation + angle_even
            x = x+length*math.cos(math.radians(rotation))
            y = y+length*math.sin(math.radians(rotation))
            set[index+1].assign_coord(x,y)
        if j == 1:
            rotation = rotation + angle_odd
            x = x+length*math.cos(math.radians(rotation))
            y = y+length*math.sin(math.radians(rotation))
            set[index+1].assign_coord(x,y)
    set[0].assign_coord(0,0)
    return set

def width_point(bigset): # assign the width of line segment associated with each point to each point. Width is dependent on frequency
    compare = []
    for list in bigset:
        for element in list:
            compare.append(element.number.frequency)
    m = max(compare)
    for list in bigset:
        for element in list:
            width = element.number.frequency*(1/m)
            element.assign_width(width)
    return bigset


def counting(bigset): # count the frequency of each number in each sequence among a large set of sequences, then assign the frequency back to the numbers.
    dictionary = {}
    for list in bigset:
        for element in list:
            x = element.number.number
            if x in dictionary:
                dictionary[x] = dictionary[x]+1
            if not x in dictionary:
                new = {x:1}
                dictionary.update(new)
    for list in bigset:
        for element in list:
            x = element.number.number
            element.number.frequency = dictionary[x]
    
    return bigset

def color(bigset): #assign the color of each line segments based on the length of the sequence
    for list in bigset:
        startcolor = [0,0,0]
        increment = 1/(len(list))
        amount = [increment,increment*2,increment]
        for element in list:
            element.color = startcolor
            startcolor = change_RGB(amount,startcolor)
    
    return bigset

def color2(bigset): #assign the color of each line segments based on the length of the sequence
    for list in bigset:
        startcolor = [0,0,0]
        for element in list:
            x = random.randint(1,1000)/1000
            y = random.randint(1,1000)/1000
            z = random.randint(1,1000)/1000
            element.color = [x,y,z]
    
    return bigset

def gray(bigset):
    for list in bigset:
        for element in list:
            x = random.randint(1,1000)/1000
            element.gray = x
    return bigset




#different types of drawing defined on a list of points________________________________________________________________________________________________________________________________________________

def draw_line(set): #draw line according to the coordinate assigned to each point
    x = len(set)
    for index in range(0,x-1):
        lineto(set[index+1].x,set[index+1].y,set[index].x,set[index].y)

def draw_line_width(set,max): #draw line according to the coordinate assigned to each point and width
    x = len(set)
    for index in range(0,x-1):
        width = max*set[index].width
        line_width(width)
        lineto(set[index+1].x,set[index+1].y,set[index].x,set[index].y)

def draw_line_color(set): #draw line according to the coordinate assigned to each point and color
    x = len(set)
    for index in range(0,x-1):
        RGB(set[index].color)
        lineto(set[index+1].x,set[index+1].y,set[index].x,set[index].y)

def draw_line_width_color(set,max): #draw line according to the coordinate assigned to each point and both color and width
    x = len(set)
    for index in range(0,x-1):
        width = max*set[index].width
        line_width(width)
        RGB(set[index].color)
        lineto(set[index+1].x,set[index+1].y,set[index].x,set[index].y)

def draw_line_gray(set): #draw line according to the coordinate and grayscale assigned to each point
    x = len(set)
    for index in range(0,x-1):
        grayscale(set[index].gray)
        lineto(set[index+1].x,set[index+1].y,set[index].x,set[index].y)

def draw_point(set,r): #draw point according to the coordinate assigned to each point
    tree.write("0 setgray\n")
    for element in set:
        apoint(element.x,element.y,r)

def draw_point_width(set): #draw point according to the coordinate assigned to each point and frequence
    tree.write("0 setgray\n")
    for element in set:
        r = math.log(element.number.frequency)
        apoint(element.x,element.y,r)

def draw_word(set,r): #type out the number next to the coordinate assigned to each point
    tree.write("/Times-Roman findfont\n")
    tree.write("12 scalefont\n")
    tree.write("setfont\n")
    tree.write("0.4 setgray\n")
    for element in set:
        a = str(element.x-r) + " " + str(element.y+r) +" moveto\n"
        b = "(" + str(element.number.number) + ") show\n"
        #b = "(" + str(element.x)+"," + str(element.y) + ") show\n"
        tree.write("newpath\n")
        tree.write(a)
        tree.write(b)


#bounding box settings and prerun________________________________________________________________________________________________________________________________________________

def store_data(largeset,angle_even, angle_odd,segment): #creates a list of lists each representing a point, storing all data
    list = []
    for element in largeset:
        s = number_list(element)
        s1 = point_sequence(s)
        s2 = coordinate_point(s1, angle_even, angle_odd,segment)
        list.append(s2)
    list = counting(list)
    width_point(list)
    #color(list)
    color2(list)
    gray(list)
    return list
    
        
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
    change_origin(0-min_x, 0-min_y)
            

#program________________________________________________________________________________________________________________________________________________

tree.write("%!PS-Adobe-3.0 EPSF-3.0\n")


 #adjust line setting
x = efficient_number(5) #compute the condensed set of starting numbers below certain input
newx = range(1,300) #compute the set of starting numbers
y = store_data(newx,7,-21,20) #prerun the data to determine the coordinates of points with desired degrees of rotation and line length
new_bounding_box(y) #define the bounding box and change origin

line_setting(1,1,1)

for list in y:
    line_width(3)
    draw_line_color(list)
    line_width(1)
    RGB([1,1,1])
    draw_line(list)



tree.write("showpage\n")
tree.write("%EOF")
tree.close()