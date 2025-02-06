import pygame
import sys
from enviroment import ENV

pygame.init()

# Initialize all_sprites group
all_sprites = pygame.sprite.Group()


def load_image(filename):
    try:
        image = pygame.image.load(filename)
        return image
    except pygame.error as e:
        print(f"Не удалось загрузить изображение: {filename}. Ошибка: {e}")
        sys.exit()


# AnimatedSprite class definition
class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.moving = False
        self.left = False
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(x, y))

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if self.moving:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            if self.left:
                self.image = pygame.transform.flip(self.frames[self.cur_frame], True, False)
            else:
                self.image = self.frames[self.cur_frame]
            self.mask = pygame.mask.from_surface(self.image)


class FireSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.moving = False
        self.left = False
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.animation_speed = 0.1  # Скорость анимации
        self.last_update = pygame.time.get_ticks()

    def cut_sheet(self, sheet, columns, rows):
        frame_width = sheet.get_width() // columns
        frame_height = sheet.get_height() // rows
        self.rect = pygame.Rect(0, 0, frame_width, frame_height)

        for j in range(rows):
            for i in range(columns):
                frame_location = (frame_width * i, frame_height * j)
                # Убедитесь, что вы не выходите за пределы изображения
                if (frame_location[0] + frame_width <= sheet.get_width() and
                        frame_location[1] + frame_height <= sheet.get_height()):
                    self.frames.append(sheet.subsurface(pygame.Rect(
                        frame_location, self.rect.size)))

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 99:
            self.last_update = now
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            if self.left:
                self.image = pygame.transform.flip(self.frames[self.cur_frame], True, False)
            else:
                self.image = self.frames[self.cur_frame]
            self.mask = pygame.mask.from_surface(self.image)


# Load images
dragon_sheet1 = load_image("AnimationSheet_Character.png")
dragon_sheet2 = load_image("AnimationSheet_Character2.png")
background_image = load_image("back.jpg")
fire_sheet = load_image("ff-Photoroom.png")

# Game settings
WIDTH, HEIGHT = 800, 600
FPS = 60
WALL_COLOR = (255, 0, 0)
BACKGROUND_COLOR = (0, 0, 0)
GAME_OVER_COLOR = (128, 0, 0)
START_COLOR = (0, 255, 225)
END_COLOR = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Лабиринт в аду")

walls = [
    pygame.Rect(50, 100, 100, 20),
    pygame.Rect(200, 100, 100, 20)
]

start_point = pygame.Rect(50, 50, 50, 50)
end_point = pygame.Rect(700, 500, 50, 50)

# Create a single dragon character
dragon = AnimatedSprite(dragon_sheet1, 8, 1, 50, 50)
fire = FireSprite(fire_sheet, 9, 1, 150, 50)  # Создаем спрайт огня
# fire.rect.width = 100
# fire.rect.height = 100


def draw_walls():
    for wall in walls:
        pygame.draw.rect(screen, WALL_COLOR, wall)


def draw_start_end():
    pygame.draw.rect(screen, START_COLOR, start_point)
    pygame.draw.rect(screen, END_COLOR, end_point)


def game_over_screen(screen):
    screen.fill(GAME_OVER_COLOR)
    font = pygame.font.Font(None, 74)
    text = font.render("Игра окончена!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(3000)
    ENV.display_screen = 0


def level_1(screen):
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ENV.display_screen = None
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:  # Move right
            dragon.rect.x += 5
            dragon.left = False
            dragon.moving = True
        elif keys[pygame.K_a]:  # Move left
            dragon.rect.x -= 5
            dragon.left = True
            dragon.moving = True
        elif keys[pygame.K_w]:  # Move up
            dragon.rect.y -= 5
            dragon.moving = True
            dragon.left = False
        elif keys[pygame.K_s]:  # Move down
            dragon.rect.y += 5
            dragon.left = False
            dragon.moving = True
        else:
            dragon.moving = False

        player_rect = dragon.rect.copy()
        # Проверка на столкновение с огнем
        if pygame.sprite.collide_mask(dragon, fire):
        #if player_rect.colliderect(fire.rect):
            print(player_rect, fire.rect)
            game_over_screen(screen)
            ENV.display_screen = 1
            return

        for wall in walls:
            if player_rect.colliderect(wall):
                if keys[pygame.K_d]:
                    player_rect.right = wall.left
                elif keys[pygame.K_a]:
                    player_rect.left = wall.right
                elif keys[pygame.K_w]:
                    player_rect.top = wall.bottom
                elif keys[pygame.K_s]:
                    player_rect.bottom = wall.top

        dragon.rect = player_rect

        # Проверка на достижение конечной точки
        if player_rect.colliderect(end_point):
            screen.fill((0, 128, 0))
            font = pygame.font.Font(None, 74)
            text = font.render("You are alive", True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.delay(3000)
            running = False
            ENV.display_screen = 0
            return

        screen.blit(background_image, (0, 0))
        draw_walls()
        draw_start_end()


        pygame.draw.rect(screen, "green", player_rect, width=1)
        pygame.draw.rect(screen, "green", fire.rect, width=1)


        # Update and draw all sprites
        all_sprites.update()
        all_sprites.draw(screen)

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    level_1(screen)
