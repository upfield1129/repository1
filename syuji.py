#!/usr/bin/python
from core_tool import *
def Help():
        return '''First script.
        Usage: syuji.ros'''
def Run(ct,*arg):
        x= list(ct.robot.FK())
        q= list(ct.robot.FK())
        print x
        x[1]+= 0.1
        ct.robot.MoveToX(x,5.0,blocking=True)
        x[2]-= 0.2
        ct.robot.MoveToXI(x,10.0,blocking=True)
        x[1]-= 0.2
        ct.robot.MoveToXI(x,20.0,blocking=True)
        x[2]+= 0.1
        ct.robot.MoveToXI(x,5.0,blocking=True)
        q= [-0.02225494707637879, 0.027604753814144237, 0.02256845844164128, -2.2001560115435073, -0.00047772651727832574, 0.6569580325147487, 0.0010119170182285682]   #First position
        ct.robot.MoveToQ(q,5.0)
    
