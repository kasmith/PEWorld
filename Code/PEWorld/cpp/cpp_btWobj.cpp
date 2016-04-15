#include <Python.h>
#include <math.h>
#include <structmember.h>
#include <vector>
#include <string>
#include <algorithm>
#include "btBulletDynamicsCommon.h"
#include "btBulletCollisionCommon.h"
#include "structmember.h"

//extern "C" {


/**************************************
*
* Structure definitions
*
***************************************/

/*
Defines a RigidObj structure
This holds the appropriate name, body, and shapes for a single object in the world
Possible objtypes include: box, sphere, cylinder, pyramid, cone, tetrahedron, plane, vertex, compound
*/
typedef struct{
    std::string name;
    std::string objtype;
    btRigidBody* body;
    std::vector<btCollisionShape*> shapes;
} RigidObj;

/*
Define the RigidWorld structure
Includes:
    The world & various interfaces for collisions/constraints
    Array for all bodies
    Array for all shapes
    Array of body/shape names
    Gravity force
    Default timesteps to take
*/
typedef struct {
    PyObject_HEAD
    btDynamicsWorld* btW;
    btBroadphaseInterface* btBPI;
    btCollisionConfiguration* btCC;
    btCollisionDispatcher* btCD;
    btConstraintSolver* btCS;
    float gravStrength;
    float stepHZ;
    std::vector<RigidObj*> objs;
} RigidWorld;


/**************************************
*
* Functions to add/remove objects (for cpp code)
*
***************************************/

// Find the index of a RigidObj by name; return -1 if not there
static int FindByName(RigidWorld *self, std::string *name) {
    RigidObj *o;
    int s = self->objs.size();
    for (int i = 0; i < s; i++) {
        o = self->objs[i];
        if (name->compare(o->name) == 0)
            return i;
    }
    return -1;
};

// Helper to clear vector memory (from http://stackoverflow.com/questions/1525535/delete-all-items-from-a-c-stdvector)
typedef struct
{
    void operator()( btCollisionShape*& element ) const
    {
        delete element;
        element = NULL;
    }
}  delete_pointer_element;

// Remove an object from the world by name (returns 0 if good, -1 if doesn't exist)
static int RemoveObject(RigidWorld *self, std::string *name) {
    int idx = FindByName(self,name);
    if (idx == -1) return -1;
    RigidObj *o = self->objs[idx];
    btRigidBody *body = o->body;
    std::vector<btCollisionShape*> shs = o->shapes;
    self->btW->removeRigidBody(body);
    int s = shs.size();
    for (int i = 0; i < s; i++) {
        delete shs[i];

    }
    std::for_each(shs.begin(),shs.end(),delete_pointer_element);
    shs.clear();
    delete body;
    delete o;
    self->objs.erase(self->objs.begin()+idx);
    return 0;
};

// Add_Plane - defaults to infinite mass
static RigidObj* Add_Plane(RigidWorld *self, std::string *name, btVector3 *normal, float mass, btVector3 *localInertia) {
    btCollisionShape* plShape = new btStaticPlaneShape(*normal,0);
    btDefaultMotionState* plMot = new btDefaultMotionState(btTransform(btQuaternion(0,0,0,1),btVector3(0,0,0)));
    btRigidBody::btRigidBodyConstructionInfo = plRBCI(mass, plMot, plShape, *localInertia);
    btRigidBody* plBody = btRigidBody(plRBCI);
    self->btW->addRigidBody(plBody);
    std::vector<btCollisionShape*> thisshape = { *plShape };
    RigidObj thisObj = {
        name,
        "plane",
        plBody,
        thisshape
    };
    self->objs.push_back(&thisObj);
    return &thisObj;
};


/**************************************
*
* Pythonized methods
*
***************************************/

/*
static PyObject * py_objNames(RigidWorld* self) {
    long s = self->objs.size();
    PyObject* ret = PyTuple_New(s);

    for (int i = 0; i < s; i++) {
        PyTuple_SetItem(ret,i,self->objs[i]->name);
    }

};
*/

static PyObject * py_setGravity(RigidWorld *self, PyObject *args) {
    float grav;
    if (! PyArg_ParseTuple(args,"f",&grav)) {
        return -1;
    }
    self->btW->setGravity(btVector3(0,-grav,0));
    self->gravStrength = grav;
    return 0;
};

/**************************************
*
* Default functions & definitions for Python
*
***************************************/


/* Creates a new Bullet World */
static PyObject * RigidWorld_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    RigidWorld *self;

    self = (RigidWorld *)type->tp_alloc(type,0);
    if (self != NULL) {
        self->btCC = new btDefaultCollisionConfiguration();
        self->btCD = new btCollisionDispatcher(self->btCC);
        self->btBPI = new btDbvtBroadphase();
        self->btCS = new btSequentialImpulseSolver();
        self->btW = new btDiscreteDynamicsWorld(self->btCD,self->btBPI,self->btCS,self->btCC);
        self->gravStrength = 0.0;
        self->stepHZ = 0.0;
    }
    return (PyObject *)self

};

/*
    Initializes the world and adds gravity
    Called as:
        RigidWorld(gravity = 9.8, useGround = True, stepHZ = .01)
*/

static int RigidWorld_init(RigidWorld *self, PyObject *args, PyObject *kwds) {
    float grav = 0.0, hz = 0.0;
    bool ugrnd = false;

    static char *kwlist[] = {"gravity","useGround","stepHZ",NULL};

    if (! PyArg_ParseTupleAndKeywords(args,kwds,'fbf',kwlist, &grav, &ugrnd, &hz)) {
        return -1;
    }

    self->gravStrength = grav;
    self->btW->setGravity(btVector3(0,-grav,0));
    self->stepHZ = hz;

    if(ugrnd) {
        Add_Plane(self,"Ground",btVector3(0,1,0),0.0,btVector3(0,0,0));
    }
    return 0;
};

/* Shuts down Bullet objects and cleans up */
static void RigidWorld_dealloc(RigidWorld* self) {
    RigidObj* o; // Delete all objects (including unattaching them)
    while(self->objs.size() > 0) {
        o = self->objs[0];
        RemoveObject(self,o->name);
    }
    delete self->btW; // Delete the bt resolvers
    delete self->btCS;
    delete self->btCD;
    delete self->btCC;
    delete self->btBPI;
    Py_TYPE(self)->tp_free((PyObject*)self);
};


// Adding definitions for Python
static PyMemberDef RigidWorld_members[] = {
    {"gravity", T_FLOAT, offsetof(RigidWorld, gravStrength),READONLY,"Strength of gravity in Bullet World"},
    {"HZ", T_FLOAT, offsetof(RigidWorld, stepHZ), READONLY,"Default time resolution of physics"},
    {NULL} // Sentinel
};

static PyMethodDef RigidWorld_methods[] = {
    {"setGravity", (PyCFunction)py_setGravity, METH_VARARGS, "Resets the strength of gravity in the world"},
    {NULL} // Sentinel
};

//} // entern "C"

static PyTypeObject RigidWorldType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "btWorld.btRigidWorld",           /* tp_name */
    sizeof(RigidWorld),             /* tp_basicsize */
    0,                           /* tp_itemsize */
    (destructor)RigidWorld_dealloc, /* tp_dealloc */
    0,                           /* tp_print */
    0,                           /* tp_getattr */
    0,                           /* tp_setattr */
    0,                           /* tp_as_async */
    0,                           /* tp_repr */
    0,                           /* tp_as_number */
    0,                           /* tp_as_sequence */
    0,                           /* tp_as_mapping */
    0,                           /* tp_hash  */
    0,                           /* tp_call */
    0,                           /* tp_str */
    0,                           /* tp_getattro */
    0,                           /* tp_setattro */
    0,                           /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,          /* tp_flags */
    "btRigidWorld Objects",           /* tp_doc */
    0,                         /* tp_traverse */
    0,                         /* tp_clear */
    0,                         /* tp_richcompare */
    0,                         /* tp_weaklistoffset */
    0,                         /* tp_iter */
    0,                         /* tp_iternext */
    RigidWorld_methods,             /* tp_methods */
    RigidWorld_members,             /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)RigidWorld_init,      /* tp_init */
    0,                         /* tp_alloc */
    RigidWorld_new,                 /* tp_new */
};

/* Define the module */
static struct PyModuleDef RigidWorldModule = {
    PyModuleDef_HEAD_INIT,
    "RigidWorld",
    "Module for starting up btWorld objects",
    -1,
    NULL, NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC
PyInit_RigidWorld(void)
{
    PyObject* m;

    RigidWorldType.tp_new = PyType_GenericNew;
    if (PyType_Ready(&RigidWorldType) < 0)
        return NULL;

    m = PyModule_Create(&RigidWorldModule);
    if (m == NULL)
        return NULL;

    Py_INCREF(&RigidWorld_Type);
    PyModule_AddObject(m, "RigidWorld", (PyObject *)&RigidWorldType);
    return m;
}



