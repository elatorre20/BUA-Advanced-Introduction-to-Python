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
        return(self)
        
    def sub(self, b):
        self.x = self.x - b.x
        self.y = self.y - b.y
        self.z = self.z - b.z
        return(self)
        
    def mul(self, s):
        self.x = self.x * s
        self.y = self.y * s
        self.z = self.z * s
        return(self)
    
    
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
    
    def draw(self):
        self.polygons = sorted(self.polygons, key = lambda l: l.get_zmin())
        for i in self.polygons:
            self.turtle.color(i.color)
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
#             self.turtle.screen.update()


def make_triangle(turtle, side = 50, color = "red"):
    height = math.sqrt(3)*side/2
    v0 = Vector3(0,height*2/3,0)
    v1 = Vector3(-side/2,-height/3,0)
    v2 = Vector3(side/2, -height/3,0)
    return Polygon([v0,v1,v2], color, turtle)

def make_cube(turtle, side=50):
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
        Polygon([v[0], v[1], v[2], v[3]], "red", turtle),    # back
        Polygon([v[4], v[5], v[6], v[7]], "blue", turtle),   # front
        Polygon([v[0], v[1], v[5], v[4]], "green", turtle),  # bottom
        Polygon([v[2], v[3], v[7], v[6]], "yellow", turtle), # top
        Polygon([v[1], v[2], v[6], v[5]], "orange", turtle), # right
        Polygon([v[0], v[3], v[7], v[4]], "purple", turtle)  # left
    ]

    return Mesh(turtle, faces)

t = turtle.Turtle()
# turtle.tracer(0)
cube = make_cube(t, 100)
cube.translate(Vector3(100,0,0))
cube.rotate(math.pi/4,'y')
cube.rotate(math.pi/4,'x')
cube.draw()

cube1 = make_cube(t, 100)
cube1.translate(Vector3(-100,0,0))
cube1.rotate(-math.pi/4,'y')
cube1.rotate(-math.pi/4,'x')
cube1.draw()

turtle.done()
    
    
