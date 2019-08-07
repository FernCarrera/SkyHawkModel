class Vehicle:
    num_of_Vehicles = 0

    def __init__(self,name,excel):
        Vehicle.num_of_Vehicles += 1
        Data = excel.parse("Attributes")  
        self.name = name
        self.number = Vehicle.num_of_Vehicles
        self.Data = Data
        
    def get_name(self):
    
        return '{}'.format(self.name)
   
    
    def vehicle_geometry(self):
        return float(self.Data.wingarea),float(self.Data.span)
    def vehicle_mass(self):
        return float(self.Data.mass)


    def momentCoeff(self):
        Ixx = float(self.Data.Ixx)
        Izz = float(self.Data.Izz)
        Iyy = float(self.Data.Iyy)
        Ixz = float(self.Data.Ixz)
        # Moment Coefficient Calculations (only calculating moments for hw3 scenario)
        c0 = (Ixx*Izz - Ixz**2)**-1
        c3 = c0*Izz
        c4 = c0*Ixz
        c10 = c0*Ixx
        c = [c0,c3,c4,c10]
        return c

    def aero_coefficients(self):
        coeff = [float(self.Data.cyb),float(self.Data.cydr),float(self.Data.clb),float(self.Data.clp),float(self.Data.clr),\
                 float(self.Data.cldr),float(self.Data.cnb),float(self.Data.cnp),float(self.Data.cnr),float(self.Data.cndr)]
        return coeff 
