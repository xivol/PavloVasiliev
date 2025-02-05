import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пиксельный Демон")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Загрузка изображений для анимации демона
demon_images = [
    pygame.image.load('path/to/demon_frame1.png'),
    pygame.image.load('path/to/demon_frame2.png'),
    pygame.image.load('path/to/demon_frame3.png')
]

# Настройка шрифта
font = pygame.font.Font(None, 36)


class AnimatedDemon:
    def __init__(self):
        self.images = demon_images
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def update(self):
        # Обновление индекса изображения для анимации
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]


def draw_text(text, x, y, color=WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


# Создание экземпляра демона
demon = AnimatedDemon()

# Главный игровой цикл
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление анимации демона
    demon.update()

    # Заливка фона
    screen.fill(BLACK)

    # Отображение анимированного демона
    screen.blit(demon.image, demon.rect)

    # Отображение текста от демона с эффектами
    draw_text("Добро пожаловать в ад,", WIDTH // 2 - 150, HEIGHT // 2 + 100)
    draw_text("Алекс!", WIDTH // 2 - 50, HEIGHT // 2 + 140)
    draw_text("Ты открыл древнюю книгу,", WIDTH // 2 - 150, HEIGHT // 2 + 180)
    draw_text("и теперь тебе предстоит пройти", WIDTH // 2 - 150, HEIGHT // 2 + 220)
    draw_text("через темные уровни!", WIDTH // 2 - 80, HEIGHT // 2 + 260)
    draw_text("Только смелые выживут!", WIDTH // 2 - 100, HEIGHT // 2 + 300)

    # Обновление экрана
    pygame.display.flip()

    # Установка частоты кадров (FPS)
    clock.tick(10)

pygame.quit()
sys.exit()
