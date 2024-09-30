import pygame
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load("./red_player.png").convert()
        self.image_copy = self.image
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)) #rect quản lý vị trí của hình ảnh
        self.x = self.rect[0]
        self.y = self.rect[1]
        self.velocity = pygame.Vector2(0, 0)
        self.angle = -90  # Góc ban đầu của tàu
        self.max_speed = 0.0  # Tốc độ tối đa của tàu
        self.friction = 0.0007  # Ma sát
        self.rotation_speed = 0.23  # Tốc độ quay
        self.rot = False  # Kiểm tra có quay hay không

    def move_rotation(self, direction, dt):
        # direction = 1 (quay phải), -1 (quay trái)
        self.angle += self.rotation_speed * direction * dt
        # Đảm bảo góc không vượt quá 360 độ
        if self.angle > 360.0:
            self.angle -= 360.0
        if self.angle < 0.0:
            self.angle += 360.0

        self.image = pygame.transform.rotate(self.image_copy, -self.angle - 90) #xoay trên ảnh bản sao để giữ nguyên ảnh gốc
        self.rect = self.image.get_rect()


    def update(self, dt):
        radians = math.radians(self.angle)
        direction = pygame.Vector2(math.cos(radians), math.sin(radians))

        if not self.rot:
            self.velocity += direction * self.max_speed * 0.001 * dt

            if self.velocity.length() > self.max_speed:
                self.velocity = self.velocity.normalize() * self.max_speed

        else:
            self.velocity += direction * self.max_speed * 0.0006 * dt
            self.velocity *= (1 - self.friction)

        self.x += self.velocity.x * dt
        self.y += self.velocity.y * dt

        if self.x >= SCREEN_WIDTH:
            self.x = 0
        elif self.x <= 0:
            self.x = SCREEN_WIDTH

        if self.y >= SCREEN_HEIGHT:
            self.y = 0
        elif self.y <= 0:
            self.y = SCREEN_HEIGHT

        self.rect.center = (self.x, self.y)
        print(self.rect)

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

surf = pygame.Surface((33, 40))
surf.fill('white')

all_sprites = pygame.sprite.Group()
player = Player(all_sprites)


running = True
clock = pygame.time.Clock()
T = 0

while running:
    dt = clock.tick()  # clock.tick() sẽ trả về số ms/frame, /1000 để đổi sang s/frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_surface.fill('gray')

    if pygame.mouse.get_pressed()[0]:
        player.move_rotation(1, dt)
        player.rot = True
        T = 500

    T = T - 1
    if T <= 0: player.rot = False

    all_sprites.update(dt)
    display_surface.blit(player.image, player.rect)

    pygame.display.update()

pygame.quit()
