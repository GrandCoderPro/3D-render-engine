import pygame
import math

pygame.init()
#i am 15 years old and i made a 3d renderer from scratch(i used pygame only) the next step is to make it with only assembly
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TEST")
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
SKYBLUE = (160, 216, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
TEN = (255,210,122)
pygame.mixer.music.load("dosya.mp3")
pygame.mixer.music.play(-1)
def load_obj(filepath):
    Vertex = []
    Edge = set()

    with open(filepath, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if not parts:
                continue

            if parts[0] == 'v':
                vertex = list(map(float, parts[1:4]))
                Vertex.append(vertex)

            elif parts[0] == 'f':
                face_indices = [int(p.split('/')[0]) - 1 for p in parts[1:]]
                for i in range(len(face_indices)):
                    edge = (face_indices[i], face_indices[(i + 1) % len(face_indices)])
                    Edge.add(tuple(sorted(edge)))

    return Vertex, list(Edge)

obj_file = "TREN.obj"
Vertex, Edge = load_obj(obj_file)

OZ = 0
camera_x, camera_y, camera_z = 0, 0, -5
camera_rotation_x, camera_rotation_y = 0, 0
velocity_y=0
fov = 60
speed = 15
sensitivity = 0.002

running = True

def convert(Horizontal, Vertical, F):
    cz = (Horizontal - camera_x) * math.sin(camera_rotation_x) + (F - camera_z + OZ) * math.cos(camera_rotation_x)
    cx = (Horizontal - camera_x) * math.cos(camera_rotation_x) - (F - camera_z + OZ) * math.sin(camera_rotation_x)
    cy = (cz) * math.sin(camera_rotation_y) + (Vertical - camera_y) * math.cos(camera_rotation_y)
    cz = (cz) * math.cos(camera_rotation_y) - (Vertical - camera_y) * math.sin(camera_rotation_y)
    
    if cz > 0:
        return ((540 / math.tan(math.radians(fov / 2))) * (cx) / (cz) + WIDTH // 2,
                (540 / math.tan(math.radians(fov / 2))) * (-cy) / (cz) + HEIGHT // 2)
    else:
        return (WIDTH // 2, HEIGHT // 2)

while running:
    dt = pygame.time.Clock().tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            dx, dy = event.rel
            camera_rotation_x += dx * sensitivity
            camera_rotation_y += dy * sensitivity
            camera_rotation_y = max(-math.pi / 2, min(math.pi / 2, camera_rotation_y))

    pygame.mouse.set_pos(WIDTH // 2, HEIGHT // 2)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        camera_z += dt * speed * math.cos(camera_rotation_x)
        camera_x += dt * speed * math.sin(camera_rotation_x)
    if keys[pygame.K_s]:
        camera_z -= dt * speed * math.cos(camera_rotation_x)
        camera_x -= dt * speed * math.sin(camera_rotation_x)
    if keys[pygame.K_d]:
        camera_z += dt * speed * math.cos(camera_rotation_x + math.pi / 2)
        camera_x += dt * speed * math.sin(camera_rotation_x + math.pi / 2)
    if keys[pygame.K_a]:
        camera_z -= dt * speed * math.cos(camera_rotation_x + math.pi / 2)
        camera_x -= dt * speed * math.sin(camera_rotation_x + math.pi / 2)
    if keys[pygame.K_UP]:
        fov+=1
    if keys[pygame.K_DOWN]:
        fov-=1
    if keys[pygame.K_SPACE] and on_ground:
        velocity_y = 5
        on_ground = False
    if keys[pygame.K_LCTRL]:
        OZ+=4*dt
    
    velocity_y -= 9.8 * dt
    camera_y += velocity_y * dt
    if camera_y <= 0:
        camera_y = 0
        velocity_y = 0
        on_ground = True
    

    screen.fill(SKYBLUE)
    for edge in Edge:
        a = convert(Vertex[edge[0]][0], Vertex[edge[0]][1], Vertex[edge[0]][2])
        b = convert(Vertex[edge[1]][0], Vertex[edge[1]][1], Vertex[edge[1]][2])
        pygame.draw.line(screen, (0,0,0), a, b, 1)

    pygame.display.flip()

pygame.quit()
