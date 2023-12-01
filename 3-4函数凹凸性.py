import tkinter as tk
from numpy import linspace, sin, pi
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Circle
import matplotlib.gridspec as gridspec

# Function definition
def f(x):
    return 0.02 * (x- 1) ** 3 + 0.02 * x ** 2 - x + sin(1.4 * x) + (x ** 2) ** (1/3)

# Numerical derivatives
def numerical_df(x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2 * h)

def numerical_ddf(x, h=1e-5):
    return (f(x + h) - 2 * f(x) + f(x - h)) / (h ** 2)

# Function to calculate curvature circle's center and radius
def curvature_circle(x0):
    f_prime = numerical_df(x0)
    f_double_prime = numerical_ddf(x0)
    radius = (1 + f_prime**2)**1.5 / abs(f_double_prime)
    center_x = x0 - (1 + f_prime**2) / f_double_prime
    center_y = f(x0) + f_prime * (1 + f_prime**2) / f_double_prime
    return center_x, center_y, radius

# Function to update the graphs
def update_graphs(event):
    x0 = slider.get()
    x = linspace(-9, 9, 40000)
    tangent_line = numerical_df(x0) * (x - x0) + f(x0)

    # Clear previous plots
    ax1.clear()
    ax2.clear()
    ax3.clear()

    # Plotting the main function, tangent line, and vertical line
    ax1.scatter(x, f(x), s=0.01, marker='o', label=f"Function at x = {x0:.2f}")
    ax1.plot(x, tangent_line, color='orange', label="Tangent", linestyle='--')
    ax1.axvline(x=x0, color='red', linestyle='-.')
    ax1.set_ylim([-5, 10])
    ax1.legend()
    ax1.grid(True)

    # Plotting the first derivative, vertical line, and y=0 line
    dy = numerical_df(x)
    ax2.scatter(x, dy, s=0.01, marker='o', label="First Derivative", color='orange')
    ax2.axvline(x=x0, color='red', linestyle='-.')
    ax2.axhline(y=0, color='black', linewidth=2)
    ax2.set_ylim([-5, 5])
    ax2.legend()
    ax2.grid(True)

    # Plotting the second derivative, vertical line, and y=0 line
    ddy = numerical_ddf(x)
    ax3.scatter(x, ddy, s=0.01, marker='o', label="Second Derivative", color='green')
    ax3.axvline(x=x0, color='red', linestyle='-.')
    ax3.axhline(y=0, color='black', linewidth=2)
    ax3.set_ylim([-15, 5])
    ax3.legend()
    ax3.grid(True)

    # If show curvature circle option is selected, draw the circle
    if show_curvature_var.get():
        center_x, center_y, radius = curvature_circle(x0)
        circle = Circle((center_x, center_y), radius, color='blue', fill=False)
        ax1.add_patch(circle)

    # Draw the updated plots
    canvas.draw()

# Creating the main window
root = tk.Tk()
root.title("Function and Numerical Derivatives Plot with Vertical Line")
# Create a variable and checkbutton for curvature circle display option
show_curvature_var = tk.IntVar()
show_curvature_check = tk.Checkbutton(root, text="显示曲率圆", variable=show_curvature_var)
show_curvature_check.pack(side=tk.TOP)
# Displaying the function formula at the top
formula_label = tk.Label(root, text="f(x) = 0.02x³ + 0.02x² - x + sin(1.4x) + (x²)^(1/3)", font=("Arial", 15))
formula_label.pack(side=tk.TOP)

# Displaying the author information
author_label = tk.Label(root, text="汪引 - 山东财经大学 - wangyin@sdufe.edu.cn", font=("Arial", 10))
author_label.pack(side=tk.BOTTOM)

# Create a vertical slider and place it on the left side of the window
slider = tk.Scale(root, from_=-9, to=9, resolution=0.001, orient=tk.HORIZONTAL, command=update_graphs)
slider.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 10))  # Adjust padding as needed

# Create the Matplotlib figure and axes using GridSpec for layout
fig = Figure(figsize=(6, 8))  # Adjust the overall size of the figure
gs = gridspec.GridSpec(3, 1, height_ratios=[1, 1, 1])  # Adjust the height ratios

ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])
ax3 = fig.add_subplot(gs[2])

# Adjust the spacing of the subplots to accommodate the square plot
fig.subplots_adjust(hspace=0.4)  # Adjust hspace as needed

# Create the canvas and add it to the Tkinter window, below the slider
canvas = FigureCanvasTkAgg(fig, master=root)
widget = canvas.get_tk_widget()
widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


""" Initialization """
x = linspace(-9, 9, 40000)
# Clear previous plots
ax1.clear()
ax2.clear()
ax3.clear()
# Plotting the main function, tangent line, and vertical line
ax1.scatter(x, f(x), s=0.01, marker='o')
ax1.set_ylim([-5, 10])
ax1.grid(True)
# Plotting the first derivative, vertical line, and y=0 line
dy = numerical_df(x)
ax2.scatter(x, dy, s=0.01, marker='o', label="First Derivative", color='orange')
ax2.axhline(y=0, color='black', linewidth=2)
ax2.set_ylim([-5, 5])
ax2.legend()
ax2.grid(True)
# Plotting the second derivative, vertical line, and y=0 line
ddy = numerical_ddf(x)
ax3.scatter(x, ddy, s=0.01, marker='o', label="Second Derivative", color='green')
ax3.axhline(y=0, color='black', linewidth=2)
ax3.set_ylim([-15, 5])
ax3.legend()
ax3.grid(True)
canvas.draw()


# Run the Tkinter event loop
root.mainloop()
