# import matplotlib.pyplot as plt
import fluid_property as fp
import unit_converter as uc

fluid_name = "HeavyWater"
fluid_temperature = 200 # degrees C
fluid_pressure = 85 # bar

# Convert to SI units
fluid_temperature_si = uc.celsius_kelvin(fluid_temperature)
fluid_pressure_si = uc.bar_pascal(fluid_pressure)


# test

fluid_test = fp.fluid(fluid_name, fluid_temperature_si, fluid_pressure_si)
print(fluid_test.properties.density)
