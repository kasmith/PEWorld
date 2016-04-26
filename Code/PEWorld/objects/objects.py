'''

Classes for objects that can be attached to worlds

'''
from __future__ import division
import ode
import numbers
import numpy as np
from ..utils import quaternionProduct

class BasePEObj(object):

    def __init__(self,peworld,name,**kwargs):
        if (type(self) == BasePEObj): raise Exception('Base class objects should never be created!')
        # Initialize things
        self._PEWorld = peworld
        self._name = name

        if 'mass' in kwargs and 'density' in kwargs:
            raise Exception('Can only set either mass or density')

        self._mass = kwargs.get('mass',None)
        if self._mass is not None:
            self._density = None
        else:
            self._density = kwargs.get('density',1.)

        self._isStatic = (self._mass is None and self._density == 0) or \
            (self._density is None and self._mass == 0)

        self._friction = kwargs.get('friction',0.4)
        self._restitution = kwargs.get('restitution',.999)

        w = self._PEWorld._odeWorld

        if not self._isStatic:
            self._odeMass = ode.Mass()
            self._odeBody = ode.Body(w)
        else:
            self._odeMass = None
            self._odeBody = None

        self._odeGeom = None
        self._type = 'none'

    @property
    def name(self):
        return self._name

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, val):
        if not isinstance(val,numbers.Number) or val < 0:
            raise ValueError('Must provide a positive number for mass')

        if self._isStatic: raise Exception("Cannot set the mass of a static body")

        self._mass = val
        self._odeMass.adjust(val)

    @property
    def volume(self): return 0. # Fake objects can't have a volume

    @property
    def density(self):
        if self.volume == 0: return 0
        else: return self.mass / self.volume

    @density.setter
    def density(self,val):
        if not isinstance(val,numbers.Number) or val < 0:
            raise ValueError('Must provide a positive number for density')
        if self._isStatic: raise Exception('Cannot set the density of a static body')
        self._mass = val*self.volume
        self._odeMass.adjust(self._mass)

    @property
    def type(self):
        return self._type

    @property
    def friction(self): return self._friction

    @friction.setter
    def friction(self,val):
        if not isinstance(val,numbers.Number) or val < 0:
            raise Exception('Must provide a positive number for friction')
        else:
            self._friction = val

    @property
    def restitution(self): return self._restitution

    @restitution.setter
    def restitution(self,val):
        if not isinstance(val,numbers.Number) or val < 0:
            raise ValueError('Must provide a positive number for coefficient of restitution')
        else:
            self._restitution = val

    @property
    def position(self):
        if not self._isStatic: return np.array(self._odeBody.getPosition())
        else: return np.array(self._odeGeom.getPosition())

    @position.setter
    def position(self,val):
        if len(val) != 3 or not all([isinstance(x,numbers.Number) for x in val]):
            raise ValueError('Must use a 3-length tuple of numbers to set a position')
        else:
            if not self._isStatic: self._odeBody.setPosition(val)
            else: self._odeGeom.setPosition(val)

    @property
    def velocity(self):
        if self._isStatic: return np.array( (0.,0.,0.) )
        return np.array(self._odeBody.getLinearVel())

    @velocity.setter
    def velocity(self,val):
        if len(val) != 3 or not all([isinstance(x,numbers.Number) for x in val]):
            raise ValueError('Must use a 3-length tuple of numbers to set velocity')
        if self._isStatic:
            raise Exception('Cannot set the velocity of a static object')
        self._odeBody.setLinearVel(val)

    @property
    def speed(self):
        return np.linalg.norm(self.velocity)

    @speed.setter
    def speed(self,val):
        if not isinstance(val,numbers.Number):
            raise ValueError("Must provide a number to set the speed")
        speedadj = val/self.speed
        self.velocity *= speedadj

    @property
    def angvel(self):
        if self._isStatic: return np.array( (0.,0.,0.) )
        return np.array(self._odeBody.getAngularVel())

    @angvel.setter
    def angvel(self,val):
        if len(val) != 3 or not all([isinstance(x,numbers.Number) for x in val]):
            raise ValueError('Must use a 3-length tuple of numbers to set angular velocity')
        if self._isStatic:
            raise Exception('Cannot set angular velocity of a static object')
        self._odeBody.setAngularVel(val)

    @property
    def rotation(self):
        if self._isStatic: return np.array(self._odeGeom.getRotation())
        else: return np.array(self._odeBody.getRotation())

    @rotation.setter
    def rotation(self,val):
        if len(val) != 9 or not all([isinstance(x,numbers.Number) for x in val]):
            raise ValueError('Must use a 9-length tuple of numbers to set rotation')
        if self._isStatic: self._odeGeom.setRotation(val)
        else: self._odeBody.setRotation(val)

    @property
    def quaternion(self):
        if self._isStatic: return np.array(self._odeGeom.getQuaternion())
        else: return np.array(self._odeBody.getQuaternion())

    @quaternion.setter
    def quaternion(self,val):
        if len(val) != 4 or not all([isinstance(x,numbers.Number) for x in val]):
            raise ValueError('Must use a 4-length tuple of numbers to set quaternion')
        if self._isStatic: self._odeGeom.setQuaternion(val)
        else: self._odeBody.setQuaternion(val)

    @property
    def rotMatrix(self):
        r = np.matrix(self.rotation)
        r.shape = (3,3)
        return r

    @rotMatrix.setter
    def rotMatrix(self,val):
        pass # DO THIS HERE

    def rotateBy(self,quat):
        if len(val) != 4 or not all([isinstance(x,numbers.Number) for x in val]):
            raise ValueError('Must use a 4-length tuple of numbers (quaternion) to rotate')
        self.quaternion = quaternionProduct(self.quaternion,quat)

    @property
    def momentOfInertia(self):
        if self._isStatic: return None
        return self._odeMass.I


class PEBox(BasePEObj):

    def __init__(self,peworld,name,dimensions = (1.,1.,1.), initpos = (0.,0.,0.), initvel = (0.,0.,0.),
                 initquat = (1.,0.,0.,0.),**kwargs):
        super(PEBox,self).__init__(peworld,name,**kwargs)
        self._type = 'box'
        self._boxDims = dimensions
        self._odeGeom = ode.GeomBox(self._PEWorld._odeSpace,lengths=self._boxDims)
        cm = kwargs.get('customMass',None)
        if cm is not None:
            if 'mass' in kwargs and 'density' in kwargs:
                print "Note: customMass is overwriting any mass/density keywords"
            if len(cm) != 9 or not all([isinstance(x,numers.Number) for x in cm]):
                raise ValueError('Must use a 9-length tuple of numbers for setting custom mass (see PyODE API)')

        # Initialize the ODE objects
        if not self._isStatic:
            vol = dimensions[0]*dimensions[1]*dimensions[2]
            if self._mass is None:
                self._mass = vol * self._density
            else:
                self._density = self._mass / vol
            if cm is not None:
                self._odeMass.setParameters(cm[0],cm[1],cm[2],cm[3],cm[4],cm[5],cm[6],cm[7],cm[8])
            else:
                self._odeMass.setBoxTotal(self._mass,self._boxDims[0],self._boxDims[1],self._boxDims[2])
            self._odeBody.setMass(self._odeMass)
            self._odeBody.shape = self._type
            self._odeBody.boxsize = dimensions
            self._odeGeom.setBody(self._odeBody)
            self._odeBody.setPosition(initpos)
            self._odeBody.setLinearVel(initvel)
            self._odeBody.setQuaternion(initquat)
        else:
            self._odeGeom.setPosition(initpos)
            self._odeGeom.setQuaternion(initquat)
        self._odeGeom._myName = name

    def copy(self,peworld):
        newbox = PEBox(peworld,self.name,self.dimensions,self.position,self.velocity,self.quaternion,
                       mass = self.mass, friction=self.friction, restitution=self.restitution)
        return newbox

    @property
    def dimensions(self):
        return self._boxDims

    @property
    def volume(self):
        bs = self._boxDims
        return bs[0]*bs[1]*bs[2]



class PEPlane(BasePEObj):

    def __init__(self,peworld,name,normal = (0.,0.,1.), dist = 0., **kwargs):
        self._PEWorld = peworld
        self._name = name
        self._normal = normal
        self._dist = dist

        w = self._PEWorld._odeWorld
        self._odeGeom = ode.GeomPlane(self._PEWorld._odeSpace,self._normal,self._dist)
        self._type = 'plane'
        self._odeGeom._myName = name

        self._mass = 0.
        self._friction = kwargs.get('friction',0.)
        self._restitution = kwargs.get('restitution',.999)

    def copy(self,peworld):
        newplane = PEPlane(peworld,self.name,self.normal,self.dist, \
                           friction=self.friction,restitution=self.restitution)
        return newplane

    @property
    def normal(self):
        return self._normal

    @property
    def dist(self):
        return self._dist

