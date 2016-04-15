'''

The PEWorld object that controls all objects

'''
from __future__ import division
import ode
import math, numbers, os
import numpy as np
from .objects import *
import trimesh


# Function for handling collisions
def _collideCallback(world,geom1,geom2):
    contacts = ode.collide(geom1,geom2)
    nm1 = geom1._myName
    nm2 = geom2._myName

    ig1 = world.isGoal(nm1)
    ig2 = world.isGoal(nm2)

    if ig1 or ig2:
        if ig1 and ig2:
            return # Goal-goal collisions should return nothing ever
        elif ig1:
            onm = nm2
            gnm = nm1
        else:
            onm = nm1
            gnm = nm2
        if world.onGoalhit and len(contacts) > 0:
            world.onGoalhit(onm, gnm)
    else:
        # Real collisions
        fr1 = world.getObj(nm1).friction
        fr2 = world.getObj(nm2).friction
        re1 = world.getObj(nm1).restitution
        re2 = world.getObj(nm2).restitution
        world._hascollisions = True
        if world.onCollisions:
            world.onCollisions(nm1,nm2)

        fr = fr1*fr2
        re = re1*re2

        for c in contacts:
            c.setBounce(re)
            c.setMu(fr)
            j = world.makeContactJoint(c)
            j.attach(geom1.getBody(),geom2.getBody())

class PEWorld(object):

    def __init__(self,fps = 50.,stepsize = 0.001,gravity = 9.81, ERP = 0.2, CFM = 1e-5):

        self._gravity = gravity
        self._erp = ERP
        self._cfm = CFM
        self._fps = fps
        self._stepsize = stepsize
        self._time = 0.
        self._odeWorld = ode.World()
        self._odeWorld.setGravity( (0,0,-self._gravity) )
        self._odeWorld.setERP(self._erp)
        self._odeWorld.setCFM(self._cfm)
        self._odeSpace = ode.Space()
        self._odeContact = ode.JointGroup()
        self._objs = dict()
        self._planes = dict()
        self._hascollisions = False
        self.onCollisions = None
        self._goals = dict()
        self.onGoalhit = None
        self._joints = dict()
        self._odeJoints = ode.JointGroup()

    def getObj(self,name):
        if name in self._objs.keys():
            return self._objs[name]
        elif name in self._planes.keys():
            return self._planes[name]
        else: raise KeyError('Key ' + name + ' does not exist in this world')



    def addHingeJoint(self,jointname,obj1,obj2='WORLD',position=(0.,0.,0.),axis=(0.,1.,0.)):
        os = self.objNames() + ['WORLD']
        if obj1 not in os or obj2 not in os:
            raise KeyError('One or more objects do not exist in world: ' + obj1 + ' ' + obj2)
        j = PEHingeJoint(self,jointname,obj1,obj2,position,axis)
        self._joints[jointname] = j
        return j

    def removeJoint(self,jointname):
        # Sorta hacky - seems like individual joints can't be removed from jointgroups
        if jointname not in self.jointNames():
            raise KeyError('Joint ' + jointname + ' does not exist')
        self._odeJoints = ode.JointGroup()
        del self._joints[jointname]
        for j in self._joints: j.reattach()


    def removeObj(self,name):
        if name in self._objs.keys():
            # Check for any joints - remove if they are attached to this object
            for jn in self.jointNames():
                if self._joints[jn].hasObj(name):
                    self.removeJoint(jn)
            # Unlink objects
            o = self._objs[name]
            if o._isStatic:
                del o._odeGeom
            else:
                o._odeBody.setMass(None)
                o._odeGeom.setBody(None)
                del o._odeBody
                del o._odeMass
                del o._odeGeom
            del self._objs[name]
        elif name in self._planes.keys():
            del self._planes[name]._odeGeom
            del self._planes[name]
        elif name in self._goals.keys():
            del self._goals[name]._odeGeom
            del self._goals[name]
        else:
            raise KeyError('Key ' + name + ' does not exist in this world')

    def copy(self):
        neww = PEWorld(self._fps, self._stepsize, self._gravity, self._erp, self._cfm)
        neww._time = self._time
        for onm in self._objs.keys():
            neww._objs[onm] = self._objs[onm].copy(neww)
        for pnm in self._planes.keys():
            neww._planes[pnm] = self._planes[pnm].copy(neww)
        for gnm in self._goals.keys():
            neww._goals[gnm] = self._goals[gnm].copy(neww)
        for jnm in self._joints.keys():
            neww._joints[jnm] = self._joints[jnm].copy(neww)
        neww.onCollisions = self.onCollisions
        neww.onGoalhit = self.onGoalhit
        return neww

    def makeContactJoint(self,contact):
        return ode.ContactJoint(self._odeWorld,self._odeContact,contact)

    def step(self,timestep = None):
        self._hascollisions = False
        if timestep is None: timestep = 1/self._fps
        nsteps = int(math.ceil(timestep / self._stepsize))
        for i in range(nsteps):
            self._odeSpace.collide(self,_collideCallback)
            self._odeWorld.quickStep(self._stepsize)
            self._odeContact.empty()
        self._time += timestep


    def addBox(self,name,dimensions = (1.,1.,1.), initpos = (0.,0.,0.), initvel = (0.,0.,0.), \
               initquat = (1.,0.,0.,0.), mass = 1., friction = .4, restitution = .9):
        newbox = PEBox(self,name,dimensions,initpos,initvel,initquat,mass=mass,friction=friction,restitution=restitution)
        self._objs[name] = newbox
        return newbox

    def addPlane(self,name,normal = (0.,0.,1.),dist = 0., friction = .4, restitution = 1.):
        newplane = PEPlane(self,name,normal,dist,friction=friction,restitution=restitution)
        self._planes[name] = newplane
        return newplane

    def addBoxGoal(self,name,dimensions = (1.,1.,1.), position = (0.,0.,0.),quaternion = (1.,0.,0.,0.)):
        newgoal = BoxGoal(self,name,dimensions,position,quaternion)
        self._goals[name] = newgoal
        return newgoal

    @property
    def fps(self): return self._fps

    @property
    def time(self): return self._time

    @property
    def gravity(self): return self._gravity

    @gravity.setter
    def gravity(self,val):
        if not isinstance(val,numbers.Number):
            raise ValueError('Must set gravity to a number')
        self._odeWorld.setGravity((0,0,-val))
        self._gravity = val

    def jitterObject(self,name,jitterSigma,jitterType='xyz'):
        o = self.getObj(name)
        if o.type == 'plane': raise ValueError('Static planes cannot be jittered')
        else:
            usage = np.array(['x' in jitterType, 'y' in jitterType, 'z' in jitterType])
            o.position += np.random.normal(0,jitterSigma,3)*usage

    def _rescaleForce(self,forcevec):
        return np.array(forcevec) / self._stepsize

    def applyForceToObj(self,name,forcevec, relativeLoc = (0,0,0), suppressErr = False):
        o = self.getObj(name)
        if o._odeBody is None and not suppressErr:
            raise ValueError('Cannot apply force to static objects')
        else:
            o._odeBody.addForceAtRelPos(self._rescaleForce(forcevec),relativeLoc)

    # Applies a universal force to the center of mass of all objects
    def applyUniversalForce(self,forcevec):
        for onm in self.objNames():
            self.applyForceToObj(onm,forcevec,(0,0,0),True)

    # Applies a single force somewhere in the world (may or may not hit bodies)
    def applySingleForce(self,forcevec,position):
        for onm in self.objNames():
            o = self.getObj(onm)
            if o._odeBody is not None:
                o._odeBody.addForceAtPos(self._rescaleForce(forcevec),position)

    def deleteObject(self,name):
        del self._objs[name]

    def objNames(self):
        return self._objs.keys()

    def jointNames(self):
        return self._joints.keys()

    def goalNames(self):
        return self._goals.keys()

    def isGoal(self,name):
        return (name in self.goalNames())

    def loadMeshFromFile(self,filename,objname,initpos = (0.,0.,0.),initvel = (0.,0.,0.), \
                         initquat = (1.,0.,0.,0.), scale = 1., **kwargs):
        if not os.path.isfile(filename):
            raise IOError(filename + ' not found')
        mesh = trimesh.load_mesh(filename)
        #if not mesh.is_watertight: raise Exception('Only watertight meshes allowed! ' + filename)
        mesh.vertices -= mesh.center_mass
        mesh.vertices *= scale
        pem = PEMesh(self,objname,mesh,initpos,initvel,initquat,**kwargs)
        self._objs[objname] = pem
        return pem


    # Function for ensuring objects don't overlap after jittering
    # Logic thought through by P Battaglia
    def repel(self,steps=1000,thresh=10,step_size=.01,resetCFM = .9, resetERP = .9):
        # Intro - record existing attributes before resetting them
        tmp_cfm = self._odeWorld.getCFM()
        tmp_erp = self._odeWorld.getERP()
        tmp_grav = self._gravity
        tmp_t = self._time
        tmp_stepsize = self._stepsize
        tmp_origattr = dict() # [linvel,angvel,mass]
        for n in self.objNames():
            obj = self._objs[n]
            if obj.type != 'plane':
                tmp_origattr[n] = [obj.velocity,obj.angvel,obj.mass]

        # Remove all velocity
        def fullDamp(o):
            if o.mass > 0:
                o.velocity = (0,0,0)
                o.angvel = (0,0,0)

        # Set attributes to new, small amounts & turn off gravity
        self._odeWorld.setCFM(resetCFM)
        self._odeWorld.setERP(resetERP)
        self._stepsize = step_size
        self.gravity = 0.
        for n in self.objNames():
            obj = self._objs[n]
            if obj.mass > 0:
                fullDamp(obj)
                obj.density = 1.

        # Continue to take small steps until there aren't any remaining collisions
        done_ct = 0
        for istep in xrange(steps):
            self.step(step_size)
            if self._hascollisions: done_ct = 0
            else: done_ct += 1
            if done_ct > thresh: break
            [fullDamp(self._objs[n]) for n in self.objNames()] # Reset velocities

        # Coda: reset everything
        self.gravity = tmp_grav
        self._odeWorld.setCFM(tmp_cfm)
        self._odeWorld.setERP(tmp_erp)
        self._time = tmp_t
        self._stepsize = tmp_stepsize
        for n in self.objNames():
            obj = self._objs[n]
            if obj.type != 'plane':
                vel, avel, mass = tmp_origattr[n]
                if mass > 0:
                    obj.mass = mass
                    obj.velocity = vel
                    obj.angvel = avel

        return istep
