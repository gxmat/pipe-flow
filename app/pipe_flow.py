# import matplotlib.pyplot as plt
import pandas as pd
from math import pi
import fluid_properties as fp
import pipe_properties as pp
import flow_properties as flowp
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

heating_power = volheating * sector_vol_half
inlet_pipe_heatflux = heating_power / inlet_pipe.id_wall_area # W/m2, for one pipe

# Convert input coolant parameters to SI units
coolant_temperature_si = uc.celsius_kelvin(coolant_temperature)
coolant_pressure_si = uc.bar_pascal(coolant_pressure)

# Get initial coolant properties
coolant = fp.fluid(coolant_name, coolant_temperature_si, coolant_pressure_si)
# Coolant object to track properties as it travels through the loop
coolant_next = fp.fluid(coolant_name, coolant_temperature_si, coolant_pressure_si)

inlet_flowp = flowp.flow(coolant_next, inlet_pipe, coolant_mass_flowrate)

# Position of fluid along pipe length
cumulative_pipe_length = 0

# Results storage with initial values
results = {
    'Location': [0],
    'Total Length (m)': [cumulative_pipe_length],
    'Pressure (bar)': [coolant_pressure],
    'Temperature (C)': [coolant_temperature],
    'HTC (W/m2.K)': [0],
    'Input Pipe Power (W)': [0]
}

# Results appender
def append_results(height, total_length, pressure, temperature, htc, pipe_power):
    results['Location'].append(height)
    results['Total Length (m)'].append(total_length)
    results['Pressure (bar)'].append(pressure)
    results['Temperature (C)'].append(temperature)
    results['HTC (W/m2.K)'].append(htc)
    results['Input Pipe Power (W)'].append(pipe_power)

# Apply change in volumetric heating through height
volheating_vertdist = pd.read_excel(volheating_vertdist_file)
bottom = volheating_vertdist['Location'].min()
top = volheating_vertdist['Location'].max()
height_increment = int(structure_height * 100)

for h in range(bottom, (top + 1), height_increment):
    row = volheating_vertdist[volheating_vertdist['Location'] == h].index
    height_factor = volheating_vertdist.loc[row[0],"Outer Ratio"]

    coolant_next.temperature = ((height_factor * inlet_pipe_heatflux * inlet_pipe.id_wall_area) / (coolant_mass_flowrate * coolant_next.properties.specific_heat)) + coolant_next.temperature
    coolant_next.pressure -= inlet_flowp.properties.dP
    inlet_flowp.fluid = coolant_next
    inlet_pipe_power = height_factor * heating_power
    cumulative_pipe_length += inlet_pipe.length

    append_results(h, cumulative_pipe_length, uc.pascal_bar(coolant_next.pressure), uc.kelvin_celsius(coolant_next.temperature), inlet_flowp.gnielinski.htc, inlet_pipe_power)

# Table of results
results_df = pd.DataFrame(results)
results_df = results_df.set_index('Location')
print(results_df)