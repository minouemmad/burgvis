import numpy as np
from burgers_solver import BurgersSolver
from burgers_plotter import BurgersPlotter
from burgers_gui import BurgersGUI
import tkinter as tk

def default_initial_condition(x):
    return np.where((x >= 0) & (x <= 1), 1.0, 0.0)

if __name__ == "__main__":
    # Initialize components
    solver = BurgersSolver()
    solver.set_initial_condition(default_initial_condition)
    plotter = BurgersPlotter()
    
    # Create and run GUI
    root = tk.Tk()
    app = BurgersGUI(root, solver, plotter)
    root.mainloop()