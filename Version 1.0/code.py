import math
tree = open("tree.txt","w")

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
    a = str(x)
    b = "0 "+ a + " lineto\n"
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


def number_list(x):  #create a sequence of number using the collatz function that starts from x, then revserse it backwards.
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

def trial(number,angle_even,angle_odd,segment,shift): #failed attempt
    L = number_list(number)
    anglemeter = 0
    x = 0
    y = 0
    for item in L:
        j = item % 2
        if j == 0:
            rotate_page(angle_even)
            draw_line_up(segment)
            point(0,segment,3)
            change_origin(0,shift)
            anglemeter = anglemeter+angle_even
        if j ==1:
            rotate_page(angle_odd)
            draw_line_up(segment)
            point(0,segment,3)
            change_origin(0,shift)
            anglemeter = anglemeter+angle_odd

    
    anglemeter = -anglemeter
    a = str(anglemeter) + " rotate\n"
    tree.write(a)
    b = str(x)+" " + str(y) + " translate\n"
    tree.write(b)
    
def trial2(number,angle_even,angle_odd,segment): #draw a sequence of number. For each number in the sequence. If the number is even, rotate the segment counter clockwise by angle_even, and if the number is odd rotate clockwise by angle_odd.
    L = number_list(number)
    x = 0
    y = 0
    rotation = 0
    for item in L:
        j = item % 2
        if j == 0:
            point(x,y,3)
            rotation = rotation + angle_even
            newx = x+segment*math.cos(math.radians(rotation))
            newy = y+segment*math.sin(math.radians(rotation))
            lineto(newx,newy,x,y)
            x = newx 
            y = newy
        if j ==1:
            point(x,y,3)
            rotation = rotation + angle_odd
            newx = x+segment*math.cos(math.radians(rotation))
            newy = y+segment*math.sin(math.radians(rotation))
            lineto(newx,newy,x,y)
            x = newx 
            y = newy

    
def trial_color(number,angle_even,angle_odd,segment): #same as trial 2, but with color.
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



def point(x,y,r): #draw a point at (x,y), with radius r
    a = str(x) + " " + str(y) +" " + str(r) + " 0 360 arc\n"
    tree.write("newpath\n")
    tree.write(a)
    tree.write("fill\n")

def change_RGB(amount,current): #change the current RGB color(input in set) by the amount(input in set).
    new = []
    for n in range(0,3):
        if not current[n] >= 0.99:
            n = current[n] + amount[n]
            new.append(n)
        else:
            new.append(current[n])

    a = str(new[0])+" "+str(new[1])+ " " + str(new[2]) + " setrgbcolor\n"
    tree.write(a)
    return new

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


tree.write("%!PS-Adobe-3.0 EPSF-3.0\n")
bounding_box(800,700)
change_origin(500, 500)

line_setting(1,2,1)
x = efficient_number(1000)

for number in x:
    k = trial2(number,15,-15,20)


tree.write("showpage\n")
tree.write("%EOF")
tree.close()