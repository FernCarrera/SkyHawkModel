from Classes.Vehicle import Vehicle
from Classes.Mission import Mission
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

# Import vehicle Data
hawk1 = pd.ExcelFile("Data/Skyhawk_Attributes.xlsx")
hawk2 = pd.ExcelFile("Data/Skyhawk_Attributes2.xlsx")

# Enter Rudder Data
rudder_in = pd.ExcelFile("Data/rudder_test.xlsx")

# Create Vehicles
james = Vehicle('James',hawk1)

# Create Mission
test = Mission("One")
test.apply_sensor_data(rudder_in)
test.set_init_cond(190,4500,0.77)


# Run Simulations
# No control System
test.control_system(False)
yaw = test.simulate(james,rudder_in)
# Write Data to excel
pd.DataFrame(yaw).to_excel('Data/output.xlsx',header=False,index=False)

# Control System active
test.control_system(True)
yaw = test.simulate(james,rudder_in)




    
