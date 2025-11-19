import pygame
import math
import random
import sys


WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_SIZE = 40
PLAYER_SPEED = 5
STAR_SIZE = 12
ENEMY_SIZE = 32
INITIAL_ENEMIES = 3
ENEMY_SPEED = 2.0
SPEED_INCREASE_INTERVAL = 10  


WHITE = (245, 245, 245)
BLACK = (10, 10, 10)
PLAYER_COLOR = (50, 130, 255)
STAR_COLOR = (255, 200, 60)
ENEMY_COLOR = (220, 60, 60)
TEXT_COLOR = (30, 30, 30)

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        self.rect.x = max(0, min(WIDTH - PLAYER_SIZE, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - PLAYER_SIZE, self.rect.y))

    def draw(self, surf):
        pygame.draw.rect(surf, PLAYER_COLOR, self.rect, border_radius=6)
        shine_rect = pygame.Rect(self.rect.x + 6, self.rect.y + 6, 10, 10)
        pygame.draw.rect(surf, (170, 220, 255), shine_rect, border_radius=3)

class Star:
    def __init__(self):
        self.pos = self.random_pos()
        self.rect = pygame.Rect(self.pos[0], self.pos[1], STAR_SIZE, STAR_SIZE)

    @staticmethod
    def random_pos():
        x = random.randint(20, WIDTH - 20 - STAR_SIZE)
        y = random.randint(20, HEIGHT - 20 - STAR_SIZE)
        return (x, y)

    def respawn(self):
        self.pos = self.random_pos()
        self.rect.topleft = self.pos

    def draw(self, surf):
        cx = self.rect.centerx
        cy = self.rect.centery
        points = []
        for i in range(5):
            angle = i * 2 * 3.14159 / 5
            x = cx + int(10 * (1 if i%2==0 else 0.5) * math.cos(angle))
            y = cy + int(10 * (1 if i%2==0 else 0.5) * math.sin(angle))
            points.append((x, y))
        pygame.draw.polygon(surf, STAR_COLOR, points)

class Enemy:
    def __init__(self):
        x = random.randint(0, WIDTH - ENEMY_SIZE)
        y = random.randint(0, HEIGHT - ENEMY_SIZE)
        self.rect = pygame.Rect(x, y, ENEMY_SIZE, ENEMY_SIZE)
        self.vx = random.choice([-1, 1]) * (ENEMY_SPEED + random.random())
        self.vy = random.choice([-1, 1]) * (ENEMY_SPEED + random.random())

    def update(self, speed_multiplier=1.0):
        self.rect.x += self.vx * speed_multiplier
        self.rect.y += self.vy * speed_multiplier
        if self.rect.left < 0:
            self.rect.left = 0
            self.vx *= -1
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.vx *= -1
        if self.rect.top < 0:
            self.rect.top = 0
            self.vy *= -1
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.vy *= -1

    def draw(self, surf):
        pygame.draw.ellipse(surf, ENEMY_COLOR, self.rect)
        eye_r = 3
        left_eye = (self.rect.centerx - 6, self.rect.centery - 6)
        right_eye = (self.rect.centerx + 6, self.rect.centery - 6)
        pygame.draw.circle(surf, BLACK, left_eye, eye_r)
        pygame.draw.circle(surf, BLACK, right_eye, eye_r)


def draw_text_center(surf, text, size, y):
    font = pygame.font.SysFont(None, size)
    render = font.render(text, True, TEXT_COLOR)
    rect = render.get_rect(center=(WIDTH // 2, y))
    surf.blit(render, rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('زرد هارو جمع کن')
    clock = pygame.time.Clock()

    player = Player(WIDTH // 2 - PLAYER_SIZE // 2, HEIGHT - PLAYER_SIZE - 20)
    star = Star()
    enemies = [Enemy() for _ in range(INITIAL_ENEMIES)]

    score = 0
    running = True
    game_over = False
    enemy_speed_multiplier = 1.0

    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_SPACE:
                    # restart
                    player = Player(WIDTH // 2 - PLAYER_SIZE // 2, HEIGHT - PLAYER_SIZE - 20)
                    star.respawn()
                    enemies = [Enemy() for _ in range(INITIAL_ENEMIES)]
                    score = 0
                    game_over = False
                    enemy_speed_multiplier = 1.0

        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = PLAYER_SPEED

        if not game_over:
            player.move(dx, dy)

            for e in enemies:
                e.update(speed_multiplier=enemy_speed_multiplier)

            if player.rect.colliderect(star.rect):
                score += 1
                star.respawn()
                if score % 5 == 0:
                    enemies.append(Enemy())
                if score % SPEED_INCREASE_INTERVAL == 0:
                    enemy_speed_multiplier += 0.15

            for e in enemies:
                if player.rect.colliderect(e.rect):
                    game_over = True
                    break

        screen.fill(WHITE)

        star.draw(screen)
        for e in enemies:
            e.draw(screen)
        player.draw(screen)

        font = pygame.font.SysFont(None, 30)
        score_surf = font.render(f'Score: {score}', True, TEXT_COLOR)
        screen.blit(score_surf, (10, 10))

        if game_over:
            draw_text_center(screen, 'Game Over', 72, HEIGHT // 2 - 40)
            draw_text_center(screen, f'Final score: {score}', 36, HEIGHT // 2 + 10)
            draw_text_center(screen, 'Press SPACE to restart', 28, HEIGHT // 2 + 60)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
