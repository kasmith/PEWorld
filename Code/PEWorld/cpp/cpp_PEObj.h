#include <math.h>
#include <vector>
#include <string>
#include <algorithm>
#include <bullet/btBulletDynamicsCommon.h>
#include <bullet/btBulletCollisionCommon.h>

/*

*/
class PEObj // Base class for objects - should never be created
{
    public:
        // Functions to query object
        btVector3 getCenterOfMass(void); // Returns a copy of the center of mass
        float getFriction(void); // Returns the coefficient of friction
        float getElasticity(void); // Returns the elasticity of the object
        std::string getName(void);
        std::string getType(void);

        // Functions to set objects
        void setCenter(btVector3* center);
        void move(btVector3* movement);
        void setFriction(float friction);
        void setElasticity(float elasticity);
        void rotateBy(btQuaternion* rotation);

        void setName(std::string newname);

        /*
            Other functions to-do:
            Get volume
            Apply force
        */

        ~PEObj();

    protected:
        btVector3 CoM; // Center of mass
        std::vector<btVector3*> vertices;
        btScalar myFriction;
        btScalar myElasticity;
        btScalar myMass;
        std::string myName;
        std::string myType;

        btRigidBody* myBody;
        btDiscreteDynamicsWorld* myWorld;

        void remakeBody(void); // Deletes and adds body to change attributes
};

// Slight extension of the base class for non-planar things
class PEObj3D: public PEObj
{
    public:
        std::vector<btVector3*> getVertices(void); // Returns a copy of all vertices
        btVector3 getVelocity(void);
        btQuaternion getRotation(void); // Returns rotation
        float getMass(void);

        void setRotation(btQuaternion* rotation);
        void setVelocity(btVector3* velocity);
        void setMass(float mass);
};


// A rectilinear box object
class PEBox: public PEObj3D
{
    public:
        PEBox(btDiscreteDynamicsWorld* world, std::string name, btVector3* dimensions, btVector3 center = btVector3(0,0,0),
            btQuaternion rotation = btQuaternion(0,0,0,1), float mass = 0., float friction = 0., float elasticity = 1.);
};

// An infinite, static plane (typically used for the ground or bounding walls)
class PEPlane: public PEObj
{
    public:
        PEPlane(btDiscreteDynamicsWorld* world, std::string name, btVector3 center = btVector3(0,0,0),
            btVector3 normal = btVector3(0,1,0), float friction = 0., float elasticity = 1.);
};

class PEPoly: public PEObj3D
{
    public:
        PEPoly(btDiscreteDynamicsWorld* world, std::string name, std::vector<btVector3*> vertices,
        btVector3 center = btVector3(0,0,0), btQuaternion rotation = btQuaternion(0,0,0,1), float mass = 0.,
        float friction = 0., float elasticity = 1.);
};

