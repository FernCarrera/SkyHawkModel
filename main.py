from Classes.Vehicle import Vehicle
from Classes.Mission import Mission
import pandas as pd

# Import Data
hawk1 = pd.ExcelFile("Data/Skyhawk_Attributes.xlsx")
hawk2 = pd.ExcelFile("Data/Skyhawk_Attributes2.xlsx")

rudder_in = pd.ExcelFile("Data/rudder_input.xlsx")
yuh = rudder_in.parse("Sheet1")
rudder_deg = yuh.rudder_deg.tolist()
time = yuh.time_s.tolist()
yaw_real = yuh.yaw_rate_deg_s.tolist()

# Create Vehicles
james = Vehicle('James',hawk1)
bond = Vehicle('bond',hawk2)

# Create Mission
test = Mission("One")
test.apply_sensor_data(rudder_in)
test.set_init_cond(190,4500,0.77)

# Run Simulations
yaw = test.simulate(james,rudder_in)
yaw2 = test.simulate(bond,rudder_in)




    
