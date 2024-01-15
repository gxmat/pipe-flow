import CoolProp.CoolProp as cp
import unit_converter as uc

# PropsSI uses SI Units https://en.wikipedia.org/wiki/International_System_of_Units 
# PropsSI available properties http://www.coolprop.org/coolprop/HighLevelAPI.html#table-of-string-inputs-to-propssi-function 

class fluid:
    def __init__(self, name, temperature, pressure):
        self.name = name
        self.temperature = temperature
        self.pressure = pressure

    # Only getter needed here since we don't directly set any properties
    @property
    def properties(self):
        self.density = cp.PropsSI('D','T',self.temperature,'P',self.pressure,self.name) # kg/m3
        self.dynamic_viscosity = cp.PropsSI('V','T',self.temperature,'P',self.pressure,self.name) # Pa.s
        self.specific_heat = cp.PropsSI('C','T',self.temperature,'P',self.pressure,self.name) # J/kg.K
        self.thermal_conductivity = cp.PropsSI('CONDUCTIVITY','T',self.temperature,'P',self.pressure,self.name) # W/m.K
        self.pr_number = cp.PropsSI('PRANDTL','T',self.temperature,'P',self.pressure,self.name)
        self.phase = cp.PhaseSI('T',self.temperature,'P',self.pressure,self.name)
        self.temperature_saturation = cp.PropsSI('T','P',self.pressure,'Q',0,self.name) # K

        return self