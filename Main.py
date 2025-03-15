import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TEST")
pygame.mouse.set_visible(False)  # Fareyi gizle
pygame.event.set_grab(True)  # Fareyi pencere içinde tut

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
SKYBLUE = (0, 216, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

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

obj_file = "Model.obj"
Vertex, Edge = load_obj(obj_file)

OZ = 0
camera_x, camera_y, camera_z = 0, 0, -5
camera_rotation_x, camera_rotation_y = 0, 0
fov = 60
speed = 5
sensitivity = 0.002

running = True

def convert(Horizontal, Vertical, F):
    cz = (Horizontal - camera_x) * math.sin(camera_rotation_x) + (F - camera_z + OZ) * math.cos(camera_rotation_x)
    cx = (Horizontal - camera_x) * math.cos(camera_rotation_x) - (F - camera_z + OZ) * math.sin(camera_rotation_x)
    cy = (cz) * math.sin(camera_rotation_y) + (Vertical - camera_y) * math.cos(camera_rotation_y)
    cz = (cz) * math.cos(camera_rotation_y) - (Vertical - camera_y) * math.sin(camera_rotation_y)
    
    if cz > 0:
        return ((180 / math.tan(math.radians(fov / 2))) * (cx) / (cz) + WIDTH // 2,
                (180 / math.tan(math.radians(fov / 2))) * (-cy) / (cz) + HEIGHT // 2)
    else:
        return (WIDTH // 2, HEIGHT // 2)

while running:
    dt = pygame.time.Clock().tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            dx, dy = event.rel  # Fare hareketini al
            camera_rotation_x += dx * sensitivity
            camera_rotation_y += dy * sensitivity  # Ters yönde hareket etmesi için
            camera_rotation_y = max(-math.pi / 2, min(math.pi / 2, camera_rotation_y))  # Yukarı-aşağı sınırla

    # Her çerçevede fareyi ekranın ortasına koy
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
    if keys[pygame.K_SPACE]:
        camera_y += dt * speed
    if keys[pygame.K_LCTRL]:
        camera_y -= dt * speed

    screen.fill(SKYBLUE)
    for edge in Edge:
        a = convert(Vertex[edge[0]][0], Vertex[edge[0]][1], Vertex[edge[0]][2])
        b = convert(Vertex[edge[1]][0], Vertex[edge[1]][1], Vertex[edge[1]][2])
        pygame.draw.line(screen, RED, a, b, 1)

    pygame.display.flip()

pygame.quit()
