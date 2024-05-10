import pygame
import sys
import random
import time
import chatroom
import hangman
import hangman2

pygame.init()
WINDOW_WIDTH = 1511
WINDOW_HEIGHT = 840
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

def load_images():
    images = {
        "grass": pygame.image.load('images/grass.png'),
        "cloud": pygame.image.load('images/cloud.png'),
        "cloud2": pygame.image.load('images/cloud.png'),
        "cloud3": pygame.image.load('images/cloud.png'),
        "cloud4": pygame.image.load('images/cloud.png'),
        "cloud5": pygame.image.load('images/cloud.png')
    }
    return images

images = load_images()
def set_image_positions():
    positions = {
        "grass": (0, 180),
        "cloud": (0, 10),
        "cloud2": (210, 20),
        "cloud3": (1120, 58),
        "cloud4": (1280, 10),
        "cloud5": (440, 14)

    }
    return {key: image.get_rect(topleft=position) for key, image in images.items() for position in [positions[key]]}

image_rects = set_image_positions()


def room(number):
    if number == 1:
        hangman.run_game()
    elif number == 2:
        hangman2.run_game()

font = pygame.font.Font('fonts/Atop-R99O3.ttf', 100)

signin_text = font.render("Select a room to join:", True, (0, 0, 0))
signin_rect = signin_text.get_rect(center=((WINDOW_WIDTH // 2), 230))

chatroom_text = font.render("Main Chatroom", True, (0, 0, 0))
chatroom_text_rect = chatroom_text.get_rect(center=(750, 650))


room1_button_text = font.render("Room 1", True, BLACK)
room1_button_rect = room1_button_text.get_rect(center=((WINDOW_WIDTH // 2)-300, 500))

room2_button_text = font.render("Room 2", True, BLACK)
room2_button_rect = room2_button_text.get_rect(center=((WINDOW_WIDTH // 2)+300, 500))

grass_image_scaled = pygame.transform.scale(images["grass"], (1511, 700))


def sending():
    running = True
    start_time = time.time()
    while running:
        updated_time = time.time()
        for event in pygame.event.get():
            if updated_time - start_time >= 15:
                selected_room = random.choice([1, 2])
                room(selected_room)
                pygame.quit()
                sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if room1_button_rect.collidepoint(event.pos):
                    room(1)
                    pygame.quit()
                    sys.exit()
                elif chatroom_text_rect.collidepoint(event.pos):
                    chatroom.run_game()
                elif room2_button_rect.collidepoint(event.pos):
                    room(2)
                    pygame.quit()
                    sys.exit()

        window.fill((104,193,249))
        window.blit(chatroom_text, chatroom_text_rect)

        pygame.draw.rect(window, BLACK, room1_button_rect, 2)
        window.blit(room1_button_text, room1_button_rect)
        pygame.draw.rect(window, BLACK, room2_button_rect, 2)
        window.blit(room2_button_text, room2_button_rect)
        window.blit(signin_text, signin_rect)
        window.blit(grass_image_scaled, image_rects["grass"])
        mountain_image_scaled = pygame.transform.scale(images["cloud"], (190, 95))
        window.blit(mountain_image_scaled, image_rects["cloud"])
        mountain_image_scaled = pygame.transform.scale(images["cloud2"], (260, 130))
        window.blit(mountain_image_scaled, image_rects["cloud2"])
        mountain_image_scaled = pygame.transform.scale(images["cloud3"], (200, 100))
        window.blit(mountain_image_scaled, image_rects["cloud3"])
        mountain_image_scaled = pygame.transform.scale(images["cloud4"], (240, 120))
        window.blit(mountain_image_scaled, image_rects["cloud4"])
        mountain_image_scaled = pygame.transform.scale(images["cloud5"], (170, 85))
        window.blit(mountain_image_scaled, image_rects["cloud5"])
        pygame.display.flip()