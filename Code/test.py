
from PEWorld import *
from PEWorld.viewer import *
from PEWorld.utils import *
from PEWorld.objects import *
import ode, trimesh,time, random
import numpy as np

if __name__ == '__main__':

    pew = PEWorld()
    noise = .1
    p = pew.addPlane('floor',friction=10,normal=(0,0,1))
    #strut = pew.addBox('strut',initpos = (0,0,.25),dimensions=(.05,.2,.5),mass=0,restitution=.1)
    beam = pew.addBox('beam',initpos=(0,0,.55),dimensions=(5,.2,.1),restitution=.1)
    beam.density = 1.


    #b1 = pew.addBox('b1',initpos = (0,0,.25),dimensions=(.5,.5,.5),friction=10,restitution=.05)
    #b2 = pew.addBox('b2',initpos = (0,0.,1.25),mass=0,dimensions=(.5,.5,.5),friction=10,restitution=.9)
    #pew.jitterObject('b1',noise)
    #pew.jitterObject('b2',noise)

    odrop = random.random() * 5. - 2.5

    tm = pew.loadMeshFromFile('LSh.stl','oct',scale=.5,initpos =(odrop,0,3), \
                              initquat = (1,0,0,0),mass = 1., friction=10,restitution=.5)

    pew.addBoxGoal('right',dimensions=(5,5,.1),position = (3,0,.1))
    pew.addBoxGoal('left',dimensions=(5,5,.1),position=(-3,0,.1))

    colors = {'floor':WHITE,'b1':RED,'b2':GREEN,'oct':BLUE}

    h = pew.addHingeJoint('hinge','beam',position=beam.position,axis = (0,1,0))

    '''
    print tm.position
    for i in range(50):
        pew.step(.1)
        print h.position, h._joint.getAnchor()
        print h._axis, h._joint.getAxis()
        print h._joint.getFeedback()
    '''

    '''
    jg = ode.JointGroup()
    j = ode.BallJoint(pew._odeWorld,jg)
    j.attach(pew.getObj('oct')._odeBody,ode.environment)
    j.setAnchor((1,0,3))
    print j
    j.setFeedback(True)
    #j.setAxis((1,0,0))
    '''


    #pew = importWorld('test_data.json')

    #for p in pew._planes: print p

    #colors = {'Floor': GREY}



    def ghit(objnm,goalnm):
        print objnm, ';', goalnm
    #pew.onGoalhit = ghit

    def onkey(k):
        print ord(k)

    pew.repel()

    #pew.applyForceToObj('oct',(-1.5,0,0))

    cam = Camera(position = (0,-7,2),viewcenter=(0,0,1))
    #lgt = Light(position = (10,-10,3), direction = (10,-10,3))
    lgt = Light(direction = (1,1,7),ambient_rgb=DARKGREY)


    viewer = WorldViewer(pew,camera=cam,lights=[lgt],colordict=colors,
                         startPaused = True, defColor= BLUE)
    viewer.initView()
    viewer.run(True)
