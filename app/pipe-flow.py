# import matplotlib.pyplot as plt
import pandas as pd
from math import pi
import fluid_properties as fp
import pipe_properties as pp
import unit_converter as uc

# Define structure
structure_id = 2.54 # Inner diameter
structure_thickness = 0.12 # Radial thickness
structure_sector = 6 # Toroidal degrees per structure
structure_height = 0.5

# Define volumetric heating on structure
volheating = 9.41e6 # W/m3
volheating_vertdist_file = "../data/vert_dist.xlsx"

# Define pipe
pipe_od = 0.0334 # DN25
pipe_thickness = 0.001651 # Sch 5
pipe_roughness = 45e-6

# Define coolant
coolant_name = "HeavyWater"
coolant_temperature = 200 # degrees C
coolant_pressure = 85 # bar
coolant_mass_flowrate = 6.8 # kg/s

# Get pipe properties
inlet_pipe = pp.pipe(pipe_od, pipe_thickness, structure_height, pipe_roughness)
outlet_pipe = pp.pipe(pipe_od, pipe_thickness, structure_height, pipe_roughness)

# Heat flux into pipe
# Each pipe is embedded in one toroidal half the structure
structure_od = structure_id + (2 * structure_thickness)
sector_area_half = 0.5 * 0.25 * pi * ((structure_od ** 2) - (structure_id ** 2)) * (structure_sector / 360)
sector_vol_half = sector_area_half * structure_height

inlet_pipe.heatflux = volheating * sector_vol_half / inlet_pipe.id_wall_area # W/m2, for one pipe
outlet_pipe.heatflux = volheating * sector_vol_half / outlet_pipe.id_wall_area # W/m2, for one pipe

# Convert input coolant parameters to SI units
coolant_temperature_si = uc.celsius_kelvin(coolant_temperature)
coolant_pressure_si = uc.bar_pascal(coolant_pressure)

# volheating_vertdist = pd.read_excel(volheating_vertdist_file)

outlet_pipe.heatflux