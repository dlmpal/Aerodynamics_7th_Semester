# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 16:44:38 2022

@author: dlmpa
"""


import numpy as np 
from math import factorial as fact


def Bezier(x_cp , y_cp ,  n_points=100):
    N = len(x_cp)-1
    M = np.zeros((N+1,N+1))
    for i in range(N+1):
        for j in range(i,N+1):
            M[i,j] = (-1)**(j-i) * (fact(N)/(fact(N-j))) * (1/(fact(i)*fact(j-i)))
    t_range = np.linspace(0 , 1 , n_points)
    t_vec = np.array([[t**i for i in range(N+1)] for t in t_range]).T
    C = M @ t_vec
    x = C.T @ x_cp 
    y = C.T @ y_cp    
    return x,y

def AirfoilBezier(x , upy , downy):
    
    xu , yu = Bezier(x , upy)
    xd , yd = Bezier(x , downy)
    
    xu = xu.reshape((len(xu),1))
    yu = yu.reshape((len(yu),1))
    xd = xd.reshape((len(xd),1))[1:]
    yd = yd.reshape((len(yd),1))[1:]
    
    upper = np.concatenate((xu,yu),1)
    upper = np.flip(upper,0)
    lower = np.concatenate((xd,yd),1)
    return np.concatenate((upper,lower),0)


def ReadAirfoil(airfoil_filepath:str):
    file = open(airfoil_filepath , "r")
    lines = file.readlines()
    points = []
    for line in lines:
        tokens = line.split()
        tokens = [float(token) for token in tokens]
        points.append(tokens)
    return np.array(points)

def WriteAirfoil(points , airfoil_filepath:str):
    file = open(airfoil_filepath,"w")
    for i in range(len(points)):
        file.write(f"{points[i,0]} {points[i,1]}\n")
