import pygame
import random
import time
import os


pygame.init()
pygame.mixer.init()


try:
    opening_sound = pygame.mixer.Sound("opening.wav")
    opening_sound.set_volume(0.6)
    opening_sound.play()
except:
    
    opening_sound = pygame.mixer.Sound(pygame.mixer.Sound(buffer=b'\x00\x00' * 44100))  
    opening_sound.set_volume(0.0)

click_sound = pygame.mixer.Sound(pygame.mixer.Sound(buffer=b'\x00\x00' * 44100))  
try:
    click_sound = pygame.mixer.Sound("click.wav")  
except:
    pass
click_sound.set_volume(0.6)


WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock, Paper, Scissors")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
BLUE = (30, 144, 255)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)


font = pygame.font.SysFont(None, 40)
large_font = pygame.font.SysFont(None, 60)


def draw_gradient_background():
    for y in range(HEIGHT):
        r = 255
        g = 255
        b = max(100, 255 - y // 3)
        pygame.draw.line(window, (r, g, b), (0, y), (WIDTH, y))

def safe_load_image(filename):
    try:
        img = pygame.image.load(filename)
        return pygame.transform.scale(img, (150, 150))
    except:
        surface = pygame.Surface((150, 150))
        surface.fill((200, 200, 200))
        pygame.draw.line(surface, (100, 0, 0), (0, 0), (150, 150), 5)
        pygame.draw.line(surface, (100, 0, 0), (0, 150), (150, 0), 5)
        return surface

rock_img = safe_load_image("rock.png")
paper_img = safe_load_image("paper.png")
scissors_img = safe_load_image("scissors.png")


def draw_text(text, font, color, x, y, shadow=False):
    img = font.render(text, True, color)
    rect = img.get_rect(center=(x, y))
    if shadow:
        shadow_img = font.render(text, True, BLACK)
        shadow_rect = shadow_img.get_rect(center=(x + 2, y + 2))
        window.blit(shadow_img, shadow_rect)
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

def fade_transition():
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill(BLACK)
    for alpha in range(0, 255, 5):
        fade_surface.set_alpha(alpha)
        window.blit(fade_surface, (0, 0))
        pygame.display.flip()
        time.sleep(0.02)
    for alpha in range(255, -1, -5):
        fade_surface.set_alpha(alpha)
        window.blit(fade_surface, (0, 0))
        pygame.display.flip()
        time.sleep(0.02)


def load_leaderboard():
    if not os.path.exists("leaderboard.txt"):
        return []
    with open("leaderboard.txt", "r") as f:
        lines = f.readlines()
    scores = []
    for line in lines:
        try:
            name, score = line.strip().split(",")
            scores.append((name, int(score)))
        except:
            pass
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
        draw_gradient_background()
        draw_text("Leaderboard - Top 5", large_font, YELLOW, WIDTH//2, 80, shadow=True)
        scores = load_leaderboard()
        y = 150
        for i, (name, score) in enumerate(scores):
            draw_text(f"{i+1}. {name} - {score}", font, BLUE, WIDTH//2, y, shadow=True)
            y += 50
        draw_text("Press any key to return", font, WHITE, WIDTH//2, y + 50, shadow=True)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                running = False


def input_name(prompt):
    name = ""
    active = True
    while active:
        draw_gradient_background()
        draw_text(prompt, font, BLACK, WIDTH//2, HEIGHT//3, shadow=True)
        draw_text(name + "|", font, BLUE, WIDTH//2, HEIGHT//2, shadow=True)
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
                        click_sound.play()
    return name


def play_game(mode):
    player_name = input_name("Enter Player 1 Name:")
    if not player_name:
        return
    opponent_label = "Computer" if mode == "single" else input_name("Enter Player 2 Name:")
    if mode == "multi" and not opponent_label:
        return

    player_score = 0
    opponent_score = 0
    round_num = 1
    clock = pygame.time.Clock()

    while round_num <= 5:
        player_choice = None
        opponent_choice = None
        round_start = time.time()
        scale_factor = 1.0
        choice_time = 0

        while time.time() - round_start < 20:
            timer = 20 - int(time.time() - round_start)
            draw_gradient_background()
            draw_text(f"{player_name} vs {opponent_label}", font, BLACK, WIDTH//2, 40, shadow=True)
            draw_text(f"Round {round_num}/5", font, BLACK, WIDTH//2, 80, shadow=True)
            draw_text(f"Score: {player_name} {player_score} - {opponent_score} {opponent_label}", font, BLACK, WIDTH//2, 120, shadow=True)
            draw_text(f"Time Left: {timer}s", font, RED if timer <= 5 else BLACK, WIDTH//2, 160, shadow=True)

            keys = pygame.key.get_pressed()

            # Player 1 controls
            if keys[pygame.K_a]:
                player_choice = "rock"
                click_sound.play()
                choice_time = time.time()
            elif keys[pygame.K_s]:
                player_choice = "paper"
                click_sound.play()
                choice_time = time.time()
            elif keys[pygame.K_d]:
                player_choice = "scissors"
                click_sound.play()
                choice_time = time.time()

            # Player 2 or computer
            if mode == "multi":
                if keys[pygame.K_j]:
                    opponent_choice = "rock"
                    click_sound.play()
                    choice_time = time.time()
                elif keys[pygame.K_k]:
                    opponent_choice = "paper"
                    click_sound.play()
                    choice_time = time.time()
                elif keys[pygame.K_l]:
                    opponent_choice = "scissors"
                    click_sound.play()
                    choice_time = time.time()
            elif mode == "single" and player_choice:
                opponent_choice = random.choice(["rock", "paper", "scissors"])
                click_sound.play()
                choice_time = time.time()

            # Animation for choices
            if player_choice:
                img = get_image(player_choice)
                if time.time() - choice_time < 0.5:
                    scale_factor = 1.0 + 0.2 * (0.5 - (time.time() - choice_time)) / 0.5
                scaled_img = pygame.transform.scale(img, (int(150 * scale_factor), int(150 * scale_factor)))
                window.blit(scaled_img, (WIDTH//4 - 75 * scale_factor, 250 - 75 * (scale_factor - 1)))
                draw_text(player_choice.upper(), font, BLACK, WIDTH//4, 420, shadow=True)
            else:
                draw_text("Player 1: A=Rock, S=Paper, D=Scissors", font, BLACK, WIDTH//4, 250, shadow=True)

            if opponent_choice:
                img = get_image(opponent_choice)
                if time.time() - choice_time < 0.5:
                    scale_factor = 1.0 + 0.2 * (0.5 - (time.time() - choice_time)) / 0.5
                scaled_img = pygame.transform.scale(img, (int(150 * scale_factor), int(150 * scale_factor)))
                window.blit(scaled_img, (WIDTH*3//4 - 75 * scale_factor, 250 - 75 * (scale_factor - 1)))
                draw_text(opponent_choice.upper(), font, BLACK, WIDTH*3//4, 420, shadow=True)
            else:
                if mode == "multi":
                    draw_text("Player 2: J=Rock, K=Paper, L=Scissors", font, BLACK, WIDTH*3//4, 250, shadow=True)
                else:
                    draw_text("Computer is thinking...", font, BLACK, WIDTH*3//4, 250, shadow=True)

            pygame.display.flip()
            clock.tick(30)

            if player_choice and opponent_choice:
                winner = get_winner(player_choice, opponent_choice)
                draw_gradient_background()
                draw_text(f"{player_name} vs {opponent_label}", font, BLACK, WIDTH//2, 40, shadow=True)
                window.blit(get_image(player_choice), (WIDTH//4 - 75, 250))
                window.blit(get_image(opponent_choice), (WIDTH*3//4 - 75, 250))
                draw_text(player_choice.upper(), font, BLACK, WIDTH//4, 420, shadow=True)
                draw_text(opponent_choice.upper(), font, BLACK, WIDTH*3//4, 420, shadow=True)
                if winner == "player":
                    draw_text(f"{player_name} Wins Round!", large_font, GREEN, WIDTH//2, HEIGHT//2, shadow=True)
                    player_score += 1
                elif winner == "opponent":
                    draw_text(f"{opponent_label} Wins Round!", large_font, RED, WIDTH//2, HEIGHT//2, shadow=True)
                    opponent_score += 1
                else:
                    draw_text("Draw!", large_font, YELLOW, WIDTH//2, HEIGHT//2, shadow=True)
                pygame.display.flip()
                click_sound.play()
                time.sleep(2)
                fade_transition()
                round_num += 1
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

        else:
            round_num += 1

    draw_gradient_background()
    draw_text("Game Over!", large_font, BLACK, WIDTH//2, 100, shadow=True)
    draw_text(f"{player_name} Score: {player_score}", font, GREEN, WIDTH//2, 200, shadow=True)
    draw_text(f"{opponent_label} Score: {opponent_score}", font, RED, WIDTH//2, 260, shadow=True)

    if player_score > opponent_score:
        draw_text("You Win!", large_font, GREEN, WIDTH//2, 350, shadow=True)
        save_to_leaderboard(player_name, player_score)
    elif player_score < opponent_score:
        draw_text("You Lose!", large_font, RED, WIDTH//2, 350, shadow=True)
    else:
        draw_text("It's a Tie!", large_font, BLACK, WIDTH//2, 350, shadow=True)

    draw_text("Press any key to return to main menu", font, WHITE, WIDTH//2, 450, shadow=True)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

# Main menu
def main_menu():
    running = True
    clock = pygame.time.Clock()
    buttons = [
        {"text": "1. Single Player", "y": 200, "mode": "single"},
        {"text": "2. Two Player", "y": 260, "mode": "multi"},
        {"text": "3. Leaderboard", "y": 320, "mode": "leaderboard"},
        {"text": "Q. Quit", "y": 380, "mode": "quit"}
    ]

    while running:
        draw_gradient_background()
        draw_text("Rock, Paper, Scissors", large_font, YELLOW, WIDTH//2, 100, shadow=True)

        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            color = GREEN if button["y"] - 20 < mouse_pos[1] < button["y"] + 20 else BLUE
            draw_text(button["text"], font, color, WIDTH//2, button["y"], shadow=True)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    click_sound.play()
                    fade_transition()
                    play_game("single")
                elif event.key == pygame.K_2:
                    click_sound.play()
                    fade_transition()
                    play_game("multi")
                elif event.key == pygame.K_3:
                    click_sound.play()
                    fade_transition()
                    show_leaderboard()
                elif event.key == pygame.K_q:
                    click_sound.play()
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button["y"] - 20 < mouse_pos[1] < button["y"] + 20:
                        click_sound.play()
                        fade_transition()
                        if button["mode"] == "single":
                            play_game("single")
                        elif button["mode"] == "multi":
                            play_game("multi")
                        elif button["mode"] == "leaderboard":
                            show_leaderboard()
                        elif button["mode"] == "quit":
                            running = False

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main_menu()