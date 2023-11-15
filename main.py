#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from tkinter.filedialog import askopenfilename

def acc_calc(mass_arr: np.ndarray, pos_arr: np.ndarray) -> np.ndarray:  #To calculate the acceleration of each particle
    assert isinstance(mass_arr, np.ndarray), "mass_arr should be a NumPy array"
    assert isinstance(pos_arr, np.ndarray), "pos_arr should be a NumPy array"
    
    n = mass_arr.shape[0]
    acc_arr = np.zeros_like(pos_arr)

    # Calculate gravitational acceleration for each object
    for i in range(n):
        for j in range(n):
            if i != j:
                # Calculate the displacement vector between objects i and j
                r = pos_arr[:,j] - pos_arr[:,i]
                # Calculate the distance between objects i and j
                e = 20 #softening parameter so that the force doesn't shoot to infinity
                distance = (np.linalg.norm(r)**2 + e**2)**0.5
                unit_vec = r/distance
                # Calculate the gravitational force magnitude
                G = 10  # Universal gravitational constant
                force_magnitude = (G * mass_arr[i] * mass_arr[j]) / (distance ** 2)
                # Calculate the gravitational acceleration for object i in x, y, and z components
                acceleration =  force_magnitude * unit_vec / (mass_arr[i])
                # Update the x, y, and z components of acceleration in acc_arr
                acc_arr[:,i] += acceleration
                #acc_arr *= -1
    
    return acc_arr

def update_position_velocity(pos_arr: np.ndarray, vel_arr: np.ndarray, acc_arr: np.ndarray, dt: float):

    # Update velocity using the calculated acceleration
    vel_arr += acc_arr * dt

    # Update position using the updated velocity
    pos_arr += vel_arr * dt

    return pos_arr, vel_arr

def Energy_calc(mass_arr, pos_arr, vel_arr):
    #Calculating Potential Energy
    n = mass_arr.shape[0]
    e=20 #softening parameter
    G=10 #Universal Gravitational constant
    
    KE = 0.5 * np.sum(mass_arr*np.linalg.norm(vel_arr, axis=0)**2)
    PE = 0.0
    for i in range(n):
        for j in range(i+1,n):
            r = pos_arr[:, j] - pos_arr[:, i]
            distance = (np.linalg.norm(r)**2 + e**2)**0.5
            PE -= G * mass_arr[i] * mass_arr[j] / (distance)
    Total_E = KE+PE
    return KE, PE, Total_E

def COM_calc(mass_arr, pos_arr):
    COM = np.zeros(3)
    total_mass = np.sum(mass_arr)
    for i in range(3):
        COM[i] = np.sum(mass_arr*pos_arr[i])/total_mass
    
    return COM
    

def numerical_sim(mass_arr,pos_arr,vel_arr):
    pos_stack = np.copy(pos_array)
    v_sqd_arr = np.zeros_like(mass_arr) # squared magnitude of velocity
    #vel_stack = np.copy(vel_array)
    for j in range(len(mass_arr)):
        v_sqd_arr[j] = sum((vel_arr**2)[:,j])

    v_sqd_stack = np.copy(v_sqd_arr)

    dt=0.003 # each frame is taking approximately this amount of seconds on my pc will change for others
    t= 50
    Energy_arr = np.empty((3,int(t/dt)))
    for i in range(int(t/dt)):
        acc_arr = acc_calc(mass_arr, pos_arr)
        pos_arr,vel_arr = update_position_velocity(pos_arr, vel_arr, acc_arr, dt)
        
        Energy_arr[0,i],Energy_arr[1,i],Energy_arr[2,i] = Energy_calc(mass_arr, pos_arr, vel_arr)
        
        for j in range(len(mass_arr)):
            v_sqd_arr[j] = sum((vel_arr ** 2) [:, j])

        v_sqd_stack = np.vstack((v_sqd_stack, v_sqd_arr))
        pos_stack = np.vstack((pos_stack, pos_arr))

    return pos_stack, v_sqd_stack, Energy_arr
        
        

    return pos_stack, v_sqd_stack, Energy_arr

#This section creates arrays with the properties of n particles which it reads from a file
if __name__ =="__main__":
    num_body = int(input("Enter the number of particles: "))
    filename = askopenfilename(initialdir='Initial_parameters')
    
    mass_array = np.empty(num_body)        
    pos_array = np.empty((3,num_body))
    vel_array = np.empty((3,num_body))
    
    fhand = open(filename)
    
    pos_index=0
    vel_index=0
    for line in fhand:
        #line=line.rstrip()
        dummy = line.rstrip().split(':')
        data = dummy[1].split(',')
        if 'mass' in dummy[0]:
            for i in range(num_body):
                mass_array[i] = data[i]
        elif 'position' in dummy[0]:
            for i in range(num_body):
                pos_array[pos_index,i]=data[i]
            pos_index+=1
        elif 'velocity' in dummy[0]:
            for i in range(num_body):
                vel_array[vel_index,i]=data[i]
            vel_index+=1
    
    
    COM = COM_calc(mass_array, pos_array)
    
    parts= filename.split('/')
    out_filename_pos = parts[len(parts)-1].split('.')[0]+'__pos_out.csv'
    out_filename_vsqd = parts[len(parts)-1].split('.')[0]+'__vsqd_out.csv'
    out_filename_en = parts[len(parts)-1].split('.')[0]+'__energy_out.csv'
    out_filename_com = parts[len(parts)-1].split('.')[0]+'__com_out.csv'
    
    pos_stack, v_sqd_stack, Energy_arr = numerical_sim(mass_array, pos_array, vel_array)
    
    np.savetxt('Pos_outputs/'+out_filename_pos,pos_stack)
    np.savetxt('Pos_outputs/'+out_filename_vsqd,v_sqd_stack)
    np.savetxt('Pos_outputs/'+out_filename_en,Energy_arr)
    np.savetxt('Pos_outputs/'+out_filename_com,COM)