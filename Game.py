    import pygame
    import math
    import time

    pygame.init()

    WIDTH  = 800
    HEIGHT = 600
    WALL_H = 150
    RADIUS = 20

    # ── Colors ────────────────────────────────────────────────────────────────────
    BG         = (42,  42,  42)
    WALL       = (80,  80,  80)
    RED_COL    = (200,  30,  30)
    GREEN      = (0,  220,   0)
    YELLOW     = (255, 220,   0)
    VINE_GREEN = (34,  139,  34)
    WOOD_COL   = (110,  70,  30)

    P_NORMAL_STOP = (0,   191,   0)
    P_NORMAL_MOVE = (100, 200, 100)
    P_VINE_STOP   = (34,  120,  34)
    P_VINE_MOVE   = (60,  160,  60)
    P_FIRE_STOP   = (255, 200,  30)
    P_FIRE_MOVE   = (255, 230,  80)
    P_DROP_STOP   = (40,  120, 220)
    P_DROP_MOVE   = (80,  160, 255)

    # slash color per form
    SLASH_COLORS = {0:(180,255,180), 1:(30,120,30), 2:(255,180,30), 3:(60,160,255)}

    # enemy visual colors and which form kills them
    ENEMY_KINDS = {
        "fire": {"body":(220,60,40),  "outline":(160,30,10), "eye":(80,10,0),   "kills":2},
        "vine": {"body":(50,160,50),  "outline":(20,100,20), "eye":(10,50,10),  "kills":1},
        "drop": {"body":(100,180,255),"outline":(60,120,200),"eye":(20,20,80),  "kills":3},
    }

    screen     = pygame.display.set_mode((WIDTH, HEIGHT))
    clock      = pygame.time.Clock()
    pygame.display.set_caption("Dungeon Larper")
    font       = pygame.font.SysFont(None, 22)
    font_small = pygame.font.SysFont(None, 18)

    top_wall    = pygame.Rect(0, 0,              WIDTH, WALL_H)
    bottom_wall = pygame.Rect(0, HEIGHT-WALL_H,  WIDTH, WALL_H)

    # ── Room 1 walls ──────────────────────────────────────────────────────────────
    room1_walls = [
        pygame.Rect(200, WALL_H,             30, 120),
        pygame.Rect(200, HEIGHT-WALL_H-120,  30, 120),
        pygame.Rect(450, WALL_H,            500, 100),
        pygame.Rect(450, HEIGHT-WALL_H-100, 500, 100),
        pygame.Rect(320, 230,                80,  30),
        pygame.Rect(320, HEIGHT-230-30,      80,  30),
    ]

    # ── Room 2 ────────────────────────────────────────────────────────────────────
    FIRST_X=150; FIRST_THICK=60; THIN_THICK=30
    FIRST_TOP_Y=WALL_H; FIRST_H=150
    GAP_H=50; GAP_Y=FIRST_TOP_Y+(FIRST_H//2)-(GAP_H//2)

    first_wall_top    = pygame.Rect(FIRST_X, FIRST_TOP_Y,  FIRST_THICK, GAP_Y-FIRST_TOP_Y)
    first_wall_gap    = pygame.Rect(FIRST_X, GAP_Y,        THIN_THICK,  GAP_H)
    first_wall_bottom = pygame.Rect(FIRST_X, GAP_Y+GAP_H,  FIRST_THICK, (FIRST_TOP_Y+FIRST_H)-(GAP_Y+GAP_H))
    first_wall_mir    = pygame.Rect(FIRST_X, HEIGHT-WALL_H-FIRST_H, FIRST_THICK, FIRST_H)
    room2_thin_gap    = first_wall_gap

    LAVA_X=380; LAVA_THICK=40
    lava_rect = pygame.Rect(LAVA_X, WALL_H, LAVA_THICK, HEIGHT-2*WALL_H)

    room2_solid_walls = [
        first_wall_top, first_wall_bottom, first_wall_mir,
        pygame.Rect(560, 200,        100, 30),
        pygame.Rect(560, HEIGHT-230, 100, 30),
    ]

    # ── Room 3 ────────────────────────────────────────────────────────────────────
    WATER_X1=220; WATER_X2=580
    water_rect = pygame.Rect(WATER_X1, WALL_H, WATER_X2-WATER_X1, HEIGHT-2*WALL_H)
    BRIDGE_Y=HEIGHT//2-15; BRIDGE_H=30
    BRIDGE_LEFT  = pygame.Rect(WATER_X1,       BRIDGE_Y, 100, BRIDGE_H)
    BRIDGE_RIGHT = pygame.Rect(WATER_X2-100,   BRIDGE_Y, 100, BRIDGE_H)
    BRIDGE_GAP_X1=WATER_X1+100; BRIDGE_GAP_X2=WATER_X2-100

    # ── Room 4 layout (left→right: lava zone | vine wall | water puddles) ─────────
    # Lava zone: x 60..260  (40px thick lava column)
    R4_LAVA_X=240; R4_LAVA_THICK=35
    r4_lava = pygame.Rect(R4_LAVA_X, WALL_H, R4_LAVA_THICK, HEIGHT-2*WALL_H)

    # Vine wall: x ~380, same style as room2 but no gap — player must use vine form
    R4_VINE_X=420; R4_VINE_THICK=30
    R4_VINE_GAP_H=55
    R4_VINE_GAP_Y=WALL_H+(HEIGHT-2*WALL_H)//2-R4_VINE_GAP_H//2
    r4_vine_top    = pygame.Rect(R4_VINE_X, WALL_H,         R4_VINE_THICK, R4_VINE_GAP_Y-WALL_H)
    r4_vine_gap    = pygame.Rect(R4_VINE_X, R4_VINE_GAP_Y,  R4_VINE_THICK, R4_VINE_GAP_H)  # vine-passable
    r4_vine_bottom = pygame.Rect(R4_VINE_X, R4_VINE_GAP_Y+R4_VINE_GAP_H, R4_VINE_THICK,
                                HEIGHT-WALL_H-(R4_VINE_GAP_Y+R4_VINE_GAP_H))

    # Water puddles: two rects right side
    r4_puddle1 = pygame.Rect(530, WALL_H+10,         120, (HEIGHT-2*WALL_H)//2-20)
    r4_puddle2 = pygame.Rect(530, HEIGHT//2+10,       120, (HEIGHT-2*WALL_H)//2-20)

    # Enemy spawn zones (center of each zone)
    R4_FIRE_SPAWN = (160,  HEIGHT//2)
    R4_VINE_SPAWN = (340,  HEIGHT//2)
    R4_DROP_SPAWN = (620,  HEIGHT//2)

    # ── Items ─────────────────────────────────────────────────────────────────────
    VINE_X=175;  VINE_Y=WALL_H+10
    VINE_RECT=pygame.Rect(VINE_X-12,VINE_Y-12,24,24)

    MAGMA_X=FIRST_X+FIRST_THICK+14; MAGMA_Y=FIRST_TOP_Y+FIRST_H-14
    MAGMA_RECT=pygame.Rect(MAGMA_X-12,MAGMA_Y-12,24,24)

    DROP_X=100; DROP_Y=HEIGHT//2
    DROP_RECT=pygame.Rect(DROP_X-12,DROP_Y-12,24,24)

    # ── Go-back + portal ──────────────────────────────────────────────────────────
    BACK_RECT   = pygame.Rect(10, HEIGHT//2-30, 25, 60)
    PORTAL_RECT = pygame.Rect(750, 262, 30, 75)

    # ── Slash ─────────────────────────────────────────────────────────────────────
    class Slash:
        def __init__(self, x, y, angle, color):
            self.x=x; self.y=y; self.angle=angle; self.color=color
            self.life=0.22; self.born=time.time()

        @property
        def alive(self): return (time.time()-self.born)<self.life

        def draw(self, surf):
            frac=(time.time()-self.born)/self.life
            length=38+int(frac*10); spread=0.55
            for off in(-spread,-spread*0.5,0,spread*0.5,spread):
                a=self.angle+off
                ex=int(self.x+math.cos(a)*length); ey=int(self.y+math.sin(a)*length)
                dim=tuple(int(c*(1-frac*0.7)) for c in self.color)
                pygame.draw.line(surf,dim,
                    (int(self.x+math.cos(a)*RADIUS),int(self.y+math.sin(a)*RADIUS)),
                    (ex,ey),max(1,3-int(frac*2)))

    # ── Enemy ─────────────────────────────────────────────────────────────────────
    class Enemy:
        SPEED=0.55
        def __init__(self, x, y, kind="drop"):
            self.x=float(x); self.y=float(y)
            self.r=18; self.hp=3; self.kind=kind
            self.hit_flash=0; self.dmg_cd=0

        @property
        def alive(self): return self.hp>0

        def update(self, px, py):
            ddx=px-self.x; ddy=py-self.y; dist=math.hypot(ddx,ddy)
            if dist>0: self.x+=(ddx/dist)*self.SPEED; self.y+=(ddy/dist)*self.SPEED
            self.x=max(self.r,min(WIDTH-self.r,self.x))
            self.y=max(WALL_H+self.r,min(HEIGHT-WALL_H-self.r,self.y))
            if self.hit_flash>0: self.hit_flash-=1
            if self.dmg_cd>0:    self.dmg_cd-=1

        def touches_player(self,px,py):
            return math.hypot(self.x-px,self.y-py)<self.r+RADIUS

        def can_be_hit_by(self, frm):
            return ENEMY_KINDS[self.kind]["kills"]==frm

        def draw(self, surf):
            info=ENEMY_KINDS[self.kind]
            col=(255,255,255) if self.hit_flash else info["body"]
            pygame.draw.circle(surf,col,(int(self.x),int(self.y)),self.r)
            pygame.draw.circle(surf,info["outline"],(int(self.x),int(self.y)),self.r,2)
            for ox in(-5,5):
                pygame.draw.circle(surf,info["eye"],(int(self.x)+ox,int(self.y)-3),3)
            for i in range(self.hp):
                pygame.draw.circle(surf,(255,80,80),(int(self.x)-8+i*8,int(self.y)-self.r-6),3)

    # ── Player state ──────────────────────────────────────────────────────────────
    player_x,player_y=60.0,300.0
    speed=3; room=1; dx,dy=1,0
    player_hp=10; player_hp_max=10; player_iframe=0
    has_vine=False; has_magma=False; has_drop=False
    form=0  # 0=normal 1=vine 2=fire 3=drop
    thin_gap_is_vine=False
    r4_vine_opened=False  # vine gap in room4 opened by vine form

    slashes=[]
    # room3 enemies (blue only)
    r3_enemies=[Enemy(500,250,"drop"),Enemy(450,380,"drop")]
    # room4 enemies (one of each kind)
    r4_enemies=[Enemy(*R4_FIRE_SPAWN,"fire"),Enemy(*R4_VINE_SPAWN,"vine"),Enemy(*R4_DROP_SPAWN,"drop")]

    e_was=q_was=f_was=False

    # ── Helpers ───────────────────────────────────────────────────────────────────
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

    def player_color(frm,moving):
        t={0:(P_NORMAL_MOVE,P_NORMAL_STOP),1:(P_VINE_MOVE,P_VINE_STOP),
        2:(P_FIRE_MOVE,P_FIRE_STOP),3:(P_DROP_MOVE,P_DROP_STOP)}
        return t[frm][0 if moving else 1]

    def draw_leaf(surf,x,y,radius):
        lx,ly=int(x),int(y-radius-8)
        pygame.draw.line(surf,(20,80,20),(int(x),int(y-radius+2)),(lx,ly+6),2)
        pts=[(lx,ly-5),(lx+6,ly),(lx,ly+6),(lx-6,ly)]
        pygame.draw.polygon(surf,(50,180,50),pts); pygame.draw.polygon(surf,(30,130,30),pts,1)
        pygame.draw.line(surf,(30,130,30),(lx,ly-4),(lx,ly+5),1)

    def draw_flame(surf,x,y,radius):
        cx,cy=int(x),int(y-radius-6)
        for ox,oy,r,col in[(-6,0,5,(255,80,0)),(0,-4,6,(255,160,0)),(6,0,5,(255,80,0))]:
            pygame.draw.circle(surf,col,(cx+ox,cy+oy),r)

    def draw_drop_crown(surf,x,y,radius):
        cx,cy=int(x),int(y-radius-6)
        pygame.draw.circle(surf,(80,180,255),(cx,cy),6)
        pygame.draw.circle(surf,(40,120,220),(cx,cy),6,1)

    def draw_slime(surf,color,x,y,radius,ddx,ddy,frm=0):
        dc=(255,255,255) if player_iframe>0 and player_iframe%4<2 else color
        pygame.draw.circle(surf,dc,(int(x),int(y)),radius)
        out={0:(134,218,134),1:(60,160,60),2:(255,200,80),3:(100,200,255)}
        pygame.draw.circle(surf,out[frm],(int(x),int(y)),radius,2)
        ln=math.hypot(ddx,ddy); nx,ny=(ddx/ln,ddy/ln) if ln else (1,0)
        ex=int(x+nx*(radius//3)); ey=int(y+ny*(radius//3))
        pygame.draw.circle(surf,(25,25,25),(ex,ey),radius//4)
        pygame.draw.circle(surf,(217,217,217),(int(ex+nx*(radius//8)),int(ey+ny*(radius//8))),radius//12)
        if frm==1: draw_leaf(surf,x,y,radius)
        elif frm==2: draw_flame(surf,x,y,radius)
        elif frm==3: draw_drop_crown(surf,x,y,radius)

    def draw_item(surf,cx,cy,inner,glow,label,collected):
        if collected: return
        pygame.draw.circle(surf,glow,(cx,cy),14); pygame.draw.circle(surf,inner,(cx,cy),11)
        lb=font_small.render(label,True,(240,240,200))
        surf.blit(lb,(cx-lb.get_width()//2,cy+16))

    def draw_lava(surf,rect,t):
        pygame.draw.rect(surf,(200,40,0),rect)
        cols=[(255,120,0),(255,80,0),(230,60,0),(255,160,30)]
        for i in range(6):
            bx=rect.left+(i*rect.width//5)+int(math.sin(t*2+i)*6)
            by=rect.top+int(i*rect.height/5.5)+int(math.cos(t*1.5+i*0.7)*10)
            br=8+int(math.sin(t+i*1.2)*3)
            pygame.draw.circle(surf,cols[i%4],(bx,by),br)
        pygame.draw.rect(surf,(255,60,0),rect,3)

    def draw_water(surf,rect,t):
        pygame.draw.rect(surf,(20,70,160),rect)
        for i in range(5):
            wy=rect.top+int(rect.height*(i+1)/6); ox=int(math.sin(t*1.5+i*0.8)*12)
            pygame.draw.line(surf,(60,130,220),(rect.left+10+ox,wy),(rect.right-10+ox,wy),2)

    def draw_puddle(surf,rect,t,seed=0):
        """Smaller water puddle."""
        pygame.draw.rect(surf,(20,70,160),rect)
        for i in range(3):
            wy=rect.top+int(rect.height*(i+1)/4); ox=int(math.sin(t*1.5+i*0.8+seed)*8)
            pygame.draw.line(surf,(60,130,220),(rect.left+4+ox,wy),(rect.right-4+ox,wy),2)
        pygame.draw.rect(surf,(40,100,200),rect,2)

    def draw_bridge(surf):
        pygame.draw.rect(surf,WOOD_COL,BRIDGE_LEFT); pygame.draw.rect(surf,(80,50,20),BRIDGE_LEFT,2)
        pygame.draw.rect(surf,WOOD_COL,BRIDGE_RIGHT); pygame.draw.rect(surf,(80,50,20),BRIDGE_RIGHT,2)
        pygame.draw.line(surf,(80,50,20),(BRIDGE_GAP_X1,BRIDGE_Y),(BRIDGE_GAP_X1,BRIDGE_Y+BRIDGE_H),3)
        pygame.draw.line(surf,(80,50,20),(BRIDGE_GAP_X2,BRIDGE_Y),(BRIDGE_GAP_X2,BRIDGE_Y+BRIDGE_H),3)

    def draw_hint(surf,text,color=(220,220,180)):
        s=font_small.render(text,True,color)
        surf.blit(s,(WIDTH//2-s.get_width()//2,HEIGHT-WALL_H+(WALL_H-s.get_height())//2))

    def draw_back(surf):
        pygame.draw.rect(surf,RED_COL,BACK_RECT)
        lb=font_small.render("BACK",True,(255,220,220))
        surf.blit(lb,(BACK_RECT.x+BACK_RECT.w//2-lb.get_width()//2,
                    BACK_RECT.y+BACK_RECT.h//2-lb.get_height()//2))

    def draw_hp(surf,hp,hp_max):
        bw,bh=160,16; bx=WIDTH-bw-10; by=10
        pygame.draw.rect(surf,(60,10,10),(bx,by,bw,bh))
        fc=(220,40,40) if hp<=3 else (200,80,80)
        pygame.draw.rect(surf,fc,(bx,by,int(bw*hp/hp_max),bh))
        pygame.draw.rect(surf,(200,100,100),(bx,by,bw,bh),2)
        lb=font_small.render(f"HP  {hp}/{hp_max}",True,(255,200,200))
        surf.blit(lb,(bx+bw//2-lb.get_width()//2,by+1))

    def draw_hud(surf,frm,items_owned):
        names={0:"Normal",1:"Vine",2:"Fire",3:"Droplet"}
        lines=["[WASD] Move  [E] Interact  [Q] Form  [F] Attack"]
        if items_owned:
            lines.append(f"Items: {', '.join(items_owned)}  |  Form: {names[frm]}")
        for i,l in enumerate(lines):
            surf.blit(font.render(l,True,(200,200,200)),(10,10+i*20))

    def draw_portal(surf,rect,color):
        pygame.draw.rect(surf,color,rect)
        # little glow border
        glow=tuple(min(255,c+60) for c in color)
        pygame.draw.rect(surf,glow,rect,3)

    def zone_label(surf, text, cx, color):
        """Small zone label near top of playfield."""
        lb=font_small.render(text,True,color)
        surf.blit(lb,(cx-lb.get_width()//2, WALL_H+6))

    # ── Main loop ─────────────────────────────────────────────────────────────────
    running=True
    while running:
        t=time.time(); clock.tick(60)

        for event in pygame.event.get():
            if event.type==pygame.QUIT: running=False

        keys=pygame.key.get_pressed()
        ndx=ndy=0; moving=False
        if keys[pygame.K_a]: player_x-=speed; ndx-=1; moving=True
        if keys[pygame.K_d]: player_x+=speed; ndx+=1; moving=True
        if keys[pygame.K_w]: player_y-=speed; ndy-=1; moving=True
        if keys[pygame.K_s]: player_y+=speed; ndy+=1; moving=True
        if ndx or ndy: dx,dy=ndx,ndy

        # Q: cycle form
        q_now=keys[pygame.K_q]
        if q_now and not q_was:
            avail=[0]
            if has_vine:  avail.append(1)
            if has_magma: avail.append(2)
            if has_drop:  avail.append(3)
            if len(avail)>1:
                idx=avail.index(form) if form in avail else 0
                form=avail[(idx+1)%len(avail)]
        q_was=q_now

        # E: interact
        e_now=keys[pygame.K_e]
        if e_now and not e_was:
            pcr=pygame.Rect(player_x-RADIUS,player_y-RADIUS,RADIUS*2,RADIUS*2)
            if room==1 and not has_vine  and pcr.colliderect(VINE_RECT.inflate(20,20)):  has_vine=True
            if room==2 and not has_magma and pcr.colliderect(MAGMA_RECT.inflate(20,20)): has_magma=True
            if room==2 and form==1 and not thin_gap_is_vine and pcr.colliderect(room2_thin_gap.inflate(30,30)):
                thin_gap_is_vine=True
            if room==3 and not has_drop  and pcr.colliderect(DROP_RECT.inflate(20,20)):  has_drop=True
            # Room4 vine gap — open with vine form
            if room==4 and form==1 and not r4_vine_opened and pcr.colliderect(r4_vine_gap.inflate(30,30)):
                r4_vine_opened=True
        e_was=e_now

        # F: attack
        f_now=keys[pygame.K_f]
        if f_now and not f_was:
            slashes.append(Slash(player_x,player_y,math.atan2(dy,dx),SLASH_COLORS[form]))
            active_enemies = r3_enemies if room==3 else r4_enemies if room==4 else []
            for en in active_enemies:
                if not en.alive: continue
                if math.hypot(en.x-player_x,en.y-player_y)<RADIUS+en.r+42:
                    if en.can_be_hit_by(form):
                        en.hp-=1; en.hit_flash=8
        f_was=f_now

        # Clamp
        player_x=max(RADIUS,min(WIDTH-RADIUS,player_x))
        player_y=max(WALL_H+RADIUS,min(HEIGHT-WALL_H-RADIUS,player_y))

        # Wall collision per room
        if room==1:
            for w in room1_walls: player_x,player_y=resolve_wall(player_x,player_y,RADIUS,w)
        elif room==2:
            for w in room2_solid_walls: player_x,player_y=resolve_wall(player_x,player_y,RADIUS,w)
            if not thin_gap_is_vine: player_x,player_y=resolve_wall(player_x,player_y,RADIUS,room2_thin_gap)
            if form!=2: player_x,player_y=resolve_wall(player_x,player_y,RADIUS,lava_rect)
        elif room==3:
            if form!=3: player_x,player_y=resolve_wall(player_x,player_y,RADIUS,water_rect)
        elif room==4:
            # lava blocks non-fire
            if form!=2: player_x,player_y=resolve_wall(player_x,player_y,RADIUS,r4_lava)
            # vine wall: solid top+bottom, gap only passable in vine form
            player_x,player_y=resolve_wall(player_x,player_y,RADIUS,r4_vine_top)
            player_x,player_y=resolve_wall(player_x,player_y,RADIUS,r4_vine_bottom)
            if not r4_vine_opened:
                player_x,player_y=resolve_wall(player_x,player_y,RADIUS,r4_vine_gap)
            # puddles block non-drop
            if form!=3:
                player_x,player_y=resolve_wall(player_x,player_y,RADIUS,r4_puddle1)
                player_x,player_y=resolve_wall(player_x,player_y,RADIUS,r4_puddle2)

        pcircle=pygame.Rect(player_x-RADIUS,player_y-RADIUS,RADIUS*2,RADIUS*2)

        # Enemy updates + player damage
        if player_iframe>0: player_iframe-=1
        active_en = r3_enemies if room==3 else r4_enemies if room==4 else []
        for en in active_en:
            if en.alive:
                en.update(player_x,player_y)
                if en.touches_player(player_x,player_y) and player_iframe==0:
                    player_hp=max(0,player_hp-1); player_iframe=50

        # Back platform
        if pcircle.colliderect(BACK_RECT) and room>1:
            room-=1; player_x,player_y=WIDTH-80,300

        # Forward portal
        if pcircle.colliderect(PORTAL_RECT):
            if room==1: room=2; player_x,player_y=60,300
            elif room==2: room=3; player_x,player_y=60,300
            elif room==3: room=4; player_x,player_y=60,300
            elif room==4:
                # only advance if all r4 enemies dead
                if all(not e.alive for e in r4_enemies):
                    room=5; player_x,player_y=60,300
            elif room==5: pass  # no room 6 yet

        P_color=player_color(form,moving)
        items_owned=(["Vine"] if has_vine else [])+(["Magma"] if has_magma else [])+(["Droplet"] if has_drop else [])
        slashes=[sl for sl in slashes if sl.alive]

        # ════════════════════════════ DRAW ══════════════════════════════════════════

        # ── Room 1 ──
        if room==1:
            screen.fill(BG)
            pygame.draw.rect(screen,WALL,top_wall); pygame.draw.rect(screen,WALL,bottom_wall)
            for w in room1_walls: pygame.draw.rect(screen,WALL,w)
            draw_item(screen,VINE_X,VINE_Y,(60,179,60),(20,80,20),"Vine",has_vine)
            draw_portal(screen,PORTAL_RECT,GREEN)
            draw_back(screen)
            for sl in slashes: sl.draw(screen)
            draw_slime(screen,P_color,player_x,player_y,RADIUS,dx,dy,form)
            draw_hint(screen,"Reach the green portal  |  [E] pick up Vine")
            draw_hud(screen,form,items_owned); draw_hp(screen,player_hp,player_hp_max)

        # ── Room 2 ──
        elif room==2:
            screen.fill((20,20,60))
            pygame.draw.rect(screen,WALL,top_wall); pygame.draw.rect(screen,WALL,bottom_wall)
            for w in room2_solid_walls: pygame.draw.rect(screen,WALL,w)
            pygame.draw.rect(screen,VINE_GREEN if thin_gap_is_vine else WALL,room2_thin_gap)
            draw_lava(screen,lava_rect,t)
            draw_item(screen,MAGMA_X,MAGMA_Y,(220,80,0),(120,30,0),"Magma",has_magma)
            draw_portal(screen,PORTAL_RECT,YELLOW)
            draw_back(screen)
            for sl in slashes: sl.draw(screen)
            draw_slime(screen,P_color,player_x,player_y,RADIUS,dx,dy,form)
            if not thin_gap_is_vine: draw_hint(screen,"Press E on the thin wall  (need Vine form)")
            elif form!=2: draw_hint(screen,"Fire form lets you cross the lava!")
            else: draw_hint(screen,"Walk through the lava to the next room!")
            draw_hud(screen,form,items_owned); draw_hp(screen,player_hp,player_hp_max)

        # ── Room 3 ──
        elif room==3:
            screen.fill((10,10,25))
            pygame.draw.rect(screen,WALL,top_wall); pygame.draw.rect(screen,WALL,bottom_wall)
            draw_water(screen,water_rect,t)
            draw_bridge(screen)
            draw_item(screen,DROP_X,DROP_Y,(60,140,255),(20,60,160),"Droplet",has_drop)
            for en in r3_enemies:
                if en.alive: en.draw(screen)
            for sl in slashes: sl.draw(screen)
            draw_portal(screen,PORTAL_RECT,(100,200,255))
            draw_back(screen)
            draw_slime(screen,P_color,player_x,player_y,RADIUS,dx,dy,form)
            if not has_drop: draw_hint(screen,"[E] pick up Droplet  — only Droplet form hurts blue enemies")
            elif form!=3:    draw_hint(screen,"[Q] switch to Droplet form  [F] to attack")
            else:            draw_hint(screen,"[F] Attack blue enemies with Droplet form!")
            draw_hud(screen,form,items_owned); draw_hp(screen,player_hp,player_hp_max)

        # ── Room 4 ──
        elif room==4:
            screen.fill((15,8,8))
            pygame.draw.rect(screen,WALL,top_wall); pygame.draw.rect(screen,WALL,bottom_wall)

            # Zone: lava (left)
            draw_lava(screen,r4_lava,t)
            zone_label(screen,"FIRE ZONE", R4_LAVA_X//2+30, (255,120,60))

            # Zone: vine wall (middle)
            pygame.draw.rect(screen,VINE_GREEN,r4_vine_top)
            pygame.draw.rect(screen,VINE_GREEN,r4_vine_bottom)
            vc=VINE_GREEN if r4_vine_opened else WALL
            pygame.draw.rect(screen,vc,r4_vine_gap)
            zone_label(screen,"VINE ZONE",(R4_LAVA_X+R4_VINE_X)//2,(80,200,80))

            # Zone: puddles (right)
            draw_puddle(screen,r4_puddle1,t,seed=0)
            draw_puddle(screen,r4_puddle2,t,seed=3)
            zone_label(screen,"WATER ZONE",(R4_VINE_X+750)//2,(80,160,255))

            # Enemies
            for en in r4_enemies:
                if en.alive: en.draw(screen)

            # Portal — locked until all dead
            all_dead=all(not e.alive for e in r4_enemies)
            pcol=(180,180,50) if all_dead else (60,60,60)
            draw_portal(screen,PORTAL_RECT,pcol)
            if not all_dead:
                lb=font_small.render("Defeat all enemies to proceed",True,(200,180,80))
                screen.blit(lb,(WIDTH//2-lb.get_width()//2,HEIGHT-WALL_H+(WALL_H-lb.get_height())//2))
            else:
                draw_hint(screen,"All clear! Enter the portal.")

            for sl in slashes: sl.draw(screen)
            draw_back(screen)
            draw_slime(screen,P_color,player_x,player_y,RADIUS,dx,dy,form)

            # Zone tip
            tip_map={2:"Fire form defeats red enemies",1:"Vine form defeats green enemies",3:"Droplet form defeats blue enemies",0:"Switch form with [Q]!"}
            draw_hint(screen,tip_map[form]) if all_dead==False else None
            draw_hud(screen,form,items_owned); draw_hp(screen,player_hp,player_hp_max)

        # ── Room 5 ──
        elif room==5:
            screen.fill((5,5,12))
            draw_back(screen)
            draw_slime(screen,P_color,player_x,player_y,RADIUS,dx,dy,form)
            draw_hint(screen,"...",color=(60,60,100))
            draw_hud(screen,form,items_owned); draw_hp(screen,player_hp,player_hp_max)

        pygame.display.update()

    pygame.quit()
