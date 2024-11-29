from matplotlib.collections import PathCollection
import matplotlib.pyplot as plt
from matplotlib import animation
from astros import Astro, AstroList

def create_animation(lists: list[AstroList], filename: str):
    """
    Creates an animated 3D visualization of astronomical objects and
    saves it to a file.
    Args:
        lists: List of AstroList objects containing position data
        filename: Name of the output file
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # ax.set_xlim(0, 30)
    # ax.set_ylim(0, 30)
    # ax.set_zlim(0, 30)
    ax.set_aspect("equal")

    def update(list_astros: AstroList) -> list[PathCollection]:
        """
        Updates the scatter plot for each frame of the animation
        Args:
            list_astros: AstroList object containing current positions
        Returns:
            scat: List of scatter plot objects for current frame
        """
        scat = []
        for astro in list_astros.get_all_astros():
            scat.append(ax.scatter(*astro.position.T))

        return scat

    frames = []
    for l in lists:
        frames.append(update(l))

    anim = animation.ArtistAnimation(fig, frames, 1000/60)

    anim.save(f'{filename}.gif', writer='pillow')
