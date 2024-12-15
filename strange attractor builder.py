import random
import math
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

# Number of strange attractors to find
n = 12
found = 0

# Function to generate a strange attractor
def generate_attractor():
    global x, y, xe, ye, a, d0, x_list, y_list, lyapunov, converging
    x = random.uniform(-0.5, 0.5)
    y = random.uniform(-0.5, 0.5)

    # Random alternative point nearby - perturb x, y by epsilon
    xe = x + random.uniform(-0.5, 0.5) / 1000
    ye = y + random.uniform(-0.5, 0.5) / 1000

    # Distance between two points
    dx = xe - x
    dy = ye - y
    d0 = math.sqrt(dx * dx + dy * dy)  # sqrt distance

    a = [random.uniform(-2, 2) for _ in range(12)]

    # Lists to store the path, which we graph
    x_list = [x]
    y_list = [y]

    # Initializing convergence boolean and Lyapunov exponent
    lyapunov = 0
    converging = False

# Initialize the first attractor
generate_attractor()

# Create the figure
fig, ax = plt.subplots()
plt.style.use('dark_background')
ax.axis('off')
scat = ax.scatter([], [], s=0.1, c='white', linewidth=0)

# Update function for animation
def update(frame):
    global x, y, xe, ye, x_list, y_list, lyapunov, converging, found

    if converging or found >= n:
        return scat,

    # Generate new points
    xnew = a[0] + a[1] * x + a[2] * x * x + a[3] * y + a[4] * y * y + a[5] * x * y
    ynew = a[6] + a[7] * x + a[8] * x * x + a[9] * y + a[10] * y * y + a[11] * x * y

    if abs(xnew) > 1e10 or abs(ynew) > 1e10:
        converging = True

    if abs(x - xnew) < 1e-10 and abs(y - ynew) < 1e-10:
        converging = True

    # Checking for chaotic behavior
    if not converging and len(x_list) > 1000:
        xenew = a[0] + a[1] * xe + a[2] * xe * xe + a[3] * ye + a[4] * ye * ye + a[5] * xe * ye
        yenew = a[6] + a[7] * xe + a[8] * xe * xe + a[9] * ye + a[10] * ye * ye + a[11] * xe * ye

        dx = xenew - xe
        dy = yenew - ye
        d = math.sqrt(dx * dx + dy * dy)

        lyapunov += math.log(abs(d / d0))

        # Rescale alternate point
        xe = xnew + d0 * dx / d
        ye = ynew + d0 * dy / d

    x = xnew
    y = ynew

    x_list.append(x)
    y_list.append(y)

    if not converging and lyapunov >= 100:
        found += 1
        print("We found a strange attractor with L = " + str(lyapunov))
        generate_attractor()

    # Update scatter plot
    scat.set_offsets(list(zip(x_list[-100:], y_list[-100:])))
    return scat,

# Create the animation
ani = FuncAnimation(fig, update, frames=10000, interval=1, blit=True)

# Display the animation
plt.show()
