#include <iostream>
#include <BulletDynamics/btBulletDynamicsCommon.h>
//#include <bullet/btBulletCollisionCommon.h>
//#include "cpp_PEObj.h"

/*
    Test 1: does basic object creation work
*/

int main () {


    /*
    btBroadphaseInterface* broadphase = new btDbvtBroadphase();

    // Set up the collision configuration and dispatcher
    btDefaultCollisionConfiguration* collisionConfiguration = new btDefaultCollisionConfiguration();
    btCollisionDispatcher* dispatcher = new btCollisionDispatcher(collisionConfiguration);

    // The actual physics solver
    btSequentialImpulseConstraintSolver* solver = new btSequentialImpulseConstraintSolver;

    // The world.
    btDiscreteDynamicsWorld* dynamicsWorld = new btDiscreteDynamicsWorld(dispatcher, broadphase, solver, collisionConfiguration);
    dynamicsWorld->setGravity(btVector3(0, -10, 0));
    */

    //std::string name = "plane";
    //PEPlane* myplane = new PEPlane(dynamicsWorld,name);

    //std::cout << "Name: " << myplane->getName() << std::endl;
    //std::cout << "Position: " << myplane->getCenterOfMass() << std::endl;

    std::cout << "Hello world" << std::endl;

    /*
    delete dynamicsWorld;
    delete solver;
    delete dispatcher;
    delete collisionConfiguration;
    delete broadphase;
    */

    return 0;

}