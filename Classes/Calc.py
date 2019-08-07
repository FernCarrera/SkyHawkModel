import numpy as np
class Calc():

    # 4th Order Runge-Kutta
    # x: value, rates: rate-of-change
    @staticmethod
    def RK4(x, rates):
        rn = []
        dt = 0.05 # need user to set interval 
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
    def aeroC(vehicle,mission,r_def,v):
        area,b = vehicle.vehicle_geometry() # area, and span
        c = vehicle.aero_coefficients()
        
        state = mission.state()
        
        beta = state[0]
        p = state[1]
        r = state[2]
        
        
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
        # c = [c0,c3,c4,c10]
        betaDot = (1/v)*(f[0]/m + g*np.sin(x[3]))-x[2]
        pAcc = c[1]*f[1] + c[2]*f[2]
        rAcc = c[2]*f[1] + c[3]*f[2]
        phiDot = x[1]
        psiDot = x[2]*np.cos(x[3])

        

        rates = [betaDot,pAcc,rAcc,phiDot,psiDot]
       
        return rates