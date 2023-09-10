import tkinter as tk
from tkinter import messagebox
import sympy
from sympy import *
from sympy.parsing.sympy_parser import  parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import numpy as np  

x = sympy.symbols('x')
transformations = (standard_transformations + (implicit_multiplication_application,) + (convert_xor,))


canvas=None

window = tk.Tk()
window.title="Metodo Newton-Raphson Mejorado"
wSize=800
hSize=600
ws=window.winfo_screenwidth()
hs=window.winfo_screenheight()
xSize=(ws/2)-(wSize/2)
ySize=(hs/2)-(hSize/2)
window.geometry('%dx%d+%d+%d'%(wSize,hSize,xSize,ySize))  


# Funciones
def getEquation():
    eq = equation.get()
    eqParse = parse_expr(eq,transformations=transformations)
    initialValue = xi.get()
    if initialValue == "":
        initialValue = 0
    else:
        initialValue = float(initialValue)
    improvedNewtonRaphson(eqParse, initialValue)

def improvedNewtonRaphson(eq, xi):
    max_iterations=100
    iterations=0
    derivative = diff(eq, x)
    print(derivative)
    secondDerivative = diff(derivative, x)
    print(secondDerivative)
    actualError=100
    lastSolution=xi
    while(actualError>0 and iterations < max_iterations):
        xSolution=lastSolution-((eq.subs(x,lastSolution).evalf()*derivative.subs(x,lastSolution).evalf())/(pow(derivative.subs(x,lastSolution).evalf(),2)-eq.subs(x,lastSolution).evalf()*secondDerivative.subs(x,lastSolution).evalf()))
        xSolutionValue=xSolution.evalf()
        print(xSolutionValue)
        print(lastSolution)
        actualError=float(abs((xSolutionValue-lastSolution)/xSolutionValue)*100)
        lastSolution=xSolutionValue
        print(actualError)
        iterations+=1
    if(lastSolution==nan):
        result_label.config(text=f"Raíz no encontrada")
    else:
        result_label.config(text=f"Raíz encontrada: {lastSolution}")
    plotGraph()
    

def plotGraph():
    global canvas

    # Si ya existe una gráfica anterior, destrúyela para limpiarla
    if (canvas != None):
        canvas.get_tk_widget().destroy()
    plt.clf()

    eq = equation.get()
    eqParse = parse_expr(eq, transformations=transformations)
    x_values = np.linspace(-25, 25, 400)
    y_values = [eqParse.subs(x, val).evalf() for val in x_values]
    
    plt.figure(figsize=(8, 6))
    plt.plot(x_values, y_values, label="Ecuación")
    plt.axhline(0, color='red', linestyle='--', label="Y=0")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.title("Gráfica de la Ecuación")
    plt.grid(True)
    #plt.show()

    canvas = FigureCanvasTkAgg(plt.gcf(), master=window)
    
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(padx=20,pady=10)
    isActive=1

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

btnGraficar = tk.Button(text="Mostrar Gráfica", width=20, command=plotGraph)
btnGraficar.pack(padx=10, pady=10)

result_label = tk.Label(text="Resultado: ")
result_label.pack(pady=10)


# Pack and loop
window.mainloop()
