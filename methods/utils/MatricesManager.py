import numpy as np


class MatricesManager:
    @staticmethod
    def get_matrix_determinant(matrix):
        return np.linalg.det(matrix)
