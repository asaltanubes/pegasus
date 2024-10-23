from astros import *
from verlet import *
import matplotlib.pyplot as plt

sun = Astro([0, 0, 0], [0, 0, 0], 1.98847e30, "sun")
earth = Astro((1.496e11,0,0), (0,29806,0), 5.97e24, "earth")

mercury = Astro((5.791e10,0,0), (0,47872.5,0), 3.302e23)
venus = Astro((1.08e11,0,0), (0,35000,0), 4.87e24)
moon = Astro((1.4998e11,0,0), (0,30806,0), 7.343e22)
mars = Astro((2.228e11,0,0), (0,24077,0), 6.4185e23)
jupiter = Astro((7.778e11,0,0), (0,13069.7,0), 1.899e27)
saturn = Astro((1.427e12,0,0), (0,9620.24,0), 5.688e26)
uranus = Astro((2.871e12,0,0), (0,6810,0), 8.686e25)
neptune = Astro((4.498e12,0,0), (0,5477.8,0), 1.024e26)

solar_system = AstroList([earth, sun, mercury, venus, moon, mars, jupiter, saturn, uranus, neptune])

# print(solar_system.second_order_func(None, np.array([[0, 1.496e11, 0], [0, 0, 0]]), None))

verlet = Verlet(200)

final_time = 365*24*3600

dot_interval = 24*3600 

positions = []

while solar_system.time < final_time:
    v, r, t = verlet.advance_time(solar_system, dot_interval+solar_system.time)
    solar_system.update_state(v, r, t)
    positions.append(r)


plt.plot([i[0][0] for i in positions], [i[0][1] for i in positions])
plt.plot([i[1][0] for i in positions], [i[1][1] for i in positions])
plt.plot([i[2][0] for i in positions], [i[2][1] for i in positions])
plt.plot([i[3][0] for i in positions], [i[3][1] for i in positions])
plt.plot([i[4][0] for i in positions], [i[4][1] for i in positions])
plt.plot([i[5][0] for i in positions], [i[5][1] for i in positions])
plt.plot([i[6][0] for i in positions], [i[6][1] for i in positions])
plt.plot([i[7][0] for i in positions], [i[7][1] for i in positions])
plt.show()
