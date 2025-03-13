import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TEST")

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
#model details
Vertex=[[-1,-1,-1],
         [-1,-1,1],
         [-1,1,-1],
         [-1,1,1],
         [1,-1,-1],
         [1,-1,1],
         [1,1,-1],
         [1,1,1],
         [-1,-1,-1]]

Edge=[[Vertex[0],Vertex[1]],
         [Vertex[1],Vertex[2]],
         [Vertex[2],Vertex[3]],
         [Vertex[3],Vertex[4]],
         [Vertex[0],Vertex[1]],
         [Vertex[0],Vertex[1]],
         [Vertex[0],Vertex[1]],
         [Vertex[0],Vertex[1]]]
#camera properties
camera_x, camera_y, camera_z = 0, 0, -5
camera_rotation_x, camera_rotation_y, camera_rotation_z = 0, 0, 0
fov=1
speed = 5

running = True
#Perspective illusion
def convert(Horizontal,Vertical,F):
    cz=(Horizontal-camera_x)*math.sin(camera_rotation_x)+(F-camera_z)*math.cos(camera_rotation_x)
    cx=(Horizontal-camera_x)*math.cos(camera_rotation_x)-(F-camera_z)*math.sin(camera_rotation_x)
    cy=(cz)*math.sin(camera_rotation_y)+(Vertical-camera_y)*math.cos(camera_rotation_y)
    cz=(cz)*math.cos(camera_rotation_y)-(Vertical-camera_y)*math.sin(camera_rotation_y)
    return (180-fov)*(cx)/(cz)+WIDTH//2,(180-fov)*(cy)/(cz)+HEIGHT//2
while running:
    dt = pygame.time.Clock().tick(60) / 1000
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        camera_z += dt*speed*math.cos(camera_rotation_x)
        camera_x += dt*speed*math.sin(camera_rotation_x)
    if keys[pygame.K_s]:
        camera_z -= dt*speed*math.cos(camera_rotation_x)
        camera_x -= dt*speed*math.sin(camera_rotation_x)
    if keys[pygame.K_d]:
        camera_z += dt*speed*math.cos(camera_rotation_x+math.pi/2)
        camera_x += dt*speed*math.sin(camera_rotation_x+math.pi/2)
    if keys[pygame.K_a]:
        camera_z -= dt*speed*math.cos(camera_rotation_x+math.pi/2)
        camera_x -= dt*speed*math.sin(camera_rotation_x+math.pi/2)
    if keys[pygame.K_SPACE]:
        camera_y += dt*speed
    if keys[pygame.K_LCTRL]:
        camera_y -= dt*speed
    if keys[pygame.K_RIGHT]:
        camera_rotation_x += dt*speed
    if keys[pygame.K_LEFT]:
        camera_rotation_x -= dt*speed
    if keys[pygame.K_UP]:
        camera_rotation_y += dt*speed
    if keys[pygame.K_DOWN]:
        camera_rotation_y -= dt*speed
    screen.fill(BLACK)
    #render model
    for i in range(0,len(Vertex)-1):
        a=convert(Vertex[i][0],Vertex[i][1],Vertex[i][2])
        b=convert(Vertex[i+1][0],Vertex[i+1][1],Vertex[i+1][2])
        pygame.draw.line(screen, BLUE, a,b, 1)
    pygame.display.flip()

pygame.quit()