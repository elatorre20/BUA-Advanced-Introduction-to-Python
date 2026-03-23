import math
import turtle
import time

class Vector3:
    
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
        
    def add(self, b):
        return Vector3(self.x + b.x, self.y + b.y, self.z + b.z)
    
    def __add__(self, b):
        return self.add(b)
    
    def subtract(self, b):
        return Vector3(self.x - b.x, self.y - b.y, self.z - b.z)
    
    def __sub__(self, b):
        return self.subtract(b)
    
    def mul(self, s):
        return Vector3(self.x * s, self.y * s, self.z * s)
    
    def __mul__(self, s):
        return self.mul(s)

class Polygon:
    
    def __init__(self,scene, points, color = (255,0,0)):
        self.points = points
        self.color = color
        self.scene = scene
        
    def translate(self, a):
        for i in range(len(self.points)):
            self.points[i] = self.points[i] + a
        
    def scale(self, a):
        for i in range(len(self.points)):
            self.points[i] = Vector3(self.points[i].x * a.x, self.points[i].y * a.y, self.points[i].z * a.z)
        
    def mirror(self, a):
        for i in range(len(self.points)):
            b = Vector3(self.points[i].x, self.points[i].y, self.points[i].z)
            if(a.x != 0):
                b.x = self.points[i].x * -1
            if(a.y != 0):
                b.y = self.points[i].y * -1
            if(a.z != 0):
                b.z = self.points[i].z * -1
            self.points[i] = b
            
    def shear(self, phi, axis):
        for i in self.points:
            if(axis == 'x'): #horizontal shear
                i.x = i.x + phi*i.y
            elif(axis == 'y'): #vertical shear
                i.y = i.y + phi*i.x
        
    def draw(self):
        self.scene.turtle.goto(self.points[0].x, self.points[0].y)
        self.scene.turtle.color(self.color[0], self.color[1], self.color[2])
        self.scene.turtle.penup()
        self.scene.turtle.goto(self.points[0].x, self.points[0].y)
        self.scene.turtle.pendown()
        self.scene.turtle.begin_fill()
        for i in self.points:
            self.scene.turtle.goto(i.x, i.y)
        self.scene.turtle.goto(self.points[0].x, self.points[0].y)
        self.scene.turtle.end_fill()
        self.scene.turtle.penup()
        

class Scene:
    
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.colormode(255)
        self.turtle = turtle.Turtle()
        self.turtle.hideturtle()
        self.turtle.penup()
        self.turtle.speed(0)
        turtle.tracer(0)
        self.polygons = []
        
    def add_polygon(self, polygon):
        self.polygons.append(polygon)
        
    def update(self):
        self.turtle.clear()
        for i in self.polygons:
            i.draw()
        turtle.update()
        
canvas = Scene()
a = Vector3(0,57,0)
b = Vector3(-50,-28,-0)
c = Vector3(50,-28,0)
triangle = Polygon(canvas,[a,b,c])
direction = 0
position = Vector3(50,50,0)
triangle.translate(position)
canvas.add_polygon(triangle)
canvas.update()
while(True):
    if(direction == 0):
        step = Vector3(0,-1,0)
        triangle.translate(step)
        position = position + step
        if(position.y == -50):
            direction = 1
    elif(direction == 1):
        step = Vector3(-1,0,0)
        triangle.translate(step)
        position = position + step
        if(position.x == -50):
            direction = 2
    if(direction == 2):
        step = Vector3(0,1,0)
        triangle.translate(step)
        position = position + step
        if(position.y == 50):
            direction = 3
    if(direction == 3):
        step = Vector3(1,0,0)
        triangle.translate(step)
        position = position + step
        if(position.x == 50):
            direction = 0
    canvas.update()
    time.sleep(0.03)
    
