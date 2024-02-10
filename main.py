import sys
import pygame
from os import listdir
import random
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

# Розмір нашого вікна
screen = width, height = 800, 600

# Кольори які ми будем використовувати
BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GOLD = 255, 215, 0
GREEN = 0, 255, 0

font = pygame.font.SysFont('Impact', 50)


# Вікно
main_surface = pygame.display.set_mode(screen)
game_over_text = font.render('GAME OVER', True, RED)
game_over_rect = game_over_text.get_rect(center=main_surface.get_rect().center)


IMGS_PATH = 'goose'
bonSfx = pygame.mixer.Sound('sound_bonus.wav')
pygame.mixer.music.load("sound2.mp3")
pygame.mixer.music.set_volume(0.1)
collision_sound = pygame.mixer.Sound('collision_sound.mp3')
collision_sound.set_volume(0.1)
pygame.mixer.music.play(-1)

# Параметри нашого GOOSE
player_imgs = [pygame.image.load(IMGS_PATH + '/' + file).convert_alpha() for file in listdir(IMGS_PATH)]
for i in range(len(player_imgs)):
    player_imgs[i] = pygame.transform.scale(player_imgs[i], (player_imgs[i].get_width() // 2, player_imgs[i].get_height() // 2))
player = player_imgs[0]
player_speed = 6
player_rect = player.get_rect(center=(width // 2, height // 2))


# Вороги та бонуси (за допомогою функції def )
# noinspection PyUnreachableCode
def create_enemy():
    enemy = pygame.image.load("enemy.png").convert_alpha()
    enemy = pygame.transform.scale(enemy, (enemy.get_width() // 2, enemy.get_height() // 2))
    enemy_rect = pygame.Rect(width, random.randint(0, height-enemy.get_height()), *enemy.get_size())
    enemy_speed = random.randint(2, 5)
    return [enemy, enemy_rect, enemy_speed]
    if enemy_rect.bottom > game_height:
        enemy_rect.bottom = game_height


# noinspection PyUnreachableCode
def create_bonus():
    bonus = pygame.image.load("bonus.png").convert_alpha()
    bonus = pygame.transform.scale(bonus, (bonus.get_width() // 2, bonus.get_height() // 2))
    bonus_rect = pygame.Rect(random.randint(0, width-bonus.get_width()), -bonus.get_height(), *bonus.get_size())
    bonus_speed = random.randint(2, 5)
    return [bonus, bonus_rect, bonus_speed]
    if bonus_rect.right > game_width:
        bonus_rect.right = game_width


bg = pygame.transform.scale(pygame.image.load('background.png').convert(), screen)
bgX = 0
bgX2 = bg.get_width()
bg_speed = 3

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1000)

CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 200)

img_index = 0

scores = 0

enemies = []
bonuses = []


# Цикл гри безкінечний
game_over = False

while not game_over:
    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.mixer.music.play(-1)
            pygame.quit()
            sys.exit()

        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())

        if event.type == CHANGE_IMG:
            img_index += 1
            if img_index == len(player_imgs):
                img_index = 0
            player = player_imgs[img_index]

    pressed_keys = pygame.key.get_pressed()
    bgX -= bg_speed
    bgX2 -= bg_speed

    if bgX < -bg.get_width():
        bgX = bg.get_width()
    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()

    main_surface.blit(bg, (bgX, 0))
    main_surface.blit(bg, (bgX2, 0))
    main_surface.blit(player, player_rect)

    main_surface.blit(font.render(str(scores), True, GREEN), (0, 0))

    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])

        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

        if player_rect.colliderect(enemy[1]):
            collision_sound.play()
            game_over = True

    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])

        if bonus[1].bottom >= height:
            bonuses.pop(bonuses.index(bonus))

        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            pygame.mixer.Sound.play(bonSfx)
            scores += 1

    if not game_over:
        # Керування мячем
        if pressed_keys[K_DOWN] and not player_rect.bottom >= height:
            player_rect = player_rect.move(0, player_speed)

        if pressed_keys[K_UP] and not player_rect.top <= 0:
            player_rect = player_rect.move(0, -player_speed)

        if pressed_keys[K_RIGHT] and not player_rect.right >= width:
            player_rect = player_rect.move(player_speed, 0)

        if pressed_keys[K_LEFT] and not player_rect.left <= 0:
            player_rect = player_rect.move(-player_speed, 0)

    pygame.display.flip()

    # Відображення надпису про кінець гри
    if game_over:
        main_surface.blit(game_over_text, game_over_rect)
        pygame.mixer.music.stop()
        continue_text = font.render('Щоб продовжити, натисни пробіл', True, (GOLD))
        continue_rect = continue_text.get_rect(center=(width // 2, height - 50))
        main_surface.blit(continue_text, continue_rect)
        main_surface.blit(continue_text, continue_rect)
        pygame.display.update()

        # Очікування натискання клавіші для початку нової гри
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # Якщо натиснуто пробіл
                        pygame.mixer.music.play(-1)
                        game_over = False
                        player_rect.center = (width // 2, height // 2)
                        scores = 0
                        enemies.clear()
                        bonuses.clear()
                        waiting = False
