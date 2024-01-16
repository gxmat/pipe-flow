from math import log10

class flow:
    def __init__(self, fluid, pipe, mass_flowrate):
        self.fluid = fluid
        self.pipe = pipe
        self.mass_flowrate = mass_flowrate

    # Properties that change every iteration
    # Friction factor equation https://en.wikipedia.org/wiki/Darcy_friction_factor_formulae#Haaland_equation
    @property
    def properties(self):
        self.volumetric_flowrate = self.mass_flowrate / self.fluid.density # m3/s
        self.velocity = self.volumetric_flowrate / self.pipe.id_cs_area # m/s
        self.re_number = self.fluid.density * self.velocity * self.pipe.id / self.fluid.dynamic_viscosity
        self.f = (1 / (-1.8 * log10(((self.pipe.relative_roughness / 3.7) ** 1.11) + (6.9 / self.re_number)))) ** 2
        self.dP = (self.f * self.pipe.length * (self.fluid.density / 2) * ((self.velocity ** 2) / self.pipe.id)) # Pa
        return self

    # Gnielinkski correlation for Nusselt number https://en.wikipedia.org/wiki/Nusselt_number#Gnielinski_correlation
    @property
    def gnielinski(self):
        if ((self.re_number >= 3000 and self.re_number <= 5e6) and (self.fluid.pr_number >= 0.5 and self.fluid.pr_number <= 2000)):
            self.nu_number = ((self.f / 8) * (self.re_number - 1000) * self.fluid.pr_number) / (1 + 12.7 * ((self.f / 8) ** 0.5) * ((self.fluid.pr_number ** (2/3)) - 1))
            self.htc = self.nu_number * self.fluid.thermal_conductivity / self.pipe.id # W/m2.K
            return self
        else:
            print("Pipe and fluid parameters not valid for Gnielinski correlation")