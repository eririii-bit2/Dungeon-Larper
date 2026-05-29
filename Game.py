import pygame, math, time
pygame.init()

WIDTH, HEIGHT = 800, 600
WALL_H = 150
R5_WALL_H = WALL_H // 2
RADIUS = 20

font_title = pygame.font.SysFont("Georgia", 52, bold=True)
font_big   = pygame.font.SysFont("Georgia", 32, bold=True)
font_med   = pygame.font.SysFont(None, 26)
font_small = pygame.font.SysFont(None, 20)
font_tiny  = pygame.font.SysFont(None, 17)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock  = pygame.time.Clock()
pygame.display.set_caption("Dungeon Larper")

# ── Colors ────────────────────────────────────────────────────────────────────
BG       = (42, 42, 42)
WALL_C   = (75, 75, 75)
WALL_LIT = (105,100, 90)
RED_C    = (200, 30, 30)
GREEN_C  = (0, 220, 0)
YELLOW_C = (255, 220, 0)
VINE_GRN = (34, 139, 34)
WOOD_C   = (110, 70, 30)
CARPET_C = (160, 20, 20)
GOLD_C   = (200, 170, 40)
STONE_C  = (90, 85, 78)

P_COLS = {
    0: {"stop":(0,191,0),    "move":(100,200,100),"out":(134,218,134)},
    1: {"stop":(34,120,34),  "move":(60,160,60),  "out":(60,160,60)},
    2: {"stop":(255,200,30), "move":(255,230,80),  "out":(255,200,80)},
    3: {"stop":(40,120,220), "move":(80,160,255),  "out":(100,200,255)},
}
SLASH_C = {0:(180,255,180),1:(30,120,30),2:(255,180,30),3:(60,160,255)}
ENEMY_KINDS = {
    "fire":{"body":(220,60,40), "out":(160,30,10),"eye":(80,10,0),  "kills":2},
    "vine":{"body":(50,160,50), "out":(20,100,20),"eye":(10,50,10), "kills":1},
    "drop":{"body":(100,180,255),"out":(60,120,200),"eye":(20,20,80),"kills":3},
}

# ── Audio stubs ───────────────────────────────────────────────────────────────
pygame.mixer.music.load("bg_music.mp3"); pygame.mixer.music.play(-1)
sfx_slash = pygame.mixer.Sound("slash.mp3")
sfx_hit   = pygame.mixer.Sound("hit.mp3")
audio_volume = 3

# ── Globals ───────────────────────────────────────────────────────────────────
hint_visible = True
paused       = False
score        = 0
game_mode    = "menu"
menu_screen  = "main"
gs           = None

# ── Pause button — top center ─────────────────────────────────────────────────
PAUSE_BTN = pygame.Rect(WIDTH//2 - 18, 8, 36, 36)

# ── HUD / hint button ────────────────────────────────────────────────────────
HUD_SLOTS = [
    {"rect":pygame.Rect(10, HEIGHT-WALL_H+18, 44, 44),"form":1,"key":"1"},
    {"rect":pygame.Rect(60, HEIGHT-WALL_H+18, 44, 44),"form":2,"key":"2"},
    {"rect":pygame.Rect(110,HEIGHT-WALL_H+18, 44, 44),"form":3,"key":"3"},
]
HINT_BTN = pygame.Rect(WIDTH-70, HEIGHT-WALL_H+20, 60, 30)
BACK_RECT   = pygame.Rect(10, HEIGHT//2-30, 25, 60)
PORTAL_RECT = pygame.Rect(750, 262, 30, 75)

# ── Attack cooldown bar (top-left) ───────────────────────────────────────────
ATK_CD_MAX   = 0.45
ATK_BAR_RECT = pygame.Rect(10, 10, 120, 14)

# ── Room geometry ─────────────────────────────────────────────────────────────
top_wall    = pygame.Rect(0, 0,             WIDTH, WALL_H)
bottom_wall = pygame.Rect(0, HEIGHT-WALL_H, WIDTH, WALL_H)

# Room 1
room1_walls = [
    pygame.Rect(200, WALL_H,            45, 130),
    pygame.Rect(200, HEIGHT-WALL_H-130, 45, 130),
    pygame.Rect(450, WALL_H,           500, 115),
    pygame.Rect(450, HEIGHT-WALL_H-115,500, 115),
    pygame.Rect(310, 228,               95,  40),
    pygame.Rect(310, HEIGHT-228-40,     95,  40),
]

# Room 2
FX=150; FTH=72; FTHIN=36; FTY=WALL_H; FH=160
GAPH=52; GAPY=FTY+(FH//2)-(GAPH//2)
r2_wtop = pygame.Rect(FX, FTY,         FTH, GAPY-FTY)
r2_wgap = pygame.Rect(FX, GAPY,        FTHIN, GAPH)
r2_wbot = pygame.Rect(FX, GAPY+GAPH,   FTH, (FTY+FH)-(GAPY+GAPH))
r2_wmir = pygame.Rect(FX, HEIGHT-WALL_H-FH, FTH, FH)
r2_lava = pygame.Rect(375, WALL_H, 50, HEIGHT-2*WALL_H)
r2_solid= [r2_wtop, r2_wbot, r2_wmir,
           pygame.Rect(555, 195, 115, 40),
           pygame.Rect(555, HEIGHT-235, 115, 40)]

# Room 3
WX1,WX2 = 210, 590
r3_water = pygame.Rect(WX1, WALL_H, WX2-WX1, HEIGHT-2*WALL_H)
BRY=HEIGHT//2-18; BRH=36
BR_L=pygame.Rect(WX1,      BRY, 110, BRH)
BR_R=pygame.Rect(WX2-110,  BRY, 110, BRH)
BRG1=WX1+110; BRG2=WX2-110

# Room 4
r4_lava  = pygame.Rect(235, WALL_H, 50, HEIGHT-2*WALL_H)
R4VX=415; R4VTH=42; R4VGH=58
R4VGY=WALL_H+(HEIGHT-2*WALL_H)//2-R4VGH//2
r4_vtop  = pygame.Rect(R4VX, WALL_H, R4VTH, R4VGY-WALL_H)
r4_vgap  = pygame.Rect(R4VX, R4VGY,  R4VTH, R4VGH)
r4_vbot  = pygame.Rect(R4VX, R4VGY+R4VGH, R4VTH, HEIGHT-WALL_H-(R4VGY+R4VGH))
r4_pd1   = pygame.Rect(525, WALL_H+10,   130, (HEIGHT-2*WALL_H)//2-18)
r4_pd2   = pygame.Rect(525, HEIGHT//2+8, 130, (HEIGHT-2*WALL_H)//2-18)

# Room 5
r5_top    = pygame.Rect(0, 0,              WIDTH, R5_WALL_H)
r5_bot    = pygame.Rect(0, HEIGHT-R5_WALL_H, WIDTH, R5_WALL_H)
CARPET_Y  = HEIGHT//2-22; CARPET_H=44
r5_carpet = pygame.Rect(0, CARPET_Y, WIDTH, CARPET_H)
THRONE_X=708; THRONE_Y=HEIGHT//2-50; THRONE_W=64; THRONE_H=96
throne_rect=pygame.Rect(THRONE_X,THRONE_Y,THRONE_W,THRONE_H)

def torch_positions(wall_y, wall_h):
    return [(int(WIDTH*(i+1)/5), wall_y+wall_h//2) for i in range(4)]
r5_torches_top = torch_positions(0,          R5_WALL_H)
r5_torches_bot = torch_positions(HEIGHT-R5_WALL_H, R5_WALL_H)

# Items
VINE_POS   = (175, WALL_H+12)
MAGMA_POS  = (FX+FTH+16, FTY+FH-16)
DROP_POS   = (100, HEIGHT//2)
VINE_RECT  = pygame.Rect(VINE_POS[0]-12,  VINE_POS[1]-12,  24, 24)
MAGMA_RECT = pygame.Rect(MAGMA_POS[0]-12, MAGMA_POS[1]-12, 24, 24)
DROP_RECT  = pygame.Rect(DROP_POS[0]-12,  DROP_POS[1]-12,  24, 24)

# ── Classes ───────────────────────────────────────────────────────────────────
class Slash:
    def __init__(self,x,y,angle,color):
        self.x=x;self.y=y;self.angle=angle;self.color=color
        self.life=0.20;self.born=time.time()
    @property
    def alive(self): return (time.time()-self.born)<self.life
    def draw(self,surf):
        frac=(time.time()-self.born)/self.life
        length=40+int(frac*12);spread=0.60
        for off in(-spread,-spread*0.5,0,spread*0.5,spread):
            a=self.angle+off
            ex=int(self.x+math.cos(a)*length);ey=int(self.y+math.sin(a)*length)
            dim=tuple(int(c*(1-frac*0.75)) for c in self.color)
            pygame.draw.line(surf,dim,
                (int(self.x+math.cos(a)*RADIUS),int(self.y+math.sin(a)*RADIUS)),
                (ex,ey),max(1,3-int(frac*2)))

class Enemy:
    SPEED=0.52
    def __init__(self,x,y,kind="drop",boss=False):
        self.x=float(x);self.y=float(y);self.kind=kind;self.boss=boss
        self.r=38 if boss else 18
        self.hp_max=10 if boss else 3; self.hp=self.hp_max
        self.hit_flash=0; self.atk_cd=0
        self.form_timer=time.time()
        if boss: self.kind="fire"
    @property
    def alive(self): return self.hp>0
    def update(self,px,py):
        if self.boss and time.time()-self.form_timer>3.0:
            kinds=["fire","vine","drop"]
            self.kind=kinds[(kinds.index(self.kind)+1)%3]
            self.form_timer=time.time()
        ddx=px-self.x; ddy=py-self.y; dist=math.hypot(ddx,ddy)
        spd=self.SPEED*(0.65 if self.boss else 1)
        if dist>0: self.x+=ddx/dist*spd; self.y+=ddy/dist*spd
        self.x=max(self.r,min(WIDTH-self.r,self.x))
        self.y=max(WALL_H+self.r,min(HEIGHT-WALL_H-self.r,self.y))
        if self.hit_flash>0: self.hit_flash-=1
        if self.atk_cd>0:    self.atk_cd-=1
    def touches(self,px,py): return math.hypot(self.x-px,self.y-py)<self.r+RADIUS
    def can_hit(self,frm):   return ENEMY_KINDS[self.kind]["kills"]==frm
    def draw_crown(self,surf):
        cx,cy=int(self.x),int(self.y)-self.r-2
        pts=[(cx-14,cy),(cx-14,cy-10),(cx-8,cy-5),(cx,cy-14),(cx+8,cy-5),(cx+14,cy-10),(cx+14,cy)]
        pygame.draw.polygon(surf,GOLD_C,pts)
        pygame.draw.polygon(surf,(255,220,80),pts,1)
        for tx,ty in[(cx-14,cy-10),(cx,cy-14),(cx+14,cy-10)]:
            pygame.draw.circle(surf,(255,240,100),(tx,ty),3)
    def draw(self,surf):
        info=ENEMY_KINDS[self.kind]
        col=(255,255,255) if self.hit_flash else info["body"]
        pygame.draw.circle(surf,col,(int(self.x),int(self.y)),self.r)
        pygame.draw.circle(surf,info["out"],(int(self.x),int(self.y)),self.r,3 if self.boss else 2)
        if self.boss:
            pygame.draw.circle(surf,GOLD_C,(int(self.x),int(self.y)),self.r+5,2)
            self.draw_crown(surf)
        for ox in((-8,8) if self.boss else (-5,5)):
            pygame.draw.circle(surf,info["eye"],(int(self.x)+ox,int(self.y)-4),4 if self.boss else 3)
        if self.boss:
            bw=90;bx=int(self.x)-bw//2;by=int(self.y)-self.r-28
            pygame.draw.rect(surf,(40,10,10),(bx,by,bw,9))
            pygame.draw.rect(surf,(220,40,40),(bx,by,int(bw*self.hp/self.hp_max),9))
            pygame.draw.rect(surf,(180,80,80),(bx,by,bw,9),1)
        else:
            for i in range(self.hp):
                pygame.draw.circle(surf,(255,80,80),(int(self.x)-8+i*8,int(self.y)-self.r-7),3)

# ── Draw helpers ──────────────────────────────────────────────────────────────
def resolve_wall(px,py,rad,wall):
    cr=pygame.Rect(px-rad,py-rad,rad*2,rad*2)
    if not cr.colliderect(wall): return px,py
    ol=(px+rad)-wall.left; orr=wall.right-(px-rad)
    ot=(py+rad)-wall.top;  ob=wall.bottom-(py-rad)
    if min(ol,orr)<min(ot,ob):
        px=wall.left-rad if ol<orr else wall.right+rad
    else:
        py=wall.top-rad if ot<ob else wall.bottom+rad
    return px,py

def draw_wall_block(surf, rect, lit_top=True):
    pygame.draw.rect(surf, WALL_C, rect)
    pygame.draw.line(surf, WALL_LIT, rect.topleft, rect.topright, 2)
    pygame.draw.line(surf, WALL_LIT, rect.topleft, rect.bottomleft, 1)
    pygame.draw.line(surf, (50,50,50), rect.bottomleft, rect.bottomright, 2)
    pygame.draw.line(surf, (50,50,50), rect.topright,   rect.bottomright, 1)
    for i in range(1, rect.width//30):
        cx=rect.left+i*30
        pygame.draw.line(surf,(60,58,55),(cx,rect.top+4),(cx+4,rect.top+12),1)

def draw_border_walls(surf, room=1):
    t_col = WALL_C if room!=5 else (55,45,35)
    tw = top_wall if room!=5 else r5_top
    bw = bottom_wall if room!=5 else r5_bot
    pygame.draw.rect(surf, t_col, tw)
    pygame.draw.rect(surf, t_col, bw)
    for wall in (tw, bw):
        for row in range(0, wall.height, 18):
            offset = 20 if (row//18)%2==0 else 0
            for col in range(-offset, wall.width, 40):
                brk=pygame.Rect(wall.left+col, wall.top+row, 38, 16)
                pygame.draw.rect(surf,(t_col[0]+12,t_col[1]+10,t_col[2]+8),brk)
                pygame.draw.rect(surf,(t_col[0]-15,t_col[1]-15,t_col[2]-15),brk,1)
    pygame.draw.line(surf,WALL_LIT,tw.bottomleft,tw.bottomright,2)
    pygame.draw.line(surf,WALL_LIT,bw.topleft,bw.topright,2)

def draw_floor(surf, color, t, room=1):
    surf.fill(color)
    tc=tuple(min(255,c+8) for c in color)
    fc=tuple(max(0,c-8) for c in color)
    sz=40
    for gy in range(WALL_H, HEIGHT-WALL_H, sz):
        for gx in range(0, WIDTH, sz):
            r=pygame.Rect(gx,gy,sz,sz)
            pygame.draw.rect(surf,tc if ((gx//sz+gy//sz)%2==0) else fc,r)

def draw_leaf(s,x,y,r):
    lx,ly=int(x),int(y-r-8)
    pygame.draw.line(s,(20,80,20),(int(x),int(y-r+2)),(lx,ly+6),2)
    pts=[(lx,ly-5),(lx+6,ly),(lx,ly+6),(lx-6,ly)]
    pygame.draw.polygon(s,(50,180,50),pts);pygame.draw.polygon(s,(30,130,30),pts,1)
def draw_flame(s,x,y,r):
    cx,cy=int(x),int(y-r-6)
    for ox,oy,rr,c in[(-6,0,5,(255,80,0)),(0,-4,6,(255,160,0)),(6,0,5,(255,80,0))]:
        pygame.draw.circle(s,c,(cx+ox,cy+oy),rr)
def draw_drop_cr(s,x,y,r):
    cx,cy=int(x),int(y-r-6)
    pygame.draw.circle(s,(80,180,255),(cx,cy),6);pygame.draw.circle(s,(40,120,220),(cx,cy),6,1)

def draw_slime(surf,color,x,y,rad,ddx,ddy,frm=0,iframe=0):
    dc=(255,255,255) if iframe>0 and iframe%4<2 else color
    pygame.draw.circle(surf,dc,(int(x),int(y)),rad)
    pygame.draw.circle(surf,P_COLS[frm]["out"],(int(x),int(y)),rad,2)
    ln=math.hypot(ddx,ddy);nx,ny=(ddx/ln,ddy/ln) if ln else (1,0)
    ex=int(x+nx*(rad//3));ey=int(y+ny*(rad//3))
    pygame.draw.circle(surf,(25,25,25),(ex,ey),rad//4)
    pygame.draw.circle(surf,(217,217,217),(int(ex+nx*(rad//8)),int(ey+ny*(rad//8))),rad//12)
    if frm==1: draw_leaf(surf,x,y,rad)
    elif frm==2: draw_flame(surf,x,y,rad)
    elif frm==3: draw_drop_cr(surf,x,y,rad)

def draw_item_pickup(surf,cx,cy,inner,glow,label,collected):
    if collected: return
    pygame.draw.circle(surf,glow,(cx,cy),14);pygame.draw.circle(surf,inner,(cx,cy),11)
    lb=font_tiny.render(label,True,(240,240,200))
    surf.blit(lb,(cx-lb.get_width()//2,cy+16))

def draw_lava(surf,rect,t):
    pygame.draw.rect(surf,(200,40,0),rect)
    cols=[(255,120,0),(255,80,0),(230,60,0),(255,160,30)]
    for i in range(8):
        bx=rect.left+(i*rect.width//7)+int(math.sin(t*2+i)*5)
        by=rect.top+int(i*rect.height/7.5)+int(math.cos(t*1.5+i*0.7)*10)
        br=7+int(math.sin(t+i*1.2)*3)
        pygame.draw.circle(surf,cols[i%4],(bx,by),br)
    pygame.draw.rect(surf,(255,60,0),rect,3)

def draw_water(surf,rect,t):
    pygame.draw.rect(surf,(18,65,155),rect)
    deep=pygame.Rect(rect.left,rect.centery,rect.width,rect.height//2)
    pygame.draw.rect(surf,(12,50,120),deep)
    for i in range(6):
        wy=rect.top+int(rect.height*(i+1)/7);ox=int(math.sin(t*1.4+i*0.9)*14)
        pygame.draw.line(surf,(55,125,215),(rect.left+8+ox,wy),(rect.right-8+ox,wy),2)

def draw_puddle(surf,rect,t,seed=0):
    pygame.draw.rect(surf,(18,65,155),rect)
    for i in range(4):
        wy=rect.top+int(rect.height*(i+1)/5);ox=int(math.sin(t*1.5+i*0.8+seed)*8)
        pygame.draw.line(surf,(55,125,215),(rect.left+4+ox,wy),(rect.right-4+ox,wy),2)
    pygame.draw.rect(surf,(40,100,200),rect,2)

def draw_bridge(surf):
    for pl in (BR_L, BR_R):
        pygame.draw.rect(surf,WOOD_C,pl)
        for i in range(3):
            pygame.draw.line(surf,(90,55,20),(pl.left,pl.top+i*12+4),(pl.right,pl.top+i*12+4),1)
        pygame.draw.rect(surf,(80,50,20),pl,2)
    pygame.draw.line(surf,(80,50,20),(BRG1,BRY),(BRG1,BRY+BRH),3)
    pygame.draw.line(surf,(80,50,20),(BRG2,BRY),(BRG2,BRY+BRH),3)
    for gx in range(BRG1+8,BRG2-8,18):
        gy=BRY+int(math.sin((gx-BRG1)*0.18)*6)+BRH//2
        pygame.draw.circle(surf,(60,40,15),(gx,gy),2)

def draw_back(surf):
    pygame.draw.rect(surf,RED_C,BACK_RECT,border_radius=4)
    pygame.draw.rect(surf,(240,60,60),BACK_RECT,1,border_radius=4)
    lb=font_tiny.render("BACK",True,(255,220,220))
    surf.blit(lb,(BACK_RECT.centerx-lb.get_width()//2,BACK_RECT.centery-lb.get_height()//2))

def draw_portal(surf,rect,color):
    pygame.draw.rect(surf,color,rect,border_radius=4)
    g=tuple(min(255,c+55) for c in color)
    pygame.draw.rect(surf,g,rect,3,border_radius=4)
    inner=rect.inflate(-8,-8)
    s=pygame.Surface((inner.width,inner.height),pygame.SRCALPHA)
    s.fill((*g,40))
    surf.blit(s,inner.topleft)

def draw_throne(surf,rect,t):
    x,y,w,h=rect
    pygame.draw.rect(surf,(80,60,20),(x,y+h-22,w,22))
    pygame.draw.rect(surf,(100,75,25),(x+6,y+h-42,w-12,26))
    pygame.draw.rect(surf,(90,68,22),(x+9,y,w-18,h-37))
    pygame.draw.rect(surf,(100,75,25),(x,y+h-58,13,22))
    pygame.draw.rect(surf,(100,75,25),(x+w-13,y+h-58,13,22))
    gx=x+w//2; gy=y
    pygame.draw.polygon(surf,GOLD_C,[(gx-13,gy),(gx,gy-17),(gx+13,gy),(gx+9,gy-9),(gx-9,gy-9)])
    pygame.draw.rect(surf,GOLD_C,(x+9,y,w-18,h-37),2)
    pygame.draw.rect(surf,GOLD_C,(x,y+h-42,w,6))
    glow=int(abs(math.sin(t*2))*45)+55
    s=pygame.Surface((w+10,h+10),pygame.SRCALPHA)
    pygame.draw.rect(s,(glow,glow-20,0,60),(0,0,w+10,h+10),border_radius=6)
    surf.blit(s,(x-5,y-5))

def draw_torch(surf,cx,cy,t,seed=0):
    pygame.draw.rect(surf,(65,45,20),(cx-4,cy-10,8,18))
    pygame.draw.rect(surf,(100,70,30),(cx-4,cy-10,8,18),1)
    for ox,oy,rr,c in[(-3,0,4,(255,80,0)),(0,-6,5,(255,160,0)),(3,0,4,(220,60,0))]:
        flicker=int(math.sin(t*7+seed+ox)*2)
        pygame.draw.circle(surf,c,(cx+ox,cy-12+oy+flicker),rr)
    halo=pygame.Surface((28,28),pygame.SRCALPHA)
    alpha=int(abs(math.sin(t*3+seed))*30)+20
    pygame.draw.circle(halo,(255,200,80,alpha),(14,14),13)
    surf.blit(halo,(cx-14,cy-20))

def draw_vine_wall(surf, top, gap, bot, opened, t):
    for seg in (top, bot):
        pygame.draw.rect(surf, WALL_C, seg)
        pygame.draw.line(surf,WALL_LIT,seg.topleft,seg.topright,2)
        pygame.draw.line(surf,(50,50,50),seg.bottomleft,seg.bottomright,2)
        for i in range(0, seg.height, 18):
            vx=seg.left+seg.width//2+int(math.sin(t*0.8+i*0.4)*4)
            pygame.draw.circle(surf,VINE_GRN,(vx,seg.top+i+9),3)
    gcol=VINE_GRN if opened else WALL_C
    pygame.draw.rect(surf,gcol,gap)
    if opened:
        pygame.draw.line(surf,(60,200,60),gap.topleft,gap.bottomright,1)

def draw_hp(surf,hp,hp_max):
    bw,bh=150,16; bx=WIDTH-bw-10; by=10
    pygame.draw.rect(surf,(50,10,10),(bx,by,bw,bh),border_radius=3)
    fc=(220,40,40) if hp<=3 else (190,75,75)
    pygame.draw.rect(surf,fc,(bx,by,int(bw*max(0,hp)/hp_max),bh),border_radius=3)
    pygame.draw.rect(surf,(180,90,90),(bx,by,bw,bh),2,border_radius=3)
    lb=font_tiny.render(f"HP {hp}/{hp_max}",True,(255,200,200))
    surf.blit(lb,(bx+bw//2-lb.get_width()//2,by+1))

def draw_atk_bar(surf, ready_frac):
    pygame.draw.rect(surf,(20,20,40),ATK_BAR_RECT,border_radius=3)
    col=(80,200,255) if ready_frac>=1.0 else (40,100,180)
    fill=int(ATK_BAR_RECT.width*min(1.0,ready_frac))
    pygame.draw.rect(surf,col,(ATK_BAR_RECT.x,ATK_BAR_RECT.y,fill,ATK_BAR_RECT.height),border_radius=3)
    pygame.draw.rect(surf,(80,120,160),ATK_BAR_RECT,1,border_radius=3)
    lb=font_tiny.render("ATK",True,(140,180,220))
    surf.blit(lb,(ATK_BAR_RECT.x+2,ATK_BAR_RECT.bottom+1))

def draw_score(surf,sc):
    lb=font_small.render(f"Score: {sc}",True,(220,220,100))
    surf.blit(lb,(WIDTH-lb.get_width()-10,30))

def draw_hud_slots(surf,has_v,has_m,has_d,frm):
    owned={1:has_v,2:has_m,3:has_d}
    for sl in HUD_SLOTS:
        r=sl["rect"]; f=sl["form"]
        active=frm==f
        bg=(75,58,38) if active else (45,36,26)
        pygame.draw.rect(surf,bg,r,border_radius=5)
        bc=(160,130,80) if active else (80,65,45)
        pygame.draw.rect(surf,bc,r,2,border_radius=5)
        cx,cy=r.centerx,r.centery-4
        if owned[f]:
            if f==1:
                pts=[(cx,cy-7),(cx+7,cy),(cx,cy+7),(cx-7,cy)]
                pygame.draw.polygon(surf,(50,180,50),pts)
                pygame.draw.line(surf,(20,100,20),(cx,cy-6),(cx,cy+6),1)
            elif f==2:
                for ox,oy,rr,c in[(-4,2,4,(255,80,0)),(0,-2,5,(255,160,0)),(4,2,4,(255,80,0))]:
                    pygame.draw.circle(surf,c,(cx+ox,cy+oy),rr)
            elif f==3:
                pygame.draw.circle(surf,(80,180,255),(cx,cy),7)
                pygame.draw.circle(surf,(40,120,220),(cx,cy),7,1)
        num=font_tiny.render(sl["key"],True,(180,160,120))
        surf.blit(num,(r.centerx-num.get_width()//2,r.bottom+2))

def draw_hint_btn(surf,visible):
    col=(60,50,38) if visible else (38,32,24)
    pygame.draw.rect(surf,col,HINT_BTN,border_radius=4)
    pygame.draw.rect(surf,(100,88,65),HINT_BTN,1,border_radius=4)
    lb=font_tiny.render("Hint "+("ON" if visible else "OFF"),True,(200,178,130))
    surf.blit(lb,(HINT_BTN.centerx-lb.get_width()//2,HINT_BTN.centery-lb.get_height()//2))

def draw_hint(surf,text,color=(220,215,170)):
    if not hint_visible: return
    hy=HEIGHT-WALL_H+(WALL_H-font_tiny.get_height())//2
    bg=pygame.Surface((len(text)*7+20,20),pygame.SRCALPHA)
    bg.fill((0,0,0,90))
    bx=WIDTH//2-bg.get_width()//2
    surf.blit(bg,(bx,hy-1))
    s=font_tiny.render(text,True,color)
    surf.blit(s,(WIDTH//2-s.get_width()//2,hy))

def draw_pause_btn(surf):
    pygame.draw.rect(surf,(45,45,45),PAUSE_BTN,border_radius=4)
    pygame.draw.rect(surf,(110,110,110),PAUSE_BTN,1,border_radius=4)
    bx,by=PAUSE_BTN.x+10,PAUSE_BTN.y+8
    pygame.draw.rect(surf,(200,200,200),(bx,by,5,20))
    pygame.draw.rect(surf,(200,200,200),(bx+12,by,5,20))
    lb=font_tiny.render("P",True,(160,160,160))
    surf.blit(lb,(PAUSE_BTN.centerx-lb.get_width()//2,PAUSE_BTN.bottom+2))

def draw_pause_overlay(surf):
    ov=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA); ov.fill((0,0,0,165))
    surf.blit(ov,(0,0))
    pw,ph=340,265; pr=pygame.Rect(WIDTH//2-pw//2,HEIGHT//2-ph//2,pw,ph)
    pygame.draw.rect(surf,(75,52,28),pr,border_radius=10)
    pygame.draw.rect(surf,(140,100,58),pr,3,border_radius=10)
    tl=font_big.render("PAUSED",True,(230,200,138)); surf.blit(tl,(pr.centerx-tl.get_width()//2,pr.y+16))
    vl=font_med.render(f"Volume:  {audio_volume} / 5",True,(210,183,138))
    surf.blit(vl,(pr.centerx-vl.get_width()//2,pr.y+68))
    for i in range(1,6):
        br=pygame.Rect(pr.x+28+(i-1)*54,pr.y+100,46,28)
        bc=(105,78,42) if i==audio_volume else (52,38,22)
        pygame.draw.rect(surf,bc,br,border_radius=4);pygame.draw.rect(surf,(160,128,78),br,1,border_radius=4)
        bl=font_med.render(str(i),True,(222,195,148));surf.blit(bl,(br.centerx-bl.get_width()//2,br.centery-bl.get_height()//2))
    res=pygame.Rect(pr.centerx-72,pr.y+152,144,38)
    pygame.draw.rect(surf,(52,95,52),res,border_radius=6);pygame.draw.rect(surf,(95,158,95),res,2,border_radius=6)
    rl=font_med.render("Resume",True,(175,238,175));surf.blit(rl,(res.centerx-rl.get_width()//2,res.centery-rl.get_height()//2))
    return pr,res

def draw_died_screen(surf,respawn_left,easy):
    ov=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA); ov.fill((0,0,0,205)); surf.blit(ov,(0,0))
    tl=font_title.render("YOU DIED",True,(200,30,30)); surf.blit(tl,(WIDTH//2-tl.get_width()//2,HEIGHT//2-105))
    sl=font_med.render(f"Score: {score}",True,(200,178,78)); surf.blit(sl,(WIDTH//2-sl.get_width()//2,HEIGHT//2-44))
    buttons={}
    if easy and respawn_left>0:
        rb=pygame.Rect(WIDTH//2-175,HEIGHT//2+18,152,46)
        pygame.draw.rect(surf,(95,58,18),rb,border_radius=6);pygame.draw.rect(surf,(178,118,58),rb,2,border_radius=6)
        rl=font_med.render("Revive",True,(240,208,158));surf.blit(rl,(rb.centerx-rl.get_width()//2,rb.centery-rl.get_height()//2))
        at=font_tiny.render(f"attempts: {respawn_left}",True,(178,148,98));surf.blit(at,(rb.centerx-at.get_width()//2,rb.bottom+3))
        buttons["revive"]=rb
    mb=pygame.Rect(WIDTH//2+22 if (easy and respawn_left>0) else WIDTH//2-75,HEIGHT//2+18,152,46)
    pygame.draw.rect(surf,(48,28,28),mb,border_radius=6);pygame.draw.rect(surf,(138,58,58),mb,2,border_radius=6)
    ml=font_med.render("Menu",True,(240,178,178));surf.blit(ml,(mb.centerx-ml.get_width()//2,mb.centery-ml.get_height()//2))
    buttons["menu"]=mb; return buttons

def draw_win_screen(surf,sc):
    ov=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA); ov.fill((0,0,0,182)); surf.blit(ov,(0,0))
    tl=font_title.render("VICTORY!",True,GOLD_C); surf.blit(tl,(WIDTH//2-tl.get_width()//2,HEIGHT//2-115))
    sl=font_big.render("You claimed the throne!",True,(220,198,138)); surf.blit(sl,(WIDTH//2-sl.get_width()//2,HEIGHT//2-52))
    sc_lb=font_big.render(f"Final Score: {sc}",True,(195,218,95)); surf.blit(sc_lb,(WIDTH//2-sc_lb.get_width()//2,HEIGHT//2+8))
    mb=pygame.Rect(WIDTH//2-75,HEIGHT//2+68,152,46)
    pygame.draw.rect(surf,(48,68,28),mb,border_radius=6);pygame.draw.rect(surf,(98,158,58),mb,2,border_radius=6)
    ml=font_med.render("Menu",True,(198,238,158));surf.blit(ml,(mb.centerx-ml.get_width()//2,mb.centery-ml.get_height()//2))
    return mb

# ── Menu ──────────────────────────────────────────────────────────────────────
def draw_menu_bg(surf,t):
    surf.fill((16,11,7))
    for i in range(8):
        draw_torch(surf,int(WIDTH*(i+0.5)/8),int(HEIGHT*0.12),t,seed=i)
        draw_torch(surf,int(WIDTH*(i+0.5)/8),int(HEIGHT*0.88),t,seed=i+8)
    pygame.draw.rect(surf,(28,18,10),(0,HEIGHT//2-22,WIDTH,44))

def menu_button(surf,text,rect,hov=False):
    bg=(68,48,26) if hov else (48,33,16)
    pygame.draw.rect(surf,bg,rect,border_radius=7)
    bc=(178,138,68) if hov else (118,88,38)
    pygame.draw.rect(surf,bc,rect,2,border_radius=7)
    lb=font_big.render(text,True,(228,202,138) if hov else (188,162,98))
    surf.blit(lb,(rect.centerx-lb.get_width()//2,rect.centery-lb.get_height()//2))

def run_menu(surf,t,mx,my,clicked):
    global menu_screen,gs,hint_visible,audio_volume,paused
    draw_menu_bg(surf,t)
    tl=font_title.render("Dungeon Larper",True,GOLD_C)
    surf.blit(tl,(WIDTH//2-tl.get_width()//2,55))
    sub=font_tiny.render("A slime's odyssey",True,(138,118,78))
    surf.blit(sub,(WIDTH//2-sub.get_width()//2,118))
    result=None

    if menu_screen=="main":
        for label,ry in[("Play",210),("Settings",275),("Credits",340)]:
            r=pygame.Rect(300,ry,200,50); hov=r.collidepoint(mx,my)
            menu_button(surf,label,r,hov)
            if clicked and hov:
                if label=="Play": menu_screen="diff"
                elif label=="Settings": menu_screen="settings"
                elif label=="Credits": menu_screen="credits"

    elif menu_screen=="diff":
        tl2=font_med.render("Choose Difficulty",True,(208,182,138)); surf.blit(tl2,(WIDTH//2-tl2.get_width()//2,185))
        for label,diff,ry in[("Easy","easy",235),("Normal","normal",295)]:
            r=pygame.Rect(278,ry,242,48); hov=r.collidepoint(mx,my)
            menu_button(surf,label,r,hov)
            dm={"easy":"Enemy dmg ÷2 | Hints on | 1 Revive","normal":"Standard — no hints, no revive"}
            dl=font_tiny.render(dm[diff],True,(148,128,88)); surf.blit(dl,(r.right+10,r.centery-dl.get_height()//2))
            if clicked and hov:
                gs=make_game_state(diff); hint_visible=(diff=="easy"); paused=False; result="play"
        back=pygame.Rect(18,558,102,32); menu_button(surf,"Back",back,back.collidepoint(mx,my))
        if clicked and back.collidepoint(mx,my): menu_screen="main"

    elif menu_screen=="settings":
        tl2=font_med.render("Settings",True,(208,182,138)); surf.blit(tl2,(WIDTH//2-tl2.get_width()//2,185))
        vl=font_med.render(f"Audio Volume:  {audio_volume} / 5",True,(208,182,138)); surf.blit(vl,(WIDTH//2-vl.get_width()//2,238))
        for i in range(1,6):
            br=pygame.Rect(WIDTH//2-132+(i-1)*54,278,46,32)
            bc=(100,74,38) if i==audio_volume else (52,38,22)
            pygame.draw.rect(surf,bc,br,border_radius=4); pygame.draw.rect(surf,(158,128,78),br,1,border_radius=4)
            bl=font_med.render(str(i),True,(218,192,148)); surf.blit(bl,(br.centerx-bl.get_width()//2,br.centery-bl.get_height()//2))
            if clicked and br.collidepoint(mx,my): audio_volume=i
        back=pygame.Rect(18,558,102,32); menu_button(surf,"Back",back,back.collidepoint(mx,my))
        if clicked and back.collidepoint(mx,my): menu_screen="main"

    elif menu_screen=="credits":
        tl2=font_med.render("Credits",True,(208,182,138)); surf.blit(tl2,(WIDTH//2-tl2.get_width()//2,158))
        lines=["Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
               "Sed do eiusmod tempor incididunt ut labore et dolore magna.",
               "Ut enim ad minim veniam, quis nostrud exercitation ullamco.",
               "","Design & Code — You","","Music — Placeholder","Art — Placeholder"]
        for i,line in enumerate(lines):
            lb=font_small.render(line,True,(168,148,108)); surf.blit(lb,(WIDTH//2-lb.get_width()//2,206+i*26))
        back=pygame.Rect(18,558,102,32); menu_button(surf,"Back",back,back.collidepoint(mx,my))
        if clicked and back.collidepoint(mx,my): menu_screen="main"

    return result

# ── Game state factory ────────────────────────────────────────────────────────
def make_game_state(diff):
    return {
        "room":1,"player_x":60.0,"player_y":300.0,"dx":1,"dy":0,
        "player_hp":10,"player_hp_max":10,"player_iframe":0,
        "atk_last":0.0,
        "has_vine":False,"has_magma":False,"has_drop":False,"form":0,
        "thin_gap_vine":False,"r4_vine_open":False,
        "score":0,"sitting_since":None,
        # FIX: enemies reset properly — use lambdas to avoid shared state
        "r3_enemies":[Enemy(500,250,"drop"),Enemy(450,380,"drop")],
        "r4_enemies":[Enemy(155,HEIGHT//2,"fire"),Enemy(338,HEIGHT//2,"vine"),Enemy(618,HEIGHT//2,"drop")],
        "r5_boss":Enemy(WIDTH//2,HEIGHT//2,"fire",boss=True),
        "slashes":[],"e_was":False,"q_was":False,"f_was":False,
        "diff":diff,"respawn_left":1 if diff=="easy" else 0,
    }

# ── Room 4 contextual hint helper ─────────────────────────────────────────────
def get_r4_hint(s):
    """Returns the most relevant hint for the player's current R4 situation."""
    enemies = s["r4_enemies"]
    fire_alive = enemies[0].alive
    vine_alive = enemies[1].alive
    drop_alive = enemies[2].alive
    frm = s["form"]
    vine_open = s["r4_vine_open"]
    all_dead = not fire_alive and not vine_alive and not drop_alive

    if all_dead:
        return "All enemies defeated! Touch the portal on the right  →"
    if drop_alive and not vine_open:
        if frm == 1:
            return "[E] on the vine wall gap (center) to open it — then use [3] Drop for blue enemy"
        return "[1] Vine form  →  [E] on vine wall gap to unlock it"
    if fire_alive and frm != 2:
        return "[2] Fire form beats the RED enemy  |  [F] attack"
    if vine_alive and frm != 1:
        return "[1] Vine form beats the GREEN enemy  |  [F] attack"
    if drop_alive and frm != 3:
        return "[3] Drop form beats the BLUE enemy  |  [F] attack"
    if frm == 2:
        return "Fire form: cross the lava!  [F] attack red enemy"
    if frm == 3:
        return "Drop form: cross the puddles!  [F] attack blue enemy"
    return "Match your form color to the enemy — [F] attack  |  kill all to open portal"

# ═══════════════════════════════ MAIN LOOP ════════════════════════════════════
running=True
while running:
    t=time.time(); clock.tick(60)
    mx,my=pygame.mouse.get_pos(); clicked=False

    for event in pygame.event.get():
        if event.type==pygame.QUIT: running=False
        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1: clicked=True
        if event.type==pygame.KEYDOWN and game_mode=="play" and event.key==pygame.K_p:
            paused=not paused

    # ── MENU ──────────────────────────────────────────────────────────────────
    if game_mode=="menu":
        res=run_menu(screen,t,mx,my,clicked)
        if res=="play": game_mode="play"
        pygame.display.update(); continue

    # ── PLAY ──────────────────────────────────────────────────────────────────
    if game_mode=="play":
        s=gs
        easy     = s["diff"]=="easy"
        enemy_dmg= 0.5 if easy else 1
        hit_pts  = 5   if easy else 10

        if clicked and PAUSE_BTN.collidepoint(mx,my): paused=not paused
        if clicked and HINT_BTN.collidepoint(mx,my):  hint_visible=not hint_visible

        if not paused:
            keys=pygame.key.get_pressed()
            ndx=ndy=0; moving=False
            if keys[pygame.K_a]: s["player_x"]-=3;ndx-=1;moving=True
            if keys[pygame.K_d]: s["player_x"]+=3;ndx+=1;moving=True
            if keys[pygame.K_w]: s["player_y"]-=3;ndy-=1;moving=True
            if keys[pygame.K_s]: s["player_y"]+=3;ndy+=1;moving=True
            if ndx or ndy: s["dx"],s["dy"]=ndx,ndy

            # form keys
            for key,frm,need in[(pygame.K_1,1,"has_vine"),(pygame.K_2,2,"has_magma"),(pygame.K_3,3,"has_drop")]:
                if keys[key] and s[need]: s["form"]=frm
            if keys[pygame.K_0]: s["form"]=0

            # Q cycle
            q_now=keys[pygame.K_q]
            if q_now and not s["q_was"]:
                avail=[0]+[f for f,k in[(1,"has_vine"),(2,"has_magma"),(3,"has_drop")] if s[k]]
                if len(avail)>1:
                    idx=avail.index(s["form"]) if s["form"] in avail else 0
                    s["form"]=avail[(idx+1)%len(avail)]
            s["q_was"]=q_now

            # E interact
            e_now=keys[pygame.K_e]
            if e_now and not s["e_was"]:
                pcr=pygame.Rect(s["player_x"]-RADIUS,s["player_y"]-RADIUS,RADIUS*2,RADIUS*2)
                rm2=s["room"]
                if rm2==1 and not s["has_vine"]  and pcr.colliderect(VINE_RECT.inflate(20,20)):  s["has_vine"]=True
                if rm2==2 and not s["has_magma"] and pcr.colliderect(MAGMA_RECT.inflate(20,20)): s["has_magma"]=True
                if rm2==2 and s["form"]==1 and not s["thin_gap_vine"] and pcr.colliderect(r2_wgap.inflate(30,30)):
                    s["thin_gap_vine"]=True
                if rm2==3 and not s["has_drop"]  and pcr.colliderect(DROP_RECT.inflate(20,20)):  s["has_drop"]=True
                # FIX: Room 4 vine wall — E in Vine form opens the vine wall gap
                if rm2==4 and s["form"]==1 and not s["r4_vine_open"] and pcr.colliderect(r4_vgap.inflate(30,30)):
                    s["r4_vine_open"]=True
            s["e_was"]=e_now

            # F attack — with cooldown
            atk_ready = (t - s["atk_last"]) >= ATK_CD_MAX
            f_now=keys[pygame.K_f]
            if f_now and not s["f_was"] and atk_ready:
                s["atk_last"]=t
                s["slashes"].append(Slash(s["player_x"],s["player_y"],math.atan2(s["dy"],s["dx"]),SLASH_C[s["form"]]))
                aen=(s["r3_enemies"] if s["room"]==3 else
                     s["r4_enemies"] if s["room"]==4 else
                     [s["r5_boss"]]  if s["room"]==5 else [])
                for en in aen:
                    if not en.alive: continue
                    if math.hypot(en.x-s["player_x"],en.y-s["player_y"])<RADIUS+en.r+44:
                        if en.can_hit(s["form"]):
                            en.hp-=1; en.hit_flash=8
                            if en.hp<=0: s["score"]+=20
            s["f_was"]=f_now

            # clamp
            wt=R5_WALL_H if s["room"]==5 else WALL_H
            s["player_x"]=max(RADIUS,min(WIDTH-RADIUS,s["player_x"]))
            s["player_y"]=max(wt+RADIUS,min(HEIGHT-wt-RADIUS,s["player_y"]))

            # wall collision
            rm=s["room"]; px,py=s["player_x"],s["player_y"]; frm=s["form"]
            if rm==1:
                for w in room1_walls: px,py=resolve_wall(px,py,RADIUS,w)
            elif rm==2:
                for w in r2_solid: px,py=resolve_wall(px,py,RADIUS,w)
                if not s["thin_gap_vine"]: px,py=resolve_wall(px,py,RADIUS,r2_wgap)
                if frm!=2: px,py=resolve_wall(px,py,RADIUS,r2_lava)
            elif rm==3:
                if frm!=3: px,py=resolve_wall(px,py,RADIUS,r3_water)
            elif rm==4:
                if frm!=2: px,py=resolve_wall(px,py,RADIUS,r4_lava)
                px,py=resolve_wall(px,py,RADIUS,r4_vtop)
                px,py=resolve_wall(px,py,RADIUS,r4_vbot)
                if not s["r4_vine_open"]: px,py=resolve_wall(px,py,RADIUS,r4_vgap)
                if frm!=3:
                    px,py=resolve_wall(px,py,RADIUS,r4_pd1)
                    px,py=resolve_wall(px,py,RADIUS,r4_pd2)
            s["player_x"],s["player_y"]=px,py
            pcircle=pygame.Rect(px-RADIUS,py-RADIUS,RADIUS*2,RADIUS*2)

            # enemies AI + attack cooldown + player damage
            if s["player_iframe"]>0: s["player_iframe"]-=1
            aen=(s["r3_enemies"] if rm==3 else
                 s["r4_enemies"] if rm==4 else
                 [s["r5_boss"]]  if rm==5 else [])
            for en in aen:
                if en.alive:
                    en.update(px,py)
                    if en.touches(px,py) and en.atk_cd==0 and s["player_iframe"]==0:
                        s["player_hp"]=max(0,s["player_hp"]-enemy_dmg)
                        s["score"]=max(0,s["score"]-hit_pts)
                        s["player_iframe"]=50
                        en.atk_cd=55

            # throne win
            if rm==5:
                boss=s["r5_boss"]
                if not boss.alive and pcircle.colliderect(throne_rect):
                    if s["sitting_since"] is None: s["sitting_since"]=t
                    elif t-s["sitting_since"]>1.5:
                        s["score"]+=200; score=s["score"]; game_mode="win"
                else:
                    s["sitting_since"]=None

            if s["player_hp"]<=0: score=s["score"]; game_mode="died"

            if pcircle.colliderect(BACK_RECT) and rm>1:
                s["room"]-=1; s["player_x"],s["player_y"]=WIDTH-80,300

            # ── FIX: portal transition — Room 4→5 requires all enemies dead ──
            if pcircle.colliderect(PORTAL_RECT):
                if rm==1: s["room"]=2;s["player_x"],s["player_y"]=60,300
                elif rm==2: s["room"]=3;s["player_x"],s["player_y"]=60,300
                elif rm==3: s["room"]=4;s["player_x"],s["player_y"]=60,300
                elif rm==4:
                    # Require all R4 enemies dead AND vine wall opened (player must engage both sides)
                    r4_all_dead = all(not e.alive for e in s["r4_enemies"])
                    if r4_all_dead:
                        s["room"]=5;s["player_x"],s["player_y"]=60,300

            s["slashes"]=[sl for sl in s["slashes"] if sl.alive]

        # ── DRAW ──────────────────────────────────────────────────────────────
        rm=s["room"]; frm=s["form"]; px,py=s["player_x"],s["player_y"]
        moving2=s["dx"]!=0 or s["dy"]!=0
        P_col=P_COLS[frm]["move"] if moving2 else P_COLS[frm]["stop"]
        has_v,has_m,has_d=s["has_vine"],s["has_magma"],s["has_drop"]

        if rm==1:
            draw_floor(screen,BG,t,1)
            for w in room1_walls: draw_wall_block(screen,w)
            draw_border_walls(screen,1)
            draw_item_pickup(screen,*VINE_POS,(60,179,60),(20,80,20),"Vine",has_v)
            draw_portal(screen,PORTAL_RECT,GREEN_C)
            draw_back(screen)
            for sl in s["slashes"]: sl.draw(screen)
            draw_slime(screen,P_col,px,py,RADIUS,s["dx"],s["dy"],frm,s["player_iframe"])
            draw_hint(screen,"Reach the green portal  |  [E] pick up Vine")

        elif rm==2:
            draw_floor(screen,(18,18,55),t,2)
            for w in r2_solid: draw_wall_block(screen,w)
            draw_vine_wall(screen,r2_wtop,r2_wgap,r2_wbot,s["thin_gap_vine"],t)
            draw_border_walls(screen,2)
            draw_lava(screen,r2_lava,t)
            draw_item_pickup(screen,*MAGMA_POS,(220,80,0),(120,30,0),"Magma",has_m)
            draw_portal(screen,PORTAL_RECT,YELLOW_C)
            draw_back(screen)
            for sl in s["slashes"]: sl.draw(screen)
            draw_slime(screen,P_col,px,py,RADIUS,s["dx"],s["dy"],frm,s["player_iframe"])
            if not s["thin_gap_vine"]: draw_hint(screen,"Press E on the vine wall  (Vine form)")
            elif frm!=2: draw_hint(screen,"Fire form lets you cross the lava!")
            else: draw_hint(screen,"Walk through the lava to next room!")

        elif rm==3:
            draw_floor(screen,(8,8,22),t,3)
            draw_water(screen,r3_water,t)
            draw_bridge(screen)
            draw_border_walls(screen,3)
            draw_item_pickup(screen,*DROP_POS,(60,140,255),(20,60,160),"Droplet",has_d)
            for en in s["r3_enemies"]:
                if en.alive: en.draw(screen)
            for sl in s["slashes"]: sl.draw(screen)
            draw_portal(screen,PORTAL_RECT,(100,200,255))
            draw_back(screen)
            draw_slime(screen,P_col,px,py,RADIUS,s["dx"],s["dy"],frm,s["player_iframe"])
            if not has_d: draw_hint(screen,"[E] pick up Droplet — Droplet form hurts blue enemies")
            elif frm!=3: draw_hint(screen,"[3] Droplet form  [F] Attack")
            else: draw_hint(screen,"[F] Attack blue enemies!")

        elif rm==4:
            draw_floor(screen,(14,7,7),t,4)
            draw_border_walls(screen,4)
            draw_lava(screen,r4_lava,t)
            draw_vine_wall(screen,r4_vtop,r4_vgap,r4_vbot,s["r4_vine_open"],t)
            draw_puddle(screen,r4_pd1,t,0)
            draw_puddle(screen,r4_pd2,t,3)
            for en in s["r4_enemies"]:
                if en.alive: en.draw(screen)
            all_dead=all(not e.alive for e in s["r4_enemies"])
            pcol=(175,175,48) if all_dead else (55,55,55)
            draw_portal(screen,PORTAL_RECT,pcol)
            draw_back(screen)
            for sl in s["slashes"]: sl.draw(screen)
            draw_slime(screen,P_col,px,py,RADIUS,s["dx"],s["dy"],frm,s["player_iframe"])
            # FIX: always show contextual Room 4 hint
            draw_hint(screen, get_r4_hint(s))

        elif rm==5:
            draw_floor(screen,(9,5,3),t,5)
            pygame.draw.rect(screen, CARPET_C, r5_carpet)
            pygame.draw.rect(screen, (200,30,30), r5_carpet, 2)
            draw_border_walls(screen,5)
            for cx2,cy2 in r5_torches_top: draw_torch(screen,cx2,cy2,t,seed=cx2)
            for cx2,cy2 in r5_torches_bot: draw_torch(screen,cx2,cy2,t,seed=cx2+1)
            boss=s["r5_boss"]
            if boss.alive: boss.draw(screen)
            draw_throne(screen,throne_rect,t)
            draw_back(screen)
            for sl in s["slashes"]: sl.draw(screen)
            draw_slime(screen,P_col,px,py,RADIUS,s["dx"],s["dy"],frm,s["player_iframe"])
            if boss.alive:
                # FIX: boss hint — tell player the boss cycles forms and which form to use
                kind_label = {"fire":"[2] Fire","vine":"[1] Vine","drop":"[3] Drop"}
                draw_hint(screen, f"Boss changes form! Use {kind_label[boss.kind]} form now  |  [F] attack")
            else:
                lb=font_med.render("Sit on the throne!",True,GOLD_C)
                screen.blit(lb,(WIDTH//2-lb.get_width()//2,HEIGHT//2-80))

        # ── Shared HUD ────────────────────────────────────────────────────────
        draw_hud_slots(screen,has_v,has_m,has_d,frm)
        draw_hint_btn(screen,hint_visible)
        draw_hp(screen,int(s["player_hp"]),s["player_hp_max"])
        atk_frac=min(1.0,(t-s["atk_last"])/ATK_CD_MAX)
        draw_atk_bar(screen,atk_frac)
        draw_score(screen,int(s["score"]))
        draw_pause_btn(screen)

        if paused:
            pr,res_btn=draw_pause_overlay(screen)
            if clicked:
                if res_btn.collidepoint(mx,my): paused=False
                for i in range(1,6):
                    br=pygame.Rect(pr.x+28+(i-1)*54,pr.y+100,46,28)
                    if br.collidepoint(mx,my): audio_volume=i

        pygame.display.update(); continue

    # ── DIED ──────────────────────────────────────────────────────────────────
    if game_mode=="died":
        screen.fill((10,5,5))
        btns=draw_died_screen(screen,gs["respawn_left"] if gs else 0,gs["diff"]=="easy" if gs else False)
        if clicked:
            if "revive" in btns and btns["revive"].collidepoint(mx,my):
                gs["player_hp"]=gs["player_hp_max"]; gs["player_iframe"]=120
                gs["respawn_left"]-=1; game_mode="play"
            if btns["menu"].collidepoint(mx,my):
                game_mode="menu"; gs=None; menu_screen="main"
        pygame.display.update(); continue

    # ── WIN ───────────────────────────────────────────────────────────────────
    if game_mode=="win":
        screen.fill((8,6,2))
        mb=draw_win_screen(screen,score)
        if clicked and mb.collidepoint(mx,my):
            game_mode="menu"; gs=None; menu_screen="main"
        pygame.display.update(); continue

pygame.quit()
