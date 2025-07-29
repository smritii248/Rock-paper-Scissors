# Rock, Paper, Scissors Game


A classic Rock, Paper, Scissors game built with Pygame, featuring single-player (vs. computer) and two-player modes, a leaderboard, and enhanced visuals like gradient backgrounds, animated choices, and fade transitions. Players can compete in 5-round matches, with scores saved to a leaderboard for winners.
Features

# Game Modes:
Single-Player: Play against a computer that randomly selects rock, paper, or scissors.
Two-Player: Compete against another player on the same keyboard.


# Leaderboard: Saves the top 5 scores to leaderboard.txt for single-player wins.
Visual Enhancements:
Gradient background (white to light blue).
Animated choice selection (images scale up briefly when chosen).
Smooth fade transitions between rounds and menus.
Menu options highlight in green when hovered over with the mouse.


# Sound Effects:
Opening sound on startup (opening.wav).
Click sound for selections (click.wav).
Fallback silent sounds if audio files are missing.


# Input Options:
Keyboard controls: A/S/D for Player 1, J/K/L for Player 2.
Mouse support for menu navigation.


# Error Handling:
Fallback images (red "X") if rock.png, paper.png, or scissors.png are missing.
Robust leaderboard parsing to skip invalid entries.



# Requirements

Python 3.6+
Pygame: Install via pip install pygame
Optional Files (place in the same directory as game.py):
rock.png, paper.png, scissors.png (150x150 images for game choices)
opening.wav (startup sound)
click.wav (selection sound)



If image or sound files are missing, the game uses fallback surfaces (gray with red "X") and silent sounds.
Installation

#Clone the Repository:
git clone https://github.com/smritii248/Rock-paper-Scissors.git
cd rock-paper-scissors


# Install Pygame:
pip install pygame


# Add Optional Files (if available):

Place rock.png, paper.png, scissors.png, opening.wav, and click.wav in the project directory.



# How to Run

Ensure Python and Pygame are installed.
Navigate to the project directory:cd path/to/rock-paper-scissors


Run the game:python game.py



# Gameplay Instructions

Main Menu:

Use keys 1, 2, 3, or Q, or click options with the mouse:
1: Start single-player mode.
2: Start two-player mode.
3: View the leaderboard.
Q: Quit the game.




Name Input:

Enter a name (up to 10 characters) for Player 1.
For two-player mode, enter a name for Player 2 (computer is automatic in single-player mode).


# Gameplay:

Play 5 rounds, each with a 20-second timer.
Player 1 Controls:
A: Rock
S: Paper
D: Scissors


Player 2 Controls (two-player mode):
J: Rock
K: Paper
L: Scissors


In single-player mode, the computer chooses randomly after Player 1 selects.
Choices are displayed with a scaling animation, and the winner is shown for 2 seconds.


# Game End:

After 5 rounds, the final scores and outcome (win, lose, or tie) are displayed.
Winning scores in single-player mode are saved to leaderboard.txt.


# Leaderboard:

View the top 5 scores with names.
Press any key to return to the main menu.


Exit:

Press Q in the main menu or close the window to quit.



# File Structure

game.py: Main game script.
leaderboard.txt: Stores top 5 scores (created automatically).
rock.png, paper.png, scissors.png: Optional image files for choices.
opening.wav, click.wav: Optional sound files for audio effects.





