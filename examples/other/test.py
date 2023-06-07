#Example of how to use the vertex enumeration algorithm to obtain the V-representation of a polyhedron given by the H-representation

import numpy as np
import matplotlib.pyplot as plt
import cdd


def getVertexesRaysFromGenerators(gen):
	generators=list(gen)
	vertices=np.array([[],[]]);
	rays=np.array([[],[]]);
	for i in range(len(generators)):
		gen_i=generators[i];
		tmp=np.asarray(gen_i[1:]).reshape((-1,1));

		if(gen_i[0]==1):
			vertices=np.append(vertices,tmp, axis=1)
		else: #it is zero
			rays=np.append(rays,tmp, axis=1)

	return vertices, rays

#The polyhedron is given by Ax<=b
def plot2DPolyhedron(A, b):
	npoints=300
	d = np.linspace(-2,16,npoints)
	x1,x2 = np.meshgrid(d,d)

	tmp=1;
	for i in range(A.shape[0]):
		tmp=tmp & (A[i,0]*x1 + A[i,1]*x2 <=b[i,0]);

	plt.imshow( tmp.astype(int), extent=(x1.min(),x1.max(),x2.min(),x2.max()),origin="lower", cmap="Greys", alpha = 0.3);

def getVertexesRaysFromAb(A, b):
	bmA= np.concatenate([b, -A], axis=1) # See https://pycddlib.readthedocs.io/en/latest/matrix.html
	bmA_cdd = cdd.Matrix(bmA.tolist(), number_type='float')
	bmA_cdd.rep_type = cdd.RepType.INEQUALITY
	poly = cdd.Polyhedron(bmA_cdd)
	gen = poly.get_generators()
	print(gen)
	vertices, rays = getVertexesRaysFromGenerators(gen)
	return vertices, rays 

#points is a 2 x n matrix, where n is the number of points
def plot2DPoints(points):
	plt.scatter(points[0,:], points[1,:])

#points is a 2 x n matrix, where n is the number of rays
def plot2DRays(rays):
	for i in range(rays.shape[0]):
		plt.arrow(0, 0, rays[i,0], rays[i,1], length_includes_head=True, width=0.1)


#https://www.sharpsightlabs.com/blog/numpy-softmax/
def softmax_stable(x):
    return(np.exp(x - np.max(x)) / np.exp(x - np.max(x)).sum())

def softmax(x):
    return(np.exp(x)/np.exp(x).sum())

#https://stackoverflow.com/questions/65154622/sample-uniformly-at-random-from-a-simplex-in-python
def runif_in_simplex(n):
  ''' Return uniformly random vector in the n-simplex '''

  k = np.random.exponential(scale=1.0, size=n)
  return k / sum(k)

# Partly Taken from https://datascience.stackexchange.com/questions/102096/how-to-visualize-optimization-problems-feasible-region


#First example: Polytope (i.e., bounded polyhedron)
plt.figure(0)
A=np.array([[0,-1], [1,2], [2,-4], [-2,1]]);
b=np.array([[-2], [25], [8], [-5]]);
plot2DPolyhedron(A,b)
vertices, rays = getVertexesRaysFromAb(A,b)
plot2DPoints(vertices)
# plt.show()

# rng = np.random.default_rng()
# vals = rng.uniform(0.0,1.0,vertices.shape[1])
# bar_coord=softmax_stable(vals);

def sampleInsideConvexHullOfVertices(vertices, nsamples):
	dim=vertices.shape[0]
	all_samples=np.empty((dim,0))
	for i in range(nsamples):
		x=runif_in_simplex(vertices.shape[1])
		tmp=(vertices@x).reshape(-1,1);
		all_samples=np.append(all_samples, tmp, axis=1)
	return all_samples


def sampleInsideConicHullOfRays(rays, nsamples):
	dim=rays.shape[0]
	all_samples=np.empty((dim,0))
	for i in range(nsamples):
		mu=np.random.uniform(0.0,2.5,rays.shape[1])
		tmp=(rays@mu).reshape(-1,1);
		all_samples=np.append(all_samples, tmp, axis=1)
	return all_samples


all_samples=sampleInsideConvexHullOfVertices(vertices, 1000)
plot2DPoints(all_samples)

#Second example: Polyhedron
plt.figure(1)
A=np.array([[0,-1], [2,-4], [-2,1]]);
b=np.array([[-2], [8], [-5]]);
plot2DPolyhedron(A,b)
vertices, rays = getVertexesRaysFromAb(A,b)
plot2DPoints(vertices)
plot2DRays(rays)

nsamples=5000;
all_samples_convex_hull=sampleInsideConvexHullOfVertices(vertices, nsamples)
all_samples_conic_hull=sampleInsideConicHullOfRays(rays, nsamples)

plot2DPoints(all_samples_convex_hull+all_samples_conic_hull)

print(f"vertices=\n{vertices}\n\nrays=\n{rays}")

plt.show()





## If you wanna plot the lines
# x = np.linspace(0, 16, 2000)

# # y >= 2
# y1 = (x*0) + 0
# # 2y <= 25 - x
# y2 = (25-x)/2.0
# # 4y >= 2x - 8 
# y3 = (2*x-8)/4.0
# # y <= 2x - 5 
# y4 = 2 * x -5

# plt.plot(x, 2*np.ones_like(y1))
# plt.plot(x, y2, label=r'$2y\leq25-x$')
# plt.plot(x, y3, label=r'$4y\geq 2x - 8$')
# plt.plot(x, y4, label=r'$y\leq 2x-5$')
# plt.xlim(0,16)
# plt.ylim(0,11)
# plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
# plt.xlabel(r'$x$')
# plt.ylabel(r'$y$')