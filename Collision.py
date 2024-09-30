import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hehe")

#color
BG = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

#hide mouse cursor
pygame.mouse.set_visible(False)

#create ship
ship = pygame.image.load('./red_player.png').convert_alpha()
ship_rect = ship.get_rect()
ship_mask = pygame.mask.from_surface(ship)
mask_image = ship_mask.to_surface()

#create bullet and mask
bullet = pygame.Surface((7,7))
bullet.fill(RED)
bullet_mask = pygame.mask.from_surface(bullet)

#position ship rectangle
ship_rect.topleft = (350, 250)

#game loop
run = True
while run:

    pos = pygame.mouse.get_pos()

    #update background
    screen.fill(BG)

    #check map overlap
    if ship_mask.overlap(bullet_mask, (pos[0] - ship_rect.x, pos[1] - ship_rect.y)):
        col = RED
    else:
        col = GREEN

    #draw mask image
    screen.blit(mask_image, (0, 0))

    #draw solider
    screen.blit(ship, ship_rect)

    #draw rectangle
    bullet.fill(col)
    screen.blit(bullet, pos)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update display
    pygame.display.flip()

pygame.quit()
