import matplotlib
import numpy as np
from math import sqrt

def makeRange(low, step, high):
    """
    makeRange(low, step, high):
        returns a vector (range_vec) which has values from low to high, at intervals of step.
        
        3 inputs:
            low  - Must be a number of any type (int, float, etc).  It will be the 0th index of range_vec.

            step - Must be a number of any type (int, float, etc), and will be the difference between every
                   adjacent element of range_vec.

            high - Must be a number of any type (int, float, etc).  It will be the final value in range_vec

        1 output:
            range_vec - An array of undefined length, which will be determined by the low and high values,
                        and the number of steps between them.
    """
    range_vec = [low]
    while range_vec[-1] <= high:
        range_vec.append(range_vec[-1]+step)

    return range_vec

def makeGrid(mesh_size,val=0):
    """
    makeGrid(mesh_size):
        Returns a n-element array of n-element arrays of zero--designed to be an n x n matrix of all zero values.
        This is to account for initial condition of theta = 0 throughout domain.

        2 inputs:
            mesh_size - Determines the number of elements (n = mesh_size + 1) in each row/col of the n x n matrix
                        n = mesh_size + 1 because len(0,1,2,...,n) = n + 1
            val       - Determines the value filled by the matrix.  Default is 0, and val can be omitted from the
                        input unless otherwise necessary.

        1 output:
            grid_matrix - An empty n x n matrix
    """
    empty_row = []
    grid_matrix = []
    for i in range(0,mesh_size+1):
        empty_row.append(val)
    for i in range(0,mesh_size+1):
        grid_matrix.append(empty_row)
    return grid_matrix

def error_calc(error):
    """
    error_calc(error):
        Returns a scalar value of the error from the given error matrix

        1 input:
            error - Matrix created by makeGrid() of values defined in the main() function

        1 output:
            rel_error - Relative error calculated using the L2-norm of the given error matrix
    """
    squared_sum = 0.0
    for row in error:
        for val in row:
            squared_sum = val**2
    rel_error = sqrt(squared_sum)
    return rel_error

def main():
    alpha = .01
    THETA_ALL = {}
    for mesh_size in [ 10, 20, 40, 80 ]:
        d_x = 1/mesh_size
        d_t = .01
        while d_t > ((d_x^2)/(4*alpha)):
            response = ''
            while response not in ['y','n']:
                response = raw_input('d_t too low, unstable function.  Continue? [y]es [n]o: ')
            if response == 'y':
                continue
            else:
                d_t = int(raw_input('New d_t = '))
        long_const_term = 1-((4*d_t*alpha)/(d_x^2))
        short_const_term = ((4*d_t*alpha)/(d_x^2))
        time_vec = [0]
        error = makeGrid(mesh_size,1)
        theta = [makeGrid(mesh_size)]
        iter_num = 0
        while error_calc(error) > 10**-6:
            iter_num += 1
            theta_0 = theta[-1] #THETA IS ASSUMED TO BE AN ARRAY OF VERTICAL VECTORS, IE i = X, j = y for theta[i][j]
            theta_1 = makeGrid(mesh_size,None)
            for i in range(0,mesh_size+1):
                for j in range(0,mesh_size+1):
                    if i == 0:
                        theta_i_1 = 1
                        theta_i1 = theta_0[i+1][j]
                    elif i == mesh_size:
                        d_theta_i1 = 0
                        theta_i1 = 0
                        theta_i_1 = theta_0[i-1][j]
                    else:
                        theta_i1 = theta_0[i+1][j]
                        theta_i_1 = theta_0[i-1][j]
                    if j == mesh_size:
                        theta_j1 = i/mesh_size
                        theta_j_1 = theta_0[i][j-1]
                    elif j == 0:
                        theta_j_1 = 0
                        theta_j1 = theta_0[i][j+1]
                    else:
                        theta_j1 = theta_0[i][j+1]
                        theta_j_1 = theta_0[i][j-1]
                    theta_ij = theta_0[i][j]

                    new_term = long_const_term*theta_ij+short_const_term*(theta_i_1+theta_i1+theta_j_1+theta_j1-4*theta_ij)
                    theta_1[i][j] = new_term
                    error[i][j] = theta_1[i][j] - theta_0[i][j]
            theta.append(theta_1)
            time_vec.append(time_vec[-1]+d_t)
            if iter_num > 75:
                print "STOPPED AT 75 ITERATIONS"
                break
        mesh_string = "MESH #%i" %mesh_size
        THETA_ALL[mesh_string] = theta
    return THETA_ALL

if __name__ == "__main__":
    THETA_ALL = main()
    user_input = ''
    while user_input != 'end':
        user_input = raw_input("Mesh size? [10] [20] [40] [80] [end]:  ")
        if user_input !=  'end':
            theta = THETA_ALL["MESH #%s" %user_input]
            theta_1 = theta[-1]
            x = []
            y = []
            for 
