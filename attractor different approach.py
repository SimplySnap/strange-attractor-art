import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import matplotlib.animation as animation

res = 1000
txtfile = []

def attractor_dynamics(t, z, a, b):
    x, y = z
    dxdt = np.sin(a * y) - np.cos(b * x)
    dydt = np.sin(b * x) - np.cos(a * y)
    return [dxdt, dydt]

print("Let's go :)")

fig, ax = plt.subplots()
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
line, = ax.plot([], [], lw=0.5)

trajectory = []

ani = None  # Global animation variable to prevent deletion

def init():
    line.set_data([], [])
    return line,

def update(frame):
    if frame < len(trajectory):
        x, y = trajectory[frame]
        line.set_data(x, y)
    return line,

def attractor(a, b):
    global trajectory, ani
    t_span = [0, 50]
    t_eval = np.linspace(*t_span, 5000)
    z0 = np.random.rand(2) * 5 - 2.5
    sol = solve_ivp(attractor_dynamics, t_span, z0, args=(a, b), t_eval=t_eval, dense_output=True)

    x, y = sol.y
    trajectory = [(x[:i], y[:i]) for i in range(1, len(x))]

    ani = animation.FuncAnimation(fig, update, frames=len(trajectory), init_func=init, blit=True, interval=1)
    plt.show()

    if len(x) == len(t_eval):
        print("^" * 10)
        txtfile.append(f"{a} {b}")

for a in np.linspace(-6, 6, 5):
    for b in np.linspace(-6, 6, 5):
        attractor(a, b)

with open("vals.txt", "w") as f:
    f.write("\n".join(txtfile))
