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
        return float(self.Data.wingarea),float(self.Data.span)
    def vehicle_mass(self):
        return float(self.Data.mass)


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
        c = [c0,c3,c4,c10]
        return c

    def aero_coefficients(self):
        coeff = [float(self.Data.cyb),float(self.Data.cdr),float(self.Data.clb),float(self.Data.clp),float(self.Data.clr),\
                 float(self.Data.cdr),float(self.Data.cnb),float(self.Data.cnp),float(self.Data.cnr),float(self.Data.cdr)]
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
    altitude = 0
    density = 0
    # note: need to calc density based on alt
    def __init__(self,name, altitude, velocity, density):
        self.name = name
        #self.altitude = altitude
        #self.velocity = velocity
        #self.density = density
        #self.time = time
    
    # Sets custom initial conditions
    @classmethod
    def set_init_cond(cls,velocity,altitude,density):
        
        cls.velocity = velocity
        cls.altitude = altitude
        cls.density = density
    
    def return_velocity(self):
        return self.velocity


    @classmethod
    def apply_sensor_data(cls,rudder_data):
        Data = rudder_data.parse("Sheet1")
        
        time = Data.time_s.tolist()     
        rudder_deg = Data.rudder_deg.tolist() 
        yaw_rate = Data.yaw_rate_deg_s.tolist()
        #time = [round(x) for x in time]
        #rudder_deg = [round(x) for x in rudder_deg]
        #yaw_rate = [round(x) for x in yaw_rate] 
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
        #cls.r_def = state[5]
        #cls.velocity = state[6]


    # Provides orientation data
    @classmethod
    def state(cls):
        state = [cls.beta,cls.p,cls.r,cls.phi,cls.psi]
        return state

    # Run Simulation
    # can run different planes
    @classmethod
    def simulate(cls,james,rudder_in):
        cls.apply_sensor_data(rudder_in)
        state = cls.state()
        v = cls.return_velocity(cls)
      
        yaw = []
        yaw.append(0)
        i = 0
        for x in cls.time:
           
            
            r_def = cls.rudder_deg[i]
            aero = Calc.aeroC(james,cls,r_def,v)
            #print("aero",aero)
            forces = Calc.forceCalc(james,qbar,aero)
            rates = Calc.EOM(forces,james,v,cls)
            new_state = Calc.RK4(state,rates)
            
            cls.update_state(new_state)

            yaw.append(new_state[2]*(180/np.pi))
            i += 1

        # declare arrays/variables needed for math
        # call for custom rudder input based off duration input
        
        # calc aero coefficients
        # calc forces and moments
        # calculate equations of motion

        # control system method?

        # runge kutta method

        # append data
        return yaw


        


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
    def aeroC(vehicle,test,r_def,v):
        area,b = vehicle.vehicle_geometry() # area, and span
        c = vehicle.aero_coefficients()
        #print("C",c)
        state = test.state()
        
        beta = state[0]
        p = state[1]
        r = state[2]
        #r_def = state[5]
        #v = state[6]
        
        Cy = c[0]*beta + c[1]*r_def
        Cl = c[2]*beta + c[3]*(p*b/(2*v)) + c[4]*(r*b/(2*v)) + c[5]*r_def
        Cn = c[6]*beta + c[7]*(p*b/(2*v)) + c[8]*(r*b/(2*v)) + c[9]*r_def
        
        aero = [Cy,Cl,Cn]
        return aero

    # calculates forces and moments
    @staticmethod
    def forceCalc(vehicle,qbar,aero):
        S,b = vehicle.vehicle_geometry()
        # Forces
        fy = qbar*S*aero[0]
               
        # Moments
        L = qbar*S*b*aero[1]
        N = qbar*S*b*aero[2]

        forces = [fy,L,N]
        return forces
    
    # Equations of motion calculation
    @staticmethod
    def EOM(forces,vehicle,v,mission):
        f = forces
        g = 9.81
        x = mission.state()
        c = vehicle.momentCoeff()
        m = vehicle.vehicle_mass()

        # x = [beta,p,r,phi,psi]

        betaDot = (1/v)*(f[0]/m + g*np.sin(x[3]))-x[2]
        pAcc = c[1]*f[1] + c[2]*f[2]
        rAcc = c[2]*f[1] + c[3]*f[2]
        phiDot = x[1]
        psiDot = x[2]*np.cos(x[3])

        rates = [betaDot,pAcc,rAcc,phiDot,psiDot]

        return rates

        


# math class that takes care of runge kutta?
hawk1 = pd.ExcelFile("Data/Skyhawk_Attributes.xlsx")
hawk2 = pd.ExcelFile("Data/Skyhawk_Attributes2.xlsx")

rudder_in = pd.ExcelFile("Data/rudder_input.xlsx")


qbar = 13898.5
# plotting class?
james = Vehicle('James',hawk1)
charles = Vehicle('Charles',hawk2)

test = Mission("One",4500,190,0.77)
test.apply_sensor_data(rudder_in)
test.set_init_cond(190,4500,0.77)
#print("coef",james.aero_coefficients())
yaw = test.simulate(james,rudder_in)

#print("yaw",yaw)
fig = plt.subplot()
fig.plot(yaw,label='No Control System [deg/s]')
plt.show()


#Simulate(james,test,rudder_in)


    
