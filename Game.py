import abc
import random
import time
import pygame
pygame.init()


size = (1280, 720)
BACKGROUND = (0, 0, 0)
FPS = 60
font = pygame.font.SysFont(None, 64)
small_font = pygame.font.SysFont(None, 36)
player_name = "Аноним"

pacman_images = {"up": pygame.image.load("resours/pacman_up.png"), "down": pygame.image.load("resours/pacman_down.png"),
                 "left": pygame.image.load("resours/pacman_left.png"), "right": pygame.image.load("resours/pacman_right.png"),
                 "up_left": pygame.image.load("resours/pacman_up_left.png"), "up_right": pygame.image.load("resours/pacman_up_right.png"),
                 "down_left": pygame.image.load("resours/pacman_down_left.png"),
                 "down_right": pygame.image.load("resours/pacman_down_right.png") }

ghost_images = {"red": pygame.image.load("resours/red_ghost.png"), "pink": pygame.image.load("resours/pink_ghost.png"),
               "blue": pygame.image.load("resours/blue_ghost.png"), "orange": pygame.image.load("resours/orange_ghost.png"),
                "cherry": pygame.image.load("resours/cherry.png")}

ghost_types = ["red", "pink", "blue", "orange", "cherry"]


class State(abc.ABC):
    @abc.abstractmethod
    def handle_events(self, events):
        pass

    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def draw(self, screen):
        pass


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


class SplashScreen(State):
    def __init__(self):
        self.text = "Заставка"
        self.surface = font.render(self.text, True, (255, 255, 255))

        self.hint = "Нажмите для продолжения"
        self.hint_surface = font.render(self.hint, True, (255, 255, 255))
        self.hint_visible = True
        self.hint_time = pygame.time.get_ticks()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return MenuScreen()

        return self

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.hint_time > 800:
            self.hint_visible = not self.hint_visible
            self.hint_time = current_time

    def draw(self, screen):
        screen.fill(BACKGROUND)
        rect = self.surface.get_rect()
        rect.centerx = screen.get_rect().centerx
        rect.centery = screen.get_rect().centery - 100
        screen.blit(self.surface, rect)

        if self.hint_visible:
            hint_rect = self.hint_surface.get_rect()
            hint_rect.centerx = screen.get_rect().centerx
            hint_rect.centery = screen.get_rect().centery + 100
            screen.blit(self.hint_surface, hint_rect)



class MenuScreen(State):
    def __init__(self):
        self.items = ["Играть", "Выбрать имя игрока", "Выйти"]
        self.surfaces = [font.render(item, True, (255, 255, 255)) for item in self.items]
        self.selected = 0

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.prev()
                if event.key == pygame.K_DOWN:
                    self.next()
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    return self.process_item()

        return self

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(BACKGROUND)
        for i, surface in enumerate(self.surfaces):
            rect = surface.get_rect()
            rect.centerx = screen.get_rect().centerx
            rect.top = screen.get_rect().top + 100*(i+1)
            if i == self.selected:
                surface = font.render(self.items[i], True, (255, 0, 0))
            screen.blit(surface, rect)

    def next(self):
        if self.selected < len(self.items) - 1:
            self.selected += 1

    def prev(self):
        if self.selected > 0:
            self.selected -= 1

    def process_item(self):
        if self.selected == 0:
            return GameScreen()
        if self.selected == 1:
            return NameScreen()
        if self.selected == 2:
            pygame.quit()
            exit()


class NameScreen(State):
    def __init__(self):
        self.text = "Введите имя игрока"
        self.surface = font.render(self.text, True, (255, 255, 255))
        self.name = ""
        self.name_surface = None

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if len(self.name) > 0:
                        self.name = self.name[:-1]
                elif event.key == pygame.K_RETURN:
                    global player_name
                    player_name = self.name
                    return MenuScreen()
                else:
                    if event.unicode.isalnum() and len(self.name) < 10:
                        self.name += event.unicode
                        self.name_surface = font.render(self.name, True, (255, 255, 255))

        return self

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(BACKGROUND)
        rect = self.surface.get_rect()
        rect.centerx = screen.get_rect().centerx
        rect.top = screen.get_rect().top + 100
        screen.blit(self.surface, rect)
        if self.name_surface is not None:
            name_rect = self.name_surface.get_rect()
            name_rect.centerx = screen.get_rect().centerx
            name_rect.top = screen.get_rect().top + 200
            screen.blit(self.name_surface, name_rect)


class GameScreen(State):
    def __init__(self):
        self.pacman_pos = (size[0] // 2, size[1] // 2)
        self.speed = 12
        self.points = 0
        self.lives = 3
        self.ghost_pos = spawn(self.pacman_pos, size)
        self.ghost_color = random.choice(ghost_types)
        self.ghost_spawn_time = time.time()
        self.ghost_duration = 1.5
        self.end_text = ""
        self.game_over = False
        self.game_won = False
        self.end_font = pygame.font.SysFont(None, 70)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return MenuScreen()
                if (self.game_over or self.game_won) and event.key == pygame.K_SPACE:
                    return MenuScreen()

        return self

    def update(self):
        if self.game_over or self.game_won:
            return

        current_time = time.time()
        mouse_pos = pygame.mouse.get_pos()

        direction = get_direction(self.pacman_pos, mouse_pos)
        self.pacman_pos = move_towards(self.pacman_pos, mouse_pos, self.speed)

        if current_time - self.ghost_spawn_time >= self.ghost_duration:
            self.ghost_pos = spawn(self.pacman_pos, size)
            self.ghost_color = random.choice(ghost_types)
            self.ghost_spawn_time = current_time

        if check_collision(self.pacman_pos, self.ghost_pos):
            if self.ghost_color == "cherry":
                self.lives -= 1
            else:
                self.points += 1
            self.ghost_pos = spawn(self.pacman_pos, size)
            self.ghost_color = random.choice(ghost_types)
            self.ghost_spawn_time = current_time

        if self.lives <= 0:
            self.game_over = True
            self.end_text = self.end_font.render("Вы проиграли!", True, (255, 255, 255))
            self.speed = 0
            self.pacman_pos = (size[0] // 2, size[1] // 2)
            self.ghost_duration = 100

        if self.points >= 30:
            self.game_won = True
            self.end_text = self.end_font.render("Вы выиграли!", True, (255, 255, 255))
            self.speed = 0
            self.pacman_pos = (size[0] // 2, size[1] // 2)
            self.ghost_duration = 100

    def draw(self, screen):
        screen.fill(BACKGROUND)

        direction = get_direction(self.pacman_pos, pygame.mouse.get_pos())
        pacman_image = pacman_images[direction]
        screen.blit(pacman_image, self.pacman_pos)

        current_time = time.time()
        if current_time - self.ghost_spawn_time < self.ghost_duration:
            ghost_image = ghost_images[self.ghost_color]
            screen.blit(ghost_image, self.ghost_pos)

        points_text = small_font.render(f"Очки: {self.points}", True, (255, 255, 255))
        screen.blit(points_text, (10, 10))

        lives_text = small_font.render(f"Жизни: {self.lives}", True, (255, 255, 255))
        screen.blit(lives_text, (size[0] - 150, 10))

        name_text = small_font.render(f"Игрок: {player_name}", True, (255, 255, 255))
        screen.blit(name_text, (size[0] // 2 - 100, 10))

        if self.game_over or self.game_won:
            end_rect = self.end_text.get_rect()
            end_rect.centerx = screen.get_rect().centerx
            end_rect.centery = screen.get_rect().centery
            screen.blit(self.end_text, end_rect)

            hint = small_font.render("Нажмите ESC для выхода в меню", True, (255, 255, 255))
            hint_rect = hint.get_rect()
            hint_rect.centerx = screen.get_rect().centerx
            hint_rect.centery = screen.get_rect().centery + 100
            screen.blit(hint, hint_rect)


screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pac-Man наоборот")

clock = pygame.time.Clock()

state = SplashScreen()

running = True

while running:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    state = state.handle_events(events)
    state.update()
    state.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()