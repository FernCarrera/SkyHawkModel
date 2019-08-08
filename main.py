from Classes.Vehicle import Vehicle
from Classes.Mission import Mission
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

# Import Data
hawk1 = pd.ExcelFile("Data/Skyhawk_Attributes.xlsx")
hawk2 = pd.ExcelFile("Data/Skyhawk_Attributes2.xlsx")

rudder_in = pd.ExcelFile("Data/rudder_test.xlsx")
yuh = rudder_in.parse("Sheet1")
rudder_deg = yuh.rudder_deg.tolist()
time = yuh.time_s.tolist()
yaw_real = yuh.yaw_rate_deg_s.tolist()

# Create Vehicles
james = Vehicle('James',hawk1)

# Create Mission
test = Mission("One")
test.apply_sensor_data(rudder_in)
test.set_init_cond(190,4500,0.77)
x,y,z = test.return_sensor_data()
test.control_system(False)

# Run Simulations
yaw = test.simulate(james,rudder_in)
pd.DataFrame(yaw,yaw_real).to_excel('Data/output.xlsx',header=False,index=False)

test.control_system(True)
yaw = test.simulate(james,rudder_in)




    
