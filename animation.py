import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

def read_coordinates(filename):
    """
    Read coordinates from file. Assuming the file has format:
    x1 y1 z1
    x2 y2 z2
    ...
    """
    x, y, z = [], [], []
    with open(filename, 'r') as file:
        for line in file:
            coords = line.strip().split()
            x.append(float(coords[0]))
            y.append(float(coords[1]))
            z.append(float(coords[2]))
    return np.array(x), np.array(y), np.array(z)

def update(frame, scatter, x, y, z):
    """Update function for animation"""
    scatter._offsets3d = (x[:frame], y[:frame], z[:frame])
    return scatter,

def create_animation(filename):
    # Read coordinates
    x, y, z = read_coordinates(filename)

    # Create figure and 3D axes
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Set labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Coordinate Animation')

    # Set axis limits
    ax.set_xlim(min(x), max(x))
    ax.set_ylim(min(y), max(y))
    ax.set_zlim(min(z), max(z))

    # Initial scatter plot
    scatter = ax.scatter([], [], [], c='b', marker='o')

    # Create animation
    anim = animation.FuncAnimation(fig, update, frames=len(x),
                                 fargs=(scatter, x, y, z),
                                 interval=50, blit=True)

    return plt, anim

# Example usage
if __name__ == "__main__":
    # Example of how your data file might look:
    # Let's create a sample data file
    with open('coordinates.txt', 'w') as f:
        for t in range(100):
            # Creating some sample coordinates (e.g., a spiral)
            x = t * np.cos(t/10)
            y = t * np.sin(t/10)
            z = t
            f.write(f"{x} {y} {z}\n")

    # Create and show animation
    plt, anim = create_animation('coordinates.txt')

    # To save the animation (optional)
    anim.save('coordinate_animation.gif', writer='pillow')
