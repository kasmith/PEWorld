#include <Python.h>
#include <math.h>
#include <structmember.h>
#include <vector>
#include <string>
#include <algorithm>
#include "btBulletDynamicsCommon.h"
#include "btBulletCollisionCommon.h"
#include "structmember.h"


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

// Return a new RigidWorld with default configurations
static RigidWorld* NewRW() {
    RigidWorld* rw;
    rw->btCC = new btDefaultCollisionConfiguration();
    rw->btCD = new btCollisionDispatcher(self->btCC);
    rw->btBPI = new btDbvtBroadphase();
    rw->btCS = new btSequentialImpulseSolver();
    rw->btW = new btDiscreteDynamicsWorld(self->btCD,self->btBPI,self->btCS,self->btCC);
    rw->gravStrength = 0.0;
    rw->stepHZ = 0.0;
    return rw;
};

// Initialize a RigidWorld structure - takes gravity, whether a ground is added, speed of physics updating
static RigidWorld* RWInit(RigidWorld *rw, float gravity, bool useGround, float stepHZ);

// Find the index of a RigidObj by name within a RigidWorld; return -1 if not there
static int FindByName(RigidWorld *self, std::string *name);

// Remove an object from the world by name (returns 0 if good, -1 if doesn't exist)
static int RemoveObject(RigidWorld *rw, std::string *name);

// Add_Plane - adds a plane to the world and returns a pointer to that plane
static RigidObj* Add_Plane(RigidWorld *rw, std::string *name, btVector3 *normal, float mass, btVector3 *localInertia);

// Add_Box - adds a rectilinear box to the world and returns a pointer to that object
static RigidObj* Add_Box(RigidWorld *rw, std::string *name, btVector3 *midpt, btVector3 *dimensions, float mass, btVector3 *localInertia);