import pygame
import sys
import random

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()
# Constants
WIDTH, HEIGHT = 800, 800
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (169, 169, 169)
WHITE = (255, 255, 255)

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test Game")

# Classes
class BlueCircle(pygame.sprite.Sprite):
    def __init__(self): 
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 50  # Spawn on the right side
        self.rect.y = random.randint(50, HEIGHT - 80)  # Random Y position

    def update(self):
        pass

class GreyRock(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 70  # Spawn on the right side
        self.rect.y = random.randint(50, HEIGHT - 80)  # Random Y position

    def update(self):
        pass

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = 7

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

# Create sprite groups
all_sprites = pygame.sprite.Group()
blue_circles = pygame.sprite.Group()
grey_rocks = pygame.sprite.Group()
#players = pygame.sprite.Group()

# Create objects
blue_circle = BlueCircle()
#grey_rock = GreyRock()
player = Player()

# Add objects to sprite groups
all_sprites.add(blue_circle, player)
blue_circles.add(blue_circle)
# Create rocks and add them to the grey_rocks group
rock_positions = [(100, 100), (200, 300), (500, 200)]  # Example positions
for x,y in rock_positions:
    rock = GreyRock()
    rock.rect.x = x
    rock.rect.y = y
    grey_rocks.add(rock)
    all_sprites.add(rock)
#players.add(player)


# Setting up Background
# Load background image
background_image = pygame.image.load('Grass_BackGround.png').convert()
background_image = pygame.transform.scale(background_image, (WIDTH*3, HEIGHT*3))
#background_surface = pygame.Surface((WIDTH * 2, HEIGHT * 2))  # Create a larger surface

# Camera settings
camera = pygame.Vector2(0, 0)  # Create a Rect representing the camera's view


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Exit the game when Esc is pressed
                running = False
    
    # LEts add collision mechanics
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.rect.x -= player.speed
    if keys[pygame.K_RIGHT]:
        player.rect.x += player.speed
    if keys[pygame.K_UP]:
        player.rect.y -= player.speed
    if keys[pygame.K_DOWN]:
        player.rect.y += player.speed

    # Check collision between player and rocks
    if pygame.sprite.spritecollide(player, grey_rocks, False):
        print("Collision detected!")  # This will print a message when collision occurs
    collided_rocks = pygame.sprite.spritecollide(player, grey_rocks, False)
    if collided_rocks:
        for rock in collided_rocks:
            if player.rect.colliderect(rock.rect):  # Check if the player's rect collides with the rock's rect
                # If colliding, prevent player movement in that direction
                if player.rect.right > rock.rect.left and keys[pygame.K_LEFT]:
                    player.rect.left = rock.rect.right
                if player.rect.left < rock.rect.right and keys[pygame.K_RIGHT]:
                    player.rect.right = rock.rect.left
                if player.rect.bottom > rock.rect.top and keys[pygame.K_UP]:
                    player.rect.top = rock.rect.bottom
                if player.rect.top < rock.rect.bottom and keys[pygame.K_DOWN]:
                    player.rect.bottom = rock.rect.top

    # Update
    camera = pygame.Vector2(player.rect.center) - pygame.Vector2(WIDTH / 2, HEIGHT / 2)
    # Calculate the adjusted position for the background image
    #bg_x = -(camera.x % background_image.get_width())
    #bg_y = -(camera.y % background_image.get_height())
    # Fill the background surface with the repeated pattern of the image
    #for x in range(0, WIDTH * 2, background_image.get_width()):
    #    for y in range(0, HEIGHT * 2, background_image.get_height()):
    #        background_surface.blit(background_image, (x, y))


    # Draw
    screen.fill(GREEN)
    screen.blit(background_image, (-camera.x, -camera.y))

    # Draw the background surface at the adjusted position relative to the camera
    #screen.blit(background_surface, (-camera.x % (WIDTH * 2), -camera.y % (HEIGHT * 2)))


    #all_sprites.draw(screen)
    for sprite in all_sprites:
        screen.blit(sprite.image, sprite.rect.topleft - camera)
    
    # Refresh screen
    pygame.display.flip()
    # Control frame rate
    clock.tick(60)

pygame.quit()
sys.exit()
