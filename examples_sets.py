import numpy as np
import utils

def getCube():
	A1=np.array([ [1.0, 0, 0],
				 [0, 1.0, 0],
				 [0, 0, 1.0],
				 [-1.0, 0, 0],
				 [0, -1.0, 0],
				 [0, 0, -1.0]]);

	b1=np.array([[1.0],
				[1.0],
				[1.0],
				[0],
				[0],
				[0]])

	return A1, b1

#Ellipsoid is defined as {x | (x-c)'E(x-c)<=1}
#Where E is a positive semidefinite matrix
def getEllipsoidConstraint(E, c):
	#Convert to (1/2)x'P_ix + q_i'x +r_i <=0
	P=2*E;
	q=(-2*E@c)
	r=c.T@E@c-1
	return utils.convexQuadraticConstraint(P, q, r)

#Sphere of radius r centered around c
def getSphereConstraint(r, c):
	return getEllipsoidConstraint((1/(r*r))*np.eye(c.shape[0]),c)

def getParaboloid3DConstraint():
	P=np.array([[1.0, 0.0, 0.0],
				[0.0, 1.0, 0.0],
				[0.0, 0.0, 0.0]])
	q=np.array([[0.0],[0.0],[-1.0]])
	r=np.array([[0.0]])

	return utils.convexQuadraticConstraint(P,q,r)

def getSOC3DConstraint():
	M=np.array([[1.0, 0.0, 0.0],
				[0.0, 1.0, 0.0],
				[0.0, 0.0, 0.0]])
	s=np.array([[0.0],[0.0],[0.0]])
	c=np.array([[0.0],[0.0],[1.0]])
	d=np.array([[0.0]])

	return utils.SOCConstraint(M, s, c, d)

def getNoneLinearConstraints():
	return None, None, None, None

def getNoneQuadraticConstraints():
	return [], [], []

def getExample(example):

	# A1, b1, A2, b2 = getNoneLinearConstraints()
	# all_P, all_q, all_r = getNoneQuadraticConstraints()
	lc=None
	qcs=[]
	socs=[]

	if example==0: #A 2D polygon embeded in 3D
		A1, b1=getCube()
		A2=np.array([[1.0, 1.0, 1.0]]);
		b2=np.array([[1.0]]);
		lc=utils.LinearConstraint(A1, b1, A2, b2)

	elif example==1: #A polygon embeded in 3D with an sphere

		A1, b1=getCube()
		A2=np.array([[1.0, 1.0, 1.0]]);
		b2=np.array([[1.0]]);
		lc=utils.LinearConstraint(A1, b1, A2, b2)
		qcs.append(getSphereConstraint(0.8,np.zeros((3,1))))


	elif example==2: #Just a sphere

		qcs.append(getSphereConstraint(2.0,np.zeros((3,1))))

	elif example==3: #Just a paraboloid

		qcs.append(getParaboloid3DConstraint())

	#A 2d polyhedron 
	elif (example==4  
	#A 2d polyhedron with a cirle
	     or example==5):   
		A1=np.array([[-1,0],
					 [0, -1.0],
					 [0, 1.0],
					 [0.2425,    0.9701]]);

		b1=np.array([[0],
					[0],
					[1],
					[1.2127]])

		lc=utils.LinearConstraint(A1, b1, None, None)

		if(example==5):
			qcs.append(getSphereConstraint(1.0,np.zeros((2,1))))

	elif example==6: #The intersection between a cube and two planes 
		A1, b1=getCube()
		A2=np.array([[1.0, 1.0, 1.0],
					  [-1.0, 1.0, 1.0] ]);
		b2=np.array([[1.0],[0.1]]);
		lc=utils.LinearConstraint(A1, b1, A2, b2)

	elif example==7: #Just a plane
		A2=np.array([[1.0, 1.0, 1.0]]);
		b2=np.array([[1.0]]);	
		lc=utils.LinearConstraint(None, None, A2, b2)


	elif example==8: #Unbounded 2d polyhedron. It has two vertices and two rays

		A1=np.array([[0.0,-1.0], [2.0,-4.0], [-2.0,1.0]]);
		b1=np.array([[-2.0], [8.0], [-5.0]]);
		lc=utils.LinearConstraint(A1, b1, None, None)

	elif example==9: #A paraboloid and a plane
		qcs.append(getParaboloid3DConstraint())

		A2=np.array([[1.0, 1.0, 1.0]]);
		b2=np.array([[1.0]]);		

	elif example==10: #A paraboloid and a shpere
		qcs.append(getParaboloid3DConstraint())
		qcs.append(getSphereConstraint(2.0,np.zeros((3,1))))	

	elif example==11: #A second-order cone 
		socs.append(getSOC3DConstraint())

	else:
		raise Exception("Not implemented yet")


	return utils.convexConstraints(lc=lc, qcs=qcs, socs=socs)