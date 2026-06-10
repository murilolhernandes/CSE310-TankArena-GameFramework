# Overview

## Description:
As a software developer building my skills in backend architecture and logic systems, I wrote this software to challenge my understanding of Object-Oriented Programming (OOP), state machines, and game loop architecture. Managing continuous state updates, vector-based AI steering, and strict separation of concerns (keeping physics logic separate from rendering logic) provided an excellent environment to practice writing clean, maintainable, and highly coupled code.

**Tank Arena** is a 2D top-down arcade survival shooter. The objective is to survive endless waves of enemy tanks for as long as possible. As your score increases, the game automatically scales in difficulty by increasing the number of enemies and their firing speeds.

## **How to Play:**
* Use the **W, A, S, D** or **Arrow Keys** to drive your tank.
* Use the **Mouse** to aim your turret and **Left-Click** to fire.
* Use the environment (rusted cars) for cover.
* Press **Spacebar** to restart after a Game Over.
* Press **ESC** to close the game.

[Software Demo Video - Project Walkthrough](https://www.youtube.com/watch?v=7_AnW7nN8qE)

# Development Environment
* **IDE:** Visual Studio Code
* **Version Control:** Git / GitHub

* **Programming Language:** Python 3
* **Primary Library:** Arcade (Used for window management, 2D rendering, collision detection via `PhysicsEngineSimple`, and audio playback).
* **Standard Libraries:** `math` (used for vector calculations and AI steering behavior) and `random` (used for procedural safe-spawning).

# Useful Websites

* [Python Arcade Library Official Documentation](https://api.arcade.academy/en/latest/)
* [Python `math` Module Documentation](https://docs.python.org/3/library/math.html)
* [Understanding Steering Behaviors for AI](https://natureofcode.com/autonomous-agents/)

# Future Work

* Implement a more robust A* (A-Star) pathfinding algorithm or Navigation Mesh to allow enemy AI to navigate highly complex, closed-in mazes without relying solely on repulsion vectors.
* Integrate a local database (such as SQLite) or file saving system to permanently persist the player's High Score across different application sessions.
* Introduce a power-up system (e.g., wrench icons to restore health, or stars for temporary rapid-fire) that utilizes timed lifespan variables similar to the explosion animations.