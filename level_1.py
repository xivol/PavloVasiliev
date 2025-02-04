import pygame
import sys
from enviroment import ENV, Block, Movable_Block

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_SIZE = 50
WALL_COLOR = (255, 0, 0)
BACKGROUND_COLOR = (0, 0, 0)
GAME_OVER_COLOR = (128, 0, 0)
START_COLOR = (0, 255, 225)  # Зеленый для начальной точки
END_COLOR = (0, 0, 255)    # Синий для конечной точки

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Лабиринт в аду")

player_pos = [50, 50]

walls = [
    pygame.Rect(0, 0, 800, 20),
    pygame.Rect(100, 0, 20, 400),
    pygame.Rect(680, 0, 20, 500),
    pygame.Rect(0, 480, 300, 20),
    pygame.Rect(400, 480, 300, 20),
    pygame.Rect(300, 300, 20, 200),
    pygame.Rect(300, 300, 200, 20),
]

start_point = pygame.Rect(50, 50, PLAYER_SIZE, PLAYER_SIZE)
end_point = pygame.Rect(700, 500, PLAYER_SIZE, PLAYER_SIZE)

def draw_player():
    pygame.draw.rect(screen, (0, 255, 0), (player_pos[0], player_pos[1], PLAYER_SIZE, PLAYER_SIZE))

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
    player_pos[0], player_pos[1] = start_point.topleft
    tst = Movable_Block(pos=(100, 50), velocity=(0, 7))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ENV.display_screen = None
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_pos[0] -= 5
        if keys[pygame.K_d]:
            player_pos[0] += 5
        if keys[pygame.K_w]:
            player_pos[1] -= 5
        if keys[pygame.K_s]:
            player_pos[1] += 5

        player_rect = pygame.Rect(player_pos[0], player_pos[1], PLAYER_SIZE, PLAYER_SIZE)

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
        draw_player()
        tst.draw(screen)
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    level_1(screen)