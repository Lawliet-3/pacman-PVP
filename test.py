import pygame
import sys

import pygame
import sys

pygame.init()

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

if __name__ == "__main__":
    num_players = game_menu()
    print("Selected number of players:", num_players)

    # Now you can use the 'num_players' variable in your game code to determine how many players to initialize.

