import turtle

class Vector3:
    
    def __init__(self, x=0,y=0,z=0):
        self.x = x
        self.y = y
        self.z = z
        
    def add(self, b):
        self.x = self.x + b.x
        self.y = self.y + b.y
        self.z = self.z + b.z
        
    def sub(self, b):
        self.x = self.x - b.x
        self.y = self.y - b.y
        self.z = self.z - b.z
        
    def mul(self, s):
        self.x = self.x * s
        self.y = self.y * s
        self.z = self.z * s
    
    
# class Polygon:



    
    
