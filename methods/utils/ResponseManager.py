class ResponseManager:

    @staticmethod
    def success_response(table, message=None, headers=None):
        if not message and table:
            message = f"The solution was found on x = {table[-1][1]} with a value of f(x) = {table[-1][2]}"
        return {
            'status': 'success',
            'message': message,
            'table_headers': headers,
            'table': table,
        }

    @staticmethod
    def warning_response(table, message=None):
        if not message:
            message = "The iterations limit was reached"
        return {
            "status": "warning",
            "message": f"Warning: {message}",
            "table": table,
        }

    @staticmethod
    def error_response(error):
        return {
            "status": "error",
            "message": f"An error ocurred: {error}",
        }
