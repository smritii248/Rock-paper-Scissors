
import pygame
import random
import time
import os

# Initialize pygame
pygame.init()

# Window setup
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock, Paper, Scissors")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
BLUE = (30, 144, 255)
GREEN = (0, 200, 0)

# Fonts
font = pygame.font.SysFont(None, 40)
large_font = pygame.font.SysFont(None, 60)

# Load images with fallback placeholder
def safe_load_image(filename):
    try:
        img = pygame.image.load(filename)
        return pygame.transform.scale(img, (150, 150))
    except:
        # placeholder surface with red cross
        surface = pygame.Surface((150, 150))
        surface.fill((200, 200, 200))
        pygame.draw.line(surface, (100, 0, 0), (0, 0), (150, 150), 5)
        pygame.draw.line(surface, (100, 0, 0), (0, 150), (150, 0), 5)
        return surface

rock_img = safe_load_image("rock.png")
paper_img = safe_load_image("paper.png")
scissors_img = safe_load_image("scissors.png")

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    rect = img.get_rect(center=(x, y))
    window.blit(img, rect)

def get_winner(c1, c2):
    if c1 == c2:
        return "draw"
    beats = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
    if beats[c1] == c2:
        return "player"
    return "opponent"

def get_image(choice):
    return {"rock": rock_img, "paper": paper_img, "scissors": scissors_img}[choice]

def load_leaderboard():
    if not os.path.exists("leaderboard.txt"):
        return []
    with open("leaderboard.txt", "r") as f:
        lines = f.readlines()
    scores = []
    for line in lines:
        name, score = line.strip().split(",")
        scores.append((name, int(score)))
    return sorted(scores, key=lambda x: x[1], reverse=True)[:5]

def save_to_leaderboard(name, score):
    scores = load_leaderboard()
    scores.append((name, score))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[:5]
    with open("leaderboard.txt", "w") as f:
        for n, s in scores:
            f.write(f"{n},{s}\n")

def show_leaderboard():
    running = True
    while running:
        window.fill(WHITE)
        draw_text("Leaderboard - Top 5", large_font, BLACK, WIDTH//2, 80)
        scores = load_leaderboard()
        y = 150
        for i, (name, score) in enumerate(scores):
            draw_text(f"{i+1}. {name} - {score}", font, BLUE, WIDTH//2, y)
            y += 50
        draw_text("Press any key to return", font, BLACK, WIDTH//2, y + 50)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return
            elif event.type == pygame.KEYDOWN:
                running = False

def input_name(prompt):
    name = ""
    active = True
    while active:
        window.fill(WHITE)
        draw_text(prompt, font, BLACK, WIDTH//2, HEIGHT//3)
        draw_text(name + "|", font, BLUE, WIDTH//2, HEIGHT//2)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(name) > 0:
                        active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 10 and event.unicode.isprintable():
                        name += event.unicode
    return name

def play_game(mode):
    player_name = input_name("Enter Player 1 Name:")
    opponent_label = "Computer" if mode == "single" else input_name("Enter Player 2 Name:")

    player_score = 0
    opponent_score = 0
    round_num = 1

    clock = pygame.time.Clock()

    while round_num <= 5:
        player_choice = None
        opponent_choice = None
        round_start = time.time()

        while time.time() - round_start < 20:
            timer = 20 - int(time.time() - round_start)
            window.fill(WHITE)
            draw_text(f"{player_name} vs {opponent_label}", font, BLACK, WIDTH//2, 40)
            draw_text(f"Round {round_num}/5", font, BLACK, WIDTH//2, 80)
            draw_text(f"Score: {player_name} {player_score} - {opponent_score} {opponent_label}", font, BLACK, WIDTH//2, 120)
            draw_text(f"Time Left: {timer}s", font, RED if timer <= 5 else BLACK, WIDTH//2, 160)

            keys = pygame.key.get_pressed()

            # Player 1 controls: A,R,S for rock, paper, scissors
            if keys[pygame.K_a]:
                player_choice = "rock"
            elif keys[pygame.K_s]:
                player_choice = "paper"
            elif keys[pygame.K_d]:
                player_choice = "scissors"

            # Player 2 or computer
            if mode == "multi":
                if keys[pygame.K_j]:
                    opponent_choice = "rock"
                elif keys[pygame.K_k]:
                    opponent_choice = "paper"
                elif keys[pygame.K_l]:
                    opponent_choice = "scissors"
            elif mode == "single" and player_choice:
                opponent_choice = random.choice(["rock", "paper", "scissors"])

            # Display choices
            if player_choice:
                window.blit(get_image(player_choice), (WIDTH//4 - 75, 250))
                draw_text(player_choice.upper(), font, BLACK, WIDTH//4, 420)
            else:
                draw_text("Player 1: A=Rock, S=Paper, D=Scissors", font, BLACK, WIDTH//4, 250)

            if opponent_choice:
                window.blit(get_image(opponent_choice), (WIDTH*3//4 - 75, 250))
                draw_text(opponent_choice.upper(), font, BLACK, WIDTH*3//4, 420)
            else:
                if mode == "multi":
                    draw_text("Player 2: J=Rock, K=Paper, L=Scissors", font, BLACK, WIDTH*3//4, 250)
                else:
                    draw_text("Computer is thinking...", font, BLACK, WIDTH*3//4, 250)

            pygame.display.flip()
            clock.tick(30)

            # If both players made a choice, break and decide winner
            if player_choice and opponent_choice:
                time.sleep(1)
                winner = get_winner(player_choice, opponent_choice)
                if winner == "player":
                    player_score += 1
                elif winner == "opponent":
                    opponent_score += 1
                round_num += 1
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

        else:
            # Timer expired without both choices
            round_num += 1  # skip round

    # Show result
    window.fill(WHITE)
    draw_text("Game Over!", large_font, BLACK, WIDTH//2, 100)
    draw_text(f"{player_name} Score: {player_score}", font, GREEN, WIDTH//2, 200)
    draw_text(f"{opponent_label} Score: {opponent_score}", font, RED, WIDTH//2, 260)

    if player_score > opponent_score:
        draw_text("You Win!", large_font, GREEN, WIDTH//2, 350)
        save_to_leaderboard(player_name, player_score)
    elif player_score < opponent_score:
        draw_text("You Lose!", large_font, RED, WIDTH//2, 350)
    else:
        draw_text("It's a Tie!", large_font, BLACK, WIDTH//2, 350)

    draw_text("Press any key to return to main menu", font, BLACK, WIDTH//2, 450)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

def main_menu():
    running = True
    clock = pygame.time.Clock()

    while running:
        window.fill(WHITE)
        draw_text("Rock, Paper, Scissors", large_font, BLACK, WIDTH//2, 100)
        draw_text("1. Single Player", font, BLUE, WIDTH//2, 200)
        draw_text("2. Two Player", font, BLUE, WIDTH//2, 260)
        draw_text("3. Leaderboard", font, BLUE, WIDTH//2, 320)
        draw_text("Q. Quit", font, RED, WIDTH//2, 380)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    play_game("single")
                elif event.key == pygame.K_2:
                    play_game("multi")
                elif event.key == pygame.K_3:
                    show_leaderboard()
                elif event.key == pygame.K_q:
                    running = False

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main_menu()
