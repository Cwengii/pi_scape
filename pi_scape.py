import pygame   
import random
import math

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# --- Classes ---
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([20, 30])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 0
        self.speed_y = 0
        self.can_jump = True

    def update(self):
        # Basic movement
        self.rect.x += self.speed_x

        # Gravity
        self.speed_y += 0.5

        self.rect.y += self.speed_y

        # Keep player within screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.speed_y = 0
            self.can_jump = True
        if self.rect.top < 0:
            self.rect.top = 0

    def jump(self):
        if self.can_jump:
            self.speed_y = -10
            self.can_jump = False

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.type = type
        if self.type == "erratic":
            self.image = pygame.Surface([30, 30])
            self.image.fill((255, 0, 0))
            self.speed_x = random.randint(-5, 5)
            self.speed_y = random.randint(-5, 5)
        elif self.type == "static":
            self.image = pygame.Surface([40, 20])
            self.image.fill((200, 0, 0))
            self.speed_x = 0
            self.speed_y = 0

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def update(self):
        if self.type == "erratic":
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

            if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
                self.speed_x *= -1

            if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
                self.speed_y *= -1
        elif self.type == "static":
            pass

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.type = type
        self.image = pygame.Surface([20, 20])
        if self.type == "speed_boost":
            self.image.fill((0, 255, 0))
        elif self.type == "invincibility":
            self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        # Simple floating movement
        self.rect.y += math.sin(pygame.time.get_ticks() / 1000) * 0.5

# --- Game Functions ---
def generate_level(level_number):
    level = []
    pi_digits = str(math.pi).replace(".", "")
    level_width = 20
    for i in range(level_width * level_number):
        digit = int(pi_digits[i % len(pi_digits)])
        level.append(digit)
    return level

def draw_level(screen, level):
    block_width = 50
    block_height = 30
    for i, digit in enumerate(level):
        y_pos = SCREEN_HEIGHT - ((digit + 1) * block_height)
        x_pos = i * block_width
        if i % 2 == 0:
             pygame.draw.rect(screen, (100, 100, 100), (x_pos, y_pos, block_width, block_height))
        else:
            pygame.draw.rect(screen, (150, 150, 150), (x_pos, y_pos, block_width, block_height))

# --- Game Initialization ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pi-Scape")

# --- Sprite Groups ---
all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()

# --- Player ---
player = Player(50, SCREEN_HEIGHT - 50)
all_sprites.add(player)

# --- Enemies ---
for i in range(5):
    if random.random() < 0.5:
        enemy_type = "erratic"
    else:
        enemy_type = "static"

    enemy = Enemy(random.randint(0, SCREEN_WIDTH), 50, enemy_type)
    all_sprites.add(enemy)
    enemy_sprites.add(enemy)

# --- Level ---
current_level = 1
level_data = generate_level(current_level)

# --- Power-Up ---
power_up = PowerUp(random.randint(100, SCREEN_WIDTH - 100), 100, "speed_boost")
all_sprites.add(power_up)

# --- Font ---
pygame.font.init()
font = pygame.font.Font(None, 30)

# --- Game Loop ---
running = True
clock = pygame.time.Clock()
score = 0

while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    # --- Game Logic ---
    all_sprites.update()

    # Collision Detection
    collisions = pygame.sprite.spritecollide(player, enemy_sprites, False)
    if collisions:
        print("Game Over!")
        running = False

    # Power-up collision detection
    powerup_collision = pygame.sprite.spritecollide(player, [power_up], True)
    if powerup_collision:
        print("Collected power-up!")
        score += 10  # Give some score for collecting a power-up
        # Respawn the power-up
        power_up = PowerUp(random.randint(100, SCREEN_WIDTH - 100), 100, "speed_boost")
        all_sprites.add(power_up)

    # --- Drawing ---
    screen.fill(WHITE)

    draw_level(screen, level_data)

    all_sprites.draw(screen)

    # Render score
    text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(text, (10, 10))

    # --- Update the Display ---
    pygame.display.flip()

    # --- Limit Frame Rate ---
    clock.tick(60)

pygame.quit()