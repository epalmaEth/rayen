import fixpath
import torch
import numpy as np
from rayen import constraints, constraint_module

# y =[tau_1,...,tau_n]'

n = 7; #Number of joints
total_tau_max = 5.0;
joint_tau_max = 1.0;

#Linear constraint:  |tau_j| <= joint_tau_max
A1 = np.concatenate((np.eye(n), -np.eye(n)), axis=0);
b1 = joint_tau_max * np.ones((2*n,1))
A2 = None;
b2 = None;
lc=constraints.LinearConstraint(A1, b1, A2, b2) 

#Quadratic constraint:   tau_1^2 + ... + tau_n^2 <= total_tau_max^2
P = 2*np.eye(n)
q = np.zeros((n,1))
r = -np.power([[total_tau_max]], 2)
qcs = [constraints.ConvexQuadraticConstraint(P, q, r)]
                                                      
cs = constraints.ConvexConstraints(lc=lc, qcs=qcs, socs=[], lmic=None)

model = torch.nn.Sequential(torch.nn.Flatten(), torch.nn.Linear(3, 64),
                            torch.nn.ReLU(),    torch.nn.Linear(64, 7),
                            constraint_module.ConstraintModule(cs, input_dim=7, create_map=True)) 

x_batched = torch.Tensor(500, 3).uniform_(-1.0, 1.0)
print(x_batched)
print(x_batched.size())
y_batched = model(x_batched)
y_batched = y_batched.squeeze()
print(y_batched)
print(y_batched.size())
print(model)

#Each element of y_batched is guaranteed to satisfy the torque constraints

# loss = ...      # y_batched can be used here
# loss.backward() # Backpropagate