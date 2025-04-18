from all_colors import *
import random
import time
import pygame
pygame.init()

pacman_images = {"up": pygame.image.load("resours/pacman_up.png"), "down": pygame.image.load("resours/pacman_down.png"),
                 "left": pygame.image.load("resours/pacman_left.png"), "right": pygame.image.load("resours/pacman_right.png"),
                 "up_left": pygame.image.load("resours/pacman_up_left.png"), "up_right": pygame.image.load("resours/pacman_up_right.png"),
                 "down_left": pygame.image.load("resours/pacman_down_left.png"),
                 "down_right": pygame.image.load("resours/pacman_down_right.png") }

ghost_images = {"red": pygame.image.load("resours/red_ghost.png"), "pink": pygame.image.load("resours/pink_ghost.png"),
               "blue": pygame.image.load("resours/blue_ghost.png"), "orange": pygame.image.load("resours/orange_ghost.png"),
                "cherry": pygame.image.load("resours/cherry.png")}

ghost = ["red", "pink", "blue", "orange", "cherry"]


def get_direction(pos1, pos2):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    direction = "right"

    if dy < 0:
        if dx < 0:
            direction = "up_left"
        elif dx > 0:
            direction = "up_right"
        else:
            direction = "up"

    elif dy > 0:
        if dx < 0:
            direction = "down_left"
        elif dx > 0:
            direction = "down_right"
        else:
            direction = "down"

    else:
        if dx < 0:
            direction = "left"
        elif dx > 0:
            direction = "right"

    return direction


def move_towards(pos1, pos2, speed):
    x1, y1 = pos1
    x2, y2 = pos2
    dx = x2 - x1
    dy = y2 - y1

    if abs(dx) > speed:
        if dx > 0:
            x1 += speed
        else:
            x1 -= speed
    else:
        x1 = x2

    if abs(dy) > speed:
        if dy > 0:
            y1 += speed
        else:
            y1 -= speed
    else:
        y1 = y2

    return (x1, y1)


def check_collision(pos1, pos2, radius=50):
    distance = ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5
    return distance < radius

def spawn(pacman_pos, size, min_distance=100):
    while True:
        ghost_pos = (random.randint(0, size[0] - 100), random.randint(0, size[1] - 100))
        distance = ((ghost_pos[0] - pacman_pos[0]) ** 2 + (ghost_pos[1] - pacman_pos[1]) ** 2) ** 0.5
        if distance >= min_distance:
            return ghost_pos


size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pac-Man наоборот")

BACKGROUND = (0, 0, 0)

pacman_pos = (400, 300)
speed = 8

points = 0
lives = 3

ghost_pos = spawn(pacman_pos, size)
ghost_color = random.choice(ghost)

ghost_spawn_time = 0
ghost_duration = 1.5

clock = pygame.time.Clock()
FPS = 60

font = pygame.font.Font(None, 36)
end_font = pygame.font.Font(None, 70)

end_text = end_font.render("", True, WHITE)

running = True

while running:
    current_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_pos = pygame.mouse.get_pos()

    direction = get_direction(pacman_pos, mouse_pos)
    pacman_pos = move_towards(pacman_pos, mouse_pos, speed)


    if current_time - ghost_spawn_time >= ghost_duration:
        ghost_pos = spawn(pacman_pos, size)
        ghost_color = random.choice(ghost)
        ghost_spawn_time = current_time


    if check_collision(pacman_pos, ghost_pos):
        if ghost_color == "cherry":
            lives -= 1
        else:
            points += 1
        ghost_pos = spawn(pacman_pos, size)
        ghost_color = random.choice(ghost)
        ghost_spawn_time = current_time


    screen.fill(BACKGROUND)

    pacman_image = pacman_images[direction]
    screen.blit(pacman_image, pacman_pos)

    if ghost_pos and (current_time - ghost_spawn_time < ghost_duration):
        ghost_image = ghost_images[ghost_color]
    screen.blit(ghost_image, ghost_pos)

    points_text = font.render(f"Очки: {points}", True, WHITE)
    screen.blit(points_text, (10, 10))

    lives_text = font.render(f"Жизни: {lives}", True, WHITE)
    screen.blit(lives_text, (670, 10))


    if lives == 0:
        speed = 0
        pacman_pos = (400, 300)
        ghost_duration = 100
        end_text = end_font.render("Вы проиграли!", True, WHITE)

    if points == 30:
        speed = 0
        pacman_pos = (400, 300)
        ghost_duration = 100
        end_text = end_font.render("Вы выиграли!", True, WHITE)

    screen.blit(end_text, (200, 200))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()