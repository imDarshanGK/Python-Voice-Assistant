import math 
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import re
import plotly.graph_objs as go
import plotly.io as pio

def basic_arithmetic(op, a, b):
    try:
        if op == 'add':
            return a + b
        elif op == 'subtract':
            return a - b
        elif op == 'multiply':
            return a * b
        elif op == 'divide':
            return a / b if b != 0 else "Error: Cannot divide by zero"
        else:
            return "Error: Invalid operation"
    except Exception as e:
        return f"Error: {str(e)}"

def solve_equation(equation):
    try:
        x = sp.symbols('x')
        solution = sp.solve(equation, x)
        return solution
    except Exception as e:
        return f"Error solving equation: {str(e)}"

def trigonometric_function(func, angle):
    try:
        angle_rad = np.radians(angle)
        if func == 'sin':
            return np.sin(angle_rad)
        elif func == 'cos':
            return np.cos(angle_rad)
        elif func == 'tan':
            return np.tan(angle_rad)
        else:
            return "Error: Invalid trigonometric function"
    except Exception as e:
        return f"Error: {str(e)}"

def differentiate(expr):
    try:
        x = sp.symbols('x')
        return sp.diff(expr, x)
    except Exception as e:
        return f"Error in differentiation: {str(e)}"

def integrate(expr):
    try:
        x = sp.symbols('x')
        return sp.integrate(expr, x)
    except Exception as e:
        return f"Error in integration: {str(e)}"

def factorial(n):
    if n < 0:
        raise ValueError("Negative numbers do not have a factorial.")
    return math.factorial(n)

def fibonacci(n):
    try:
        if n <= 0:
            return "Error: Input must be a positive integer."
        seq = [0, 1]
        for i in range(2, n):
            seq.append(seq[-1] + seq[-2])
        return seq[:n]
    except Exception as e:
        return f"Error: {str(e)}"

def matrix_operations(matrix_a, matrix_b, operation):
    try:
        if operation == 'add':
            return np.add(matrix_a, matrix_b)
        elif operation == 'subtract':
            return np.subtract(matrix_a, matrix_b)
        elif operation == 'multiply':
            return np.dot(matrix_a, matrix_b)
        else:
            return "Error: Invalid matrix operation"
    except Exception as e:
        return f"Error: {str(e)}"

def plot_function(expr, x_range):
    try:
        x = sp.symbols('x')
        f = sp.lambdify(x, expr, 'numpy')

        x_vals = np.linspace(x_range[0], x_range[1], 1000)
        y_vals = f(x_vals)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=x_vals, y=y_vals,
            mode='lines',
            name=str(expr),
            line=dict(color='blue', width=2),
            hoverinfo='x+y',  
        ))

        fig.add_trace(go.Scatter(
            x=[x_range[0], x_range[1]], y=[0, 0],
            mode='lines',
            line=dict(color='black', dash='dash'),
            hoverinfo='skip',
            showlegend=False
        ))
        fig.add_trace(go.Scatter(
            x=[0, 0], y=[min(y_vals), max(y_vals)],
            mode='lines',
            line=dict(color='black', dash='dash'),
            hoverinfo='skip',
            showlegend=False
        ))
        fig.update_layout(
            title=f'Plot of {str(expr)}',
            xaxis_title='x',
            yaxis_title='f(x)',
            xaxis=dict(
                zeroline=True,
                showline=True,
                showgrid=True,
                gridcolor='lightgray',
                zerolinecolor='black'
            ),
            yaxis=dict(
                zeroline=True,
                showline=True,
                showgrid=True,
                gridcolor='lightgray',
                zerolinecolor='black'
            ),
            plot_bgcolor='white', 
            hovermode="closest",   
        )

        fig.show()

    except Exception as e:
        return f"Error in plotting: {str(e)}"

def statistical_analysis(data):
    try:
        mean = np.mean(data)
        median = np.median(data)
        std_dev = np.std(data)
        variance = np.var(data)
        correlation = np.corrcoef(data) if len(data) > 1 else None
        regression = stats.linregress(range(len(data)), data) if len(data) > 1 else None
        
        return {
            'mean': mean,
            'median': median,
            'std_dev': std_dev,
            'variance': variance,
            'correlation': correlation[0, 1] if correlation is not None and correlation.shape == (2, 2) else None,
            'slope': regression.slope if regression else None,
            'intercept': regression.intercept if regression else None
        }
    except Exception as e:
        return f"Error in statistical analysis: {str(e)}"

def complex_operations(op, a, b):
    try:
        a_complex = complex(a)
        b_complex = complex(b)
        
        if op == 'add':
            return a_complex + b_complex
        elif op == 'subtract':
            return a_complex - b_complex
        elif op == 'multiply':
            return a_complex * b_complex
        elif op == 'divide':
            return a_complex / b_complex if b_complex != 0 else "Error: Cannot divide by zero"
        else:
            return "Error: Invalid operation"
    except Exception as e:
        return f"Error: {str(e)}"

def unit_conversion(value, from_unit, to_unit):
    conversion_factors = {
        'meters_to_feet': 3.28084,
        'feet_to_meters': 1 / 3.28084,
        'kilograms_to_pounds': 2.20462,
        'pounds_to_kilograms': 1 / 2.20462,
        # Add more conversions as needed
    }
    
    try:
        key = f"{from_unit}_to_{to_unit}"
        if key in conversion_factors:
            return value * conversion_factors[key]
        else:
            return "Error: Conversion not supported."
    except Exception as e:
        return f"Error: {str(e)}"

# Extraction functions
def extract_numbers(command):
    numbers = list(map(float, re.findall(r'-?\d+\.?\d*', command)))
    return numbers

def extract_equation(command):
    # Extract equation like "x**2 - 4"
    equation = re.search(r'solve (.+)', command)
    return sp.sympify(equation.group(1)) if equation else None

def extract_expression(command):
    # Extract expression for differentiation or integration
    expression = re.search(r'differentiate (.+)|integrate (.+)', command)
    return sp.sympify(expression.group(1) or expression.group(2)) if expression else None

def extract_trig_function(command):
    if "sin" in command:
        return "sin"
    elif "cos" in command:
        return "cos"
    elif "tan" in command:
        return "tan"
    return None

def extract_angle(command):
    angle = re.search(r'(\d+)', command)
    return float(angle.group(1)) if angle else None

def extract_matrix_a(command):
    # Example: extract matrix A from "matrix A is [[1, 2], [3, 4]]"
    matrix_a = re.search(r'matrix A is (\[\[.*?\]\])', command)
    return np.array(eval(matrix_a.group(1))) if matrix_a else None

def extract_matrix_b(command):
    # Example: extract matrix B from "matrix B is [[5, 6], [7, 8]]"
    matrix_b = re.search(r'matrix B is (\[\[.*?\]\])', command)
    return np.array(eval(matrix_b.group(1))) if matrix_b else None

def extract_matrix_operation(command):
    if "add" in command:
        return 'add'
    elif "subtract" in command:
        return 'subtract'
    elif "multiply" in command:
        return 'multiply'
    return None

def extract_complex_numbers(command):
    # Example: extract complex numbers from "complex 1+2j and 3+4j"
    numbers = re.findall(r'[-+]?\d*\.?\d*[-+]\d*\.?\d*j', command)
    return [n.strip() for n in numbers] if numbers else [None, None]

def extract_complex_operation(command):
    if "add" in command:
        return 'add'
    elif "subtract" in command:
        return 'subtract'
    elif "multiply" in command:
        return 'multiply'
    elif "divide" in command:
        return 'divide'
    return None

def extract_units(command):
    # Example: extract value and units from "convert 10 meters to feet"
    match = re.search(r'convert (\d+) (\w+) to (\w+)', command)
    if match:
        value = float(match.group(1))
        from_unit = match.group(2)
        to_unit = match.group(3)
        return value, from_unit, to_unit
    return None, None, None
