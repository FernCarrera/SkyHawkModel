# Skyhawk 4D model
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class Vehicle:
    num_of_Vehicles = 0

    def __init__(self,name,excel):
        Vehicle.num_of_Vehicles += 1
        Data = excel.parse("Attributes")  
        self.name = name
        self.number = Vehicle.num_of_Vehicles
        self.Data = Data
        
    def name_num(self):
        return '{} Num: {}'.format(self.name,self.number)
    # method ofr moment coeffs
    # method for exquations of motion
    
    def vehicle_geometry(self):
        return int(self.Data.wingarea),int(self.Data.span)
    def vehicle_mass(self):
        return int(self.Data.mass)


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

    def aero_coefficients(self):
        coeff = [int(self.Data.cyb),int(self.Data.cdr),int(self.Data.clb),int(self.Data.clp),int(self.Data.clr),\
                 int(self.Data.cdr),int(self.Data.cnb),int(self.Data.cnp),int(self.Data.cnr),int(self.Data.cdr)]
        return coeff 


    



class Mission():
    # default attributes
    beta = 0
    p = 0
    r = 0
    phi = 0
    psi = 0
    r_def = 0
    rudder_in = 0
    velocity = 0
    # note: need to calc density based on alt
    def __init__(self,name, altitude, velocity, density):
        self.name = name
        self.altitude = altitude
        self.velocity = velocity
        self.density = density
        #self.time = time
    
    # Sets custom initial conditions
    @classmethod
    def set_init_cond(cls,beta,p,r,phi,psi,r_def,velocity):
        cls.beta = beta
        cls.p = p
        cls.r = r
        cls.phi = phi
        cls.psi = psi
        cls.r_def = r_def
        cls.velocity = velocity
    
    @classmethod
    def apply_sensor_data(cls,rudder_data):
        Data = rudder_data.parse("Sheet1")
        
        cls.time = Data.time_s     
        cls.rudder_deg = Data.rudder_deg 
        cls.yaw_rate = Data.yaw_rate_deg_s
    
    @classmethod
    def return_sensor_data(cls):
        return cls.time,cls.rudder_deg,cls.yaw_rate
  
    # updates vehicle position, to use during calculation
    @classmethod
    def update_state(cls,beta,p,r,phi,psi,r_def,velocity):
        cls.beta = beta
        cls.p = p
        cls.r = r
        cls.phi = phi
        cls.psi = psi
        cls.r_def = r_def
        cls.velocity = velocity


    # Provides orientation data
    @classmethod
    def state(cls):
        state = [cls.beta,cls.p,cls.r,cls.phi,cls.psi,cls.r_def,cls.velocity]
        return state

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


class Calc():

    # 4th Order Runge-Kutta
    # x: value, rates: rate-of-change
    @staticmethod
    def RK4(x, rates):
        rn = []
        dt = 0.01
        for i in range(len(x)):
            rn.append(x[i])
        r1 = rates
        for i in range(len(x)):
            rn[i] = x[i]+0.5*dt*r1[i]
        r2 = rates
        for i in range(len(x)):
            rn[i] = x[i]+0.5*dt*r2[i]
        r3 = rates
        for i in range(len(x)):
            rn[i] = x[i]+dt*r3[i]
        r4 = rates
        for i in range(len(x)):
            rn[i] = x[i] + (dt/6.0)*(r1[i]+2.0*r2[i]+2.0*r3[i]+r4[i])
        return rn

    # Cy,Cl,Cn calculator
    @staticmethod
    def aeroC(vehicle,simulation):
        area,b = vehicle.vehicle_geometry() # area, and span
        c = vehicle.aero_coefficients()
        state = simulation.state()
        
        beta = state[0]
        p = state[1]
        r = state[2]
        r_def = state[5]
        v = state[6]
        
        Cy = c[0]*beta + c[1]*r_def
        Cl = c[2]*beta + c[3]*(p*b/(2*v)) + c[4]*(r*b/(2*v)) + c[5]*r_def
        Cn = c[6]*beta + c[7]*(p*b/(2*v)) + c[8]*(r*b/(2*v)) + c[9]*r_def
        
        return Cy,Cl,Cn

    # forces and moments method



# math class that takes care of runge kutta?
hawk1 = pd.ExcelFile("Data/Skyhawk_Attributes.xlsx")
hawk2 = pd.ExcelFile("Data/Skyhawk_Attributes2.xlsx")

rudder_in = pd.ExcelFile("Data/rudder_input.xlsx")

# plotting class?
james = Vehicle('James',hawk1)
charles = Vehicle('Charles',hawk2)

test = Mission("One",10000,1000,1.225)
test.apply_sensor_data(rudder_in)
test.update_state(0,0,0,0,0,0,100)

Cy,Cl,Cn = Calc.aeroC(james,test)
print("Cy",Cy)

    
