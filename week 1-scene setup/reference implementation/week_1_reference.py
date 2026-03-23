import math
import turtle
import time

class Vector3:
    
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

class Polygon:
    
    def __init__(self,scene, points, color = (255,0,0)):
        self.points = points
        self.color = color
        self.scene = scene
        
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
        self.polygons = []
        
    def add_polygon(self, polygon):
        self.polygons.append(polygon)
        
    def update(self):
        self.turtle.clear()
        for i in self.polygons:
            i.draw()
        
canvas = Scene()
a = Vector3(0,57,0)
b = Vector3(-50,-28,-0)
c = Vector3(50,-28,0)
triangle = Polygon(canvas,[a,b,c])
canvas.add_polygon(triangle)
canvas.update()
turtle.mainloop()
