import pygame
import math
import random


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load("./red_player.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.image_copy = self.image
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)) #rect quản lý vị trí của hình ảnh
        self.x = self.rect[0]
        self.y = self.rect[1]
        self.velocity = pygame.Vector2(0, 0)
        self.angle = 270  # Góc ban đầu của tàu
        self.max_speed = 0.25  # Tốc độ tối đa của tàu
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
        # self.check_collision_with_rock()

    def check_collision_with_rock(self):
        collided_wall = pygame.sprite.spritecollide(self, rocks, False, pygame.sprite.collide_mask)
        if collided_wall:
            rock = collided_wall[0]
            rock.speed = 0.1
            self.max_speed = 0.1
        else:
            self.max_speed = 0.25
#Chưa hoàn thành Rocks, sửa sau
class Rock(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.size = random.randint(3, 4)
        if self.size == 3:
            self.image = pygame.image.load("./big_rock.png").convert_alpha()
        if self.size == 4:
            self.image = pygame.image.load("./small_rock.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 750)
        self.rect.y = random.randint(0, 550)
        self.x = self.rect.x
        self.y = self.rect.y
        self.angle = random.randint(0, 360)
        self.friction = 0.000001
        self.velocity = pygame.Vector2(0, 0)
        self.speed = 0.05

    def update(self, dt):
        if self.angle > 360.0:
            self.angle -= 360.0
        if self.angle < 0.0:
            self.angle += 360.0
        radians = math.radians(self.angle)
        direction = pygame.Vector2(math.cos(radians), math.sin(radians))
        self.speed -= self.friction
        if self.speed < 0:
            self.speed = 0

        self.velocity = direction * self.speed * dt

        self.x += self.velocity.x * dt
        self.y -= self.velocity.y * dt

        if self.x >= SCREEN_WIDTH:
            self.x = 0
        elif self.x <= 0:
            self.x = SCREEN_WIDTH

        if self.y >= SCREEN_HEIGHT:
            self.y = 0
        elif self.y <= 0:
            self.y = SCREEN_HEIGHT

        self.rect.center = (self.x, self.y)
        self.check_collision_with_another_rock()
        self.check_collision_with_player()

    def check_collision_with_another_rock(self):
        collided_rocks = pygame.sprite.spritecollide(self, rocks, False)
        if len(collided_rocks) > 1:
            self.angle = -self.angle

    def check_collision_with_player(self):
        collided_player = pygame.sprite.spritecollide(self, all_sprites, False, pygame.sprite.collide_mask)
        if collided_player:
            player = collided_player[0]
            self.angle = (360 - player.angle + self.angle)
            self.speed = 0.1

class Dragonfly(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load('./Dragonfly.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 750)
        self.rect.y = random.randint(0, 550)
        self.x = self.rect.x
        self.y = self.rect.y
        self.angle = random.randint(0,360)
        self.velocity = pygame.Vector2(0, 0)
        self.max_speed = 0.15

    def update(self, p_x, p_y, dt):
        "chuồn chuồn sẽ đuổi theo player(p_x, p_y)"
        radians = math.atan2(p_y - self.y, p_x - self.x)
        direction = pygame.Vector2(math.cos(radians), math.sin(radians))

        self.velocity += direction * self.max_speed * 0.001 * dt

        if self.velocity.length() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

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


class Suriken(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load("./suriken.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 750)
        self.rect.y = random.randint(0, 550)
        self.x = self.rect.x
        self.y = self.rect.y

    def update(self):
        pass



pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

surf = pygame.Surface((33, 40))
surf.fill('white')

all_sprites = pygame.sprite.Group()
player = Player(all_sprites)

# rocks = pygame.sprite.Group()
# 
# for i in range(5):
#     rock = Rock(rocks)
#     rocks.add(rock)

surikens = pygame.sprite.Group()
for i in range(5):
    suriken = Suriken(surikens)
    surikens.add(suriken)

dragonflies = pygame.sprite.Group()
for i in range(2):
    dragonfly = Dragonfly(dragonflies)
    dragonflies.add(dragonfly)

running = True
clock = pygame.time.Clock()
T = 0

while running:
    dt = clock.tick()  # clock.tick() sẽ trả về số ms/frame, /1000 để đổi sang s/frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_surface.fill('black')

    if pygame.mouse.get_pressed()[0]:
        player.move_rotation(1, dt)
        player.rot = True
        T = 500

    T = T - 1
    if T <= 0: player.rot = False

    all_sprites.update(dt)
    all_sprites.draw(display_surface)

    # rocks.update(dt)
    # rocks.draw(display_surface)

    # surikens.update(dt)
    # surikens.draw(display_surface)
    dragonflies.update(player.x, player.y, dt)
    dragonflies.draw(display_surface)

    pygame.display.update()

pygame.quit()
