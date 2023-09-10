import tkinter as tk
from sympy import *
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

x = symbols('x')
transformations = (standard_transformations + (implicit_multiplication_application,) + (convert_xor,))

window = tk.Tk()
window.geometry("600x600")

# Funciones
def getEquation():
    eq = equation.get()
    eqParse = parse_expr(eq, transformations=transformations)
    initialValue = xi.get()
    if initialValue == "":
        initialValue = 0
    else:
        initialValue = float(initialValue)
    improvedNewtonRaphson(eqParse, initialValue)

def improvedNewtonRaphson(eq, xi):
    derivative = diff(eq, x)
    secondDerivative = diff(derivative, x)
    max_iterations = 100  # Número máximo de iteraciones
    tolerance = 1e-6     # Tolerancia de convergencia
    for i in range(max_iterations):
        xSolution = xi - ((eq.subs(x, xi) * derivative.subs(x, xi)) / (derivative.subs(x, xi)**2 - eq.subs(x, xi) * secondDerivative.subs(x, xi)))
        if xSolution == sympy.nan:
            print("El método no converge o produce un resultado no válido.")
            break
        xSolutionValue = xSolution.evalf()
        actualError = abs((xSolutionValue - xi) / xSolutionValue)
        if actualError < tolerance:
            break
        xi = xSolutionValue
    print("Resultado:", xSolutionValue)


# Ecuacion
equationLabel = tk.Label(text="Ingresa la ecuacion")
equationLabel.pack(pady=20)

equation = tk.Entry(width=50)
equation.pack()

initialLabel = tk.Label(text="Ingresa valor inicial")
initialLabel.pack()

xi = tk.Entry(width=50)
xi.pack()

btnIngresar = tk.Button(text="Calcular raices", width=20, command=getEquation)
btnIngresar.pack(padx=10, pady=10)

# Pack and loop
window.mainloop()
