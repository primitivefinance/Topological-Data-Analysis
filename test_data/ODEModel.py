import numpy as np
from scipy.sparse import csr_matrix

def model(y, t, L, source):

        # constant_vertex_matrix = np.identity(np.shape(y)[0])
        # constant_vertex_matrix[source][source] = 0
        # constant_vertex_matrix = csr_matrix(constant_vertex_matrix)
        # return - constant_vertex_matrix * L * y
        source_array = np.zeros(np.shape(y)[0])
        source_array[source] = 1
        return - L * y + source_array
