import math

from matplotlib import animation
from scipy import constants
import numpy as np
import matplotlib.pyplot as plt
from time import time

class ThreeBodyProblem:

    def __init__(self, planets_polar_coordinates, planets_velocities_polar_coordinates, masses):
        self.u = [0 for i in range(12)]
        self.planets_polar_coordinates = planets_polar_coordinates
        self.planets_velocities_polar_coordinates = planets_velocities_polar_coordinates
        self.masses = masses
        self.reset_state_to_initial_conditions()



    def printit(self):
        for i in range(12):
            print(self.u[i])

    def derivative(self):
        du = [0 for i in range(12)]

        for i_body in range(3):
            body_start = i_body * 4
            du[body_start + 0] = self.u[body_start + 0 + 2]
            du[body_start + 1] = self.u[body_start + 0 + 3]
            du[body_start + 2] = self.acceleration(i_body, 0)
            du[body_start + 3] = self.acceleration(i_body, 1)

        return du

    def calculate_center_of_mass(self):
        center_of_mass = [0, 0]
        sum_of_masses = 0

        for i_body in range(3):
            body_start = i_body * 4
            center_of_mass[0] += self.masses[i_body] * self.u[body_start + 0]
            center_of_mass[1] += self.masses[i_body] * self.u[body_start + 1]
            sum_of_masses += self.masses[i_body]

        center_of_mass[0] /= sum_of_masses/4
        center_of_mass[1] /= sum_of_masses/4

        return center_of_mass


    def calculate_center_of_mass_velocity(self):
        center_of_mass_velocity = [0, 0]
        sum_of_masses = 0

        for i_body in range(3):
            body_start = i_body * 4
            center_of_mass_velocity[0] += self.masses[i_body] * self.u[body_start + 2]
            center_of_mass_velocity[1] += self.masses[i_body] * self.u[body_start + 3]
            sum_of_masses += self.masses[i_body]

        center_of_mass_velocity[0] /= sum_of_masses
        center_of_mass_velocity[1] /= sum_of_masses

        return center_of_mass_velocity

    def reset_state_to_initial_conditions(self):
        for i_body in range(3):
            body_start = i_body * 4

            position = self.planets_polar_coordinates[i_body]
            self.u[body_start + 0] = position[0] * np.cos(position[1]) # x
            self.u[body_start + 1] = position[0] * np.sin(position[1]) # y

            velocity = self.planets_velocities_polar_coordinates[i_body]
            self.u[body_start + 2] = velocity[0] * np.cos(velocity[1]) # x
            self.u[body_start + 3] = velocity[0] * np.sin(velocity[1]) # y

        center_of_mass_velocity = self.calculate_center_of_mass_velocity()
        center_of_mass = self.calculate_center_of_mass()

        for i_body in range(3):
            body_start = i_body * 4
            self.u[body_start + 0] -= center_of_mass[0]
            self.u[body_start + 1] -= center_of_mass[1]
            self.u[body_start + 2] -= center_of_mass_velocity[0]
            self.u[body_start + 3] -= center_of_mass_velocity[1]


    def acceleration(self, i_from_body, coordinate):
        result = 0
        i_from_body_start = i_from_body * 4

        for i_to_body in range(3):
            if i_to_body == i_from_body:
                continue

            i_to_body_start = i_to_body * 4

            distance_x = self.u[i_to_body_start + 0] - self.u[i_from_body_start + 0]
            distance_y = self.u[i_to_body_start + 1] - self.u[i_from_body_start + 1]
            distance = math.sqrt(math.pow(distance_x, 2) + math.pow(distance_y, 2))

            result += 1 * self.masses[i_to_body] * (self.u[i_to_body + coordinate] - self.u[i_from_body_start + coordinate]) / math.pow(distance, 3)

        return result

    def update_position(self, timestamp):
        self.runge_kutta_calculation(timestamp)

    def runge_kutta_calculation(self, h):

        a = [h/2, h/2, h, 0]
        b = [h/6, h/3, h/3, h/6]
        dimension = len(self.u)
        u0 = [self.u[i] for i in range(dimension)]
        ut = [0 for i in range(dimension)]


        for j in range(4):
            du = self.derivative()

            for d in range(dimension):
                self.u[d] = u0[d] + a[j] * du[d]
                ut[d] = ut[d] + b[j] * du[d]

        for d in range(dimension):
            self.u[d] = u0[d] + ut[d]


    def plot_it(self):
        plt.scatter([self.u[i * 4] for i in range(3)], [self.u[i * 4 + 1] for i in range(3)])
        plt.xlim(-3, 3)
        plt.ylim(-3, 3)
        plt.show()

    def animate(self, i):
        timestamp = 3.9335 / 60 / 250
        for i in range(250):
            self.update_position(timestamp)

        thisx = [self.u[0], self.u[4], self.u[8]]
        thisy = [self.u[1], self.u[5], self.u[9]]
        print(thisx, thisy)

        line.set_data(thisx, thisy)
        time_text.set_text(time_template % (i * 0.05))
        return line, time_text




planets_polar_coordinates               = [#[[0,0], [1.496 * math.pow(10, 11), 0], [7.78 * math.pow(10, 11), 0]]
    [1, 0],
                                           [1, 2 * np.pi / 3],
                                           [1, 4 * np.pi / 3]]

planets_velocities_polar_coordinates    = [#[[0, math.pi/2], [30*math.pow(10,3), math.pi/2], [13.1*math.pow(10,3), math.pi/2]]
    [0.55, np.pi / 2],
                                           [0.55, 2 * np.pi / 3 + np.pi / 2],
                                           [0.55, 4 * np.pi / 3 + np.pi / 2]]

masses                                  =[ #[1.98855 * math.pow(10, 30), 5.972 * math.pow(10, 24), 1.898 * math.pow(10, 27)]
    1,
                                           1,
                                           1]

tbp = ThreeBodyProblem(planets_polar_coordinates, planets_velocities_polar_coordinates, masses)
# timestamp = 3.9335/60/250
#
# for i in range(300):
#     for j in range(250*10):
#         tbp.update_position(3.9335)
#     tbp.plot_it()

fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-20, 20), ylim=(-20, 20))
ax.set_aspect('equal')
ax.grid()

line, = ax.plot([], [], 'o', lw=1)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)


def init():
    line.set_data([], [])
    time_text.set_text('')
    return line, time_text


ani = animation.FuncAnimation(fig, tbp.animate, np.arange(1, 10000), interval=25, blit=True, init_func=init)

plt.show()