

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from ..world import PEWorld
from ..utils import rotatePointAroundOrigin
import sys, time
import numpy as np
import trimesh

# Colors in rgba
WHITE = (1.,1.,1.,1.)
BLACK = (0.,0.,0.,1.)
BLUE = (0.,0.,1.,1.)
RED = (1.,0.,0.,1.)
GREEN = (0.,1.,0.,1.)
GREY = (190./255.,190./255.,190./255.,1.)
LIGHTGREY = (211./255.,211./255.,211./255.,1.)
DARKGREY = (.2,.2,.2,1.)
YELLOW = (1.,1.,0.,1.)
GOLD = (1.,215./255.,0.,1.)
PURPLE = (160./255.,32./255.,240./255.,1.)
SKYBLUE = (.4,.7,1.,1.)


def _defaultKeyFunc(ch,spk,view):
    if ch == " ": # Spacebar pauses and unpauses by default
        view.paused = not view.paused
    if ch == 'r':
        view.reset()
    if spk == GLUT_KEY_LEFT:
        view.cam.pos = rotatePointAroundOrigin((0,0,1),-np.pi/10.,view.cam.pos)
    if spk == GLUT_KEY_RIGHT:
        view.cam.pos = rotatePointAroundOrigin((0,0,1),np.pi/10.,view.cam.pos)
    if spk == GLUT_KEY_UP:
        cpos = np.array(view.cam.pos,dtype=np.float_)
        v = cpos - np.array(view.cam.cent)
        vl = np.linalg.norm(v)
        if vl > 1:
            v = v / vl
            cpos -= v * .2
            view.cam.pos = list(cpos)
    if spk == GLUT_KEY_DOWN:
        cpos = np.array(view.cam.pos,dtype=np.float_)
        v = cpos - np.array(view.cam.cent)
        v /= np.linalg.norm(v)
        cpos += v * .2
        view.cam.pos = list(cpos)



# Basic wrapper for camera information that gets fed into the WorldViewer
class Camera(object):
    def __init__(self,position = (0,-5,3),viewcenter = (0,0,1),fov = 45,zNear=.2,zFar=20):
        self.pos = list(position)
        self.cent = list(viewcenter)
        self.fov = fov
        self.zNear = zNear
        self.zFar = zFar

class Light(object):
    def __init__(self,position = (0,0,0),direction = (0,0,-1),ambient_rgb = LIGHTGREY,
                 diffuse_rgb = WHITE, specular_rgb = WHITE):
        if list(position) == [0,0,0]:
            self.pos = list(direction) + [0]
            self.dir = None
        else:
            self.pos = list(position) + [1]
            self.dir = list(direction)
        self.amb = ambient_rgb
        self.dif = diffuse_rgb
        self.spec = specular_rgb

    def setOGL(self,lightnum):
        glLightfv(lightnum,GL_POSITION,self.pos)
        if self.amb: glLightfv(lightnum,GL_AMBIENT,self.amb)
        if self.dif: glLightfv(lightnum,GL_DIFFUSE,self.dif)
        if self.spec: glLightfv(lightnum,GL_SPECULAR,self.spec)
        if self.dir: glLightfv(lightnum,GL_SPOT_DIRECTION,self.dir)
        glEnable(lightnum)


class WorldViewer:
    def __init__(self,world, screendims = (640,480), camera = Camera(),
                 lights = [Light()],colordict = dict(),defColor = GREY, bkgrndColor = SKYBLUE,
                 framerate = 40., startPaused = True, onStep = None, keyHandler = _defaultKeyFunc,
                 vizGoal = False):

        self.oworld = world
        self.w = self.oworld.copy()
        self.dims = screendims
        self.asp = screendims[0] / screendims[1]
        self.cam = camera
        self.lights = lights
        self.colors = colordict
        self.defC = defColor
        self.bkC = bkgrndColor
        self.paused = startPaused
        self.frtm = 1/framerate
        self.stepfnc = onStep
        self.keyfnc = keyHandler
        self.lasttime = -1
        self.vgoal = vizGoal

    def initView(self):

        glutInit([])
        glutInitDisplayMode (GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowPosition(0,0)
        glutInitWindowSize(self.dims[0],self.dims[1])
        glutCreateWindow("WorldViewer")

    def reset(self):
        self.w = self.oworld.copy()

    def draw(self,wireframe = False):

        # Set up the view
        glViewport(0,0,self.dims[0],self.dims[1])
        glClearColor(self.bkC[0],self.bkC[1],self.bkC[2],self.bkC[3])
        glClearDepth(1.)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glDisable(GL_LIGHTING)
        glEnable(GL_LIGHTING)
        glEnable(GL_NORMALIZE)
        #glCullFace(GL_BACK)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Set up the camera view
        gluPerspective (self.cam.fov,self.asp,self.cam.zNear,self.cam.zFar)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        lidx = GL_LIGHT0
        for l in self.lights:
            l.setOGL(lidx)
            lidx += 1
            if lidx >= GL_LIGHT0 + GL_MAX_LIGHTS: raise Exception('Added too many lights for your system!')

        gluLookAt(self.cam.pos[0],self.cam.pos[1],self.cam.pos[2],
                  self.cam.cent[0],self.cam.cent[1],self.cam.cent[2],
                  0,0,1)

        # Draw all objects
        for pnm in self.w._planes.keys():
            self.drawPlane(self.w.getObj(pnm),self.colors.get(pnm,self.defC),wireframe)

        for onm in self.w.objNames():
            self.drawItem(self.w.getObj(onm),self.colors.get(onm,self.defC),wireframe)

        if self.vgoal:
            for gnm in self.w._goals.keys():
                self.drawItem(self.w._goals[gnm],self.colors.get(gnm,self.defC),wireframe)

        # Swap buffers for smooth animations
        glutSwapBuffers()

        # Runs the viewer in a loop
    def run(self,wireframe = False):
        def _kfnc(c,x,y):
            if c == '\x1b':
                sys.exit(0)
            elif self.keyfnc is not None:
                self.keyfnc(c,None,self)

        def _spfnc(sp,x,y):
            if self.keyfnc:
                self.keyfnc(None,sp,self)

        glutKeyboardFunc(_kfnc)
        glutSpecialFunc(_spfnc)

        def _dfnc(): self.draw(wireframe)
        glutDisplayFunc(_dfnc)

        def _idle():
            remt = self.frtm - (time.time() - self.lasttime)
            if remt > 0:
                time.sleep(remt)

            if not self.paused:
                self.w.step(self.frtm)
                if self.stepfnc: self.stepfnc(self.w)
            glutPostRedisplay()
            self.lasttime = time.time()

        glutIdleFunc(_idle)
        glutMainLoop()

    def drawItem(self,obj,color,wireframe = False):
        type = obj.type
        r,g,b,a = color
        x,y,z = obj.position
        R = obj.rotation
        rot = [R[0],R[3],R[6],0.,
               R[1],R[4],R[7],0.,
               R[2],R[5],R[8],0.,
               x,y,z,1.]
        glPushMatrix()
        glMaterialfv(GL_FRONT,GL_AMBIENT_AND_DIFFUSE,color)
        glMultMatrixd(rot)
        if type == 'box' or type == 'goal':
            sx,sy,sz = obj.dimensions
            glScalef(sx,sy,sz)
            if wireframe:
                glutWireCube(1)
            else:
                glutSolidCube(1)
        elif type == 'trimesh':
            self.drawTrimesh(obj,wireframe) # Separated out because of complexity
        glPopMatrix()

    def drawPlane(self,obj,color,wireframe = False):
        cr,cg,cb,ca = color
        a,b,c = obj.normal

        # Figure out the rotation needed to go from (0,0,1) to normal
        nrm = np.array(obj.normal)
        nrm = nrm / np.linalg.norm(nrm)

        x,y,z = np.cross( (0,0,1), nrm)
        ang = np.arccos(np.dot( (0,0,1), nrm))

        glPushMatrix()
        glRotatef(ang,x,y,z)

        glMaterialfv(GL_FRONT_AND_BACK,GL_AMBIENT,color)

        glBegin(GL_QUADS)

        #glColor4f(cr,cg,cb,ca)

        _wparam = .00001
        #_wparam = 1


        glVertex4f(-1,-1,-obj.dist,_wparam)
        glVertex4f(-1,1,-obj.dist,_wparam)
        glVertex4f(1,1,-obj.dist,_wparam)
        glVertex4f(1,-1,-obj.dist,_wparam)

        glEnd()

        glPopMatrix()

    def drawTrimesh(self,obj,wireframe=False):
        if obj.type != 'trimesh': raise ValueError("drawTrimesh requires trimesh objects")
        vertices = obj._mesh.vertices
        faces = obj._mesh.faces
        if wireframe: glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
        for f in faces:
            glBegin(GL_TRIANGLES)
            v11,v12,v13 = vertices[f[0]]
            glVertex3f(v11,v12,v13)
            v21,v22,v23 = vertices[f[1]]
            glVertex3f(v21,v22,v23)
            v31,v32,v33 = vertices[f[2]]
            glVertex3f(v31,v32,v33)
            glEnd()
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)

