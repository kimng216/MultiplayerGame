import pygame
import sys
import socket
import login
import putserverinfohere

pygame.init()
screen_width, screen_height = 1500, 840
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Welcome to the Game!")
clock = pygame.time.Clock()
font = pygame.font.SysFont('times new roman', 32)

host = putserverinfohere.ipaddress  # The server's hostname or IP address
port = putserverinfohere.port
white = (255, 255, 255)
black = (0, 0, 0)
grey = (200, 200, 200)


hangman_font = pygame.font.Font('fonts/Atop-R99O3.ttf', 100)
hangman_font_2 = pygame.font.Font('fonts/showg.tff.TTF', 85)
hangman_font_3 = pygame.font.Font('fonts/a_ReportSansRgh.ttf', 75)

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    client.connect(server_address)
    connect = True
    print("connected")
except Exception as e:
    print(e)
    connect = False
    print("not connected")


def load_images():
    images = {
        "title": pygame.image.load('images/title.png'),
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
        "title": (245, 30),
        "grass": (0, 180),
        "cloud": (0,10),
        "cloud2": (160, 50),
        "cloud3": (1120, 58),
        "cloud4": (1280, 10),
        "cloud5": (20, 150)
    }
    return {key: image.get_rect(topleft=position) for key, image in images.items() for position in [positions[key]]}

image_rects = set_image_positions()

def display_main_menu():
    screen.fill((104,193,249))

    mountain_image_scaled = pygame.transform.scale(images["cloud"], (190, 95))
    screen.blit(mountain_image_scaled, image_rects["cloud"])
    mountain_image_scaled = pygame.transform.scale(images["cloud2"], (260, 130))
    screen.blit(mountain_image_scaled, image_rects["cloud2"])
    mountain_image_scaled = pygame.transform.scale(images["cloud3"], (200, 100))
    screen.blit(mountain_image_scaled, image_rects["cloud3"])
    mountain_image_scaled = pygame.transform.scale(images["cloud4"], (240, 120))
    screen.blit(mountain_image_scaled, image_rects["cloud4"])
    mountain_image_scaled = pygame.transform.scale(images["cloud5"], (170, 85))
    screen.blit(mountain_image_scaled, image_rects["cloud5"])

    play_text = hangman_font.render("Play", True, (0, 0, 0))
    play_text_rect = play_text.get_rect(center=((screen_width // 2) - 200, 550))
    screen.blit(play_text, play_text_rect)

    quit_text = hangman_font.render("Quit", True, (0, 0, 0))
    quit_text_rect = quit_text.get_rect(center=((screen_width // 2) + 200, 550))
    screen.blit(quit_text, quit_text_rect)

    game_text = hangman_font_2.render("Game", True, (0, 0, 0))
    game_text_rect = game_text.get_rect(center=((screen_width // 2), 380))
    screen.blit(game_text, game_text_rect)

    screen.blit(images["title"], image_rects["title"].topleft)

    grass_image_scaled = pygame.transform.scale(images["grass"], (1511, 700))
    screen.blit(grass_image_scaled, image_rects["grass"])


    pygame.display.flip()


def display_login_screen():
    screen.fill((255, 255, 255))

    hex_color = 0x68c1f9
    red = (hex_color >> 16) & 0xFF
    green = (hex_color >> 8) & 0xFF
    blue = hex_color & 0xFF
    screen.fill((red, green, blue))


    signin_text = hangman_font.render("Sign In", True, (0, 0, 0))
    signin_rect = signin_text.get_rect(center=((screen_width // 2), 200))
    screen.blit(signin_text, signin_rect)

    sign_up = hangman_font.render("Sign Up", True, (0, 0, 0))
    sign_up_rect = sign_up.get_rect(center=((screen_width // 2), 500))
    screen.blit(sign_up, sign_up_rect)

    pygame.draw.line(screen, (0, 0, 0), ((screen_width//2) - 75, 350), ((screen_width//2) + 75, 350), 8)

    mountain_image_scaled = pygame.transform.scale(images["cloud"], (190, 95))
    screen.blit(mountain_image_scaled, image_rects["cloud"])
    mountain_image_scaled = pygame.transform.scale(images["cloud4"], (240, 120))
    screen.blit(mountain_image_scaled, image_rects["cloud4"])
    mountain_image_scaled = pygame.transform.scale(images["cloud5"], (170, 85))
    screen.blit(mountain_image_scaled, image_rects["cloud5"])
    grass_image_scaled = pygame.transform.scale(images["grass"], (1511, 700))
    screen.blit(grass_image_scaled, image_rects["grass"])
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if signin_rect.collidepoint(mouse_pos):
                login.sign_in()
            elif sign_up_rect.collidepoint(mouse_pos):
                login.sign_up()

    pygame.display.flip()


def menu():
    menu_running = True
    play_clicked = False

    play_text = hangman_font.render("Play", True, (0, 0, 0))
    play_text_rect = play_text.get_rect(center=((screen_width // 2) - 200, 550))
    quit_text = hangman_font.render("Quit", True, (0, 0, 0))
    quit_text_rect = quit_text.get_rect(center=((screen_width // 2) + 200, 550))

    while menu_running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_text_rect.collidepoint(mouse_pos):
                    play_clicked = True
                elif quit_text_rect.collidepoint(mouse_pos):
                    client.close() if client else None
                    pygame.quit()
                    sys.exit()
        if play_clicked:
            pygame.time.wait(100)  # dont remove this
            display_login_screen()
            client.close()
        else:
            display_main_menu()

menu()
pygame.quit()
sys.exit()
