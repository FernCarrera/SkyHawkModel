# Skyhawk 4D model
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class Skyhawk:
    num_of_Skyhawks = 0

    def __init__(self,name,excel):
        Skyhawk.num_of_Skyhawks += 1
        Data = excel.parse("Attributes")  
        self.name = name
        self.number = Skyhawk.num_of_Skyhawks
        self.Data = Data
        
    def name_num(self):
        return '{} Num: {}'.format(self.name,self.number)
    # method ofr moment coeffs
    # method for exquations of motion
    
    
    def momentCoeff(self):
        Ixx = int(self.Data.Ixx)
        Izz = int(self.Data.Izz)
        Iyy = int(self.Data.Iyy)
        Ixz = int(self.Data.Ixz)
        # Moment Coefficient Calculations (only calculating moments for hw3 scenario)
        c0 = (Ixx*Izz - Ixz**2)**-1
        c3 = c0*Izz
        c4 = c0*Ixz
        c10 = c0*Ixx
        return c0,c3,c4,c10

        
class Mission():
    # default attributes
    beta = 0
    p = 0
    r = 0
    phi = 0
    psi = 0
    r_def = 0
    # note: need to calc density based on alt
    def __init__(self, altitude, velocity, density):
        self.altitude = altitude
        self.velocity = velocity
        self.density = density
        #self.time = time
    
    # Sets custom initial conditions
    @classmethod
    def set_init_cond(cls,beta,p,r,phi,psi,r_def):
        cls.beta = beta
        cls.p = p
        cls.r = r
        cls.phi = phi
        cls.psi = psi
        cls.r_def = r_def
    
    # Run Simulation
    # can run different planes
    @staticmethod
    def simulate(Duration):
        # declare arrays/variables needed for math
        # call for custom rudder input based off duration input
        
        # calc aero coefficients
        # calc forces and moments
        # calculate equations of motion

        # control system method?

        # runge kutta method

        # append data



        pass

# math class that takes care of runge kutta?
hawk1 = pd.ExcelFile("Data/Skyhawk_Attributes.xlsx")
hawk2 = pd.ExcelFile("Data/Skyhawk_Attributes2.xlsx")


# plotting class?
james = Skyhawk('James',hawk1)
charles = Skyhawk('Charles',hawk2)

#print(hawk1.name_num())
print(james.name_num())
print(charles.name_num())

print(james.momentCoeff())
print(charles.momentCoeff())
    
