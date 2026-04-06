import turtle
import math

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
    
    
class Polygon:
    
    def __init__(self, vertices, color, turtle):
        self.vertices = vertices
        self.color = color
        self.turtle = turtle
    
    def draw(self):
        self.turtle.color(self.color)
        self.turtle.begin_fill()
        self.turtle.penup()
        self.turtle.goto(self.vertices[0].x,self.vertices[0].y)
        self.turtle.pendown()
        for i in self.vertices:
            self.turtle.goto(i.x,i.y)
        self.turtle.goto(self.vertices[0].x,self.vertices[0].y)
        self.turtle.end_fill()
        
    def translate(self,a):
        for i in self.vertices:
            i.add(a)
            
    def scale(self, a):
        for i in self.vertices:
            i.mul(a)
            
    def rotate(self, theta, axis):
        for i in range(len(self.vertices)):
            if(axis == 'x'):
                self.vertices[i] = Vector3(self.vertices[i].x, (self.vertices[i].y*math.cos(theta))-(self.vertices[i].z*math.sin(theta)), (self.vertices[i].y*math.sin(theta))+(self.vertices[i].z*math.cos(theta)))
            elif(axis == 'y'):
                self.vertices[i] = Vector3((self.vertices[i].x*math.cos(theta)) + (self.vertices[i].z*math.sin(theta)), self.vertices[i].y, -(self.vertices[i].x*math.sin(theta))+(self.vertices[i].z*math.cos(theta)))
            elif(axis == 'z'):
                self.vertices[i] = Vector3((self.vertices[i].x*math.cos(theta))-(self.vertices[i].y*math.sin(theta)), (self.vertices[i].x*math.sin(theta))+(self.vertices[i].y*math.cos(theta)), self.vertices[i].z)



def make_triangle(turtle, side = 50, color = "red"):
    height = math.sqrt(3)*side/2
    v0 = Vector3(0,height*2/3,0)
    v1 = Vector3(-side/2,-height/3,0)
    v2 = Vector3(side/2, -height/3,0)
    return Polygon([v0,v1,v2], color, turtle)

t = turtle.Turtle()
triangle = make_triangle(turtle)
triangle.draw()
triangle.translate(Vector3(100,100,100))
triangle.rotate(math.pi/3, 'z')
triangle.draw()
turtle.mainloop()
    
    
