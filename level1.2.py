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
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
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
            self.image = self.frames[self.cur_frame]


# Load your sprite sheet image
dragon_sheet = load_image("AnimationSheet_Character.png")  # Ensure this function is defined elsewhere
dragon = AnimatedSprite(dragon_sheet, 8, 1, 50, 50)

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
    pygame.Rect(300, 300, 200, 20)
]

start_point = pygame.Rect(50, 50, dragon.rect.width, dragon.rect.height)
end_point = pygame.Rect(700, 500, dragon.rect.width, dragon.rect.height)


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
        if keys[pygame.K_a]:
            dragon.rect.x -= 5
        elif keys[pygame.K_d]:
            dragon.rect.x += 5
        elif keys[pygame.K_w]:
            dragon.rect.y -= 5
        elif keys[pygame.K_s]:
            dragon.rect.y += 5
            dragon.moving = True
        else:
            dragon.moving = False


        player_rect = dragon.rect.copy()

        for wall in walls:
            if player_rect.colliderect(wall):
                game_over_screen(screen)
                ENV.display_screen = 1
                return

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

        screen.fill(BACKGROUND_COLOR)
        draw_walls()
        draw_start_end()

        # Update and draw all sprites
        all_sprites.update()
        all_sprites.draw(screen)

        # Draw the animated sprite at its updated position
        screen.blit(dragon.image, dragon.rect)

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    level_1(screen)
