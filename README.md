ENHANCED PONG GAME
==========================================

A modern implementation of the classic Pong game with AI opponent and visual enhancements.

------------------------------------------
DESCRIPTION
------------------------------------------
This project is an enhanced version of the classic Pong arcade game. Play against an 
intelligent AI opponent with adjustable difficulty. The game features smooth animations, 
particle effects, and a polished visual style.

------------------------------------------
FEATURES
------------------------------------------
- Intelligent AI opponent with predictive movement
- Adjustable AI difficulty levels (1-9 keys)
- Realistic physics with angle-based ball bounces
- Particle effects for collisions
- Visual enhancements including paddle gradients and ball glow
- Score tracking with win condition
- Countdown timer between points
- Game over screen with restart option

------------------------------------------
CONTROLS
------------------------------------------
- UP/DOWN ARROW KEYS: Move your paddle
- 1-9 KEYS: Adjust AI difficulty (1=easiest, 9=hardest)
- 0 KEY: Set AI to maximum difficulty
- SPACE: Restart game after someone wins

------------------------------------------
REQUIREMENTS
------------------------------------------
- Python 3.6+
- Pygame 2.0+

------------------------------------------
INSTALLATION
------------------------------------------
1. Clone the repository:
   git clone https://github.com/yourusername/enhanced-pong.git
   cd enhanced-pong

2. Install the required dependencies:
   pip install pygame

3. Run the game:
   python pong.py

------------------------------------------
GAME MECHANICS
------------------------------------------
- First player to reach 5 points wins
- Ball speed increases slightly with each paddle hit
- Ball bounce angle depends on where it hits the paddle
- AI predicts ball trajectory with accuracy based on difficulty

------------------------------------------
CUSTOMIZATION
------------------------------------------
You can modify the following constants at the top of the file:

- WIDTH, HEIGHT: Change the window size
- BALL_RADIUS: Adjust the ball size
- PADDLE_WIDTH, PADDLE_HEIGHT: Change paddle dimensions
- score_limit: Change how many points needed to win

------------------------------------------
SOUND EFFECTS
------------------------------------------
The game will look for sound files in a 'sounds' directory:
- sounds/paddle_hit.wav
- sounds/wall_hit.wav
- sounds/score.wav

If these files are not found, the game will run without sound.

------------------------------------------
LICENSE
------------------------------------------
This project is licensed under the MIT License - see the LICENSE file for details.

------------------------------------------
ACKNOWLEDGMENTS
------------------------------------------
- Original Pong game created by Atari in 1972
- Pygame community for their excellent documentation and examples

------------------------------------------
This project was created for educational purposes.
