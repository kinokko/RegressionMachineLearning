#!/usr/bin/env python

# Run logistic regression training.

import numpy as np
import scipy.special as sps
import matplotlib.pyplot as plt
import assignment2 as a2


# Offset for log(0)
epsilon = 0.00000000000001

# Maximum number of iterations.  Continue until this limit, or when error change is below tol.
max_iter = 500
tol = 0.00001

# Step size for gradient descent.
etas = [0.5, 0.3, 0.1, 0.05, 0.01]

# Load data.
data = np.genfromtxt('data.txt')

# Data matrix, with column of ones at end.
X = data[:,0:3]
# Target values, 0 for class 1, 1 for class 2.
t = data[:,3]
# For plotting data
class1 = np.where(t==0)
X1 = X[class1]
class2 = np.where(t==1)
X2 = X[class2]

DATA_FIG = 1

# Set up the slope-intercept figure
# SI_FIG = 2
# plt.figure(SI_FIG)
# plt.rcParams.update({'font.size': 15})
# plt.title('Separator in slope-intercept space')
# plt.xlabel('slope')
# plt.ylabel('intercept')
# plt.axis([-5, 5, -10, 0])

EOI_FIG = 3

# Set up the error over iterations figure
plt.figure(EOI_FIG)
plt.ylabel('Negative log likelihood')
plt.title('Training logistic regression')
plt.xlabel('Epoch')

indexes = range(np.size(X, 0))
np.random.shuffle(indexes)

for eta in etas:
  # Error values over all iterations.
  e_all = []

  # Initialize w.
  w = np.array([0.1, 0, 0])

  for iter in range (0,max_iter):
    for index in indexes:
      # Compute output using current w on all data X.
      y = sps.expit(np.dot(X[index],w))
      if (y > 1 or y < 0):
        test = -1

      # Gradient of the error, using Eqn 4.91
      grad_e = np.multiply((y - t[index]), X[index].T)

      # Update w, *subtracting* a step in the error derivative since we're minimizing
      w_old = w
      w = w - eta*grad_e
      
      # Add next step of separator in m-b space.
      # plt.figure(SI_FIG)
      # a2.plot_mb(w,w_old)

    # Plot current separator and data.  Useful for interactive mode / debugging.
    # plt.figure(DATA_FIG)
    # plt.clf()
    # plt.plot(X1[:,0],X1[:,1],'b.')
    # plt.plot(X2[:,0],X2[:,1],'g.')
    # a2.draw_sep(w)
    # plt.axis([-5, 15, -10, 10])
    # plt.show()
    
    
    # Compute output using current w on all data X.
    y = sps.expit(np.dot(X,w))
    
    # e is the error, negative log-likelihood (Eqn 4.90)
    e = -np.mean(np.multiply(t,np.log(epsilon + y)) + np.multiply((1-t),np.log(epsilon + 1 - y)))

    # Add this error to the end of error vector.
    e_all.append(e)

    # Print some information.
    # print 'epoch {0:d}, negative log-likelihood {1:.4f}, w={2}'.format(iter, e, w.T)

    # Stop iterating if error doesn't change more than tol.
    if iter>0:
      if np.absolute(e-e_all[iter-1]) < tol:
        break
    
  plt.figure(EOI_FIG)  
  plt.plot(e_all, label = 'eta = {0:.2f}'.format(eta))
  # print 'epoch {0:d}, negative log-likelihood {1:.4f}, w={2}'.format(iter, e, w.T)
  
  # Plot current separator and data.  Useful for interactive mode / debugging.
  # plt.figure(DATA_FIG)
  # plt.clf()
  # plt.plot(X1[:,0],X1[:,1],'b.')
  # plt.plot(X2[:,0],X2[:,1],'g.')
  # a2.draw_sep(w)
  # plt.axis([-5, 15, -10, 10])
  # plt.show()

plt.legend()
plt.show()
