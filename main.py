# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 02:43:23 2022

@author: dlmpa
"""

import PyFoil
import Bezier
import matplotlib.pyplot as plt

#%% Cl,Cd,Cm

points = Bezier.ReadAirfoil("NACA6716.dat")
Bezier.WriteAirfoil(points, "NACA6716.dat")
instance = PyFoil.XfoilInstance(0)
instance.N = 250
instance.aseq = [1, 25 , 0.1]
instance.visc = True

fig , axs = plt.subplots(nrows = 1 , ncols=3)


Re = [1e6, 3e6, 5e6]
for i in range(len(Re)):
    instance.re = Re[i]
    instance.run_instance("NACA6716.dat")
    Cl_panel = instance.results["CL"]
    Cd_panel = instance.results["CD"]
    Cm_panel = instance.results["CM"]
    alpha_panel = instance.results["alpha"]
    axs[0].plot(alpha_panel,Cl_panel,'-',label=f"Re={Re[i]}")
    axs[1].plot(alpha_panel,Cd_panel,'-',label=f"Re={Re[i]}")
    axs[2].plot(alpha_panel,Cm_panel,'-',label=f"Re={Re[i]}")

axs[0].set_xlabel("AoA [deg]")
axs[0].set_ylabel("Cl")
axs[0].legend()
axs[0].grid()

axs[1].set_xlabel("AoA [deg]")
axs[1].set_ylabel("Cd")
axs[1].legend()
axs[1].grid()

axs[2].set_xlabel("AoA [deg]")
axs[2].set_ylabel("Cm")
axs[2].legend()
axs[2].grid()

fig.tight_layout()
plt.show()
#plt.savefig("ReynoldsAoA.png")

#%% Cp

import PyFoil
fig,ax = plt.subplots(nrows=1,ncols=1)
x,y,Cp_panel_v = PyFoil.ReadCp("NACA6716_CP_v.dat")
_,_,Cp_panel_i = PyFoil.ReadCp("NACA6716_CP_i.dat")

ax.plot(x,Cp_panel_i,label="inviscid, Cl=2.3")
ax.plot(x,Cp_panel_v,label="viscous, Cl=1.664")

ax.set_xlabel("x")
ax.set_ylabel("Cp")
ax.set_title("AoA = 10 deg")
ax.grid()
ax.legend()
plt.savefig("ViscousInviscidComparisonAoA10.png")

#%% Optimization

from AirfoilOptimization import PSO
upx = [0, 0,  0.25,0.5,0.75,1]
downx = upx
upy =   [0,  0.05,    0.2,  0.15,  0.1 ,       0]
downy = [0, -0.05,   -0.1,  0.10,  0.05,       0]
baseline = {"lower":{"x":downx,"y":downy},
            "upper":{"x":upx,"y":upy}}
n_particles = 10 
optimizer = PSO(n_particles, 6, baseline)
optimizer.optimize(50)
optimizer.plot_results()



    
