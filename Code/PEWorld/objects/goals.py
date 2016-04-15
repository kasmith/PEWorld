'''

Classes for making areas that trigger events when objects move into them

'''

from __future__ import division
import ode
import numpy as np


class BoxGoal(object):

    def __init__(self,peworld,name,dimensions = (1.,1.,1.), position = (0.,0.,0.), quaternion = (1.,0.,0.,0.)):
        self._PEWorld = peworld
        self._name = name
        self._dims = dimensions
        self._odeGeom = ode.GeomBox(self._PEWorld._odeSpace,dimensions)
        self._odeGeom.setPosition(position)
        self._odeGeom.setQuaternion(quaternion)
        self._type = 'goal'
        self._odeGeom._myName = name

    def copy(self,peworld):
        return BoxGoal(peworld,self.name,self.dimensions,self.position,self.quaternion)

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def dimensions(self):
        return np.array(self._dims)

    @property
    def position(self):
        return np.array(self._odeGeom.getPosition())

    @position.setter
    def position(self,val):
        if len(val) != 3 or not all([isinstance(x,numbers.Number) for x in val]):
            raise ValueError('Must use a 3-length tuple of numbers to set a position')
        self._odeGeom.setPosition(val)

    @property
    def rotation(self):
        return np.array(self._odeGeom.getRotation())

    @rotation.setter
    def rotation(self,val):
        if len(val) != 9 or not all([isinstance(x,numbers.Number) for x in val]):
            raise ValueError('Must use a 9-length tuple of numbers to set rotation')
        self._odeGeom.setRotation(val)

    @property
    def quaternion(self):
        return np.array(self._odeGeom.getQuaternion())

    @quaternion.setter
    def quaternion(self,val):
        if len(val) != 4 or not all([isinstance(x,numbers.Number) for x in val]):
            raise ValueError('Must use a 4-length tuple of numbers to set quaternion')
        self._odeGeom.setQuaternion(val)
