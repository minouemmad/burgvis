import numpy as np
import matplotlib.pyplot as plt

# Define initial condition u0(x)
def u0(x):
    return np.where((x >= 0) & (x <= 1), 1.0, 0.0)

# Domain settings
x_min, x_max = -1, 3
t_max = 2.0
nx = 400
nt = 200
x_vals = np.linspace(x_min, x_max, nx)
t_vals = np.linspace(0, t_max, nt)

# Compute characteristics
def compute_characteristics():
    x0 = np.linspace(x_min, x_max, 100)
    char_data = []
    for xi in x0:
        u_val = u0(xi)
        x_char = xi + u_val * t_vals
        char_data.append((xi, x_char, u_val))
    return char_data

# Plot characteristics
def plot_characteristics(char_data):
    plt.figure(figsize=(10, 6))
    for xi, x_char, u_val in char_data:
        plt.plot(x_char, t_vals, color='blue', alpha=0.4)
    plt.title('Characteristic Curves for Burgers Equation')
    plt.xlabel('x')
    plt.ylabel('t')
    plt.grid(True)
    plt.axhline(0, color='black')
    plt.axvline(0, color='black')
    plt.show()

# Estimate shock location (approximate)
def estimate_shock_location():
    # Shock forms where du0/dx < 0
    dx = x_vals[1] - x_vals[0]
    du_dx = np.gradient(u0(x_vals), dx)
    min_slope_index = np.argmin(du_dx)
    x_s = x_vals[min_slope_index]
    slope = du_dx[min_slope_index]
    t_shock = -1.0 / slope if slope < 0 else np.inf
    return x_s, t_shock

# Compute u(x, t) for a given time using characteristics
def compute_solution_at_t(t):
    u_sol = np.zeros_like(x_vals)
    for i, x in enumerate(x_vals):
        # Invert x = x0 + u0(x0) * t to find x0
        # Try all x0 and find the one that gives closest x
        x0_candidates = np.linspace(x_min, x_max, 500)
        distances = np.abs(x0_candidates + u0(x0_candidates) * t - x)
        x0 = x0_candidates[np.argmin(distances)]
        u_sol[i] = u0(x0)
    return u_sol

# Plot solution
def plot_solution(t):
    u_t = compute_solution_at_t(t)
    plt.figure(figsize=(8, 4))
    plt.plot(x_vals, u_t, label=f'u(x,{t:.2f})')
    plt.title(f'Solution at time t={t:.2f}')
    plt.xlabel('x')
    plt.ylabel('u')
    plt.grid(True)
    plt.legend()
    plt.show()

# Run everything
char_data = compute_characteristics()
plot_characteristics(char_data)

x_s, t_s = estimate_shock_location()
print(f"Estimated shock forms at x ≈ {x_s:.2f}, t ≈ {t_s:.2f}")

# Plot solution before and after shock
plot_solution(t=0.5)
plot_solution(t=1.0)
plot_solution(t=1.5)
