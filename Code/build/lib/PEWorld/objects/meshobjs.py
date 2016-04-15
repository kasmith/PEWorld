from __future__ import division
import ode
from .objects import BasePEObj

class PEMesh(BasePEObj):
    def __init__(self,peworld,name,mesh,initpos=(0.,0.,0.),initvel=(0.,0.,0.),
                 initquat=(1.,0.,0.,0.),**kwargs):
        # Do initialization again (super is wonky)
        super(PEMesh,self).__init__(peworld,name,**kwargs)
        self._type = 'trimesh'

        w = self._PEWorld._odeWorld
        s = self._PEWorld._odeSpace

        self._odeBody = ode.Body(w)
        self._mesh = mesh

        mdat = ode.TriMeshData()
        mdat.build(mesh.vertices,mesh.faces)
        self._odeGeom = ode.GeomTriMesh(mdat,s)

        if not self._isStatic:

            if self._mass is None:
                self._mass = self._density * mesh.volume
            else:
                self._density = self._mass / mesh.volume

            I = mesh.moment_inertia * self._density
            self._odeMass.setParameters(mesh.volume * self._density,0.,0.,0.,
                               I[0][0],I[1][1],I[2][2],I[0][1],I[0][2],I[1][2])
            self._odeBody.setMass(self._odeMass)
            self._odeGeom.setBody(self._odeBody)
            self._odeBody.setPosition(initpos)
            self._odeBody.setLinearVel(initvel)
            self._odeBody.setQuaternion(initquat)
        else:
            self._odeGeom.setPosition(initpos)
            self._odeGeom.setQuaternion(initquat)
        self._odeGeom._myName = name

    def copy(self,peworld):
        newmesh = PEMesh(peworld,self.name,self._mesh,self.position,self.velocity,self.quaternion,
                         mass = self.mass, friction=self.friction, restitution=self.restitution)
        return newmesh

    @property
    def vertices(self):
        return self._mesh.vertices

    @property
    def faces(self):
        return self._mesh.faces

    @property
    def volume(self):
        return self._mesh.volume