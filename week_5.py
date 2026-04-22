import turtle
import math
import time

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
        return self.subtract(b)
    
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
        for i in self.vertices:
            i.add(a)
            
    def scale(self, a):
        for i in self.vertices:
            i.mul(a)
            
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
        point0 = self.vertices[0]
        point1 = self.vertices[1]
        point2 = self.vertices[2]
        a = point1.sub(point0)
        b = point2.sub(point0)
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
        self.offset.add(a)
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
        for i in self.polygons:
            i.scale(a)
        
    def mirror(self, a):
        for i in self.polygons:
            i.mirror(a)
    
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

def make_triangle(turtle, side = 50, color = "red"):
    height = math.sqrt(3)*side/2
    v0 = Vector3(0,height*2/3,0)
    v1 = Vector3(-side/2,-height/3,0)
    v2 = Vector3(side/2, -height/3,0)
    return Polygon([v0,v1,v2], color, turtle)

def make_cube(turtle, side, colors=[
        (255, 0, 0),      # red
        (0, 0, 255),      # blue
        (0, 255, 0),      # green
        (0, 255, 255),    # cyan
        (255, 255, 0),    # yellow
        (255, 0, 255)     # magenta
    ]):
    h = side / 2
    v = [
        Vector3(-h, -h, -h),  # 0
        Vector3(h, -h, -h),   # 1
        Vector3(h, h, -h),    # 2
        Vector3(-h, h, -h),   # 3
        Vector3(-h, -h, h),   # 4
        Vector3(h, -h, h),    # 5
        Vector3(h, h, h),     # 6
        Vector3(-h, h, h)     # 7
    ]
    faces = [
        Polygon([v[0], v[1], v[2], v[3]], colors[0], turtle),    # back
        Polygon([v[4], v[7], v[6], v[5]], colors[1], turtle),   # front
        Polygon([v[0], v[4], v[5], v[1]], colors[2], turtle),  # bottom
        Polygon([v[3], v[2], v[6], v[7]], colors[3], turtle), # top
        Polygon([v[1], v[5], v[6], v[2]], colors[4], turtle), # right
        Polygon([v[0], v[3], v[7], v[4]], colors[5], turtle)  # left
    ]

    return Mesh(turtle, faces)

scene1 = Scene()
scene1.add_cube(200)
scene1.meshes[0].rotate(math.pi/4,"x")
scene1.meshes[0].rotate(math.pi/4,"z")
while(True):
    scene1.meshes[0].rotate(math.pi/64,"y")
    scene1.update()
    time.sleep(0.03)
    
    
