import CoolProp.CoolProp as cp
import matplotlib.pyplot as plt
import pandas as pd
from math import pi, log10, sin, radians, floor

# Unit converters
celsius_kelvin = 273.15
pascal_bar = 1e5
mega = 1e6

# PropsSI uses SI Units https://en.wikipedia.org/wiki/International_System_of_Units 
# PropsSI available properties http://www.coolprop.org/coolprop/HighLevelAPI.html#table-of-string-inputs-to-propssi-function 

class fluid:
    def __init__(self, name, temperature, pressure):
        self.name = name
        self.temperature = temperature
        self.pressure = pressure

    @property
    def properties(self):
        temperature_si = self.temperature + celsius_kelvin
        pressure_si = self.pressure * pascal_bar
        
        self.density = cp.PropsSI('D','T',temperature_si,'P',pressure_si,self.name) # kg/m3
        self.dynamic_viscosity = cp.PropsSI('V','T',temperature_si,'P',pressure_si,self.name) # Pa.s
        self.specific_heat = cp.PropsSI('C','T',temperature_si,'P',pressure_si,self.name) # J/kg.K
        self.thermal_conductivity = cp.PropsSI('CONDUCTIVITY','T',temperature_si,'P',pressure_si,self.name) # W/m.K
        self.pr_number = cp.PropsSI('PRANDTL','T',temperature_si,'P',pressure_si,self.name)
        self.phase = cp.PhaseSI('T',temperature_si,'P',pressure_si,self.name)
        self.temperature_saturation = cp.PropsSI('T','P',pressure_si,'Q',0,self.name) - celsius_kelvin # C

        return self


# Calculate all pipe parameters
# Friction factor equation https://en.wikipedia.org/wiki/Darcy_friction_factor_formulae#Haaland_equation
# Gnielinkski correlation for Nusselt number https://en.wikipedia.org/wiki/Nusselt_number#Gnielinski_correlation

class pipe:
    def __init__(self, od, thickness, roughness, length, fluid, mass_flowrate):
        self.od = od # m
        self.thickness = thickness # m
        self.length = length # m
        self.roughness = roughness # m
        self.fluid = fluid
        self.fluid.properties # Initialise fluid properties
        self.mass_flowrate = mass_flowrate # kg/s
        self.heatflux = 0 # W/m2
        self.heatflux_flomaster = 0 # W/m2
        self.power = 0 # W

    @property
    def static_properties(self):
        self.id = self.od - (2 * self.thickness) # m
        self.id_wall_area = pi * self.id * self.length # m2
        self.id_cs_area = 0.25 * pi * (self.id ** 2) # m2
        self.relative_roughness = self.roughness / self.id

        return self

    # Properties that change every iteration
    @property
    def dynamic_properties(self):
        self.volumetric_flowrate = self.mass_flowrate / self.fluid.density # m3/s
        self.velocity = self.volumetric_flowrate / self.id_cs_area # m/s
        self.re_number = self.fluid.density * self.velocity * self.id / self.fluid.dynamic_viscosity
        self.f = (1 / (-1.8 * log10(((self.relative_roughness / 3.7) ** 1.11) + (6.9 / self.re_number)))) ** 2
        self.dP = (self.f * self.length * (self.fluid.density / 2) * ((self.velocity ** 2) / self.id)) / pascal_bar # bar

        return self

    @property
    def gnielinski(self):
        if ((self.re_number >= 3000 and self.re_number <= 5e6) and (self.fluid.pr_number >= 0.5 and self.fluid.pr_number <= 2000)):
            self.nu_number = ((self.f / 8) * (self.re_number - 1000) * self.fluid.pr_number) / (1 + 12.7 * ((self.f / 8) ** 0.5) * ((self.fluid.pr_number ** (2/3)) - 1))
            self.htc = self.nu_number * self.fluid.thermal_conductivity / self.id # W/m2.K

            return self

        else:
            print("Pipe and fluid parameters not valid for Gnielinski correlation")