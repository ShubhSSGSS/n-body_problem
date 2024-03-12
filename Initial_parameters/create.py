#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 03:22:39 2023

@author: shubh
"""
import random

# Define the number of objects
num_objects = 150

# Define the range of values for mass, position, and velocity
mass_range = (5000, 10000)
position_range = (-100, 100)
velocity_range = (-20, 20)

# Open the file in write mode
with open("objects_data.txt", "w") as file:
    # Write data for each attribute of the objects
    for attribute in ["mass", "x-position", "y-position", "z-position", "x-velocity", "y-velocity", "z-velocity"]:
        file.write(attribute + ": ")

        # Generate random data points for each object
        data_points = [random.randint(*mass_range) if attribute == "mass" else random.randint(*position_range) if "position" in attribute else random.randint(*velocity_range) for _ in range(num_objects)]

        # Write the data points to the file
        file.write(", ".join(str(data_point) for data_point in data_points) + "\n")
