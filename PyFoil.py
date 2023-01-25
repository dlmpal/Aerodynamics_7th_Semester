# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 16:41:35 2022

@author: dlmpa
"""

import numpy as np 
import os
import subprocess

class XfoilInstance():
    def __init__(self, tag):
        self.input_filepath =  f"XFOIL_INPUT_INSTANCE{tag}.in"
        self.tag = tag
        self.iter = 250
        self.N = 200
        self.visc = True
        self.re = 50e3
        self.aseq = [4, 6, 0.5]
        self.polar_filepath = f"POLAR_{tag}.txt"
        self.results = {}
    
    def _create_file_core(self, airfoil_filepath: str):
        input_file = open(self.input_filepath, "w")
        input_file.write("PLOP\n")
        input_file.write("G F\n\n")
        input_file.write(f"LOAD {airfoil_filepath}\n")
        input_file.write("CUSTOM_AIRFOIL\n")
        input_file.write("PPAR\n")
        input_file.write(f"N {self.N}\n\n\n")
        input_file.write("OPER\n")
        if self.visc:
            input_file.write(f"VISC {self.re}\n")
        input_file.write("PACC\n")
        input_file.write(f"{self.polar_filepath}\n\n")
        #input_file.write(f"ITER {self.iter}\n")
        input_file.write(
            f"ASEQ {self.aseq[0]} {self.aseq[1]} {self.aseq[2]}\n")
        input_file.write("\n\n")
        input_file.write("quit\n")
        input_file.close()

    def _read_polar_file(self):
        output_file = open(self.polar_filepath, "r")
        lines = output_file.readlines()

        start_idx = 0
        self.results = {}
        for line in lines:
            tokens = line.split()
            start_idx += 1
            if len(tokens) == 0:
                continue
            if tokens[0] == "alpha":
                for token in tokens:
                    self.results[token] = []
                break

        for idx in range(start_idx+1, len(lines)):
            line = lines[idx]
            tokens = line.split()
            tokens = [float(token) for token in tokens]
            col_idx = 0
            for key in self.results:
                self.results[key].append(tokens[col_idx])
                col_idx += 1
    
    def run_instance(self, airfoil_filepath: str):
        
        if not os.path.exists(airfoil_filepath):
            print(f"File: {airfoil_filepath} does not exist\n")
            return
        if os.path.exists(self.polar_filepath):
            os.remove(self.polar_filepath)
        self._create_file_core(airfoil_filepath)
        subprocess.call(f"xfoil.exe < {self.input_filepath}", shell=True)
        self._read_polar_file()
        
    def finalize(self):
        if os.path.exists(self.input_filepath):
            os.remove(self.input_filepath)
        if os.path.exists(self.polar_filepath):
            os.remove(self.polar_filepath)
            
def ReadCp(filepath):
    if not os.path.exists(filepath):
        print(f"File {filepath} does not exist")
        return 
    file = open(filepath, "r")
    x = []
    y = []
    Cp = []
    lines = file.readlines()
    lines = lines[3:]
    for line in lines: 
        tokens = [float(token) for token in line.split()]
        x.append(tokens[0])
        y.append(tokens[1])
        Cp.append(tokens[2])
    return x,y,Cp
    
    
    