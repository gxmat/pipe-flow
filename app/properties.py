import CoolProp.CoolProp as cp
import unit_converter as uc

# Units in SI - Pascal, bar

temperature = 100
pressure = 1

temperature_conv = uc.celsius_kelvin(temperature)
pressure_conv = uc.bar_pascal(pressure)

# PropsSI uses SI Units https://en.wikipedia.org/wiki/International_System_of_Units 
# PropsSI available properties http://www.coolprop.org/coolprop/HighLevelAPI.html#table-of-string-inputs-to-propssi-function 

def properties



a = 1