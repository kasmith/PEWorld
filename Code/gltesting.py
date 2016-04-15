__author__ = 'ksmith'

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import ode
import trimesh

w = ode.World()
w.setGravity((0,0,-9.81))
b = ode.Body(w)
s = ode.Space()

cgroup = ode.JointGroup()

def callback(args,g1,g2):
    contacts = ode.collide(g1,g2)
    world,cgroup = args
    for c in contacts:
        c.setBounce(.9)
        c.setMu(1000)
        j = ode.ContactJoint(world,cgroup,c)
        j.attach(g1.getBody(),g2.getBody())

floor = ode.GeomPlane(s, (0,0,1), 0)

mesh = trimesh.load_mesh('unit_sphere.stl')
mdat = ode.TriMeshData()
mdat.build(mesh.vertices,mesh.faces)

I = mesh.moment_inertia
#print I

mass = ode.Mass()
mass.setParameters(mesh.volume,0.,0.,0.,
                   I[0][0],I[1][1],I[2][2],I[0][1],I[0][2],I[1][2])

b.setMass(mass)
g = ode.GeomTriMesh(mdat,s)
g.setBody(b)
b.setPosition((0,0,2))

for i in range(10):
    for k in range(10):
        s.collide((w,cgroup),callback)
        w.step(.01)
        cgroup.empty()
    print b.getPosition()
