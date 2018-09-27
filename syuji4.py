#!/usr/bin/python


import json,codecs
import re
import math

def linearCurve(p0,p1,w0,w1,time):
  strokes = []
  currentPoint = (p0[0],p0[1])
  strokes.append(currentPoint)
  complete = 0
  while (complete <= 1):
    complete += .05
    x = (1-complete)*p0[0] + complete*p1[0]
    y = (1-complete)*p0[1] + complete*p1[1]
    strokes.append((x,y))
  #strokes.append((p1[0],p1[1]))
  if (len(strokes) > 75 and filtering) :
    skip = len(strokes)//75
    strokes = strokes[0:len(strokes):skip] + [strokes[-1]]
  return strokes

def bezierCurve(p0,p1,p2,w0,w1,time):
  #print("B",p0,p1,p2)
  strokes = []
  strokes.append((p0[0],p0[1]))
  complete = 0
  while (complete <= 1):
    complete += .05
    x = ((1-complete)**2)*p0[0] + 2*(1-complete)*complete*p1[0] + (complete**2)*p2[0]
    y = ((1-complete)**2)*p0[1] + 2*(1-complete)*complete*p1[1] + (complete**2)*p2[1]
    strokes.append((x,y))
  #strokes.append((p1[0],p1[1]))
  if (len(strokes) > 75 and filtering) :
    skip = len(strokes)//75
    strokes = stokes[0]*8 + strokes[0:len(strokes):skip] + [strokes[-1]]*8
  return strokes

def quadradicCurve(p0,p1,p2,p3,w0,w1,time):
  strokes = []
  strokes.append((p0[0],p0[1]))
  complete = 0
  while (complete <= 1):
    complete += .05
    OMComplete = 1 - complete
    x = (OMComplete**3)*p0[0] + 3*(OMComplete**2)*complete*p1[0] + 3*OMComplete*(complete**2)*p2[0]+(complete**3)*p3[0]
    y = (OMComplete**3)*p0[1] + 3*(OMComplete**2)*complete*p1[1] + 3*OMComplete*(complete**2)*p2[1]+(complete**3)*p3[1]
    strokes.append((x,y))
  #strokes.append((p1[0],p1[1]))
  if (len(strokes) > 75 and filtering) :
    skip = len(strokes)//75
    strokes = strokes[0:len(strokes):skip] + [strokes[-1]]
  return strokes

def getPathingFromPath(path):
  pathing = []
  last = None
  while (len(path) > 0):
    cmd = path[0]
    i = 1
    while (i < len(path)):
      c = path[i]
      if (c.isalpha()):
        #print(c)
        break
      i += 1
    data = path[1:i]
    path = path[i:]
    data = re.sub(r'(\d)-(\d)',r'\1,-\2',data).split(",")
    #print(data)
    for j in range(len(data)):
      data[j] = float(data[j])
    if cmd.islower():
      for j in range(len(data)):
        data[j] += last[j%2]
      cmd = cmd.upper()
    if (cmd == "L"):
      pathing.append(linearCurve(last,data,7,2,1))
    if (cmd == "S"):
      pathing.append(bezierCurve(last,[data[0],data[1]],[data[2],data[3]],7,2,1))
    if (cmd == "C"):
      #print("C",data)
      pathing.append(quadradicCurve(last,[data[0],data[1]],[data[2],data[3]],[data[4],data[5]],7,2,1))
    if (cmd == "M" or cmd == "L"):
      last = data
    elif (cmd == "S"):
      last = [data[2],data[3]]
    elif (cmd == "C"):
      last = [data[4],data[5]]
  return pathing


#def rotateAndCenterPoint(point):
  #(x,y) = point
  #x = 100 - x
  ##y = 100 - y
  #x -= 50
  #y -= 50
  #xtmp = math.cos(3.14/2)*x - math.sin(3.14/2)*y
  #y = math.sin(3.14/2)*x + math.cos(3.14/2)*y
  #x = xtmp
  #return (x,y)

#def standardizePath(path):
  #newPath = []
  #for stroke in path:
    #newStroke = []
    #for point in stroke:
      #newStroke.append(rotateAndCenterPoint(point))
    #newPath.append(newStroke)
  #return newPath

#def distance(p1,p2):
  #(x1,y1) = p1
  #(x2,y2) = p2
  #return ((x1-x2)**2 + (y1-y2)**2)**0.5

#def joinCloseStrokes(strokes):
  #newStrokes = []
  #lastPoint = None
  #for stroke in strokes:
    #if (len(stroke) > 0):
      #if (lastPoint != None and distance(lastPoint,stroke[0]) <= 1):
        #newStrokes[-1] += stroke
      #else:
        #newStrokes.append(stroke)
      #lastPoint = stroke[-1]
  #return newStrokes


def getPathForChar(data, char):
  if char not in data:
    print 'Not found in database:', char
    return None
  path= data[char]
  pathing= getPathingFromPath(path)
  #pathing= standardizePath(pathing)
  #pathing= joinCloseStrokes(pathing)
  return pathing

from core_tool import *
def Help():
	return '''First script.
	Usage: test.ros'''

def Run(ct,*arg):
#if __name__=='__main__':
    
    model_dir = os.path.dirname(__file__)+'/kanji.json'
    print model_dir 
    with codecs.open(model_dir,'r',encoding='utf8') as f:
    #with codecs.open('kanji.json','r',encoding='utf8') as f:
        data= f.read()
        data= json.loads(data)
    
    #print '''
#Note: plot command:
#qplot -x -s 'set size square' /tmp/kanji.txt w lp
#qplot -x -3d -s 'set size square' /tmp/kanji.txt w p
#'''

    while True:
        c= raw_input('type a kanji: ')
        if c in ('','q'):  break
        path= getPathForChar(data, unicode(c,'utf8'))
        if path is None:  continue
        x= list(ct.robot.FK())
        
	
	hen = []
        for stroke in path:
            kaku = []
            for segment in stroke:
                zahyo = [round((segment[0]*0.001),3),round((100-segment[1])*0.001,3)] 
                kaku.append(zahyo)
            hen.append(kaku)
        t = int(len(hen)) ##ninobaai6
        ##for i in range(t):
            ##print hen[i]
            ##print '\n'
        #print hen[t-1]
        
        pen = []
        newlist = hen[0]

        for i in range(1,t):
            if hen[i-1][20] == hen[i][0]:
                newlist += hen[i]
            else:
                pen.append(newlist)
                newlist = hen[i]
        pen.append(newlist)
        
        #for i in range(len(pen)):
            #print pen[i]
            #print len(pen[i])
            #print '\n'
                
	t = int(len(pen))
        #t = 1.0
        x3 = copy.deepcopy(x)
        x3[2]-= 0.25
        ct.robot.MoveToX(x3,3.0,blocking=True)
        rospy.sleep(1.0)
        
        for i in range(t):  #1strokegoto
            x0= copy.deepcopy(x3)
            x0[0]+= pen[i][0][1]
            x0[1]-= pen[i][0][0]
            print x0[0],x0[1]
            print "\n"
            ct.robot.MoveToX(x0,5.0,blocking=True)
            rospy.sleep(0.5)
            x0[2]-= 0.05     #handnotakasa
            ct.robot.MoveToX(x0,2.0,blocking=True)
            rospy.sleep(1.0)
            x_traj= []
            t_traj= []
            for j in range(1,len(pen[i])):
                t_traj.append(j*0.3)
                x1 = copy.deepcopy(x0) 
                x1[0] += pen[i][j][1] - pen[i][0][1]
                x1[1] -= pen[i][j][0] - pen[i][0][0]
                print x1[0],x1[1]
                x_traj.append(x1)
            print t_traj
            print "\n"
            print x_traj
            ct.robot.FollowXTraj(x_traj, t_traj, blocking=True)
            rospy.sleep(3.0)
            print "\n"    
            x1[2]+= 0.05
            ct.robot.MoveToX(x1,3.0,blocking=True)
            print "next"
            print "\n"
            rospy.sleep(0.5)
        print "END"
        
        q= [-0.02225494707637879, 0.027604753814144237, 0.02256845844164128, -2.2001560115435073, -0.00047772651727832574, 0.6569580325147487, 0.0010119170182285682]   #First position
        ct.robot.MoveToQ(q,10.0)
        #rospy.sleep(1.0)
        #x[1] += pen[0][0][1] - pen[t-1][int(len(pen[t-1]))-1][1] 
        #x[1] -= 0.1
        #ct.robot.MoveToX(x,10.0,blocking=True)
        #rospy.sleep(1.0)                    ##nimojime
    #xygyaku 
    q= [-0.02225494707637879, 0.027604753814144237, 0.02256845844164128, -2.2001560115435073, -0.00047772651727832574, 0.6569580325147487, 0.0010119170182285682]   #First position
    ct.robot.MoveToQ(q,10.0)
        
            
        
        
        
        
        
        
        
        
        
    
