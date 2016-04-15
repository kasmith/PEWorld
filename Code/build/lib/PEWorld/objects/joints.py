
from .objects import *
import ode
import numpy as np

class PEBasicJoint(object):
    def __init__(self,PEWorld,name,obj1,obj2,position):
        self._name = name
        self._PEWorld = PEWorld
        self._type = 'none'
        self._joint = None
        self._o1nm = obj1
        self._o2nm = obj2
        self._pos = position

    def hasObj(self,objnm):
        return (objnm == self._o1nm or objnm == self._o2nm)

    @property
    def position(self):
        return np.array(self._pos)

    @property
    def objects(self):
        return (self._o1nm, self._o2nm)

    @property
    def type(self):
        return self._type

    @property
    def name(self):
        return self._name

    def _reattach(self):
        raise NotImplementedError('reattach must be implemented through subclassed joints')

    def copy(self,neww):
        raise NotImplementedError('copy must be implemented through subclassed joints')

class PEHingeJoint(PEBasicJoint):
    def __init__(self,PEWorld,name,obj1name,obj2name = 'WORLD',position = (0.,0.,0.),rotationaxis = (0.,1.,0.)):
        super(PEHingeJoint,self).__init__(PEWorld,name,obj1name,obj2name,position)
        self._type = 'hinge'
        o1 = self._PEWorld.getObj(obj1name)
        if obj2name is not 'WORLD': o2b = self._PEWorld.getObj(obj2name)._odeBody
        else: o2b = None
        self._axis = rotationaxis
        self._joint = ode.HingeJoint(self._PEWorld._odeWorld,self._PEWorld._odeJoints)
        #self._joint = ode.HingeJoint(self._PEWorld._odeWorld)
        self._joint.attach(o1._odeBody,o2b)
        self._joint.setAnchor(position)
        self._joint.setAxis( rotationaxis )

    @property
    def axis(self):
        return np.array(self._axis)

    def _reattach(self):
        self._joint = ode.HingeJoint(self._PEWorld._odeWorld,self._PEWorld._odeJoints)
        #self._joint = ode.HingeJoint(self._PEWorld._odeWorld)
        o1 = self._PEWorld.getObj(obj1name)
        if obj2name is not 'WORLD': o2b = self._PEWorld.getObj(obj2name)._odeBody
        else: o2b = None
        self._joint.attach(o1._odeBody,o2b)
        self._joint.setAnchor(self._pos)
        self._joint.setAxis(self._axis)

    def copy(self,neww):
        return PEHingeJoint(neww,self.name,self._o1nm,self._o2nm,self.position,self.axis)

