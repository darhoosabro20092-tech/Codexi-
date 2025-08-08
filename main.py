import pygame
import sys

# Game Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.8
PLAYER_SPEED = 5
JUMP_STRENGTH = 15

# Color definitions
SKY_BLUE = (107, 140, 255)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.on_ground = False

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        dx = 0
        if keys[pygame.K_LEFT]:
            dx -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            dx += PLAYER_SPEED

        # Apply gravity
        self.vel_y += GRAVITY
        dy = self.vel_y

        # Horizontal movement and collisions
        self.rect.x += dx
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if dx > 0:
                    self.rect.right = platform.rect.left
                elif dx < 0:
                    self.rect.left = platform.rect.right

        # Vertical movement and collisions
        self.rect.y += dy
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if dy > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif dy < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

    def jump(self):
        if self.on_ground:
            self.vel_y = -JUMP_STRENGTH


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect(topleft=(x, y))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = 1
        self.speed = 2

    def update(self, platforms):
        self.rect.x += self.direction * self.speed
        collided = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                collided = True
                break
        if collided:
            self.direction *= -1


def create_level():
    platforms = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    # Ground
    platforms.add(Platform(0, HEIGHT - 40, 2000, 40))

    # Simple platforms
    platforms.add(Platform(300, HEIGHT - 120, 120, 20))
    platforms.add(Platform(500, HEIGHT - 200, 120, 20))
    platforms.add(Platform(700, HEIGHT - 280, 120, 20))

    # Enemies
    enemies.add(Enemy(600, HEIGHT - 70))

    return platforms, enemies


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mini Mario")
    clock = pygame.time.Clock()

    player = Player(50, HEIGHT - 80)
    platforms, enemies = create_level()
    all_sprites = pygame.sprite.Group(platforms, enemies, player)

    camera_offset = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

        all_sprites.update(platforms)

        # Collision with enemies
        if pygame.sprite.spritecollide(player, enemies, False):
            player.rect.topleft = (50, HEIGHT - 80)
            camera_offset = 0

        # Update camera offset based on player position
        if player.rect.centerx - camera_offset > WIDTH // 2:
            camera_offset = player.rect.centerx - WIDTH // 2

        screen.fill(SKY_BLUE)
        for sprite in all_sprites:
            screen.blit(sprite.image, (sprite.rect.x - camera_offset, sprite.rect.y))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
