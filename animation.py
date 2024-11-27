import matplotlib.pyplot as plt
from matplotlib import animation
from astros import Astro, AstroList

def create_animation(lista: list[AstroList]):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # ax.set_xlim(0, 30)
    # ax.set_ylim(0, 30)
    # ax.set_zlim(0, 30)

    def update(list_astros: AstroList):
        scat = []
        for astro in list_astros.get_all_astros():
            scat.append(ax.scatter(*astro.position.T))

        return scat
        
    frames = []
    for l in lista:
        frames.append(update(l))

    anim = animation.ArtistAnimation(fig, frames, 1000/60)

    anim.save('coordinate_animation.gif', writer='pillow')
