import pygame
import math
import time
import random

pygame.init()

WIDTH  = 800
HEIGHT = 600
WALL_H = 150
RADIUS = 20

# ── Colors ────────────────────────────────────────────────────────────────────
BG         = (42,  42,  42)
WALL       = (80,  80,  80)
RED        = (200,  30,  30)
GREEN      = (0,  220,   0)
YELLOW     = (255, 220,   0)
VINE_GREEN = (34,  139,  34)
WATER_COL  = (30,  100, 200)
WOOD_COL   = (110,  70,  30)

P_NORMAL_STOP  = (0,   191,   0)
P_NORMAL_MOVE  = (100, 200, 100)
P_VINE_STOP    = (34,  120,  34)
P_VINE_MOVE    = (60,  160,  60)
P_FIRE_STOP    = (255, 200,  30)
P_FIRE_MOVE    = (255, 230,  80)
P_DROP_STOP    = (40,  120, 220)
P_DROP_MOVE    = (80,  160, 255)

SLASH_COLORS = {
    0: (180, 255, 180),   # normal – light green
    1: (30,  120,  30),   # vine   – dark green
    2: (255, 180,  30),   # fire   – yellow-orange
    3: (60,  160, 255),   # drop   – blue
}

screen     = pygame.display.set_mode((WIDTH, HEIGHT))
clock      = pygame.time.Clock()
pygame.display.set_caption("Dungeon Larper")
font       = pygame.font.SysFont(None, 22)
font_small = pygame.font.SysFont(None, 18)

top_wall    = pygame.Rect(0, 0,              WIDTH, WALL_H)
bottom_wall = pygame.Rect(0, HEIGHT - WALL_H, WIDTH, WALL_H)

# ── Room 1 walls ──────────────────────────────────────────────────────────────
room1_walls = [
    pygame.Rect(200, WALL_H,             30, 120),
    pygame.Rect(200, HEIGHT-WALL_H-120,  30, 120),
    pygame.Rect(450, WALL_H,            500, 100),
    pygame.Rect(450, HEIGHT-WALL_H-100, 500, 100),
    pygame.Rect(320, 230,                80,  30),
    pygame.Rect(320, HEIGHT-230-30,      80,  30),
]

# ── Room 2 — first wall (doubled, vine gap) ───────────────────────────────────
FIRST_X     = 150
FIRST_THICK = 60
THIN_THICK  = 30
FIRST_TOP_Y = WALL_H
FIRST_H     = 150
GAP_H       = 50
GAP_Y       = FIRST_TOP_Y + (FIRST_H // 2) - (GAP_H // 2)

first_wall_top    = pygame.Rect(FIRST_X, FIRST_TOP_Y,  FIRST_THICK, GAP_Y - FIRST_TOP_Y)
first_wall_gap    = pygame.Rect(FIRST_X, GAP_Y,        THIN_THICK,  GAP_H)
first_wall_bottom = pygame.Rect(FIRST_X, GAP_Y+GAP_H,  FIRST_THICK, (FIRST_TOP_Y+FIRST_H)-(GAP_Y+GAP_H))
first_wall_mir    = pygame.Rect(FIRST_X, HEIGHT-WALL_H-FIRST_H, FIRST_THICK, FIRST_H)
room2_thin_gap    = first_wall_gap

LAVA_X     = 380
LAVA_THICK = 80
lava_rect  = pygame.Rect(LAVA_X, WALL_H, LAVA_THICK, HEIGHT - 2*WALL_H)

room2_solid_walls = [
    first_wall_top, first_wall_bottom, first_wall_mir,
    pygame.Rect(560, 200,        100, 30),
    pygame.Rect(560, HEIGHT-230, 100, 30),
]

# ── Room 3 — water + bridge ───────────────────────────────────────────────────
# Water fills the middle strip of the floor
WATER_Y1 = WALL_H
WATER_Y2 = HEIGHT - WALL_H
WATER_X1 = 220
WATER_X2 = 580
water_rect = pygame.Rect(WATER_X1, WATER_Y1, WATER_X2-WATER_X1, WATER_Y2-WATER_Y1)

# Bridge: left plank, gap (water floor), right plank
BRIDGE_Y      = HEIGHT // 2 - 15
BRIDGE_H      = 30
BRIDGE_LEFT   = pygame.Rect(WATER_X1,       BRIDGE_Y, 100, BRIDGE_H)   # solid
BRIDGE_GAP_X1 = WATER_X1 + 100
BRIDGE_GAP_X2 = WATER_X2 - 100
BRIDGE_RIGHT  = pygame.Rect(WATER_X2 - 100, BRIDGE_Y, 100, BRIDGE_H)   # solid

# ── Items ─────────────────────────────────────────────────────────────────────
VINE_X    = 175;  VINE_Y  = WALL_H + 10
VINE_RECT = pygame.Rect(VINE_X-12, VINE_Y-12, 24, 24)

MAGMA_X    = FIRST_X + FIRST_THICK + 14
MAGMA_Y    = FIRST_TOP_Y + FIRST_H - 14
MAGMA_RECT = pygame.Rect(MAGMA_X-12, MAGMA_Y-12, 24, 24)

# Droplet: on the floor in room 3, left side near entry
DROP_X    = 100;  DROP_Y = HEIGHT // 2
DROP_RECT = pygame.Rect(DROP_X-12, DROP_Y-12, 24, 24)

# ── Go-back platform (RED) position per room — left edge ─────────────────────
BACK_RECT = pygame.Rect(10, HEIGHT//2 - 30, 25, 60)   # same position all rooms

# ── Slash animation ───────────────────────────────────────────────────────────
class Slash:
    def __init__(self, x, y, angle, color):
        self.x      = x
        self.y      = y
        self.angle  = angle   # radians, direction player faces
        self.color  = color
        self.life   = 0.22    # seconds
        self.born   = time.time()

    @property
    def alive(self):
        return (time.time() - self.born) < self.life

    def draw(self, surface):
        age    = time.time() - self.born
        frac   = age / self.life           # 0→1
        alpha  = int(255 * (1 - frac))
        length = 38 + int(frac * 10)
        spread = 0.55                      # arc half-width in radians

        for offset in (-spread, -spread*0.5, 0, spread*0.5, spread):
            a   = self.angle + offset
            ex  = int(self.x + math.cos(a) * length)
            ey  = int(self.y + math.sin(a) * length)
            col = tuple(min(255, max(0, c)) for c in self.color)
            # fade by drawing with dimmed color
            dim = tuple(int(c * (1 - frac * 0.7)) for c in col)
            w   = max(1, 3 - int(frac * 2))
            pygame.draw.line(surface, dim,
                             (int(self.x + math.cos(a)*RADIUS),
                              int(self.y + math.sin(a)*RADIUS)),
                             (ex, ey), w)

# ── Enemies ───────────────────────────────────────────────────────────────────
class Enemy:
    def __init__(self, x, y):
        self.x    = float(x)
        self.y    = float(y)
        self.r    = 18
        self.hp   = 3
        self.speed= 1.2
        self.hit_flash = 0   # timer for hit flash

    @property
    def alive(self):
        return self.hp > 0

    def update(self, px, py):
        dx = px - self.x
        dy = py - self.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.x += (dx/dist) * self.speed
            self.y += (dy/dist) * self.speed
        self.x = max(RADIUS+self.r, min(WIDTH-RADIUS-self.r, self.x))
        self.y = max(WALL_H+self.r, min(HEIGHT-WALL_H-self.r, self.y))
        if self.hit_flash > 0:
            self.hit_flash -= 1

    def draw(self, surface):
        col = (100, 180, 255) if self.hit_flash == 0 else (255, 255, 255)
        pygame.draw.circle(surface, col, (int(self.x), int(self.y)), self.r)
        pygame.draw.circle(surface, (60, 120, 200), (int(self.x), int(self.y)), self.r, 2)
        # angry eyes
        for ox in (-5, 5):
            pygame.draw.circle(surface, (20,20,80), (int(self.x)+ox, int(self.y)-3), 3)
        # HP pips
        for i in range(self.hp):
            pygame.draw.circle(surface, (255,80,80),
                               (int(self.x) - 8 + i*8, int(self.y) - self.r - 6), 3)

# ── Global state ──────────────────────────────────────────────────────────────
player_x, player_y = 60.0, 300.0
speed = 3
room  = 1
dx, dy = 1, 0

has_vine  = False
has_magma = False
has_drop  = False
# form: 0=normal 1=vine 2=fire 3=drop
form = 0

thin_gap_is_vine = False

slashes: list[Slash] = []

enemies = [Enemy(500, 250), Enemy(450, 380)]

e_was = False
q_was = False
f_was = False

# ── Helper functions ──────────────────────────────────────────────────────────
def resolve_wall(px, py, radius, wall):
    cr = pygame.Rect(px-radius, py-radius, radius*2, radius*2)
    if not cr.colliderect(wall): return px, py
    ol = (px+radius)-wall.left;  orr = wall.right-(px-radius)
    ot = (py+radius)-wall.top;   ob  = wall.bottom-(py-radius)
    if min(ol,orr) < min(ot,ob):
        px = wall.left-radius if ol < orr else wall.right+radius
    else:
        py = wall.top-radius  if ot < ob  else wall.bottom+radius
    return px, py

def player_color(frm, moving):
    table = {
        0: (P_NORMAL_MOVE, P_NORMAL_STOP),
        1: (P_VINE_MOVE,   P_VINE_STOP),
        2: (P_FIRE_MOVE,   P_FIRE_STOP),
        3: (P_DROP_MOVE,   P_DROP_STOP),
    }
    return table[frm][0] if moving else table[frm][1]

def draw_leaf(surface, x, y, radius):
    lx, ly = int(x), int(y-radius-8)
    pygame.draw.line(surface, (20,80,20), (int(x), int(y-radius+2)), (lx,ly+6), 2)
    pts = [(lx,ly-5),(lx+6,ly),(lx,ly+6),(lx-6,ly)]
    pygame.draw.polygon(surface, (50,180,50), pts)
    pygame.draw.polygon(surface, (30,130,30), pts, 1)
    pygame.draw.line(surface, (30,130,30),(lx,ly-4),(lx,ly+5),1)

def draw_flame(surface, x, y, radius):
    cx, cy = int(x), int(y-radius-6)
    for ox,oy,r,col in [(-6,0,5,(255,80,0)),(0,-4,6,(255,160,0)),(6,0,5,(255,80,0))]:
        pygame.draw.circle(surface, col, (cx+ox,cy+oy), r)

def draw_droplet_crown(surface, x, y, radius):
    cx, cy = int(x), int(y-radius-6)
    pygame.draw.circle(surface, (80,180,255), (cx,cy), 6)
    pygame.draw.circle(surface, (40,120,220), (cx,cy), 6, 1)

def draw_slime(surface, color, x, y, radius, ddx, ddy, frm=0):
    pygame.draw.circle(surface, color, (int(x),int(y)), radius)
    outlines = {0:(134,218,134),1:(60,160,60),2:(255,200,80),3:(100,200,255)}
    pygame.draw.circle(surface, outlines[frm], (int(x),int(y)), radius, 2)
    ln = math.hypot(ddx,ddy)
    nx,ny = (ddx/ln,ddy/ln) if ln else (1,0)
    ex = int(x+nx*(radius//3)); ey = int(y+ny*(radius//3))
    pygame.draw.circle(surface,(25,25,25),(ex,ey),radius//4)
    pygame.draw.circle(surface,(217,217,217),(int(ex+nx*(radius//8)),int(ey+ny*(radius//8))),radius//12)
    if frm == 1: draw_leaf(surface,x,y,radius)
    elif frm == 2: draw_flame(surface,x,y,radius)
    elif frm == 3: draw_droplet_crown(surface,x,y,radius)

def draw_item(surface, cx, cy, inner, glow, label, collected):
    if collected: return
    pygame.draw.circle(surface, glow,  (cx,cy), 14)
    pygame.draw.circle(surface, inner, (cx,cy), 11)
    lb = font_small.render(label, True, (240,240,200))
    surface.blit(lb, (cx-lb.get_width()//2, cy+16))

def draw_lava(surface, rect, t):
    pygame.draw.rect(surface,(200,40,0),rect)
    cols=[(255,120,0),(255,80,0),(230,60,0),(255,160,30)]
    for i in range(6):
        bx=rect.left+(i*rect.width//5)+int(math.sin(t*2+i)*6)
        by=rect.top+int((i*rect.height/5.5))+int(math.cos(t*1.5+i*0.7)*10)
        br=8+int(math.sin(t+i*1.2)*3)
        pygame.draw.circle(surface,cols[i%4],(bx,by),br)
    pygame.draw.rect(surface,(255,60,0),rect,3)

def draw_water(surface, rect, t):
    pygame.draw.rect(surface, (20,70,160), rect)
    # simple ripple lines
    for i in range(5):
        wy = rect.top + int(rect.height * (i+1) / 6)
        ox = int(math.sin(t*1.5 + i*0.8)*12)
        pygame.draw.line(surface, (60,130,220),
                         (rect.left+10+ox, wy), (rect.right-10+ox, wy), 2)

def draw_bridge(surface):
    # Left plank
    pygame.draw.rect(surface, WOOD_COL, BRIDGE_LEFT)
    pygame.draw.rect(surface, (80,50,20), BRIDGE_LEFT, 2)
    # Right plank
    pygame.draw.rect(surface, WOOD_COL, BRIDGE_RIGHT)
    pygame.draw.rect(surface, (80,50,20), BRIDGE_RIGHT, 2)
    # Broken gap — faint broken plank ends
    pygame.draw.line(surface, (80,50,20),
                     (BRIDGE_GAP_X1, BRIDGE_Y), (BRIDGE_GAP_X1, BRIDGE_Y+BRIDGE_H), 3)
    pygame.draw.line(surface, (80,50,20),
                     (BRIDGE_GAP_X2, BRIDGE_Y), (BRIDGE_GAP_X2, BRIDGE_Y+BRIDGE_H), 3)

def draw_hint_on_wall(surface, text, color=(220,220,180)):
    surf = font_small.render(text, True, color)
    surface.blit(surf, (WIDTH//2 - surf.get_width()//2,
                        HEIGHT-WALL_H+(WALL_H-surf.get_height())//2))

def draw_back_platform(surface):
    pygame.draw.rect(surface, RED, BACK_RECT)
    lb = font_small.render("BACK", True, (255,220,220))
    surface.blit(lb, (BACK_RECT.x + BACK_RECT.w//2 - lb.get_width()//2,
                      BACK_RECT.y + BACK_RECT.h//2 - lb.get_height()//2))

def hud(surface, frm, items_owned):
    names = {0:"Normal",1:"Vine",2:"Fire",3:"Droplet"}
    lines = ["[WASD] Move  [E] Pick up  [Q] Form  [F] Attack"]
    if items_owned:
        lines.append(f"Items: {', '.join(items_owned)}  |  Form: {names[frm]}")
    for i,l in enumerate(lines):
        surface.blit(font.render(l,True,(200,200,200)),(10,10+i*20))

# ── Main loop ─────────────────────────────────────────────────────────────────
running = True
while running:
    t = time.time()
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    ndx = ndy = 0
    moving = False
    if keys[pygame.K_a]: player_x -= speed; ndx -= 1; moving = True
    if keys[pygame.K_d]: player_x += speed; ndx += 1; moving = True
    if keys[pygame.K_w]: player_y -= speed; ndy -= 1; moving = True
    if keys[pygame.K_s]: player_y += speed; ndy += 1; moving = True
    if ndx or ndy: dx, dy = ndx, ndy

    # ── Q: cycle form ──
    q_now = keys[pygame.K_q]
    if q_now and not q_was:
        avail = [0]
        if has_vine:  avail.append(1)
        if has_magma: avail.append(2)
        if has_drop:  avail.append(3)
        if len(avail) > 1:
            idx  = avail.index(form) if form in avail else 0
            form = avail[(idx+1) % len(avail)]
    q_was = q_now

    # ── E: interact ──
    e_now = keys[pygame.K_e]
    if e_now and not e_was:
        pcr = pygame.Rect(player_x-RADIUS, player_y-RADIUS, RADIUS*2, RADIUS*2)
        if room == 1 and not has_vine and pcr.colliderect(VINE_RECT.inflate(20,20)):
            has_vine = True
        if room == 2 and not has_magma and pcr.colliderect(MAGMA_RECT.inflate(20,20)):
            has_magma = True
        if room == 2 and form == 1 and not thin_gap_is_vine and pcr.colliderect(room2_thin_gap.inflate(30,30)):
            thin_gap_is_vine = True
        if room == 3 and not has_drop and pcr.colliderect(DROP_RECT.inflate(20,20)):
            has_drop = True
    e_was = e_now

    # ── F: attack ──
    f_now = keys[pygame.K_f]
    if f_now and not f_was:
        angle = math.atan2(dy, dx)
        slashes.append(Slash(player_x, player_y, angle, SLASH_COLORS[form]))
        # check enemy hits (only droplet form vs blue enemies)
        if room == 3:
            for en in enemies:
                if not en.alive: continue
                dist = math.hypot(en.x - player_x, en.y - player_y)
                if dist < RADIUS + en.r + 42:
                    if form == 3:   # only droplet damages them
                        en.hp -= 1
                        en.hit_flash = 8
    f_was = f_now

    # ── Clamp ──
    player_x = max(RADIUS, min(WIDTH-RADIUS, player_x))
    player_y = max(WALL_H+RADIUS, min(HEIGHT-WALL_H-RADIUS, player_y))

    # ── Wall collision ──
    if room == 1:
        for w in room1_walls:
            player_x, player_y = resolve_wall(player_x, player_y, RADIUS, w)
    elif room == 2:
        for w in room2_solid_walls:
            player_x, player_y = resolve_wall(player_x, player_y, RADIUS, w)
        if not thin_gap_is_vine:
            player_x, player_y = resolve_wall(player_x, player_y, RADIUS, room2_thin_gap)
        if form != 2:
            player_x, player_y = resolve_wall(player_x, player_y, RADIUS, lava_rect)
    elif room == 3:
        # Water blocks unless droplet form; bridge planks always solid
        if form != 3:
            player_x, player_y = resolve_wall(player_x, player_y, RADIUS, water_rect)
        # Bridge planks are solid terrain (walkable above water)
        for plank in (BRIDGE_LEFT, BRIDGE_RIGHT):
            player_x, player_y = resolve_wall(player_x, player_y, RADIUS, plank)

    pcircle = pygame.Rect(player_x-RADIUS, player_y-RADIUS, RADIUS*2, RADIUS*2)

    # ── Enemy update (room 3) ──
    if room == 3:
        for en in enemies:
            if en.alive:
                en.update(player_x, player_y)

    # ── Back-platform: go back one room ──
    if pcircle.colliderect(BACK_RECT):
        if room > 1:
            room -= 1
            player_x, player_y = WIDTH - 80, 300

    # ── Forward goal transition ──
    goal1 = pygame.Rect(750, 262, 30, 75)
    goal2 = pygame.Rect(750, 262, 30, 75)
    if room == 1 and pcircle.colliderect(goal1):
        room = 2; player_x, player_y = 60, 300
    elif room == 2 and pcircle.colliderect(goal2):
        room = 3; player_x, player_y = 60, 300

    P_color = player_color(form, moving)
    items_owned = (["Vine"] if has_vine else []) + (["Magma"] if has_magma else []) + (["Droplet"] if has_drop else [])

    # ════════════════════ DRAW ════════════════════════════════════════════════

    # ── Room 1 ──
    if room == 1:
        screen.fill(BG)
        pygame.draw.rect(screen, WALL, top_wall)
        pygame.draw.rect(screen, WALL, bottom_wall)
        for w in room1_walls: pygame.draw.rect(screen, WALL, w)
        draw_item(screen, VINE_X, VINE_Y, (60,179,60),(20,80,20),"Vine",has_vine)
        pygame.draw.rect(screen, GREEN, goal1)
        draw_back_platform(screen)
        draw_slime(screen, P_color, player_x, player_y, RADIUS, dx, dy, form)
        for sl in slashes:
            if sl.alive: sl.draw(screen)
        draw_hint_on_wall(screen, "Reach the green portal  |  [E] pick up Vine")
        hud(screen, form, items_owned)

    # ── Room 2 ──
    elif room == 2:
        screen.fill((20, 20, 60))
        pygame.draw.rect(screen, WALL, top_wall)
        pygame.draw.rect(screen, WALL, bottom_wall)
        for w in room2_solid_walls: pygame.draw.rect(screen, WALL, w)
        pygame.draw.rect(screen, VINE_GREEN if thin_gap_is_vine else WALL, room2_thin_gap)
        draw_lava(screen, lava_rect, t)
        draw_item(screen, MAGMA_X, MAGMA_Y, (220,80,0),(120,30,0),"Magma",has_magma)
        pygame.draw.rect(screen, YELLOW, goal2)
        draw_back_platform(screen)
        draw_slime(screen, P_color, player_x, player_y, RADIUS, dx, dy, form)
        for sl in slashes:
            if sl.alive: sl.draw(screen)
        if not thin_gap_is_vine:
            draw_hint_on_wall(screen, "Press E on the thin wall  (need Vine form)")
        elif form != 2:
            draw_hint_on_wall(screen, "Fire form lets you cross the lava!")
        else:
            draw_hint_on_wall(screen, "Walk through the lava to the next room!")
        hud(screen, form, items_owned)

    # ── Room 3 ──
    elif room == 3:
        screen.fill((10, 10, 25))
        pygame.draw.rect(screen, WALL, top_wall)
        pygame.draw.rect(screen, WALL, bottom_wall)

        # Water
        draw_water(screen, water_rect, t)

        # Bridge over water
        draw_bridge(screen)

        # Droplet item (on dry land left side)
        draw_item(screen, DROP_X, DROP_Y, (60,140,255),(20,60,160),"Droplet",has_drop)

        # Enemies
        for en in enemies:
            if en.alive: en.draw(screen)

        # Slashes (draw before player so player is on top)
        for sl in slashes:
            if sl.alive: sl.draw(screen)

        draw_back_platform(screen)
        draw_slime(screen, P_color, player_x, player_y, RADIUS, dx, dy, form)

        if not has_drop:
            draw_hint_on_wall(screen, "[E] pick up Droplet  — only Droplet form hurts the blue enemies!")
        elif form != 3:
            draw_hint_on_wall(screen, "[Q] switch to Droplet form  [F] attack blue enemies")
        else:
            draw_hint_on_wall(screen, "[F] Attack!  Droplet form defeats blue enemies")
        hud(screen, form, items_owned)

    # Prune dead slashes
    slashes = [sl for sl in slashes if sl.alive]

    pygame.display.update()

pygame.quit()
