import pygame
import sys
import socket
import config
import threading
import putserverinfohere
import room

pygame.init()
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
banned = False
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

smallerfont = pygame.font.SysFont("Arial", 28)
font = pygame.font.SysFont("Arial", 36)
big_font = pygame.font.SysFont("Arial", 48)
guesses = []
guessed_letters = set()
username = config.name

def initialize_connection():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (putserverinfohere.ipaddress,putserverinfohere.port)
        client.connect(server_address)
        need = f"need world chat,,"
        client.sendall(need.encode("utf-8"))
        return  client
    except Exception as e:
        print(e)
        return None


def draw_chatbox(input_text):
    pygame.draw.rect(window, WHITE, (100, 650, 835, 100))  # Small white box
    pygame.draw.rect(window, WHITE, (100, 150, 835, 500))  # Big white box
    pygame.draw.rect(window, BLACK, (100, 150, 835, 500), 4)  # Big box outline
    pygame.draw.rect(window, BLACK, (100, 650, 835, 100), 4)  # Small box outline
    text_surface = font.render(input_text, True, BLACK)
    text_rect = text_surface.get_rect(left=120, centery=700)
    window.blit(text_surface, text_rect)

def click_on_chat(mouse_pos):
    chatbox = pygame.Rect(100, 650, 835, 100)
    return chatbox.collidepoint(mouse_pos)

def send_data_to_server(data_type, username, other):
    global client
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
                    send_data_to_server('world chat', username, input_text)
        except Exception as e:
            print("An error occurred:", e)
            return ''

def draw_messages(messages):
    y_offset = 150  # Start position for the first message
    for message in messages[-10:]:  # Display only the last 12 messages
        text_surface = font.render(message, True, BLACK)
        text_rect = text_surface.get_rect(left=130, top=y_offset)
        window.blit(text_surface, text_rect)
        y_offset += 50

def run_game():
    global worldmessages,client
    client = initialize_connection()
    pygame.display.set_caption("Chatroom")
    input_text = ''
    worldmessages = []
    chat_active = False
    threading.Thread(target=listen_for_messages, args=(client, worldmessages), daemon=True).start()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_text_rect.collidepoint(event.pos):
                    room.sending()
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if click_on_chat(mouse_pos):
                        chat_active = True
                    else:
                        chat_active = False
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
                    pass


        window.fill((104, 193, 249))

        back_text = font.render("Back", True, (0, 0, 0))
        back_text_rect = back_text.get_rect(center=(1100, 550))
        window.blit(back_text, back_text_rect)
        draw_chatbox(input_text)
        draw_messages(worldmessages)
        pygame.display.flip()
        pygame.time.Clock().tick(30)

def listen_for_messages(client, messages):
    while True:
        try:
            data = client.recv(1024).decode('utf-8')
            print(data)
            info = data.split(',')
            data_type, message,other = info
            if data_type == 'receivechatmessage':
                messages.append(message)

            if data_type == 'worldchat':
                messages.append(message)


        except Exception as e:
            print(e)
            break