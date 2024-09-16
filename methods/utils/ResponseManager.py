class ResponseManager():

    @staticmethod
    def success_response(table):
        return {
            'status': 'success',
            'message': f'The solution was found on x = {table[-1][1]} with a value of f(x) = {table[-1][2]}',
            'table': table,
        }

    @staticmethod
    def warning_response():
        pass

    @staticmethod
    def error_response():
        pass