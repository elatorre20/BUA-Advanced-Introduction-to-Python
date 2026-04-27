import turtle
import math
import time
import random

class Vector3:
    
    def __init__(self, x=0,y=0,z=0):
        self.x = x
        self.y = y
        self.z = z
        
    def add(self, b):
        return Vector3(self.x + b.x, self.y + b.y, self.z + b.z)
    
    def __add__(self, b):
        return self.add(b)
    
    def sub(self, b):
        return Vector3(self.x - b.x, self.y - b.y, self.z - b.z)
    
    def __sub__(self, b):
        return self.sub(b)
    
    def mul(self, s):
        return Vector3(self.x * s, self.y * s, self.z * s)
    
    def __mul__(self, s):
        return self.mul(s)
    
    def cross_product(self, b):
        c0 = (self.y * b.z) - (self.z * b.y)
        c1 = (self.z * b.x) - (self.x * b.z)
        c2 = (self.x * b.y) - (self.y * b.x)
        return Vector3(c0, c1, c2)
    
    def dot_product(self, b):
        return (self.x * b.x) + (self.y * b.y) + (self.z * b.z)
    
    def get_magnitude(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def get_normalized(self):
        magnitude = self.get_magnitude()
        if magnitude == 0:
            return Vector3(0, 0, 0)
        return Vector3(self.x / magnitude, self.y / magnitude, self.z / magnitude)
    
    
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
        for i in range(len(self.vertices)):
            self.vertices[i] = self.vertices[i] + a
            
    def scale(self, a):
        for i in range(len(self.vertices)):
            self.vertices[i] = Vector3(self.vertices[i].x * a.x, self.vertices[i].y * a.y, self.vertices[i].z * a.z)
            
    def mirror(self, a):
        for i in range(len(self.vertices)):
            b = Vector3(self.vertices[i].x, self.vertices[i].y, self.vertices[i].z)
            if(a.x != 0):
                b.x = self.vertices[i].x *  -1
            if(a.y != 0):
                b.y = self.vertices[i].y * -1
            if(a.z != 0):
                b.z = self.vertices[i].z * -1
            self.vertices[i] = b
            
    def rotate(self, theta, axis):
        for i in range(len(self.vertices)):
            if(axis == 'x'):
                self.vertices[i] = Vector3(self.vertices[i].x, (self.vertices[i].y*math.cos(theta))-(self.vertices[i].z*math.sin(theta)), (self.vertices[i].y*math.sin(theta))+(self.vertices[i].z*math.cos(theta)))
            elif(axis == 'y'):
                self.vertices[i] = Vector3((self.vertices[i].x*math.cos(theta)) + (self.vertices[i].z*math.sin(theta)), self.vertices[i].y, -(self.vertices[i].x*math.sin(theta))+(self.vertices[i].z*math.cos(theta)))
            elif(axis == 'z'):
                self.vertices[i] = Vector3((self.vertices[i].x*math.cos(theta))-(self.vertices[i].y*math.sin(theta)), (self.vertices[i].x*math.sin(theta))+(self.vertices[i].y*math.cos(theta)), self.vertices[i].z)
    
    def get_zmin(self):
        zmin = self.vertices[0].z
        for i in self.vertices:
            if(i.z < zmin):
                zmin = i.z
        return(zmin)
    
    def get_normal(self):
        a = self.vertices[1] - self.vertices[0]
        b = self.vertices[2] - self.vertices[0]
        return a.cross_product(b).get_normalized()

class Mesh:
    def __init__(self, turtle, polygons=[], offset=Vector3()):
        self.turtle = turtle
        self.polygons = polygons
        self.offset = Vector3()
        self.translate(offset)
    
    def add_polygon(self, polygon):
        self.polygons.append(polygon)
        
    def translate(self, a):
        self.offset = self.offset + a
        for i in self.polygons:
            i.translate(a)
        
    def rotate(self, theta, axis):
        # shift to origin
        for i in self.polygons:
            i.translate(Vector3(-self.offset.x, -self.offset.y, -self.offset.z))
        # rotate
        for i in self.polygons:
            i.rotate(theta, axis)
        # shift back
        for i in self.polygons:
            i.translate(self.offset)
                
    def scale(self, a):
        # shift to origin
        for i in self.polygons:
            i.translate(Vector3(-self.offset.x, -self.offset.y, -self.offset.z))
        #scale
        for i in self.polygons:
            i.scale(a)
        # shift back
        for i in self.polygons:
            i.translate(self.offset)
        
    def mirror(self, a):
        # shift to origin
        for i in self.polygons:
            i.translate(Vector3(-self.offset.x, -self.offset.y, -self.offset.z))
        #mirror
        for i in self.polygons:
            i.mirror(a)
        # shift back
        for i in self.polygons:
            i.translate(self.offset)
        
    
    def draw(self, ambient, directional):
        self.polygons = sorted(self.polygons, key = lambda l: l.get_zmin())
        for i in self.polygons:
            normal = i.get_normal()
            base = i.color
            diffuse = max(0, directional.dot_product(normal))
            light = ambient + diffuse
            light = min(light, 1)
            color = (int(base[0] * light),int(base[1] * light),int(base[2] * light))
            self.turtle.color(color[0], color[1], color[2])
            #draw the face
            self.turtle.penup()
            self.turtle.goto(i.vertices[0].x,i.vertices[0].y)
            self.turtle.pendown()
            self.turtle.begin_fill()
            for j in i.vertices:
                self.turtle.goto(j.x,j.y)
            self.turtle.goto(i.vertices[0].x,i.vertices[0].y)
            self.turtle.end_fill()
            self.turtle.penup()
            
    def add_polygon(self, side = 50, sides = 4, color = (255,0,0), offset= Vector3(), rot_init = Vector3()):
        self.polygons.append(make_polygon(self.turtle, side, sides, color))
        self.polygons[-1].rotate(rot_init.x, 'x')
        self.polygons[-1].rotate(rot_init.y, 'y')
        self.polygons[-1].rotate(rot_init.z, 'z')
        self.polygons[-1].translate(offset)

class Scene:
    
    def __init__(self, ambient = 0.05, directional = Vector3(0,0,-1)):
        self.screen = turtle.Screen()
        self.screen.colormode(255)
        self.turtle = turtle.Turtle()
        self.turtle.hideturtle()
        self.turtle.speed(0)
        turtle.tracer(0)
        self.ambient = ambient
        self.directional = directional.get_normalized()
        self.meshes = []
        
    def update(self):
        self.turtle.clear()
        for i in self.meshes:
            i.draw(self.ambient, self.directional)
        turtle.update()
        
    def add_cube(self, dim=50, offset=Vector3()):
        self.meshes.append(make_cube(self.turtle, dim))
        self.meshes[-1].translate(offset)

def make_triangle(turtle, side = 50, color = (255,0,0)):
    height = math.sqrt(3)*side/2
    v0 = Vector3(0,height*2/3,0)
    v1 = Vector3(-side/2,-height/3,0)
    v2 = Vector3(side/2, -height/3,0)
    return Polygon([v0,v1,v2], color, turtle)
    
def make_polygon(turtle, side = 50, sides = 4, color = (255,0,0)):
    vertices = []
    vertices.append(Vector3(0,0,0))
    internal_angle = (2*math.pi)/sides
    angle = 0
    for i in range(sides-1):
        next_side = Vector3(math.cos(angle)*side, math.sin(angle)*side, 0)
        vertices.append(next_side + vertices[-1])
        angle = angle + internal_angle
        
    center = Vector3(0, 0, 0)
    for v in vertices:
        center = center + v
    center = center * (1 / len(vertices))

    for i in range(len(vertices)):
        vertices[i] = vertices[i] - center
        
    return Polygon(vertices, color, turtle)

def make_cube(turtle, side, colors=[
        (255, 0, 0),
        (0, 0, 255),
        (0, 255, 0),
        (0, 255, 255),
        (255, 255, 0),
        (255, 0, 255)
    ]):
    h = side / 2
    faces = [
        Polygon([
            Vector3(-h, -h, -h),
            Vector3(h, -h, -h),
            Vector3(h, h, -h),
            Vector3(-h, h, -h)
        ], colors[0], turtle),
        Polygon([
            Vector3(-h, -h, h),
            Vector3(-h, h, h),
            Vector3(h, h, h),
            Vector3(h, -h, h)
        ], colors[1], turtle),
        Polygon([
            Vector3(-h, -h, -h),
            Vector3(-h, -h, h),
            Vector3(h, -h, h),
            Vector3(h, -h, -h)
        ], colors[2], turtle),
        Polygon([
            Vector3(-h, h, -h),
            Vector3(h, h, -h),
            Vector3(h, h, h),
            Vector3(-h, h, h)
        ], colors[3], turtle),
        Polygon([
            Vector3(h, -h, -h),
            Vector3(h, -h, h),
            Vector3(h, h, h),
            Vector3(h, h, -h)
        ], colors[4], turtle),
        Polygon([
            Vector3(-h, -h, -h),
            Vector3(-h, h, -h),
            Vector3(-h, h, h),
            Vector3(-h, -h, h)
        ], colors[5], turtle)
    ]

    return Mesh(turtle, faces)

scene1 = Scene()
scene1.screen.bgcolor(128,128,128)
die = make_cube(scene1.turtle, 200,[(255,255,255),(255,255,255),(255,255,255),(255,255,255),(255,255,255),(255,255,255)])
#one face
die.add_polygon(5,30,(0,0,0),Vector3(0,0,101))
#two face
die.add_polygon(5,30,(0,0,0),Vector3(50,50,-101))
die.add_polygon(5,30,(0,0,0),Vector3(-50,-50,-101))
#three face
die.add_polygon(5,30,(0,0,0),Vector3(50,101,50),Vector3(math.pi/2,0,0))
die.add_polygon(5,30,(0,0,0),Vector3(0,101,0),Vector3(math.pi/2,0,0))
die.add_polygon(5,30,(0,0,0),Vector3(-50,101,-50),Vector3(math.pi/2,0,0))
#four face
die.add_polygon(5,30,(0,0,0),Vector3(50,-101,50),Vector3(math.pi/2,0,0))
die.add_polygon(5,30,(0,0,0),Vector3(-50,-101,50),Vector3(math.pi/2,0,0))
die.add_polygon(5,30,(0,0,0),Vector3(-50,-101,-50),Vector3(math.pi/2,0,0))
die.add_polygon(5,30,(0,0,0),Vector3(50,-101,-50),Vector3(math.pi/2,0,0))
#five face
die.add_polygon(5,30,(0,0,0),Vector3(101,50,50),Vector3(0,math.pi/2,0))
die.add_polygon(5,30,(0,0,0),Vector3(101,50,-50),Vector3(0,math.pi/2,0))
die.add_polygon(5,30,(0,0,0),Vector3(101,0,0),Vector3(0,math.pi/2,0))
die.add_polygon(5,30,(0,0,0),Vector3(101,-50,-50),Vector3(0,math.pi/2,0))
die.add_polygon(5,30,(0,0,0),Vector3(101,-50,50),Vector3(0,math.pi/2,0))
#six face
die.add_polygon(5,30,(0,0,0),Vector3(-101,-50,50),Vector3(0,math.pi/2,0))
die.add_polygon(5,30,(0,0,0),Vector3(-101,0,50),Vector3(0,math.pi/2,0))
die.add_polygon(5,30,(0,0,0),Vector3(-101,50,50),Vector3(0,math.pi/2,0))
die.add_polygon(5,30,(0,0,0),Vector3(-101,-50,-50),Vector3(0,math.pi/2,0))
die.add_polygon(5,30,(0,0,0),Vector3(-101,0,-50),Vector3(0,math.pi/2,0))
die.add_polygon(5,30,(0,0,0),Vector3(-101,50,-50),Vector3(0,math.pi/2,0))

shadow = Mesh(scene1.turtle)
shadow.add_polygon(25,30,(0,0,0),Vector3(),Vector3(math.pi/4,0,0))

scene1.meshes.append(shadow)
scene1.meshes.append(die)
die.rotate(math.pi/4,"x")
die.rotate(math.pi/5,"z")
die.translate(Vector3(-500,300,0))
shadow.translate(Vector3(-500,-250,0))
xvelocity = 6
yvelocity = -20
while(True):
    #move and rotate die
    die.translate(Vector3(xvelocity,yvelocity,0))
    rotation = random.uniform(0,-math.pi/32)
    die.rotate(math.pi/32,"x")
    rotation = random.uniform(0,-math.pi/32)
    die.rotate(math.pi/32,"y")
    rotation = random.uniform(0,-math.pi/32)
    die.rotate(math.pi/32,"z")
    #move and scale shadow
    shadow.translate(Vector3(xvelocity,0,0))
    if(yvelocity < 0):
        shadow.scale(Vector3(1.0525,1.0525,1.0525))
    else:
        shadow.scale(Vector3(0.9,0.9,0.9))
    scene1.update()
    #update velocity
    if(yvelocity < 0):
        yvelocity = yvelocity * 1.5
    else:
        yvelocity = yvelocity * 0.4
        if(yvelocity < 1):
            yvelocity = -1
    if(die.offset.y < -50):
        yvelocity = yvelocity * -1
    #move back to start if out of frame
    if(die.offset.x > 500):
        shadow.translate(Vector3(die.offset.x * -2,0,0))
        die.translate(Vector3(die.offset.x * -2,300-die.offset.y,0))
        yvelocity = -20
    #delay till next frame
    time.sleep(0.02)
    
    
