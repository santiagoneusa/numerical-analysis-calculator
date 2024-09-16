# Numerical Analysis Calculator

Success response
```
response = {
    'status': 'success',
    'message': f'The solution was found on x = {solution} with a value of f(x) = {function(solution)}',
    # matrix with the values of the table in order: iteration, xi, f(xi), absolute error i
    'table': [['0', 'x0', 'f(x0)', 'e0'], ['1', 'x1', 'f(x1)', 'e1']],
}
```

Error response
```
response = {
    'status': 'error',
    'message': f'An error ocurred: {e}',
}
```
