import pygame
import math

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

T = 0

class Spaceship:
    def __init__(self):
        self.x = SCREEN_WIDTH / 2  # Tọa độ ban đầu của tàu
        self.y = SCREEN_HEIGHT / 2 # Tọa độ ban đầu của tàu
        self.angle = 0.0  # Góc ban đầu của tàu
        self.max_speed = 0.2  # Tốc độ tối đa của tàu
        self.friction = 0.001 # Ma sát
        self.rotation_speed = 0.17  # Tốc độ quay
        self.size = 40  # Kích thước của tàu (tam giác)
        self.velocity_x = 0.0  # Vận tốc trên trục X
        self.velocity_y = 0.0  # Vận tốc trên trục Y
        self.rot = False  # Kiểm tra có quay hay không


    def move_rotation(self, direction):
        # direction = 1 (quay phải), -1 (quay trái)
        self.angle += self.rotation_speed * direction
        # Đảm bảo góc không vượt quá 360 độ
        if self.angle > 360.0:
            self.angle -= 360.0
        if self.angle < 0.0:
            self.angle += 360.0

    def inertia_movement(self):
        radians = math.radians(self.angle)

        if self.rot == False:
            self.velocity_x += math.cos(radians) * self.max_speed * 0.001
            if self.velocity_x >= self.max_speed: self.velocity_x = self.max_speed
            if self.velocity_x <= -self.max_speed: self.velocity_x = -self.max_speed
            self.velocity_y += math.sin(radians) * self.max_speed * 0.001
            if self.velocity_y >= self.max_speed: self.velocity_y = self.max_speed
            if self.velocity_y <= -self.max_speed: self.velocity_y = -self.max_speed
        else:
            self.velocity_x -= self.friction * self.velocity_x
            self.velocity_y -= self.friction * self.velocity_y
        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.x >= SCREEN_WIDTH:
            self.x = 0
        elif self.x <= 0:
            self.x = SCREEN_WIDTH

        if self.y >= SCREEN_HEIGHT:
            self.y = 0
        elif self.y <= 0:
            self.y = SCREEN_HEIGHT

    def draw(self, screen):
        # Kích thước chiều dài và chiều rộng của hình chữ nhật
        rect_width = self.size * 1.5
        rect_height = self.size

        # Tính toán góc xoay của tàu
        radians = math.radians(self.angle)

        # Tính toán 4 điểm của hình chữ nhật dựa trên tọa độ và góc xoay
        point1 = (self.x + math.cos(radians) * rect_width / 2 - math.sin(radians) * rect_height / 2,
                  self.y + math.sin(radians) * rect_width / 2 + math.cos(radians) * rect_height / 2)
        point2 = (self.x - math.cos(radians) * rect_width / 2 - math.sin(radians) * rect_height / 2,
                  self.y - math.sin(radians) * rect_width / 2 + math.cos(radians) * rect_height / 2)
        point3 = (self.x - math.cos(radians) * rect_width / 2 + math.sin(radians) * rect_height / 2,
                  self.y - math.sin(radians) * rect_width / 2 - math.cos(radians) * rect_height / 2)
        point4 = (self.x + math.cos(radians) * rect_width / 2 + math.sin(radians) * rect_height / 2,
                  self.y + math.sin(radians) * rect_width / 2 - math.cos(radians) * rect_height / 2)

        # Vẽ hình chữ nhật
        pygame.draw.polygon(screen, WHITE, [point1, point2, point3, point4])

def main():
    T = 0
    ship = Spaceship()
    running = True
    while running:
        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if pygame.mouse.get_pressed()[0]:
            ship.move_rotation(1)
            ship.rot = True
            T = 500

        T = T - 1
        if T <= 0: ship.rot = False

        ship.inertia_movement()

        screen.fill(BLACK)
        ship.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
