import numpy as np 

class Planet:
    def __init__(self, center_x, center_y, radius, name):
         self.x = center_x
         self.y = center_y
         self.radius = radius 
         self.name = name

    def __str__(self): 
        return f"{self.name} at ({self.x}, {self.y}) with radius {self.radius} km."