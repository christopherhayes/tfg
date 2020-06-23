#syntax: python3 tikzfractalgenerator.py FILENAME LEVEL 4N-CARPET-N


#tikzfractalgenerator
#by christopher hayes @ uconn

#note: tikz cuts off values deeper than 3 or 4 decimal places ( double check ) so large values are recommended
#       with a small [scale=?] modifier. in fact it may be smarter to blow up the fractal, and not contract.  

#input tikz script for level 0 cell (tikz language)
#input contractions + desired level (manually in script itself / numpy)

#converts script to workable object for python
#applies contractions to level 0 cell to desired level
#(do later) deletes repeated edges / vertices for better look.
#       due to numpy inaccuracies will need small-radius detection instead of equality.
#       would be wise to sort stored edges by nearness (x coordinate then y coordinate?) 

#outputs initial graph in terminal, tikz script for desired pre-fractal (tikz language) into outputtikz.tex file in same folder

import numpy as np
import copy
import sys


#OPTIONS:

#note: unfortunately need to scroll all the way to the bottom and replace a variable with the right input graph string variable

A = np.sqrt(0.5) #needed for octacarpet functions (no longer used)
N = 2 #4N carpet, 2 is octacarpet

HEPTCONT = 0.307979

n = 3 #depth of prefractal graph

if len(sys.argv) > 2:
    n = int(sys.argv[2])

if len(sys.argv) > 3:
    N = int(sys.argv[3])


totalmaps = 7 #set equal to number of similitudes 

example4N = ""
for i in range(4*N):
    point1 = np.exp(((2*i + 1)*1j*np.pi)/(4*N))
    point2 = np.exp(((2*(i+1) + 1)*1j*np.pi)/(4*N))
    x1 = point1.real
    y1 = point1.imag
    x2 = point2.real
    y2 = point2.imag
    example4N += "\draw (" + str(x1) + ", " + str(y1) + ") -- (" + str(x2) + ", " + str(y2) + "); \n"

exampleHepta = ""
for i in range(7):
    point1 = np.exp(((2*i)*1j*np.pi)/(7))
    point2 = np.exp(((2*(i+1))*1j*np.pi)/(7))
    x1 = point1.real
    y1 = point1.imag
    x2 = point2.real
    y2 = point2.imag
    exampleHepta += "\draw (" + str(x1) + ", " + str(y1) + ") -- (" + str(x2) + ", " + str(y2) + "); \n"

exampleHeptaCG = ""
for i in range(7):
    for k in range(7):
        if k == i:
            pass
        else:
            point1 = np.exp(((2*i)*1j*np.pi)/(7))
            point2 = np.exp(((2*k)*1j*np.pi)/(7))
            x1 = point1.real
            y1 = point1.imag
            x2 = point2.real
            y2 = point2.imag
            exampleHeptaCG += "\draw (" + str(x1) + ", " + str(y1) + ") -- (" + str(x2) + ", " + str(y2) + "); \n"

exampleHeptaS = "\draw [fill] "
for i in range(6):
    point1 = np.exp(((2*i)*1j*np.pi)/(7))
    #point2 = np.exp(((2*(i+1))*1j*np.pi)/(7))
    x1 = point1.real
    y1 = point1.imag
    #x2 = point2.real
    #y2 = point2.imag
    exampleHeptaS += "(" + str(x1) + ", " + str(y1) + ") -- "
lastpoint = np.exp(((2*(6))*1j*np.pi)/(7))
xl = lastpoint.real
yl = lastpoint.imag
exampleHeptaS += "(" + str(xl) + ", " + str(yl) + ");"


example4NYgraph = ""
#define midpoints of L0, LN, L(3N-1)
L01 = np.exp(((2*(0) + 1)*1j*np.pi)/(4*N))
L02 = np.exp(((2*(0+1) + 1)*1j*np.pi)/(4*N))
LN1 = np.exp(((2*(N) + 1)*1j*np.pi)/(4*N))
LN2 = np.exp(((2*(N+1) + 1)*1j*np.pi)/(4*N))
L3Nm11 = np.exp(((2*(3*N-1) + 1)*1j*np.pi)/(4*N))
L3Nm12 = np.exp(((2*(3*N) + 1)*1j*np.pi)/(4*N)) 
M0 = (L01 + L02)/2
MN = (LN1 + LN2)/2
M3 = (L3Nm11 + L3Nm12)/2
example4NYgraph += "\draw (" + str(M0.real) + ", " + str(M0.imag) + ") -- (0, 0); \n"
example4NYgraph += "\draw (" + str(MN.real) + ", " + str(MN.imag) + ") -- (0, 0); \n"
example4NYgraph += "\draw (" + str(M3.real) + ", " + str(M3.imag) + ") -- (0, 0); \n"

exampleOC2 = """\draw (0, 0.7071067811865476) -- (0, 1.7071067811865475);
\draw (0, 1.7071067811865475) -- (0.7071067811865476, 2.414213562373095);
\draw (0.7071067811865476, 2.414213562373095) -- (1.7071067811865475, 2.414213562373095);
\draw (1.7071067811865475, 2.414213562373095) -- (2.414213562373095, 1.7071067811865475);
\draw (2.414213562373095, 1.7071067811865475) -- (2.414213562373095, 0.7071067811865476);
\draw (2.414213562373095, 0.7071067811865476) -- (1.7071067811865475, 0);
\draw (1.7071067811865475, 0) -- (0.7071067811865476, 0);
\draw (0.7071067811865476, 0) -- (0, 0.7071067811865476);"""

# A = 0.7071067811865476
# 1 + A = 1.7071067811865475
# 1 + 2A = 2.414213562373095

exampleOC3 = """\draw (0, A) -- (0, 1 + A);
\draw (0, 1 + A) -- (A, 1 + 2*A);
\draw (A, 1 + 2*A) -- (1 + A, 1 + 2*A);
\draw (1 + A, 1 + 2*A) -- (1 + 2*A, 1 + A);
\draw (1 + 2*A, 1 + A) -- (1 + 2*A, A);
\draw (1 + 2*A, A) -- (1 + A, 0);
\draw (1 + A, 0) -- (A, 0);
\draw (A, 0) -- (0, A);"""

exampleSG = """\draw (0, 0) -- (11, 0);
\draw  (11, 0) -- (0, 11);
\draw  (0, 11) -- (0, 0);"""

exampleSG2 = """\draw (0, 0) -- (5, 8.660254037844386);
\draw (5, 8.660254037844386) -- (10, 0);
\draw (10, 0) -- (0, 0)"""

exampleSG2s = """\draw [thick, fill=orange] (0, 0) -- (5, 8.660254037844386) -- (10, 0) -- (0, 0);"""

exampleSG2nodes = """\draw (0, 0) -- (5, 8.660254037844386) -- (10, 0) -- (0, 0);
\draw [ultra thick, rounded corners] (0, 0) -- (0, 0.0000001) -- (0.0000001, 0) -- (0, 0);
\draw [ultra thick, rounded corners] (10, 0) -- (10, 0.0000001) -- (10.0000001, 0) -- (10, 0);
\draw [ultra thick, rounded corners] (5, 8.660254037844386) -- (5, 8.660264037844386) -- (5.0000001, 8.660256037844386) -- (5, 8.660254037844386);
"""

exampleSCX = """\draw (0, 0) -- (9, 9);
\draw (0, 9) -- (9, 0);"""

exampleSCplus = """\draw (0, 4.5) -- (9, 4.5);
\draw (4.5, 0) -- (4.5, 9);"""

exampleSC = """\draw (0, 0) -- (0, 9);
\draw (0, 0) -- (9, 0);
\draw (9, 0) -- (9, 9);
\draw (9, 9) -- (0, 9);
\draw (0, 0) -- (9, 9);
\draw (0, 9) -- (9, 0);"""

exampleSCs = """\draw [fill=orange] (0, 0) -- (9, 0) -- (9, 9) -- (0, 9) -- (0, 0);"""

exampleAfC1 = """ \draw (0, 0) -- (0, 8);
\draw (0, 8) -- (8, 8);
\draw (8, 0) -- (8, 8);
\draw (8, 0) -- (0, 0);"""

exampleAfC1s = """\draw [fill=orange] (0, 0) -- (0, 8) -- (8, 8) -- (8, 0) -- (0, 0);"""

exampleAfC1x = """\draw (0, 0) -- (8, 8);
\draw (0, 8) -- (8, 0);"""

exampleAfC1p = """\draw (4, 0) -- (4, 8);
\draw (0, 4) -- (8, 4);"""

exampleKoch = """\draw (0, 0) -- (0.33333333333333, 0);
\draw (0.3333333333333, 0) -- (0.5, 0.28867513459481287);
\draw (0.5, 0.28867513459481287) -- (0.66666666666667, 0);
\draw (0.66666666666667, 0) -- (1, 0);"""

exampleKoch2 = """\draw (0, 0) -- (0.5, 0.28867513459481287);
\draw (0.5, 0.28867513459481287) -- (1, 0);
\draw (1, 0) -- (0, 0);"""

exampleKoch3 = """\draw (0, 0) -- (0.5, 0.25);
\draw (0.5, 0.25) -- (1, 0);
\draw (1, 0) -- (0, 0);"""

examplesquare = """\draw (0, 0) -- (4, 0);
\draw (4, 0) -- (4, 4);
\draw (4, 4) -- (0, 4);
\draw (0, 4) -- (0, 0);"""

def main():  
    thefilename = "outputtikz.tex"
    if len(sys.argv) > 1:
        thefilename = sys.argv[1] + ".tex"

    theoutput = fractalizer2(n, exampleHeptaCG) #replace 2nd variable with input graph (one-string tikz form)
    print("Now writing to " + thefilename + "...")
    #print(theoutput)
    writetofile(theoutput, thefilename)
    print("Complete")

###

def similitudes(no, point, key = "Hepta"): #input complex point and similitude label no / PLACE THEM HERE FROM ABOVE / ENTER MANUALLY
    global N
    if key == None: #enter custom / manual similitudes below
        contratio = 1/(1 + (1/np.tan(np.pi/(4*N))))
        if no % 2 == 1:
            newpoint = point*np.exp(((no)*np.pi*1j)/(2*N))
        if no % 2 == 0:
            newpoint = point*np.exp(((no-3)*np.pi*1j)/(2*N))
        if 0 <= no and no < 4*N:
            return contratio*(newpoint - np.exp(((2*no + 1)*1j*np.pi)/(4*N))) + np.exp(((2*no + 1)*1j*np.pi)/(4*N))
        else:
            return np.complex64(0)
################################################################## static similitudes (with key) below
    if key == "Hepta":
        contratio = HEPTCONT
        contpoint = np.exp(((2*no)*1j*np.pi)/(7))
        return contratio*(point - contpoint) + contpoint
        
    if key == "4Nold": #4N carpet OLD OLD OLD OLD
        contratio = 1/(1 + (1/np.tan(np.pi/(4*N))))
        if no % 2 == 1:
            newpoint = point*np.exp(((no)*np.pi*1j)/(2*N))
        if no % 2 == 0:
            newpoint = point*np.exp(((no-3)*np.pi*1j)/(2*N))
        if 0 <= no and no < 4*N:
            return contratio*(newpoint - np.exp(((2*no + 1)*1j*np.pi)/(4*N))) + np.exp(((2*no + 1)*1j*np.pi)/(4*N))
        else:
            return np.complex64(0)
    if key == "SGr": #right triangle SG with side 11
        if no == 0:
            return point*0.5j
        elif no == 1:
            return (11 + point)*0.5j
        elif no == 2:
            return (11j + point)*0.5j
        else:
            return np.complex64(0)
        
    if key == "SG2": #standard equilateral side 10
        if no == 0:
            return point*0.5
        elif no == 1:
            return (10 + point)*0.5
        elif no == 2:
            return ((5 + 8.660254037844386j)  + point)*0.5
        else:
            return np.complex64(0)

    if key == "SC": #square with side 9
        if no == 0:
            return point*(1/3)
        if no == 1:
            return 9 + (point - 9)*(1/3)
        if no == 2:
            return 9 + 4.5j + (point - 9 - 4.5j)*(1/3)
        if no == 3:
            return 9 + 9j + (point - 9 - 9j)*(1/3)
        if no == 4:
            return 4.5 + (point - 4.5)*(1/3)
        if no == 5:
            return 4.5j + (point - 4.5j)*(1/3)
        if no == 6:
            return 9j + (point - 9j)*(1/3)
        if no == 7:
            return 4.5 + 9j + (point - 4.5 - 9j)*(1/3)
        else:
            return np.complex64(0)

    if key == "Koch": #standard koch
        A = 0.5 + 0.28867513459481287j
        if no == 0:
            return A*(np.conj(point))
        elif no == 1:
            return (1 - A)*(np.conj(point) - 1) + 1
        else:
            return np.complex64(0)

    if key == "Koch3": #reu exercise koch
        A = 0.5 + 0.25j
        if no == 0:
            return A*(np.conj(point))
        elif no == 1:
            return (1 - A)*(np.conj(point) - 1) + 1
        else:
            return np.complex64(0)

    if key.lower() == "square":
        if no == 0:
            return point*0.5
        if no == 1:
            return 0.5*(point - 4) + 4
        if no == 2:
            return 0.5*(point - 4 - 4j) + 4 + 4j
        if no == 3:
            return 0.5*(point - 4j) + 4j
        else:
            return np.complex64(0)
        
    if key == "AfC1":
        if no == 0:
            return point*(0.25) + 0j
        if no == 1:
            return 0.25*(point - 8) + 8
        if no == 2:
            return 0.25*(point - 8 - 8j) + 8 + 8j
        if no == 3:
            return 0.25*(point - 8j) + 8j
        if no == 4:
            return 0.5*(point.real - 4) + 0.25*(point.imag)*1j + 4
        if no == 6: 
            return 0.5*(point.real - 4) + 0.25*(point.imag - 8)*1j + 4 + 8j
        if no == 7:
            return 0.25*(point.real) + 0.5*(point.imag - 4)*1j + 4j
        if no == 5:
            return 0.25*(point.real - 8) + 0.5*(point.imag - 4)*1j + 8 + 4j
        else:
            return np.complex64(0)
        
    else:
        return np.complex64(0)
    
def sim1(point):
    return point*0.2

def sim2(point):
    return (1 - point)*0.3

def sim3(point):
    return (1j - point)*0.4


#workable object classes along with to-tikz-string definitions

class point:
    def __init__(self, ZorXcoord, ycoord=None): #Accepts complex number (complex64 / 2 float32s) OR (x, y) (float32,float32)
        if ZorXcoord.dtype == np.complex64:
            newxcoord = ZorXcoord.real
            newycoord = ZorXcoord.imag
            newzcoord = ZorXcoord
        else:
            if ycoord == None:
                print("Error: Attempted to create point with x-coordinate only. Set to 0.")
                ycoord = np.dtype(np.float32) #default value is 0
            newxcoord = np.float32(ZorXcoord)
            newycoord = np.float32(ycoord)
            newzcoord = np.complex64(0)
            newzcoord = newxcoord + 1j*newycoord

        self.x = newxcoord
        self.y = newycoord
        self.z = newzcoord
        
    def tikzform(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def updateZ(self):
        self.z = self.x + ((self.y)*1j)
        
    def updateXY(self):
        self.x = self.z.real
        self.y = self.z.imag

    def map(self, no, function): #no is label number for function, e.g. map(1, similitudes) maps the no. 1 similitude. 
        self.z = function(no, self.z)
        self.x = self.z.real
        self.y = self.z.imag

class edge:
    def __init__(self, point1, point2, modifiers = None): #Modifiers such as dotted, dashed, ->, <->, etc
        self.pointlist = [point1, point2]
        self.options = "" #for now
#        self.tikzform = "\draw " + self.options + self.pointlist[0].tikzform() + "--" + self.pointlist[1].tikzform() + ";"

    def map(self, no, function):
        for pt in self.pointlist:
            pt.map(no, function)

    def tikzhalf(self):
        return self.pointlist[0].tikzform()

    def tikzform(self):
        return "\draw " + self.options + self.pointlist[0].tikzform() + "--" + self.pointlist[1].tikzform() + ";"

def edgelisttostring(edgelist): #input is a list, [optionstring, edge1, edge2, etc]
    outputstring = str(edgelist[0])+"] "
    for i in range(1, len(edgelist)):
        outputstring += (edgelist[i].tikzhalf()) + "--"
    outputstring += edgelist[len(edgelist)-1].pointlist[1].tikzform()+";"
    return outputstring
    
#tikz script parsing functions

def edgeconverter(edgestringwithspaces): #form is ALWAYS "\draw [options] (x1, y1) -- (x2, y2);" spaces are deleted/ignored
    edgestring = edgestringwithspaces.replace(" ", "") #removes whitespace and \n
    optionsandedge = edgestring.split("]")
    if len(optionsandedge) == 1:
        optionstr = None
        edgeonly = optionsandedge[0]
    else:
        optionstr = optionsandedge[0]
        edgeonly = optionsandedge[1]
    #for now do nothing with options.
    edgeonly = edgeonly.replace(";", "")
    edgeonly = edgeonly.replace("\\draw", "")
    pointslist = edgeonly.split("--") #returns [point1, point2]
    return edge(pointstringconvert(pointslist[0]), pointstringconvert(pointslist[1]))

def newedgeconverter(edgestringwithspace): #return [optionstring, edge1, edge2, etc, edge(N-1)] from \draw command with N points. 
    edgestring = edgestringwithspace.replace(" ", "") #removes whitespace and \n
    optionsandedge = edgestring.split("]")
    if len(optionsandedge) == 1:
        optionstr = None
        edgeonly = optionsandedge[0]
    else:
        optionstr = optionsandedge[0]
        edgeonly = optionsandedge[1]
    #for now do nothing with options.
    edgeonly = edgeonly.replace(";", "")
    edgeonly = edgeonly.replace("\\draw", "")
    pointslist = edgeonly.split("--") #returns [point1, points2, ..., pointsN]
    pointpairlist = []
    for i in range(len(pointslist) - 1):
        pointpairlist.append([pointstringconvert(pointslist[i]), pointstringconvert(pointslist[i+1])])
    edgelist = [optionstr]
    for pointpair in pointpairlist:
        edgelist.append(edge(pointpair[0], pointpair[1]))
    return edgelist

def pointstringconvert(pointstring): #converts (x,y) to a point class object and returns it.
    pointstring = pointstring.replace("(", "")
    pointstring = pointstring.replace(")", "")
    points = pointstring.split(",")
    newpoint = point(np.float32(float(points[0])), np.float32(float(points[1])))
    return newpoint
#    return point(np.fromstring(points[0], np.float32), np.fromstring(points[1], np.float32))


# fractal generator function

def fractalizer2(levels, tikzinput):
    global totalmaps
    lines = tikzinput.splitlines()
    edgelist = []
    for edgestring in lines:
        edgelist.append(edgeconverter(edgestring))
    for step in range(levels):
        print("Doing level " + str(step + 1) + "...")
        newedgelist = []
        howmanynewedges = totalmaps*len(edgelist)
        for i in range(howmanynewedges): #make enough new "temp" edges
            zeero = np.float32(0)
            negone = np.float32(-1)
            newedgelist.append(edge(point(negone, zeero), point(zeero, negone)))
        count = 1
        curcount = 0
        for similnum in range(totalmaps):
            for edges in edgelist:
                newedgelist[curcount].pointlist[0].x = edges.pointlist[0].x
                newedgelist[curcount].pointlist[0].y = edges.pointlist[0].y
                newedgelist[curcount].pointlist[1].x = edges.pointlist[1].x
                newedgelist[curcount].pointlist[1].y = edges.pointlist[1].y
                newedgelist[curcount].pointlist[0].updateZ()
                newedgelist[curcount].pointlist[1].updateZ()
                newedgelist[curcount].map(similnum, similitudes)
                curcount += 1
            count += 1
        edgelist = newedgelist.copy()
    outputstring = ""
    for edges in edgelist:
        outputstring += edges.tikzform() + "\n"
    return outputstring


def newfractalizer2(levels, tikzinput):
    global totalmaps
    lines = tikzinput.splitlines()
    objectlist = []
    for objectstring in lines:
        objectlist.append(newedgeconverter(objectstring)) #list of object-lists
    for step in range(levels):
        print("Doing level " + str(step + 1) + "...")
        newobjectlist = []
        howmanynewobjects = totalmaps*len(objectlist)
        objectlengthlist = []
        for j in range(len(objectlist)):
            objectlengthlist.append(len(objectlist[j]))
        for i in range(howmanynewobjects): #make enough new "temp" objects
            zeero = np.float32(0)
            negone = np.float32(-1)
            newobjectlist.append([]) #[] will be the new object (options, edge1, edge2...) 
            for k in range(objectlengthlist[i // totalmaps] - 1):
                newobjectlist[i].append(edge(point(negone, zeero), point(zeero, negone)))

        for j in range(howmanynewobjects):
            newobjectlist[j].insert(0, objectlist[j // totalmaps][0]) 
        
        curcount = 0
        for similnum in range(totalmaps):
            for objects in objectlist:
                j = 0
                for edges in objects:
                    if type(edges) is str:
                        pass
                    else:
                        j += 1
#                        print(newobjectlist)
                        newobjectlist[curcount][j].pointlist[0].x = edges.pointlist[0].x
                        newobjectlist[curcount][j].pointlist[0].y = edges.pointlist[0].y
                        newobjectlist[curcount][j].pointlist[1].x = edges.pointlist[1].x
                        newobjectlist[curcount][j].pointlist[1].y = edges.pointlist[1].y
                        newobjectlist[curcount][j].pointlist[0].updateZ()
                        newobjectlist[curcount][j].pointlist[1].updateZ()
                        newobjectlist[curcount][j].map(similnum, similitudes)

                curcount += 1
        objectlist = newobjectlist.copy()
    outputstring = ""
    for objects in objectlist:
        outputstring += edgelisttostring(objects) + "\n"
    return outputstring

#file writing

def writetofile(string, thefilename = "outputtikz.tex"):
    thefile = open(thefilename, "w")
    thefile.write(string)
    thefile.close()
    
#main code bit

main() 


