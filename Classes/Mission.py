from Classes.Calc import Calc
from Classes.Vehicle import Vehicle
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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
    altitude = 0
    density = 0
    qbar = 0
    name = ' '
    control = False # Better way?
    # note: need to calc density based on alt
    def __init__(self,name):
        self.name = name
    
    
    def get_name(self):
        return self.name
    @classmethod 
    def control_system(cls,value):
        cls.control = value

    # Sets custom initial conditions
    @classmethod
    def set_init_cond(cls,velocity,altitude,density):
        
        cls.velocity = velocity
        cls.altitude = altitude
        cls.density = density
        cls.qbar = 0.5*density*velocity**2
    
    def return_velocity(self):
        return self.velocity


    @classmethod
    def apply_sensor_data(cls,rudder_data):
        Data = rudder_data.parse("Sheet1")
        
        time = Data.time_s.tolist()     
        rudder_deg = Data.rudder_deg.tolist() 
        yaw_rate = Data.yaw_rate_deg_s.tolist()
        cls.time = time
        cls.rudder_deg = rudder_deg
        cls.yaw_rate = yaw_rate
    
    @classmethod
    def return_sensor_data(cls):
        return cls.time,cls.rudder_deg,cls.yaw_rate
  
    # updates vehicle position, to use during calculation
    @classmethod
    def update_state(cls,state):
        cls.beta = state[0]
        cls.p = state[1]
        cls.r = state[2]
        cls.phi = state[3]
        cls.psi = state[4]
       


    # Provides orientation data
    @classmethod
    def state(cls):
        state = [cls.beta,cls.p,cls.r,cls.phi,cls.psi]
        return state

    # Run Simulation
    # can run different planes
    @classmethod
    def simulate(cls,vehicle,rudder_in):
        
        cls.apply_sensor_data(rudder_in)
        #state = cls.state()
        v = cls.return_velocity(cls)
        yaw = []
        i = 0
        time = cls.time
        kr = -0.4
        for x in cls.time:
           
            # Control system check
            if (cls.control == True):
                state = cls.state()
                z = np.exp(-1)*state[2]
                #zdot = cls.r - z # change in time constant??
                r_def = cls.rudder_deg[i]*(np.pi/180)
                r_def = r_def + kr*(z-state[2])
            else:
                r_def = cls.rudder_deg[i]*(np.pi/180)

            aero = Calc.aeroC(vehicle,cls,r_def,v)
            forces = Calc.forceCalc(vehicle,cls.qbar,aero)
            rates = Calc.EOM(forces,vehicle,v,cls)
            new_state = Calc.RK4(cls.state(),rates)

            
            cls.update_state(new_state)

            
            yaw.append(new_state[2]*(180/np.pi))
            i += 1

        fig = plt.subplot()
        fig.plot(time,cls.rudder_deg,label='rudder in')
        fig.plot(time,yaw,label= '{}'.format(Vehicle.get_name(vehicle)) )
        fig.plot(time,cls.yaw_rate,label='Flight Data')
        plt.ylabel('yaw rate [deg/s]')
        plt.title('{},Control:{}'.format(Vehicle.get_name(vehicle),cls.control)) # Add simulation name
        plt.xlabel('time [s]')
        fig.legend()
        plt.show()
        
        return yaw
