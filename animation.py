from matplotlib.collections import PathCollection
import matplotlib.pyplot as plt
from matplotlib import animation
from astros import Astro, AstroList
from random import randrange
from tqdm import tqdm

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
    colors = ["yellow", "gray", "orange", "blue", "lightgray", "red", "khaki", "burlywood", "paleturquoise", "cornflowerblue"]
    colors = colors + [((randrange(0, 256)/255, randrange(0, 256)/255, randrange(0, 256)/255),) for _ in range(len(lists[0].get_all_astros()) - len(colors))]

    def update(list_astros: AstroList) -> list[PathCollection]:
        """
        Updates the scatter plot for each frame of the animation
        Args:
            list_astros: AstroList object containing current positions
        Returns:
            scat: List of scatter plot objects for current frame
        """
        scat = []
        for (astro, color) in zip(list_astros.get_all_astros(), colors):
            scat.append(ax.scatter(*astro.pos_com.T, c=color, label=astro.name))
        return scat
    print("generating video")
    frames = []
    for l in tqdm(lists):
        frames.append(update(l))
    ax.legend(loc = (-0.35, 0.3), labels=[i.name for i in lists[0].get_all_astros()], )
    ax.set_aspect("equal", adjustable="datalim")
    ax.axis("off")
    ax.view_init(90, -90)
    ax.set_facecolor("black")
    print("loop ended")
    anim = animation.ArtistAnimation(fig, frames, 1000/60)
    print("saving...")
    anim.save(f'{filename}.gif')
