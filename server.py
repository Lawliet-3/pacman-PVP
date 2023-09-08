import socket
from _thread import *
from world import World, world_data
from player import Player
import pickle, pygame
import sys


#start the server
server = "192.168.0.103"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

current_player = 0

#game variables and constants
width = 1000
height = 1000
tile_size = 50
frame_rate = 45
player_count = 0

WHITE = (255,255,255)
STOPPED = 0
LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4

# screen = pygame.display.set_mode((width, height))
# pygame.display.set_caption("Pacman Game")

pygame.init()
bauhaus = pygame.font.SysFont('Bauhaus 93', 30)
bauhaus_big = pygame.font.SysFont('Bauhaus 93', 150)

#create the game and players
players = [Player(50,50, 0), Player(50,900, 1), Player(900,50, 2), Player(900,900, 3)]
player_moves = [-1, -1, -1, -1]
world = World(world_data)
for player in players:
    world.player_group.add(player)

# Set up the menu window
menu_width = 400
menu_height = 400
menu_screen = pygame.display.set_mode((menu_width, menu_height))
pygame.display.set_caption("Game Menu")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define fonts
font = pygame.font.Font(None, 36)

def game_menu():
    while True:
        menu_screen.fill(WHITE)

        # Create menu title
        title_text = font.render("How many players?", True, BLACK)
        title_rect = title_text.get_rect(center=(menu_width // 2, 80))
        menu_screen.blit(title_text, title_rect)

        # Create buttons for different player counts
        player_buttons = []
        for i in range(2, 5):
            player_button = pygame.Rect(100, 150 + 70 * (i - 2), 200, 50)
            player_buttons.append(player_button)
            pygame.draw.rect(menu_screen, BLACK, player_button)
            player_text = font.render(f"{i} Players", True, WHITE)
            player_rect = player_text.get_rect(center=player_button.center)
            menu_screen.blit(player_text, player_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, button in enumerate(player_buttons):
                    if button.collidepoint(mouse_pos):
                        return i + 2  # Returns 2 for the first button, 3 for the second, and 4 for the third

def threaded_client(conn, player_num):
    conn.send(pickle.dumps((players[player_num].rect.x, players[player_num].rect.y, player_num)))
    reply = None

    while True:
        try:
            data = pickle.loads(conn.recv(4096))
            if not data:
                print("Disconnected")
                break
            else:
                player_moves[player_num] = data
                reply = world.export() #sends the positions and other necessary display data to each client

            conn.send(pickle.dumps(reply))

        except Exception as e: 
            print(e)

def check_for_connection():
    global current_player
    while True:
        conn, addr = s.accept()
        print("Connected to:", addr)

        start_new_thread(threaded_client, (conn, current_player))
        current_player += 1

def main():
    start_new_thread(check_for_connection, ())
    player_count = game_menu()
    print("count",player_count)
    run = True
    clock = pygame.time.Clock()
    # world.draw(screen)
    # pygame.display.update()
    delay = 200

    while run:
        clock.tick(frame_rate)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        #update world
        if current_player == player_count: #only update if all players have loaded in
            delay -=1
            if delay < 0:
                world.update(player_moves)

        #draw screen. only use for debug purposes
        # screen.fill((0, 0, 0))
        # world.draw(screen)
        # pygame.display.update()

main()