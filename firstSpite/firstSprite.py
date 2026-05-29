import pygame

pygame.init()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("My Player")
clock = pygame.time.Clock()

def draw_slime(surface, x, y, radius):
    # Outline
    pygame.draw.circle(surface, (144, 238, 144),
        (x, y), radius, 2)
    pygame.draw.circle(surface, (0,191,0),
        (x, y), radius)
    
    # Highlight (upper-left, ~30% of radius)
    hx = x - radius // 2
    hy = y - radius // 2 - 2
    pygame.draw.circle(surface, (255,255,255),
        (hx, hy), radius // 5)
    
    # Eyes
    Peyes = x + 50
    pygame.draw.circle(surface, (25,25,25),
        (Peyes, y), radius // 4)
    
    #pupil
    pupils = Peyes + 8
    pygame.draw.circle(surface, (217,217,217),
        (pupils, y), radius // 12)



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))   # clear screen
    draw_slime(screen, 200, 300, 100)    # draw at center
    pygame.display.flip()
    clock.tick(60)
