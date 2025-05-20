import matplotlib.pyplot as plt

class BurgersPlotter:
    @staticmethod
    def plot_characteristics(char_data, x_min, x_max, t_max):
        """Plot characteristic curves"""
        plt.figure(figsize=(10, 6))
        for xi, x_char, u_val in char_data:
            plt.plot(x_char, t_vals, color='blue', alpha=0.4)
        plt.title('Characteristic Curves for Burgers Equation')
        plt.xlabel('x')
        plt.ylabel('t')
        plt.xlim(x_min, x_max)
        plt.ylim(0, t_max)
        plt.grid(True)
        plt.axhline(0, color='black')
        plt.axvline(0, color='black')
        return plt
    
    @staticmethod
    def plot_solution(x_vals, u_t, t):
        """Plot solution at specific time"""
        plt.figure(figsize=(8, 4))
        plt.plot(x_vals, u_t, label=f'u(x,{t:.2f})')
        plt.title(f'Solution at time t={t:.2f}')
        plt.xlabel('x')
        plt.ylabel('u')
        plt.grid(True)
        plt.legend()
        return plt