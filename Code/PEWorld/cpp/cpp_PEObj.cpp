#include "cpp_PEObj.h"

/*
    Common functions for all objects
*/

btVector3 PEObj::getCenterOfMass(void) {  // DO I NEED BTTRANSFORM I THINK?
    return myBody->getCenterOfMassPosition();
}



float PEObj::getFriction(void) {
    return (float)myFriction;
}

float PEObj::getElasticity(void){
    return (float)myElasticity;
}


std::string PEObj::getName(void) {
    return myName;
}

std::string PEObj::getType(void) {
    return myType;
}

// Destructor removes the body from the world and destroys all relevant objects
PEObj::~PEObj(){
    myWorld->removeRigidBody(myBody);
    btCollisionShape* curShape = myBody->getCollisionShape();
    delete myBody->getMotionState();
    delete myBody;
    delete curShape;
}

void PEObj::remakeBody(void) {
    btMotionState* curMotion = myBody->getMotionState();
    btCollisionShape* curShape = myBody->getCollisionShape();
    btVector3 curInertia = myBody->getLocalInertia();

    // Remake the construction info with any updated information
    btRigidBody::btRigidBodyConstructionInfo newRBCI(myMass, curMotion, curShape, curInertia);
    newRBCI.m_friction = myFriction;
    newRBCI.m_restitution = myElasticity;

    // Remove old body from the world and make/add new one
    btRigidBody* newRB = new btRigidBody(newRBCI);
    myWorld->removeRigidBody(myBody);
    delete myBody;
    myBody = newRB;
    myWorld->addRigidBody(myBody);
}

/*
std::vector<btVector3*> PEObj3D::getVertices(void){
    btCollisionShape* shape = myBody->getCollisionShape();
    int nVertices = shape->getNumVertices();
    std::vector<btVector3*> ret = {};
    btVector3* r;
    for(int i = 0; i < nVertices; i++) {
        shape->getVertex(i, r);
        ret.push_back(r);
    }
    return ret;
}
*/

btQuaternion PEObj3D::getRotation(void) {
    return myBody->getOrientation();
}

float PEObj3D::getMass(void){
    return (float)myMass;
}

btVector3 PEObj3D::getVelocity(void){
    return myBody->getLinearVelocity();
}


/*
    Constructors for specific objects
*/

PEPlane::PEPlane(btDiscreteDynamicsWorld* world, std::string name, btVector3 center,
    btVector3 normal, float friction, float elasticity) {
        myWorld = world;
        myName = name;
        myFriction = friction;
        myElasticity = elasticity;
        myMass = 0;
        myType = "plane";

        btCollisionShape* pShape = new btStaticPlaneShape(normal,1);
        btDefaultMotionState* pMotion = new btDefaultMotionState(btTransform(btQuaternion(0,0,0,1),center));
        btRigidBody::btRigidBodyConstructionInfo pRBCI(0.,pMotion,pShape,btVector3(0,0,0));
        pRBCI.m_friction = friction;
        pRBCI.m_restitution = elasticity;
        myBody = new btRigidBody(pRBCI);

        myWorld->addRigidBody(myBody);
    }

