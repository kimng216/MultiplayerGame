import pygame
import sys
import socket
import room
import config
import putserverinfohere
pygame.init()

# Setup display
screen = pygame.display.set_mode((900, 800))
font = pygame.font.Font('fonts/Atop-R99O3.ttf', 80)
font_2 = pygame.font.Font('fonts/Atop-R99O3.ttf', 50)
arial = pygame.font.SysFont("Arial", 50)

# Colors and fonts
white = (255, 255, 255)
black = (0, 0, 0)
grey = (200, 200, 200)

# Input boxes: Username, Password for both login and signup
login_input_boxes = {
    "username": pygame.Rect(510, 360, 400, 50),
    "password": pygame.Rect(510, 510, 400, 50)
}
signup_input_boxes = {
    "username": pygame.Rect(750, 360, 400, 50),
    "password": pygame.Rect(750, 510, 400, 50)
}
login_inputs = {key: "" for key in login_input_boxes}
signup_inputs = {key: "" for key in signup_input_boxes}

active_box = None

# Network settings
host = putserverinfohere.ipaddress  # The server's hostname or IP address
port = putserverinfohere.port

def load_images():
    images = {
        "grass": pygame.image.load('images/grass.png'),
        "cloud3": pygame.image.load('images/cloud.png'),
        "cloud4": pygame.image.load('images/cloud.png'),
    }
    return images
images = load_images()

def set_image_positions():
    positions = {
        "grass" : (0, 180),
        "cloud3": (1120, 58),
        "cloud4": (1280, 10),
    }
    return {key: image.get_rect(topleft=position) for key, image in images.items() for position in [positions[key]]}
image_rects = set_image_positions()
def draw_box(screen, rect, color):
    pygame.draw.rect(screen, color, rect, 0)
    pygame.draw.rect(screen, black, rect, 2)

def send_data_to_server(data_type, username, password):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        data = f"{data_type},{username},{password}"
        s.sendall(data.encode('utf-8'))
        response = s.recv(1024).decode('utf-8')
        print(response)
        if response == "Login successful":
            config.name = username
            s.close()
            room.sending()
            pygame.quit()
            sys.exit()
        elif response == "Login failed":
            global loginfailed
            loginfailed = True
        elif response == "Signup successful":
            global signupsucceeded
            signupsucceeded = True
        elif response == "Signup failed: Username already exists":
            global signupfailed
            signupfailed = True


def sign_in():
    global loginfailed
    running = True
    login = False
    loginfailed = True
    pygame.display.set_caption("Sign In")

    username_text = font_2.render('Username: ', True, black)
    password_text = font_2.render('Password: ', True, black)
    enter_credentials = font.render('Please enter your', True, black)
    enter_credentials_2 = font.render('username and password', True, black)
    active_box = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for key in login_input_boxes:
                    if login_input_boxes[key].collidepoint(event.pos):
                        active_box = key
                    if signup_text_rect.collidepoint(event.pos):
                        sign_up()
                    if submit_text_rect.collidepoint(event.pos):
                        send_data_to_server('login', login_inputs['username'], login_inputs['password'])
                        login = True
            elif event.type == pygame.KEYDOWN:
                if active_box is not None:
                    if event.key == pygame.K_RETURN:
                        send_data_to_server('login', login_inputs['username'], login_inputs['password'])
                        login = True
                    elif event.key == pygame.K_BACKSPACE:
                        login_inputs[active_box] = login_inputs[active_box][:-1]
                    else:
                        login_inputs[active_box] += event.unicode
            else:
                pass

        screen.fill((104, 193, 249))
        if login == True:
            if loginfailed == True:
                submit_text = font_2.render("Login failed,incorrect username or password", True, (0, 0, 0))
                submit_text_rect = submit_text.get_rect(center=(700, 200))
                screen.blit(submit_text, submit_text_rect)

        mountain_image_scaled = pygame.transform.scale(images["cloud3"], (200, 100))
        screen.blit(mountain_image_scaled, image_rects["cloud3"])
        mountain_image_scaled = pygame.transform.scale(images["cloud4"], (240, 120))
        screen.blit(mountain_image_scaled, image_rects["cloud4"])
        grass_image_scaled = pygame.transform.scale(images["grass"], (1511, 700))
        screen.blit(grass_image_scaled, image_rects["grass"])

        signup_text = font.render("Sign up", True, (0, 0, 0))
        signup_text_rect = signup_text.get_rect(center=(1000, 650))
        screen.blit(signup_text, signup_text_rect)

        submit_text = font.render("Submit", True, (0, 0, 0))
        submit_text_rect = submit_text.get_rect(center=(500, 650))
        screen.blit(submit_text, submit_text_rect)
        if login == False:
            screen.blit(enter_credentials, (200, 80))
            screen.blit(enter_credentials_2, (100, 180))
        screen.blit(username_text, (200, 350))
        screen.blit(password_text, (200, 500))
        for key, box in login_input_boxes.items():
            draw_box(screen, box, grey)
            text_surface = arial.render(login_inputs[key], True, black)
            screen.blit(text_surface, (box.x + 4, box.y - 3))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


def sign_up():
    global signupfailed,signupsucceeded
    hide_signup_password = False
    running = True
    signupfailed = False
    signupsucceeded = False
    pygame.display.set_caption("Sign Up")
    signup = False
    username_text = font_2.render('Enter a username: ', True, black)
    password_text = font_2.render('Enter a password: ', True, black)
    enter_credentials = font.render('Choose a username', True, black)
    enter_credentials_2 = font.render('and password. Don\'t forget it!', True, black)

    active_box = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for key in signup_input_boxes:
                    if signup_input_boxes[key].collidepoint(event.pos):
                        active_box = key
                    if signin_text_rect.collidepoint(event.pos):
                        sign_in()
                    if submit_text_rect.collidepoint(event.pos):
                        send_data_to_server('signup', signup_inputs['username'], signup_inputs['password'])
                        signup = True
            elif event.type == pygame.KEYDOWN:
                if active_box is not None:
                    if event.key == pygame.K_RETURN:
                        send_data_to_server('signup', signup_inputs['username'], signup_inputs['password'])
                        signup = True
                    elif event.key == pygame.K_BACKSPACE:
                        signup_inputs[active_box] = signup_inputs[active_box][:-1]
                    else:
                        signup_inputs[active_box] += event.unicode
            else:
                pass

        screen.fill((104,193,249))


        signin_text = font.render("Sign In", True, (0, 0, 0))
        signin_text_rect = signin_text.get_rect(center=(1000, 650))
        screen.blit(signin_text, signin_text_rect)


        submit_text = font.render("Submit", True, (0, 0, 0))
        submit_text_rect = submit_text.get_rect(center=(500, 650))
        screen.blit(submit_text, submit_text_rect)
        if signup == True:
            if signupsucceeded == True:
                submit_text = font_2.render("Account created. Sign in with your new account", True, (0, 0, 0))
                submit_text_rect = submit_text.get_rect(center=(700, 200))
                screen.blit(submit_text, submit_text_rect)
                if signupfailed == True:
                    signupfailed = False

            elif signupfailed == True:
                submit_text = font_2.render("sign up failed. That username is already taken", True, (0, 0, 0))
                submit_text_rect = submit_text.get_rect(center=(700, 200))
                screen.blit(submit_text, submit_text_rect)

        mountain_image_scaled = pygame.transform.scale(images["cloud3"], (200, 100))
        screen.blit(mountain_image_scaled, image_rects["cloud3"])
        mountain_image_scaled = pygame.transform.scale(images["cloud4"], (240, 120))
        screen.blit(mountain_image_scaled, image_rects["cloud4"])
        grass_image_scaled = pygame.transform.scale(images["grass"], (1511, 700))
        screen.blit(grass_image_scaled, image_rects["grass"])
        if signup == False:
            screen.blit(enter_credentials, (200, 80))
            screen.blit(enter_credentials_2, (100, 180))

        screen.blit(username_text, (200, 350))
        screen.blit(password_text, (200, 500))
        if hide_signup_password == False:
            for key, box in signup_input_boxes.items():
                draw_box(screen, box, grey)
                text_surface = arial.render(signup_inputs[key], True, black)
                screen.blit(text_surface, (box.x + 4, box.y - 3))

        pygame.display.flip()

    pygame.quit()
    sys.exit()
