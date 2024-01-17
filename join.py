#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 03:22:39 2023

@author: shubh
"""
import numpy as np

data1 = np.loadtxt('/home/shubh/Codes/n-body_problem/Pos_outputs/param2__pos_out1.csv')
data2 = np.loadtxt('/home/shubh/Codes/n-body_problem/Pos_outputs/param2__pos_out2.csv')
data3 = np.loadtxt('/home/shubh/Codes/n-body_problem/Pos_outputs/param2__pos_out3.csv')

data = np.hstack((data1, data2, data3))

np.savetxt('/home/shubh/Codes/n-body_problem/Pos_outputs/param2__pos_out.csv', data)