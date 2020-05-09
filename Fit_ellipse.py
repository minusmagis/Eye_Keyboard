import numpy as np
import matplotlib.pyplot as plt

import numpy as np
from numpy.linalg import eig, inv

def fitEllipse(Input_array):
    x = np.squeeze(Input_array[:,:,[0]])
    y = np.squeeze(Input_array[:,:,[1]])
    x = x[:,np.newaxis]
    y = y[:,np.newaxis]
    D =  np.hstack((x*x, x*y, y*y, x, y, np.ones_like(x)))
    S = np.dot(D.T,D)
    C = np.zeros([6,6])
    C[0,2] = C[2,0] = 2; C[1,1] = -1
    E, V =  eig(np.dot(inv(S), C))
    n = np.argmax(np.abs(E))
    a = V[:,n]
    return a

# function that accepts a (n,1,2) shaped array and returns a fitted ellipse and the error in the fit
def Fit_Ellipse(Input_array):

    # # Extract x coords and y coords of the ellipse as column vectors
    X = np.squeeze(Input_array[:,:,[0]])
    Y = np.squeeze(Input_array[:,:,[1]])
    X.resize((10, 1))
    Y.resize((10, 1))
    # print(X)
    # print(Y)
    #
    # # Formulate and solve the least squares problem ||Ax - b ||^2
    A = np.hstack([X**2, X * Y, Y**2, X, Y])
    b = np.ones_like(X)
    # print(A)
    # print(b)
    x = np.linalg.lstsq(A, b,rcond=None)[0].squeeze()
    #
    # # Print the equation of the ellipse in standard form
    print('The ellipse is given by {0:.3}x^2 + {1:.3}xy+{2:.3}y^2+{3:.3}x+{4:.3}y = 1'.format(x[0], x[1],x[2],x[3],x[4]))

    plt.scatter(X, Y, label='Data Points')
    plt.show()


example_array = np.array([[[211,54]],
                          [[23,145]],
                          [[72,137]],
                          [[87,42]],
                          [[54,73]],
                          [[78,84]],
                          [[187,95]],
                          [[241,21]],
                          [[42,74]],
                          [[73,32]]])

# print(example_array.shape)
print(fitEllipse(example_array))