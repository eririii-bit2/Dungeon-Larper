import pygame
import math
pygame.init()

WIDTH = 800
HEIGHT = 600

# Color
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BG = (42, 42, 42)
WALL = (80, 80, 80)

# Player Color
P_COLOR_STOP = (0, 191, 0)
P_COLOR_MOVING = (100, 200, 100)

WALL_H = 150  # border thickness

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Dungeon Larper")

top_wall = pygame.Rect(0, 0, WIDTH, WALL_H)
bottom_wall = pygame.Rect(0, HEIGHT - WALL_H, WIDTH, WALL_H)

# interior walls for room 1
# just some rects i put in manually lol
room1_walls = [
    pygame.Rect(200, WALL_H, 30, 120),        # left wall chunk 1
    pygame.Rect(200, HEIGHT - WALL_H - 120, 30, 120),  # left wall chunk 2 (mirror)
    pygame.Rect(450, WALL_H, 500, 100),        # middle wall top
    pygame.Rect(450, HEIGHT - WALL_H - 100, 500, 100),  # middle wall bottom
    pygame.Rect(320, 230, 80, 30),            # horizontal blocker
    pygame.Rect(320, HEIGHT - 230 - 30, 80, 30),  # horizontal blocker bottom
]

# interior walls for room 2
# different layout so it feels different
room2_walls = [
    pygame.Rect(150, WALL_H, 30, 150),
    pygame.Rect(150, HEIGHT - WALL_H - 150, 30, 150),
    pygame.Rect(400, WALL_H + 50, 30, 130),
    pygame.Rect(400, HEIGHT - WALL_H - 180, 30, 130),
    pygame.Rect(560, 200, 100, 30),
    pygame.Rect(560, HEIGHT - 230, 100, 30),
]


def draw_slime(surface, P_color, x, y, radius, dx, dy):
    pygame.draw.circle(surface, P_color, (x, y), radius)
    pygame.draw.circle(surface, (134, 218, 134), (x, y), radius, 2)

    length = math.hypot(dx, dy)
    if length != 0:
        nx, ny = dx / length, dy / length
    else:
        nx, ny = 1, 0

    # Eye
    eye_x = int(x + nx * (radius // 3))
    eye_y = int(y + ny * (radius // 3))
    pygame.draw.circle(surface, (25, 25, 25), (eye_x, eye_y), radius // 4)

    # Pupil
    pupil_x = int(eye_x + nx * (radius // 8))
    pupil_y = int(eye_y + ny * (radius // 8))
    pygame.draw.circle(surface, (217, 217, 217), (pupil_x, pupil_y), radius // 12)


# push player out of a wall rect
# does x and y separately so you dont get stuck in corners
def resolve_wall(px, py, radius, wall):
    circle_rect = pygame.Rect(px - radius, py - radius, radius * 2, radius * 2)
    if not circle_rect.colliderect(wall):
        return px, py  # no collision, do nothing

    # figure out overlap on each axis
    overlap_left  = (px + radius) - wall.left
    overlap_right = wall.right - (px - radius)
    overlap_top   = (py + radius) - wall.top
    overlap_bottom = wall.bottom - (py - radius)

    # pick smallest overlap to push out
    min_x = min(overlap_left, overlap_right)
    min_y = min(overlap_top, overlap_bottom)

    if min_x < min_y:
        if overlap_left < overlap_right:
            px = wall.left - radius
        else:
            px = wall.right + radius
    else:
        if overlap_top < overlap_bottom:
            py = wall.top - radius
        else:
            py = wall.bottom + radius

    return px, py


RADIUS = 20
player_x = 60
player_y = 300
speed = 3
room = 1
dx, dy = 1, 0

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    new_dx, new_dy = 0, 0
    moving = False

    if keys[pygame.K_a]:
        player_x -= speed
        new_dx -= 1
        moving = True
    if keys[pygame.K_d]:
        player_x += speed
        new_dx += 1
        moving = True
    if keys[pygame.K_w]:
        player_y -= speed
        new_dy -= 1
        moving = True
    if keys[pygame.K_s]:
        player_y += speed
        new_dy += 1
        moving = True

    if new_dx != 0 or new_dy != 0:
        dx, dy = new_dx, new_dy

    P_color = P_COLOR_MOVING if moving else P_COLOR_STOP

    # Clamp within border walls
    player_x = max(RADIUS, min(WIDTH - RADIUS, player_x))
    player_y = max(WALL_H + RADIUS, min(HEIGHT - WALL_H - RADIUS, player_y))

    # collide with interior walls - just loop through all of them
    active_walls = room1_walls if room == 1 else room2_walls
    for w in active_walls:
        player_x, player_y = resolve_wall(player_x, player_y, RADIUS, w)

    player_circle = pygame.Rect(player_x - RADIUS, player_y - RADIUS, RADIUS * 2, RADIUS * 2)

    if room == 1:
        screen.fill(BG)
        pygame.draw.rect(screen, WALL, top_wall)
        pygame.draw.rect(screen, WALL, bottom_wall)

        # draw the interior walls
        for w in room1_walls:
            pygame.draw.rect(screen, WALL, w)

        goal_rect = pygame.Rect(750, 262, 30, 75)
        pygame.draw.rect(screen, GREEN, goal_rect)
        draw_slime(screen, P_color, player_x, player_y, RADIUS, dx, dy)

        if player_circle.colliderect(goal_rect):
            room = 2
            player_x, player_y = 60, 300

    elif room == 2:
        screen.fill((20, 20, 60))
        pygame.draw.rect(screen, WALL, top_wall)
        pygame.draw.rect(screen, WALL, bottom_wall)

        # draw the interior walls (room 2 version)
        for w in room2_walls:
            pygame.draw.rect(screen, WALL, w)

        goal_rect2 = pygame.Rect(750, 262, 30, 75)
        pygame.draw.rect(screen, YELLOW, goal_rect2)
        draw_slime(screen, P_color, player_x, player_y, RADIUS, dx, dy)

        if player_circle.colliderect(goal_rect2):
            room = 1
            player_x, player_y = 60, 300

    pygame.display.update()
    clock.tick(60)

pygame.quit()
