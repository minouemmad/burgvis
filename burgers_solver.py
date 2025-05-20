import numpy as np

class BurgersSolver:
    def __init__(self, x_min=-1, x_max=3, t_max=2.0, nx=400, nt=200):
        self.x_min = x_min
        self.x_max = x_max
        self.t_max = t_max
        self.nx = nx
        self.nt = nt
        self.x_vals = np.linspace(x_min, x_max, nx)
        self.t_vals = np.linspace(0, t_max, nt)
        
    def set_initial_condition(self, u0_func):
        """Set the initial condition function u0(x)"""
        self.u0 = u0_func
        
    def compute_characteristics(self):
        """Compute characteristic curves"""
        x0 = np.linspace(self.x_min, self.x_max, 100)
        char_data = []
        for xi in x0:
            u_val = self.u0(xi)
            x_char = xi + u_val * self.t_vals
            char_data.append((xi, x_char, u_val))
        return char_data
    
    def estimate_shock_time(self):
        """Estimate when and where shock forms"""
        dx = self.x_vals[1] - self.x_vals[0]
        du_dx = np.gradient(self.u0(self.x_vals), dx)
        min_slope_index = np.argmin(du_dx)
        x_s = self.x_vals[min_slope_index]
        slope = du_dx[min_slope_index]
        t_shock = -1.0 / slope if slope < 0 else np.inf
        return x_s, t_shock
    
    def compute_solution_at_t(self, t):
        """Compute solution at specific time t"""
        u_sol = np.zeros_like(self.x_vals)
        for i, x in enumerate(self.x_vals):
            x0_candidates = np.linspace(self.x_min, self.x_max, 500)
            distances = np.abs(x0_candidates + self.u0(x0_candidates) * t - x)
            x0 = x0_candidates[np.argmin(distances)]
            u_sol[i] = self.u0(x0)
        return u_sol