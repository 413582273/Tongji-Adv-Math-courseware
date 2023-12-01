import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np
from scipy.optimize import fsolve


# Define the function and its derivative
def f(x):
    return np.sin(x) + 0.5 * x - 1


def df(x):
    return np.cos(x) + 0.5


# Define the Newton's method step
def newton_step(x, f, df):
    return x - f(x) / df(x)


# Define the Bisection method step
def bisection_step(a, b, f):
    mid = (a + b) / 2
    if f(a) * f(mid) < 0:
        return a, mid
    else:
        return mid, b


# Define the Secant method step
def secant_step(x0, x1, f):
    return x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))


# Initialization
x0 = 1.5
a, b = 0.7, 1.5  # Initial interval for bisection
x1 = 1.4  # Second initial point for secant
current_step = 0

# Prepare steps for each method
steps_newton = [x0]
steps_bisection = [(a, b)]
steps_secant = [(x0, x1)]

# Create a figure and axes
fig, axs = plt.subplots(3, 1, figsize=(8, 12))
plt.subplots_adjust(bottom=0.25)

# Prepare x values for plotting
x = np.linspace(0, 3, 2000)

# Plot the function on all subplots
for ax in axs:
    ax.plot(x, f(x), label='sin(x)+0.5*x-1')
    ax.axhline(0, color='black', linewidth=0.8)
    ax.axvline(0, color='black', linewidth=0.8)
    ax.set_ylim(min(f(x)), max(f(x)))
    ax.legend()

# Add titles
axs[0].set_title("Newton's Method")
axs[1].set_title("Bisection Method")
axs[2].set_title("Secant Method")

# Initialize points, lines, and vertical lines
point_newton, = axs[0].plot([], [], 'go')
tangent_newton, = axs[0].plot([], [], color='orange')
vertical_line_newton = None

points_bisection, = axs[1].plot([], [], 'ro')
interval_bisection, = axs[1].plot([], [], color='blue')
vertical_line_bisection = None

points_secant, = axs[2].plot([], [], 'mo')
line_secant, = axs[2].plot([], [], color='purple')
vertical_line_secant = None

# Find the true root for comparison
true_root = fsolve(f, x0)[0]


# Update the plot
def update_plot():
    global current_step, vertical_line_newton, vertical_line_bisection, vertical_line_secant

    # Newton's Method update
    x_current_newton = steps_newton[current_step]
    y_tangent = df(x_current_newton) * (x - x_current_newton) + f(x_current_newton)
    tangent_newton.set_data(x, y_tangent)
    point_newton.set_data(x_current_newton, f(x_current_newton))

    # Update vertical line for Newton's method
    if vertical_line_newton is not None:
        vertical_line_newton.remove()
    vertical_line_newton = axs[0].axvline(x_current_newton, color='red', linestyle='--')

    axs[0].set_title(f"Newton's Method - Step {current_step + 1}, Error: {abs(x_current_newton - true_root):.4f}")

    # Bisection Method update
    a, b = steps_bisection[current_step]
    x_current_bisection = (a + b) / 2
    interval_bisection.set_data([a, b], [0, 0])
    points_bisection.set_data([a, b], [f(a), f(b)])

    # Update vertical line for Bisection method
    if vertical_line_bisection is not None:
        vertical_line_bisection.remove()
    vertical_line_bisection = axs[1].axvline(x_current_bisection, color='red', linestyle='--')

    axs[1].set_title(f"Bisection Method - Step {current_step + 1}, Error: {abs(x_current_bisection - true_root):.4f}")

    # Secant Method update
    x0, x1 = steps_secant[current_step]
    slope_secant = (f(x1) - f(x0)) / (x1 - x0)
    y_secant = slope_secant * (x - x0) + f(x0)
    line_secant.set_data(x, y_secant)
    points_secant.set_data([x0, x1], [f(x0), f(x1)])

    # Update vertical line for Secant method
    if vertical_line_secant is not None:
        vertical_line_secant.remove()
    vertical_line_secant = axs[2].axvline(x1, color='red', linestyle='--')

    axs[2].set_title(f"Secant Method - Step {current_step + 1}, Error: {abs(x1 - true_root):.4f}")

    fig.canvas.draw_idle()


# Define button actions
def next_step(event):
    global current_step
    if current_step < min(len(steps_newton), len(steps_bisection), len(steps_secant)) - 1:
        current_step += 1
        update_plot()
    else:
        # Add new steps if needed
        if current_step == len(steps_newton) - 1:
            steps_newton.append(newton_step(steps_newton[-1], f, df))
        if current_step == len(steps_bisection) - 1:
            steps_bisection.append(bisection_step(*steps_bisection[-1], f))
        if current_step == len(steps_secant) - 1:
            new_x = secant_step(*steps_secant[-1], f)
            steps_secant.append((steps_secant[-1][1], new_x))

        current_step += 1
        update_plot()


def previous_step(event):
    global current_step
    if current_step > 0:
        current_step -= 1
        update_plot()


# Add buttons for control
axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'Next')
bprev = Button(axprev, 'Previous')
bnext.on_clicked(next_step)
bprev.on_clicked(previous_step)

# Initial plot update
update_plot()

plt.show()
