from math import pi

# Class containing details of pipe section
class pipe:
    def __init__(self, od, thickness, length, roughness):
        self.od = od # m
        self.thickness = thickness # m
        self.length = length # m
        self.roughness = roughness # m
        self.id = self.od - (2 * self.thickness) # m
        self.id_wall_area = pi * self.id * self.length # m2
        self.id_cs_area = 0.25 * pi * (self.id ** 2) # m2
        self.relative_roughness = self.roughness / self.id
