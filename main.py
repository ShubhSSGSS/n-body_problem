#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import vpython as vp

#This section creates an array with the properties of n particles which it reads from a file

num_body = int(input("Enter the number of particles: "))
particle_array = np.empty((num_body, 7))        #This will create an array with rows for eaach particle where there are 7(mass; x,y,z position vectors; x,y,z velocity vetors) elements

fhand = open('data.txt')

column_count = 0
for line in fhand:                              #This for loop populates the empty array with the data from file
    dummy = line.split(': ')
    data = dummy[1].split(', ')
    
    row_count = 0
    for i in data:
        particle_array[row_count, column_count] = i
        row_count+=1
    
    column_count+=1

print(particle_array)