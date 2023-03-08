import numpy as np
import torch
import torch.nn as nn
import math

import matplotlib.pyplot as plt
import utils
from linear_constraint_walker import LinearConstraintWalker

def getCube():
	Aineq=np.array([ [1, 0, 0],
				 [0, 1, 0],
				 [0, 0, 1],
				 [-1, 0, 0],
				 [0, -1, 0],
				 [0, 0, -1]]);

	bineq=np.array([[1],
				[1],
				[1],
				[0],
				[0],
				[0]])

	return Aineq, bineq


def getExample(example):

	if example==0:

		Aineq, bineq=getCube()
		Aeq=np.array([[1, 1, 1]]);
		beq=np.array([[1]]);

	elif example==1:
		Aineq=np.array([[-1,0],
					 [0, -1],
					 [0, 1],
					 [0.2425,    0.9701]]);

		bineq=np.array([[0],
					[0],
					[1],
					[1.2127]])

		Aeq=None;
		beq=None;

	elif example==2:
		Aineq, bineq=getCube()
		Aeq=np.array([[1, 1, 1],
					  [-1, 1, 1] ]);
		beq=np.array([[1],[0.1]]);
	else:
		raise("Not implemented yet")

	return Aineq, bineq, Aeq, beq


Aineq, bineq, Aeq, beq=getExample(2)

fig = plt.figure()
if(Aineq.shape[1]==3):
	ax = fig.add_subplot(111, projection="3d")
	utils.plot3DPolytopeHRepresentation(Aineq,bineq,[-1, 2, -1, 2, -1, 2], ax)
else:
	ax = fig.add_subplot(111) 

num_steps=4; #Only used in the ellipsoid_walker method
my_layer=LinearConstraintWalker(Aineq, bineq, Aeq, beq)

numel_input_walker=my_layer.getNumelInputWalker()

##This samples different angles
# all_angles = np.arange(0,2*math.pi, 0.01)
# x_batched=torch.empty(len(all_angles), numel_input_walker, 1)

# for i in range(x_batched.shape[0]): #for each element of the batch
# 	theta=all_angles[i]
# 	if(my_layer.dim==2):
# 		tmp=torch.Tensor(np.array([[math.cos(theta)],[math.sin(theta)],[3000]])); #Assumming my_layer.dim==2 here
# 	else:
# 		raise("Not implemented yet")
# 	tmp=torch.unsqueeze(tmp, dim=0)
# 	print(f"tmp.shape={tmp.shape}")
# 	x_batched[i,:,:]=tmp


num_directions=200; #for each direction you have several samples
x_batched=torch.empty(0, numel_input_walker, 1)
for i in range(num_directions): #for each direction
	direction=utils.uniformSampleInUnitSphere(my_layer.dim)
	# scalar=np.array([[3000]]);
	for scalar in list(np.linspace(-2.0, 2.0, num=10)):
		scalar_np=np.array([[scalar]])
		direction_and_scalar=np.concatenate((direction,scalar_np), axis=0);
		tmp=torch.Tensor(direction_and_scalar)
		tmp=torch.unsqueeze(tmp, dim=0)
		print(f"direction_and_scalar={direction_and_scalar}")
		x_batched=torch.cat((x_batched, tmp), axis=0)


# print(f"x_batched={x_batched}")
# exit()
# mapper=nn.Sequential(nn.Linear(x_batched.shape[1], numel_input_walker))
mapper=nn.Sequential() #do nothing.
my_layer.setMapper(mapper)

result=my_layer(x_batched)

# my_layer.plotAllSteps(ax)

# print(f"result={result}");
# print(f"result.shape={result.shape}");
result=result.detach().numpy();


if(Aineq.shape[1]==3):
	ax.scatter3D(result[:,0,0], result[:,1,0], result[:,2,0])

if(Aineq.shape[1]==2):
	ax.scatter(result[:,0,0], result[:,1,0])
	utils.plot2DPolyhedron(Aineq,bineq,ax)
	utils.plot2DEllipsoidB(my_layer.B[0,:,:].numpy(),my_layer.x0[0,:,:].numpy(),ax)
	ax.set_aspect('equal')

plt.show()
# # plot
# ax.scatter(result[:,0,0], result[:,1,0])


# plt.show()