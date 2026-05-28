import pygame
import math
import time

pygame.init()

WIDTH  = 800
HEIGHT = 600

# ── Colors ────────────────────────────────────────────────────────────────────
GREEN       = (0,   255,  0)
YELLOW      = (255, 255,  0)
BG          = (42,   42,  42)
WALL        = (80,   80,  80)
VINE_GREEN  = (34,  139,  34)

LAVA_COLORS = [          # animated lava palette
    (207,  50,   0),
    (230,  80,   0),
    (255, 120,   0),
    (255,  60,   0),
]

# Player base colors
P_NORMAL_STOP   = (0,   191,   0)
P_NORMAL_MOVE   = (100, 200, 100)
P_VINE_STOP     = (34,  120,  34)
P_VINE_MOVE     = (60,  160,  60)
P_FIRE_STOP     = (255, 200,  30)   # sun yellow
P_FIRE_MOVE     = (255, 230,  80)

WALL_H = 150

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock  = pygame.time.Clock()
pygame.display.set_caption("Dungeon Larper")
font       = pygame.font.SysFont(None, 22)
font_small = pygame.font.SysFont(None, 18)

top_wall    = pygame.Rect(0, 0,             WIDTH, WALL_H)
bottom_wall = pygame.Rect(0, HEIGHT-WALL_H, WIDTH, WALL_H)

# ── Room 1 walls ──────────────────────────────────────────────────────────────
room1_walls = [
    pygame.Rect(200, WALL_H,              30, 120),   # left wall chunk 1
    pygame.Rect(200, HEIGHT-WALL_H-120,   30, 120),   # left wall chunk 2
    pygame.Rect(450, WALL_H,             500, 100),   # middle wall top
    pygame.Rect(450, HEIGHT-WALL_H-100,  500, 100),   # middle wall bottom
    pygame.Rect(320, 230,                 80,  30),   # horizontal blocker
    pygame.Rect(320, HEIGHT-230-30,       80,  30),   # horizontal blocker bottom
]

# ── Room 2 — first wall (doubled, vine gap) ───────────────────────────────────
FIRST_X     = 150
FIRST_THICK = 60
THIN_THICK  = 30
FIRST_TOP_Y = WALL_H
FIRST_H     = 150
GAP_H       = 50
GAP_Y       = FIRST_TOP_Y + (FIRST_H // 2) - (GAP_H // 2)

first_wall_top    = pygame.Rect(FIRST_X, FIRST_TOP_Y,   FIRST_THICK, GAP_Y - FIRST_TOP_Y)
first_wall_gap    = pygame.Rect(FIRST_X, GAP_Y,         THIN_THICK,  GAP_H)
first_wall_bottom = pygame.Rect(FIRST_X, GAP_Y+GAP_H,   FIRST_THICK, (FIRST_TOP_Y+FIRST_H)-(GAP_Y+GAP_H))
first_wall_mir    = pygame.Rect(FIRST_X, HEIGHT-WALL_H-FIRST_H, FIRST_THICK, FIRST_H)

room2_thin_gap = first_wall_gap   # vine-interactable

# ── Room 2 — lava pool (2nd wall, full height between borders) ────────────────
LAVA_X     = 380
LAVA_THICK = 100
lava_rect  = pygame.Rect(LAVA_X, WALL_H, LAVA_THICK, HEIGHT - 2*WALL_H)

# ── Room 2 — solid walls (no lava, no first-wall pieces) ─────────────────────
room2_solid_walls = [
    first_wall_top,
    first_wall_bottom,
    first_wall_mir,
    pygame.Rect(560, 200,        100, 30),
    pygame.Rect(560, HEIGHT-230, 100, 30),
]

# ── Items ─────────────────────────────────────────────────────────────────────
# Vine: top-left corner of left wall chunk 1 in room 1
VINE_X    = 175
VINE_Y    = WALL_H + 10
VINE_RECT = pygame.Rect(VINE_X-12, VINE_Y-12, 24, 24)

# Magma: bottom-right corner of first_wall in room 2
# first_wall spans x=150..210, bottom edge = FIRST_TOP_Y+FIRST_H = WALL_H+150
MAGMA_X    = FIRST_X + FIRST_THICK + 14   # just to the right of wall
MAGMA_Y    = FIRST_TOP_Y + FIRST_H - 14   # near bottom of wall
MAGMA_RECT = pygame.Rect(MAGMA_X-12, MAGMA_Y-12, 24, 24)

thin_gap_is_vine = False

# ── Player state ──────────────────────────────────────────────────────────────
RADIUS   = 20
player_x = 60.0
player_y = 300.0
speed    = 3
room     = 1
dx, dy   = 1, 0

has_vine  = False
has_magma = False
# form: 0=normal, 1=vine, 2=fire
form = 0

e_was_pressed = False
q_was_pressed = False

# ── Helpers ───────────────────────────────────────────────────────────────────
def resolve_wall(px, py, radius, wall):
    circle_rect = pygame.Rect(px-radius, py-radius, radius*2, radius*2)
    if not circle_rect.colliderect(wall):
        return px, py
    ol = (px+radius) - wall.left
    or_ = wall.right - (px-radius)
    ot = (py+radius) - wall.top
    ob = wall.bottom - (py-radius)
    mx = min(ol, or_)
    my = min(ot, ob)
    if mx < my:
        px = (wall.left - radius) if ol < or_ else (wall.right + radius)
    else:
        py = (wall.top - radius) if ot < ob else (wall.bottom + radius)
    return px, py


def draw_leaf(surface, x, y, radius, nx, ny):
    lx = int(x)
    ly = int(y - radius - 8)
    pygame.draw.line(surface, (20,80,20), (int(x), int(y-radius+2)), (lx, ly+6), 2)
    pts = [(lx,ly-5),(lx+6,ly),(lx,ly+6),(lx-6,ly)]
    pygame.draw.polygon(surface, (50,180,50), pts)
    pygame.draw.polygon(surface, (30,130,30), pts, 1)
    pygame.draw.line(surface, (30,130,30), (lx,ly-4), (lx,ly+5), 1)


def draw_flame(surface, x, y, radius):
    cx, cy = int(x), int(y - radius - 6)
    for i, (ox, oy, r, col) in enumerate([
        (-6, 0, 5, (255,80,0)),
        (0, -4, 6, (255,160,0)),
        (6, 0, 5, (255,80,0)),
    ]):
        pygame.draw.circle(surface, col, (cx+ox, cy+oy), r)


def draw_slime(surface, color, x, y, radius, dx, dy, form=0):
    pygame.draw.circle(surface, color, (int(x), int(y)), radius)
    outline = (134,218,134) if form != 2 else (255,200,80)
    pygame.draw.circle(surface, outline, (int(x), int(y)), radius, 2)

    length = math.hypot(dx, dy)
    nx, ny = (dx/length, dy/length) if length else (1, 0)

    ex = int(x + nx*(radius//3))
    ey = int(y + ny*(radius//3))
    pygame.draw.circle(surface, (25,25,25), (ex,ey), radius//4)
    px_ = int(ex + nx*(radius//8))
    py_ = int(ey + ny*(radius//8))
    pygame.draw.circle(surface, (217,217,217), (px_,py_), radius//12)

    if form == 1:
        draw_leaf(surface, x, y, radius, nx, ny)
    elif form == 2:
        draw_flame(surface, x, y, radius)


def draw_item(surface, cx, cy, inner_color, glow_color, label, collected):
    if collected:
        return
    pygame.draw.circle(surface, glow_color, (cx, cy), 14)
    pygame.draw.circle(surface, inner_color, (cx, cy), 11)
    lbl = font_small.render(label, True, (240,240,200))
    surface.blit(lbl, (cx - lbl.get_width()//2, cy+16))


def draw_lava(surface, rect, t):
    """Draw an animated lava pool."""
    # Base fill
    pygame.draw.rect(surface, (200,40,0), rect)
    # Animated blobs
    cols = [(255,120,0),(255,80,0),(230,60,0),(255,160,30)]
    for i in range(6):
        bx = rect.left + (i * rect.width // 5) + int(math.sin(t*2 + i) * 6)
        by = rect.top  + int((i * rect.height / 5.5)) + int(math.cos(t*1.5 + i*0.7) * 10)
        br = 8 + int(math.sin(t + i*1.2) * 3)
        col = cols[i % len(cols)]
        pygame.draw.circle(surface, col, (bx, by), br)
    # Edge glow
    pygame.draw.rect(surface, (255,60,0), rect, 3)


def draw_hint_on_wall(surface, text, color=(220,220,180)):
    """Bake hint text into the bottom border wall area."""
    surf = font_small.render(text, True, color)
    # centered horizontally, vertically centered in bottom wall
    bx = WIDTH//2 - surf.get_width()//2
    by = HEIGHT - WALL_H + (WALL_H - surf.get_height())//2
    surface.blit(surf, (bx, by))

# ── Main loop 
running = True
while running:
    t = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    new_dx, new_dy = 0, 0
    moving = False

    if keys[pygame.K_a]: player_x -= speed; new_dx -= 1; moving = True
    if keys[pygame.K_d]: player_x += speed; new_dx += 1; moving = True
    if keys[pygame.K_w]: player_y -= speed; new_dy -= 1; moving = True
    if keys[pygame.K_s]: player_y += speed; new_dy += 1; moving = True
    if new_dx or new_dy:
        dx, dy = new_dx, new_dy

    # ── Q: cycle form ──
    q_now = keys[pygame.K_q]
    if q_now and not q_was_pressed:
        available = [0]
        if has_vine:  available.append(1)
        if has_magma: available.append(2)
        if len(available) > 1:
            idx = available.index(form) if form in available else 0
            form = available[(idx + 1) % len(available)]
    q_was_pressed = q_now

    # ── E: interact ──
    e_now = keys[pygame.K_e]
    if e_now and not e_was_pressed:
        pcircle = pygame.Rect(player_x-RADIUS, player_y-RADIUS, RADIUS*2, RADIUS*2)

        if room == 1 and not has_vine:
            if pcircle.colliderect(VINE_RECT.inflate(20,20)):
                has_vine = True

        if room == 2 and not has_magma:
            if pcircle.colliderect(MAGMA_RECT.inflate(20,20)):
                has_magma = True

        if room == 2 and form == 1 and not thin_gap_is_vine:
            if pcircle.colliderect(room2_thin_gap.inflate(30,30)):
                thin_gap_is_vine = True
    e_was_pressed = e_now

    # ── Player color ──
    if form == 1:
        P_color = P_VINE_MOVE if moving else P_VINE_STOP
    elif form == 2:
        P_color = P_FIRE_MOVE if moving else P_FIRE_STOP
    else:
        P_color = P_NORMAL_MOVE if moving else P_NORMAL_STOP

    # ── Clamp ──
    player_x = max(RADIUS, min(WIDTH-RADIUS, player_x))
    player_y = max(WALL_H+RADIUS, min(HEIGHT-WALL_H-RADIUS, player_y))

    # ── Collision ──
    pcircle = pygame.Rect(player_x-RADIUS, player_y-RADIUS, RADIUS*2, RADIUS*2)

    if room == 1:
        for w in room1_walls:
            player_x, player_y = resolve_wall(player_x, player_y, RADIUS, w)

    elif room == 2:
        for w in room2_solid_walls:
            player_x, player_y = resolve_wall(player_x, player_y, RADIUS, w)

        # Thin vine gap
        if not thin_gap_is_vine:
            player_x, player_y = resolve_wall(player_x, player_y, RADIUS, room2_thin_gap)

        # Lava — blocks everyone except fire form
        if form != 2:
            player_x, player_y = resolve_wall(player_x, player_y, RADIUS, lava_rect)

    pcircle = pygame.Rect(player_x-RADIUS, player_y-RADIUS, RADIUS*2, RADIUS*2)

    # ══════════════ DRAW ══════════════════════════════════════════════════════

    # ── Room 1 ──
    if room == 1:
        screen.fill(BG)
        pygame.draw.rect(screen, WALL, top_wall)
        pygame.draw.rect(screen, WALL, bottom_wall)
        for w in room1_walls:
            pygame.draw.rect(screen, WALL, w)

        draw_item(screen, VINE_X, VINE_Y, (60,179,60), (20,80,20), "Vine",  has_vine)

        goal = pygame.Rect(750, 262, 30, 75)
        pygame.draw.rect(screen, GREEN, goal)
        draw_slime(screen, P_color, player_x, player_y, RADIUS, dx, dy, form)

        # HUD top-left
        lines = ["[WASD] Move  [E] Interact  [Q] Change form"]
        if has_vine or has_magma:
            items = []
            if has_vine:  items.append("Vine")
            if has_magma: items.append("Magma")
            lines.append(f"Items: {', '.join(items)}  |  Form: {['Normal','Vine','Fire'][form]}")
        for i, line in enumerate(lines):
            screen.blit(font.render(line, True, (200,200,200)), (10, 10+i*20))

        if pcircle.colliderect(goal):
            room = 2
            player_x, player_y = 60, 300

    # ── Room 2 ──
    elif room == 2:
        screen.fill((20, 20, 60))
        pygame.draw.rect(screen, WALL, top_wall)
        pygame.draw.rect(screen, WALL, bottom_wall)

        # Solid walls
        for w in room2_solid_walls:
            pygame.draw.rect(screen, WALL, w)

        # Thin vine gap
        gap_col = VINE_GREEN if thin_gap_is_vine else WALL
        pygame.draw.rect(screen, gap_col, room2_thin_gap)

        # Lava pool
        draw_lava(screen, lava_rect, t)

        # Magma item (bottom-right of first wall)
        draw_item(screen, MAGMA_X, MAGMA_Y, (220,80,0), (120,30,0), "Magma", has_magma)

        # Goal — right side, past lava
        goal2 = pygame.Rect(750, 262, 30, 75)
        pygame.draw.rect(screen, YELLOW, goal2)

        draw_slime(screen, P_color, player_x, player_y, RADIUS, dx, dy, form)

        # Hint baked into bottom border wall
        if not thin_gap_is_vine:
            draw_hint_on_wall(screen, "Press E on the thin wall (Vine form needed)")
        elif form != 2:
            draw_hint_on_wall(screen, "Fire form to cross the lava!")
        else:
            draw_hint_on_wall(screen, "Walk through the lava to the next room!")

        # HUD top-left
        lines = ["[WASD] Move  [E] Interact  [Q] Change form"]
        if has_vine or has_magma:
            items = []
            if has_vine:  items.append("Vine")
            if has_magma: items.append("Magma")
            lines.append(f"Items: {', '.join(items)}  |  Form: {['Normal','Vine','Fire'][form]}")
        for i, line in enumerate(lines):
            screen.blit(font.render(line, True, (200,200,200)), (10, 10+i*20))

        if pcircle.colliderect(goal2):
            room = 3
            player_x, player_y = 60, 300

    # ── Room 3 ──
    elif room == 3:
        screen.fill((10, 10, 25))
        pygame.draw.rect(screen, WALL, top_wall)
        pygame.draw.rect(screen, WALL, bottom_wall)

        draw_slime(screen, P_color, player_x, player_y, RADIUS, dx, dy, form)

        # Flavour hint
        draw_hint_on_wall(screen, "...", color=(100,100,140))

        lines = ["[WASD] Move  [Q] Change form"]
        if has_vine or has_magma:
            items = []
            if has_vine:  items.append("Vine")
            if has_magma: items.append("Magma")
            lines.append(f"Items: {', '.join(items)}  |  Form: {['Normal','Vine','Fire'][form]}")
        for i, line in enumerate(lines):
            screen.blit(font.render(line, True, (140,140,180)), (10, 10+i*20))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
