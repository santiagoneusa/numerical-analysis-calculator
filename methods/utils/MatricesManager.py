import numpy as np


class MatricesManager:
    @staticmethod
    def get_matrix_determinant(matrix):
        return np.linalg.det(matrix)
    
    @staticmethod
    def parse_matrix(matrix_string):
        try:
            rows = matrix_string.strip().split(';')
            matrix = []
            for row in rows:
                elements = row.strip().split()
                matrix.append([float(el) for el in elements])
            return np.array(matrix)
        except Exception as e:
            raise ValueError(f"Entrada de matriz inválida: {e}")

    @staticmethod
    def parse_vector(vector_string):
        try:
            elements = vector_string.strip().split()
            return np.array([float(el) for el in elements])
        except Exception as e:
            raise ValueError(f"Entrada de vector inválida: {e}")

    @staticmethod
    def is_square_matrix(matrix):
        return matrix.shape[0] == matrix.shape[1]

    @staticmethod
    def are_dimensions_compatible(A, b, x0):
        n = A.shape[0]
        return b.shape[0] == n and x0.shape[0] == n
