import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re

class BurgersGUI:
    def __init__(self, master, solver, plotter):
        self.master = master
        self.solver = solver
        self.plotter = plotter
        
        master.title("Burgers' Equation Characteristic Plotter")
        master.geometry("1100x900")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Frame for controls
        control_frame = ttk.LabelFrame(self.master, text="Controls", padding=10)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # Initial condition selection
        ttk.Label(control_frame, text="Initial Condition:").grid(row=0, column=0, sticky=tk.W)
        self.ic_var = tk.StringVar(value="Step Function")
        ic_options = ["Step Function", "Sinusoidal", "Gaussian", "Piecewise Linear", "Custom Equation"]
        self.ic_menu = ttk.Combobox(control_frame, textvariable=self.ic_var, values=ic_options, state="readonly")
        self.ic_menu.grid(row=0, column=1, sticky=tk.W)
        self.ic_menu.bind("<<ComboboxSelected>>", self.update_ic_options)
        
        # Custom equation frame (initially hidden)
        self.custom_eq_frame = ttk.Frame(control_frame)
        self.custom_eq_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        ttk.Label(self.custom_eq_frame, text="Custom u0(x) = ").pack(side=tk.LEFT)
        self.custom_eq_entry = ttk.Entry(self.custom_eq_frame, width=30)
        self.custom_eq_entry.pack(side=tk.LEFT)
        self.custom_eq_entry.insert(0, "np.sin(x)*np.exp(-x**2)")
        
        # Piecewise linear frame (initially hidden)
        self.piecewise_frame = ttk.Frame(control_frame)
        self.piecewise_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        ttk.Label(self.piecewise_frame, text="Piecewise definition (x1,u1;x2,u2;...):").pack(side=tk.LEFT)
        self.piecewise_entry = ttk.Entry(self.piecewise_frame, width=30)
        self.piecewise_entry.pack(side=tk.LEFT)
        self.piecewise_entry.insert(0, "0,0;1,1;2,0")
        
        # Domain parameters
        ttk.Label(control_frame, text="x_min:").grid(row=3, column=0, sticky=tk.W)
        self.x_min_slider = tk.Scale(control_frame, from_=-5, to=0, resolution=0.1, orient=tk.HORIZONTAL, length=200)
        self.x_min_slider.set(-1)
        self.x_min_slider.grid(row=3, column=1, sticky=tk.W)
        
        ttk.Label(control_frame, text="x_max:").grid(row=4, column=0, sticky=tk.W)
        self.x_max_slider = tk.Scale(control_frame, from_=1, to=5, resolution=0.1, orient=tk.HORIZONTAL, length=200)
        self.x_max_slider.set(3)
        self.x_max_slider.grid(row=4, column=1, sticky=tk.W)
        
        ttk.Label(control_frame, text="t_max:").grid(row=5, column=0, sticky=tk.W)
        self.t_max_slider = tk.Scale(control_frame, from_=0.1, to=5, resolution=0.1, orient=tk.HORIZONTAL, length=200)
        self.t_max_slider.set(2)
        self.t_max_slider.grid(row=5, column=1, sticky=tk.W)
        
        # Time selection for solution plot
        ttk.Label(control_frame, text="Solution Time:").grid(row=6, column=0, sticky=tk.W)
        self.time_slider = tk.Scale(control_frame, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL, length=200)
        self.time_slider.set(0.5)
        self.time_slider.grid(row=6, column=1, sticky=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=10)
        
        self.char_button = ttk.Button(button_frame, text="Plot Characteristics", command=self.plot_characteristics)
        self.char_button.pack(side=tk.LEFT, padx=5)
        
        self.sol_button = ttk.Button(button_frame, text="Plot Solution", command=self.plot_solution)
        self.sol_button.pack(side=tk.LEFT, padx=5)
        
        self.ic_plot_button = ttk.Button(button_frame, text="Plot Initial Condition", command=self.plot_initial_condition)
        self.ic_plot_button.pack(side=tk.LEFT, padx=5)
        
        # Frame for plots
        plot_frame = ttk.Frame(self.master)
        plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create matplotlib figure and canvas
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Shock info label
        self.shock_label = ttk.Label(control_frame, text="Shock info will appear here")
        self.shock_label.grid(row=8, column=0, columnspan=2, pady=5)
        
        # Hide optional frames initially
        self.custom_eq_frame.grid_remove()
        self.piecewise_frame.grid_remove()
        
    def update_ic_options(self, event=None):
        """Show/hide appropriate frames based on IC selection"""
        ic_type = self.ic_var.get()
        
        self.custom_eq_frame.grid_remove()
        self.piecewise_frame.grid_remove()
        
        if ic_type == "Custom Equation":
            self.custom_eq_frame.grid()
        elif ic_type == "Piecewise Linear":
            self.piecewise_frame.grid()
    
    def set_initial_condition(self):
        ic_type = self.ic_var.get()
        
        if ic_type == "Step Function":
            self.solver.set_initial_condition(lambda x: np.where((x >= 0) & (x <= 1), 1.0, 0.0))
        elif ic_type == "Sinusoidal":
            self.solver.set_initial_condition(lambda x: np.sin(np.pi * x) * (x >= 0) * (x <= 1))
        elif ic_type == "Gaussian":
            self.solver.set_initial_condition(lambda x: np.exp(-(x-0.5)**2 / 0.1) * (x >= 0) * (x <= 1))
        elif ic_type == "Piecewise Linear":
            try:
                points = self.piecewise_entry.get().split(';')
                x_points = []
                u_points = []
                for point in points:
                    x, u = map(float, point.split(','))
                    x_points.append(x)
                    u_points.append(u)
                
                def piecewise_func(x):
                    return np.interp(x, x_points, u_points)
                
                self.solver.set_initial_condition(piecewise_func)
            except Exception as e:
                messagebox.showerror("Error", f"Invalid piecewise definition: {e}")
                return False
        elif ic_type == "Custom Equation":
            try:
                expr = self.custom_eq_entry.get()
                # Validate the expression
                test_x = 0.5
                test_result = eval(expr, {'np': np, 'x': test_x})
                
                def custom_func(x):
                    return eval(expr, {'np': np, 'x': x})
                
                self.solver.set_initial_condition(custom_func)
            except Exception as e:
                messagebox.showerror("Error", f"Invalid equation: {e}")
                return False
        
        return True
    
    def plot_initial_condition(self):
        if not self.set_initial_condition():
            return
            
        x = np.linspace(self.x_min_slider.get(), self.x_max_slider.get(), 500)
        u0 = self.solver.u0(x)
        
        self.ax.clear()
        self.ax.plot(x, u0, label='Initial condition u0(x)')
        self.ax.set_title('Initial Condition')
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('u0(x)')
        self.ax.grid(True)
        self.ax.legend()
        
        self.canvas.draw()
    
    def plot_characteristics(self):
        if not self.set_initial_condition():
            return
            
        # Update solver parameters
        self.solver.x_min = self.x_min_slider.get()
        self.solver.x_max = self.x_max_slider.get()
        self.solver.t_max = self.t_max_slider.get()
        
        # Compute and plot
        char_data = self.solver.compute_characteristics()
        self.ax.clear()
        
        for xi, x_char, u_val in char_data:
            self.ax.plot(x_char, self.solver.t_vals, color='blue', alpha=0.4)
        
        self.ax.set_title('Characteristic Curves for Burgers Equation')
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('t')
        self.ax.set_xlim(self.solver.x_min, self.solver.x_max)
        self.ax.set_ylim(0, self.solver.t_max)
        self.ax.grid(True)
        self.ax.axhline(0, color='black')
        self.ax.axvline(0, color='black')
        
        self.canvas.draw()
        
        # Calculate and display shock info
        x_s, t_s = self.solver.estimate_shock_time()
        self.shock_label.config(text=f"Estimated shock forms at x ≈ {x_s:.2f}, t ≈ {t_s:.2f}")
    
    def plot_solution(self):
        if not self.set_initial_condition():
            return
            
        t = self.time_slider.get()
        u_t = self.solver.compute_solution_at_t(t)
        
        self.ax.clear()
        self.ax.plot(self.solver.x_vals, u_t, label=f'u(x,{t:.2f})')
        self.ax.set_title(f'Solution at time t={t:.2f}')
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('u')
        self.ax.grid(True)
        self.ax.legend()
        
        self.canvas.draw()