# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 16:39:15 2022

@author: dlmpa
"""

import numpy as np 
from Particle import Particle
import Bezier 
import matplotlib.pyplot as plt

class PSO():
    def __init__(self , n_particles: int , n_cp : int , baseline : {}):
        self.n_particles = n_particles
        self.n_cp = n_cp 
        self.baseline = baseline
        self.optimized = baseline
        self.particles = []
        self._create_particles()

    def _create_particles(self):
        # create particles
        for i in range(self.n_particles):
            lower_y = np.random.uniform(low=0.97, high=1.05, size=(self.n_cp,)) * self.baseline["lower"]["y"]
            upper_y = np.random.uniform(low=0.97, high=1.05, size=(self.n_cp,)) * self.baseline["upper"]["y"]
            baseline = {"lower":{"x":self.baseline["lower"]["x"] , "y":lower_y},
                        "upper":{"x":self.baseline["upper"]["x"] , "y":upper_y}}
            self.particles.append(Particle(i , self.n_cp , baseline))
            
            
    def optimize(self, max_evals=1000, tol=1e-3):

        eval_count = 0
        g_best_val = -1e8
        g_best = self.baseline
        history = {"obj":[] , "design":[]}
        
        epoch = 0 
        while(eval_count <= max_evals):
            
            print(f"Epoch : {epoch} , Obj: {g_best_val}")
            for i in range(self.n_particles):
                print(f"Particle {i} , Obj : {self.particles[i].obj}")
                self.particles[i].update(g_best_val)
                if self.particles[i].update_val is not None:
                    g_best = self.particles[i].update_val[1]
                    g_best_val = self.particles[i].update_val[2]
            history["obj"].append(g_best_val)
            history["design"].append(g_best)
            for i in range(self.n_particles):
                r = np.random.rand(2,)
                r1 = r[0]
                r2 = r[1]
                eval_count += 1
                self.particles[i].execute(r1,r2,g_best)
            
            epoch +=1 
         
        self.optimized = g_best
        self.save_optimized()
        
        return history

    def save_optimized(self):
        file = open("AIRFOIL_OPTIMIZED.dat", 'w')
        points = Bezier.AirfoilBezier(self.optimized["lower"]["x"], self.optimized["upper"]["y"], self.optimized["lower"]["y"])
        for i in range(len(self.optimized)):
            file.write(f"{points[i,0]} {points[i,1]}\n")
        file.close()
    
    def plot_results(self):
        b_points = Bezier.AirfoilBezier(self.baseline["lower"]["x"], self.baseline["upper"]["y"],
                                        self.baseline["lower"]["y"])
        opt_points = Bezier.AirfoilBezier(self.optimized["lower"]["x"], self.optimized["upper"]["y"],
                                        self.optimized["lower"]["y"])
        
        plt.plot(b_points[:,0],b_points[:,1],label="Baseline")
        plt.plot(opt_points[:,0],opt_points[:,1],label="Optimized")
        plt.xlim([0 , 1])
        plt.legend()
        plt.show()

    


