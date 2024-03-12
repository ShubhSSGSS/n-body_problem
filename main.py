#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from tkinter.filedialog import askopenfilename
from numba import njit, prange  # Import Numba

@njit(parallel=True)  # Use Numba JIT compilation with parallelization
def acc_calc(mass_arr, pos_arr):
    n = mass_arr.shape[0]
    acc_arr = np.zeros_like(pos_arr, dtype=np.float32)  # Use lower precision data type

    for i in prange(n):  # Parallelize the outer loop
        for j in range(n):
            if i != j:
                r = pos_arr[:, j] - pos_arr[:, i]
                e = 20  # softening parameter
                distance = (np.linalg.norm(r) ** 2 + e ** 2) ** 0.5
                unit_vec = r / distance
                G = 10  # Universal gravitational constant
                force_magnitude = (G * mass_arr[i] * mass_arr[j]) / (distance ** 2)
                acceleration = force_magnitude * unit_vec / mass_arr[i]
                acc_arr[:, i] += acceleration

    return acc_arr

@njit  # Use Numba JIT compilation
def update_position_velocity(pos_arr, vel_arr, acc_arr, dt):
    vel_arr += acc_arr * dt
    pos_arr += vel_arr * dt
    return pos_arr, vel_arr

@njit(parallel=True)
def Energy_calc(mass_arr, pos_arr, vel_arr):
    n = mass_arr.shape[0]
    e = 20  # softening parameter
    G = 10  # Universal Gravitational constant

    KE = 0.0
    for j in range(n):
        vx, vy, vz = vel_arr[j]  # Unpack the velocity components for each particle
        KE += 0.5 * mass_arr[j] * (vx**2 + vy**2 + vz**2)

    PE = 0.0
    distances = np.zeros((n, n), dtype=np.float32)  # Store computed distances

    for i in prange(n):  # Parallelize the outer loop
        for j in range(i + 1, n):
            r = pos_arr[j] - pos_arr[i]
            distance_sq = np.sum(r**2) + e**2
            distance = np.sqrt(distance_sq)
            distances[i, j] = distances[j, i] = distance
            PE -= G * mass_arr[i] * mass_arr[j] / distance

    Total_E = KE + PE
    return KE, PE, Total_E

def COM_calc(mass_arr, pos_arr):
    COM = np.zeros(3)
    total_mass = np.sum(mass_arr)
    for i in range(3):
        COM[i] = np.sum(mass_arr.reshape(-1, 1) * pos_arr[i, :]) / total_mass

    return COM

def numerical_sim(mass_arr, pos_arr, vel_arr):
    num_particles = mass_arr.shape[0]
    pos_stack = np.expand_dims(pos_arr, axis=0)
    v_sqd_arr = np.sum(vel_arr ** 2, axis=0)
    v_sqd_stack = np.expand_dims(v_sqd_arr, axis=0)

    dt = 0.002  # each frame is taking approximately this amount of seconds on my pc will change for others
    t = 80
    Energy_arr = np.empty((3, int(t / dt)))
    for i in range(int(t / dt)):
        acc_arr = acc_calc(mass_arr, pos_arr)
        pos_arr, vel_arr = update_position_velocity(pos_arr, vel_arr, acc_arr, dt)

        Energy_arr[0, i], Energy_arr[1, i], Energy_arr[2, i] = Energy_calc(mass_arr, pos_arr, vel_arr)

        v_sqd_arr = np.sum(vel_arr ** 2, axis=0)

        v_sqd_stack = np.vstack((v_sqd_stack, np.expand_dims(v_sqd_arr, axis=0)))
        pos_stack = np.vstack((pos_stack, np.expand_dims(pos_arr, axis=0)))

    return pos_stack, v_sqd_stack, Energy_arr

# This section creates arrays with the properties of n particles which it reads from a file
if __name__ == "__main__":
    num_body = int(input("Enter the number of particles: "))
    filename = askopenfilename(initialdir='Initial_parameters')

    # Read data from the file
    data = np.loadtxt(filename, delimiter=':', dtype=str)

    # Check if the required lines are present in the file
    mass_line = data[data[:, 0] == 'mass']
    pos_line_x = data[data[:, 0] == 'x-position']
    pos_line_y = data[data[:, 0] == 'y-position']
    pos_line_z = data[data[:, 0] == 'z-position']
    vel_line_x = data[data[:, 0] == 'x-velocity']
    vel_line_y = data[data[:, 0] == 'y-velocity']
    vel_line_z = data[data[:, 0] == 'z-velocity']

    if (
        mass_line.size == 0
        or pos_line_x.size == 0
        or pos_line_y.size == 0
        or pos_line_z.size == 0
        or vel_line_x.size == 0
        or vel_line_y.size == 0
        or vel_line_z.size == 0
    ):
        raise ValueError(
            "Input file does not contain the required lines ('mass', 'position_x', 'position_y', 'position_z', 'velocity_x', 'velocity_y', 'velocity_z')"
        )

    mass_data = mass_line[0, 1].split(',')
    pos_data_x = pos_line_x[0, 1].split(',')
    pos_data_y = pos_line_y[0, 1].split(',')
    pos_data_z = pos_line_z[0, 1].split(',')
    vel_data_x = np.array(vel_line_x[0, 1].split(','), dtype=float)
    vel_data_y = np.array(vel_line_y[0, 1].split(','), dtype=float)
    vel_data_z = np.array(vel_line_z[0, 1].split(','), dtype=float)

    # Convert data to NumPy arrays
    mass_array = np.array(mass_data, dtype=float)
    pos_array = np.column_stack(
        (np.array(pos_data_x, dtype=float), np.array(pos_data_y, dtype=float), np.array(pos_data_z, dtype=float))
    )
    vel_array = np.column_stack((vel_data_x, vel_data_y, vel_data_z))

    COM = COM_calc(mass_array, pos_array)

    parts = filename.split('/')
    out_filename_pos = parts[len(parts) - 1].split('.')[0] + '__pos_out.csv'
    out_filename_vsqd = parts[len(parts) - 1].split('.')[0] + '__vsqd_out.csv'
    out_filename_en = parts[len(parts) - 1].split('.')[0] + '__energy_out.csv'
    out_filename_com = parts[len(parts) - 1].split('.')[0] + '__com_out.csv'

    pos_stack, v_sqd_stack, Energy_arr = numerical_sim(mass_array, pos_array, vel_array)

    np.savetxt('Pos_outputs/' + out_filename_pos, pos_stack.reshape(-1, pos_stack.shape[-1]))
    np.savetxt('Pos_outputs/' + out_filename_vsqd, v_sqd_stack)
    np.savetxt('Pos_outputs/' + out_filename_en, Energy_arr)
    np.savetxt('Pos_outputs/' + out_filename_com, COM)