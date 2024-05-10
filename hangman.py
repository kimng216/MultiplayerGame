import pygame
import sys
import socket
import config
import threading
import putserverinfohere

pygame.init()
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
banned = False
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

smallerfont = pygame.font.SysFont("Arial", 24)
font = pygame.font.SysFont("Arial", 36)
big_font = pygame.font.SysFont("Arial", 48)
guesses = []
guessed_letters = set()

def initialize_connection():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (putserverinfohere.ipaddress,putserverinfohere.port)
        client.connect(server_address)
        return  client
    except Exception as e:
        print(e)
        return None


def load_images():
    images = {
        "ban": pygame.image.load('images/Ban.png')
    }
    return images

images = load_images()
def set_image_positions():
    positions = {
        "ban": (1000, 300)
    }
    return {key: image.get_rect(topleft=position) for key, image in images.items() for position in [positions[key]]}

image_rects = set_image_positions()
def draw_hangman(mistakes):
    pygame.draw.line(window, (0, 0, 0), (100, 60), (100, 460), 10)
    pygame.draw.line(window, (0, 0, 0), (100, 60), (300, 60), 10)
    pygame.draw.line(window, (0, 0, 0), (100, 60), (100, 110), 10)
    pygame.draw.line(window, (0, 0, 0), (300, 60), (300, 110), 2)
    pygame.draw.line(window, (0, 0, 0), (50, 460), (150, 460), 10)

    if mistakes >= 1:
        pygame.draw.circle(window, (0, 0, 0), (300, 160), 50, 2)
    if mistakes >= 2:
        pygame.draw.line(window, (0, 0, 0), (300, 210), (300, 360), 2)
    if mistakes >= 3:
        pygame.draw.line(window, (0, 0, 0), (300, 260), (250, 310), 2)
    if mistakes >= 4:
        pygame.draw.line(window, (0, 0, 0), (300, 260), (350, 310), 2)
    if mistakes >= 5:
        pygame.draw.line(window, (0, 0, 0), (300, 360), (250, 460), 2)
    if mistakes >= 6:
        pygame.draw.line(window, (0, 0, 0), (300, 360), (350, 460), 2)


def draw_word_to_guess(word, guessed_letters, mistakes):
    display_word = ""
    for letter in word:
        if letter in guessed_letters:
            display_word += letter + " "
        else:
            display_word += "_ "
    text_surface = font.render(display_word, True, BLACK)
    text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 5, 600))
    window.blit(text_surface, text_rect)

    display_word_2 = []
    for letters in display_word:
        display_word_2.append(letters)
    if "_" not in display_word_2 and mistakes < 6:
        winner()

def winner():
    winner_surface = big_font.render(f"You Win! Good game!", True, BLACK)
    winner_rect = winner_surface.get_rect(center=(WINDOW_WIDTH // 2, 600 - 270))
    pygame.draw.rect(window, WHITE, (winner_rect.x - 10, winner_rect.y - 10, winner_rect.width + 20, winner_rect.height + 20))
    window.blit(winner_surface, winner_rect)

def draw_unused_letters(guessed_letters):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    x_offset = 750
    y_offset = 100
    letter_spacing = 32
    line_limit = 7
    line_count = 0
    box_width = 300
    box_height = 200
    pygame.draw.rect(window, BLACK, (x_offset, y_offset, box_width, box_height), 4)
    font.set_underline(True)
    text_surface = font.render("Unused Letters", True, BLACK)
    font.set_underline(False)
    text_rect = text_surface.get_rect(center=(x_offset + box_width - 148, y_offset+25))
    window.blit(text_surface, text_rect)
    for letter in alphabet:
        if letter not in guessed_letters:
            text_surface = font.render(letter, True, BLACK)
            text_rect = text_surface.get_rect(center=(x_offset + 50, y_offset + 70))
            window.blit(text_surface, text_rect)
            x_offset += letter_spacing
            line_count += 1
            if line_count >= line_limit:
                line_count = 0
                y_offset += letter_spacing
                x_offset = 750

def draw_wrong_letters(guessed_letters, mistakes):
    x_offset = 420
    y_offset = 100
    letter_spacing = 32
    wrong_guesses = [letter for letter in guessed_letters if letter not in current_word]
    box_width = 300
    box_height = 200
    line_limit = 7
    line_count = 0
    pygame.draw.rect(window, BLACK, (x_offset, y_offset, box_width, box_height), 4)
    font.set_underline(True)
    text_surface = font.render("Wrong Letters", True, BLACK)
    font.set_underline(False)
    text_rect = text_surface.get_rect(center=(x_offset + box_width - 148, y_offset + 25))
    window.blit(text_surface, text_rect)
    for letter in wrong_guesses:
        text_surface = font.render(letter, True, BLACK)
        text_rect = text_surface.get_rect(center=(x_offset+50, y_offset+70))
        window.blit(text_surface, text_rect)
        x_offset += letter_spacing
        line_count += 1
        if line_count >= line_limit:
            line_count = 0
            y_offset += letter_spacing
            x_offset = 750
    if mistakes >= 6:
        lost_surface = big_font.render("GAME OVER. EVERYONE LOST", True, BLACK)
        lost_rect = lost_surface.get_rect(center=(WINDOW_WIDTH // 2, 600 - 270))
        pygame.draw.rect(window, WHITE,
                         (lost_rect.x - 10, lost_rect.y - 10, lost_rect.width + 20, lost_rect.height + 20))
        window.blit(lost_surface, lost_rect)

def correct_letters(word, guessed_letters):
    display_word = ""
    for letter in word:
        if letter in guessed_letters:
            display_word += letter + " "
        else:
            display_word += "_ "
    return display_word

def draw_chatbox(input_text):
    pygame.draw.rect(window, WHITE, (420, 650, 635, 100))  # Small white box
    pygame.draw.rect(window, WHITE, (420, 350, 635, 300))  # Big white box
    pygame.draw.rect(window, BLACK, (420, 350, 635, 300), 4)  # Big box outline
    pygame.draw.rect(window, BLACK, (420, 650, 635, 100), 4)  # Small box outline
    text_surface = font.render(input_text, True, BLACK)
    text_rect = text_surface.get_rect(left=430, centery=675)
    window.blit(text_surface, text_rect)



def draw_messages(messages):
    y_offset = 400  # Start position for the first message
    for message in messages[-5:]:  # Display only the last 5 messages
        text_surface = font.render(message, True, BLACK)
        text_rect = text_surface.get_rect(left=430, top=y_offset)
        window.blit(text_surface, text_rect)
        y_offset += 50

def draw_guesses(guesses):
    y_offset = 100  # Start position for the first message
    for message in guesses[-8:]:  # Display only the last 5 messages
        text_surface = smallerfont.render(message, True, BLACK)
        text_rect = text_surface.get_rect(left=1100, top=y_offset)
        window.blit(text_surface, text_rect)
        y_offset += 50


def click_on_chat(mouse_pos):
    chatbox = pygame.Rect(420, 650, 635, 300)
    return chatbox.collidepoint(mouse_pos)

def send_data_to_server(data_type, username, other):
        client.sendall(f"{data_type},{username},{other}".encode('utf-8'))


def send_chat_to_server(input_text):
    username = config.name
    if input_text:
        try:
            with open("files/banned_words.txt", "r") as file1:
                banned_words = file1.read().splitlines()
                if input_text in banned_words:
                    send_data_to_server('ban',username,"banned")
                    global banned
                    banned = True
                else:
                    send_data_to_server('chat', username, input_text)

        except Exception as e:
            print("An error occurred:", e)
            return ''
def draw_buttons():
    pygame.draw.rect(window, RED, (50, 740, 150, 50))
    quit_text = font.render("Quit", True, BLACK)
    quit_rect = quit_text.get_rect(center=(120, 765))
    window.blit(quit_text, quit_rect)

    pygame.draw.rect(window, RED, (250, 740, 150, 50))
    restart_text = font.render("Restart", True, BLACK)
    restart_rect = restart_text.get_rect(center=(320, 765))
    window.blit(restart_text, restart_rect)

def run_game():
    global mistakes, guessed_letters,banned,current_word,server_letter,client,restart
    pygame.display.set_caption("Hangman Room 1")
    client = initialize_connection()
    input_text = ""
    x = 0
    mistakes = 0
    chat_active = False
    restart = False
    server_messages = []

    current_word = ''
    server_letter = ''
    send_data_to_server('need word', config.name, 'nothing')
    pygame.time.wait(50)
    send_data_to_server('joined', config.name, 'nothing')
    threading.Thread(target=listen_for_messages, args=(client, server_messages), daemon=True).start()
    pygame.time.wait(150)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                send_data_to_server(f'quit', config.name, 'nothing')
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if click_on_chat(mouse_pos):
                        chat_active = True
                    else:
                        chat_active = False
                    if 50 <= mouse_pos[0] <= 150 and 740 <= mouse_pos[1] <= 790:
                        send_data_to_server(f'quit', config.name, 'nothing')
                        pygame.quit()
                        sys.exit()
                    if 250 <= mouse_pos[0] <= 350 and 740 <= mouse_pos[1] <= 790:
                        send_data_to_server(f'restart','nothing','nothing')
            elif event.type == pygame.KEYDOWN:
                if chat_active:
                    if event.key == pygame.K_RETURN:
                        send_chat_to_server(input_text)
                        input_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.key == pygame.K_SPACE:
                        input_text += ' '
                    elif event.key in range(97, 123):
                        letter = chr(event.key).upper()
                        input_text += letter
                else:
                    if event.key in range(97, 123):
                        letter = chr(event.key).upper()
                        send_data_to_server(f'guess', config.name, letter)
                        pygame.time.wait(100)



        window.fill((104,193,249))
        if banned:
            window.blit(images["ban"], image_rects["ban"].topleft)
            x += 1
            if x > 100:
                sys.exit()
        if restart == True:
            mistakes = 0
            guessed_letters = set()
        draw_hangman(mistakes)
        restart = False
        correct_letters(current_word, guessed_letters)
        correct_letters(current_word, guessed_letters)
        draw_word_to_guess(current_word, guessed_letters, mistakes)
        draw_unused_letters(guessed_letters)
        draw_wrong_letters(guessed_letters, mistakes)
        draw_chatbox(input_text)
        draw_guesses(guesses)
        draw_messages(server_messages)
        draw_buttons()
        pygame.display.flip()
        pygame.time.Clock().tick(30)

def listen_for_messages(client, messages):
    while True:
        try:
            data = client.recv(1024).decode('utf-8')
            info = data.split(',')
            data_type, message,other = info
            if data_type == 'chat':
                messages.append(message)
            if data_type == 'word':
                global current_word,guesses,restart
                current_word = message
                print(current_word)
                restart = True
            if data_type == 'guess':
                global server_letter,mistakes
                server_letter = other
                guesses.append(f"User: {message}, guessed the letter: {other}")
                draw_guesses(guesses)
                if server_letter not in guessed_letters:
                    guessed_letters.add(server_letter)
                    if server_letter not in current_word:
                        mistakes += 1
            if data_type == 'joined':
                guesses.append(message)
            if data_type == 'quit':
                guesses.append(message)
            if data_type == 'ban':
                guesses.append(message)

        except Exception as e:
            print("An error occurred:", e)
            break
