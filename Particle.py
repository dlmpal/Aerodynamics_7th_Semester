# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 16:55:22 2022

@author: dlmpa
"""

import numpy as np 
from PyFoil import XfoilInstance
import Bezier

class Particle():

    def __init__(self, tag , n_cp , baseline):
        self.tag = tag
        self.x_foil_instance = XfoilInstance(self.tag)
        self.airfoil_filepath = f"AIRFOIL_{self.tag}.dat"
        self.n_cp = n_cp 
        self.cp = baseline
        self.vel = {"upper":[0 for i in range(self.n_cp)] , "lower":[0 for i in range(self.n_cp)]} 
        self.best = baseline
        self.pen = 0 
        self.create_airfoil_file()
        self.obj = self._execute()
        self.update_val = (self.tag , self.cp , self.obj)

    def create_airfoil_file(self):
        airfoil_file = open(self.airfoil_filepath, "w")
        points = Bezier.AirfoilBezier(self.cp["lower"]["x"],self.cp["upper"]["y"], self.cp["lower"]["y"])
        half = int((len(points)+1)/2 -1 )
        upper = points[1:half]
        lower = np.flip(points[half+1:-1],0)
        thickness = upper - lower
        t_mean = np.mean(thickness)
        t_max = np.max(thickness)
        t_min = np.min(thickness)
        t1 = -1/t_min**2 if t_min < 0 else 0
        t2 = -1/t_max**2 if t_max > 0.2 else 0 
        self.pen = t1 + t2
        for i in range(len(points)):
            airfoil_file.write(f"{points[i,0]} {points[i,1]}\n")
        airfoil_file.close()
    
    def _execute(self):
        obj = self.pen
        if self.pen < 0 :
            return obj
        print(f"Particle {self.tag} executing")
        self.x_foil_instance.run_instance(self.airfoil_filepath)
        obj += np.mean(self.x_foil_instance.results["CL"]) 
        return obj         

    def execute(self, r1, r2 , g_best):
        
        self.update_val = None
        for key in self.vel:
            for i in range(self.n_cp):
                self.vel[key][i] = 0.6*self.vel[key][i]+2*r1 * \
                    (self.best[key]["y"][i]-self.cp[key]["y"][i])+3*r2*(g_best[key]["y"][i]-self.cp[key]["y"][i])
                self.cp[key]["y"][i] += self.vel[key][i]
          
        self.create_airfoil_file()
        temp_obj = self._execute()
        if temp_obj >= self.obj:
            self.obj = temp_obj 
            self.best = self.cp 
            self.update_val = (self.tag , self.cp , self.obj)
        
    def update(self,g_best_val):
        if self.obj < g_best_val:
            self.update_val = None
       
            