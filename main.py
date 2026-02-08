# -*- coding: utf-8 -*-
import os
import sys
from pygame import Rect
from pgzero.actor import Actor


try:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

except:
    pass

WIDTH = 800
HEIGHT = 600
TITLE = "Top-Down Roguelike - PgZero Test"

game_state = "menu"
sound_enabled = True

start_button = Rect(
    (WIDTH // 2 - 150, 230),
    (300, 60)
)

sound_button = Rect(
    (WIDTH // 2 - 150, 310),
    (300, 60)
)

exit_button = Rect(
    (WIDTH // 2 - 150, 390),
    (300, 60)
)

restart_button = Rect(
    (WIDTH // 2 - 150, 300),
    (300, 60)
)

game_over_exit_button = Rect(
    (WIDTH // 2 - 150, 380),
    (300, 60)
)

class Hero:
    def __init__(self, pos):
        self.idle_images = ["hero_idle_0", "hero_idle_1"]
        self.walk_images = ["hero_walk_0", "hero_walk_1"]
        self.walk_back_images = ["hero_walk_2"]
        
        self.idle_frame = 0
        self.walk_frame = 0
        self.walk_back_frame = 0
        
        self.timer = 0
        self.speed = 4
        
        self.actor = Actor(self.idle_images[0], pos)
        self.moving = False
        self.walking_back = False

    def update(self):
        dx = dy = 0
        self.moving = False
        self.walking_back = False

        if keyboard.a or keyboard.left:
            dx -= self.speed
            self.moving = True
            self.actor.flip_x = True
            
        if keyboard.d or keyboard.right:
            dx += self.speed
            self.moving = True
            self.actor.flip_x = False
            
        if keyboard.w or keyboard.up:
            dy -= self.speed
            self.moving = True
             
        if keyboard.s or keyboard.down:
            dy += self.speed
            self.moving = True
            self.walking_back = True
            
        self.actor.x += dx
        self.actor.y += dy

        # Limites da tela
        self.actor.left = max(self.actor.left, 0)
        self.actor.right = min(self.actor.right, WIDTH)
        self.actor.top = max(self.actor.top, 0)
        self.actor.bottom = min(self.actor.bottom, HEIGHT)

        
        self.timer += 1

        if self.walking_back:
            if self.timer >= 10:
                self.timer = 0
                self.walk_back_frame = (self.walk_back_frame + 1) % len(self.walk_back_images)
            self.actor.image = self.walk_back_images[self.walk_back_frame]

        elif self.moving:
            if self.timer >= 10:
                self.timer = 0
                self.walk_frame = (self.walk_frame + 1) % len(self.walk_images)
            self.actor.image = self.walk_images[self.walk_frame]

        else:
            if self.timer >= 20:
                self.timer = 0
                self.idle_frame = (self.idle_frame + 1) % len(self.idle_images)
            self.actor.image = self.idle_images[self.idle_frame]


class Enemy:
    def __init__(self, pos, min_x, max_x):
        self.images = ["enemy_0", "enemy_1"]
        self.frame = 0
        self.timer = 0
        self.actor = Actor(self.images[0], pos)
        self.speed = 2
        self.direction = 1
        self.min_x = min_x
        self.max_x = max_x

    def update(self):
        self.actor.x += self.speed * self.direction

        if self.actor.x <= self.min_x or self.actor.x >= self.max_x:
            self.direction *= -1

        self.timer += 1
        if self.timer >= 25:
            self.timer = 0
            self.frame = (self.frame + 1) % len(self.images)
            self.actor.image = self.images[self.frame]


hero = Hero((WIDTH // 2, HEIGHT // 2))

enemies = [
    Enemy((150, 200), 100, 300),
    Enemy((650, 150), 600, 780),
    Enemy((300, 450), 250, 450),
    Enemy((500, 350), 450, 650)
]


def draw():
    screen.clear()
    screen.fill((30, 50, 30))

    if game_state == "menu":
        draw_menu()

    elif game_state == "playing":
        hero.actor.draw()
        for enemy in enemies:
            enemy.actor.draw()
    elif game_state == "game_over":
        draw_game_over()


def draw_menu():
    screen.draw.text(
        "ROGUELIKE GAME",
        center=(WIDTH // 2, 120),
        fontsize=60,
        color="white",
        shadow=(2, 2)
    )

    screen.draw.filled_rect(start_button, (50, 80, 50))
    screen.draw.text("Start Game", center=start_button.center, fontsize=40)
    
    screen.draw.filled_rect(sound_button, (80, 50, 50))
    sound_text = "Sound: ON" if sound_enabled else "Sound: OFF"
    screen.draw.text(sound_text, center=sound_button.center, fontsize=40)
    
    screen.draw.filled_rect(exit_button, (120, 30, 30))
    screen.draw.text("Exit", center=exit_button.center, fontsize=40, color="white")

def draw_game_over():
    screen.draw.text(
        "GAME OVER",
        center=(WIDTH // 2, 180),
        fontsize=70,
        color="red"
    )

    screen.draw.filled_rect(restart_button, (50, 50, 50))
    screen.draw.text(
        "Restart",
        center=restart_button.center,
        fontsize=40,
        color="white"
    )

    screen.draw.filled_rect(game_over_exit_button, (120, 30, 30))
    screen.draw.text(
        "Exit",
        center=game_over_exit_button.center,
        fontsize=40,
        color="white"
    )


def on_mouse_down(pos):
    global game_state, hero, enemies, sound_enabled

    if game_state == "menu":
        if start_button.collidepoint(pos):
            hero = Hero((WIDTH // 2, HEIGHT // 2 + 100))
            enemies = [
                Enemy((150, 200), 100, 300),
                Enemy((650, 150), 600, 780),
                Enemy((300, 450), 250, 450),
                Enemy((500, 350), 450, 650)
            ]
            
            game_state = "playing"

            # Toca música se habilitada
            if sound_enabled:
                try:
                    music.play("background")
                    music.set_volume(0.4)
                except Exception as e:
                    print(f"Aviso: Música 'background' não encontrada na pasta 'music/'.")
        elif sound_button.collidepoint(pos):
            sound_enabled = not sound_enabled
            if sound_enabled:
                try:
                    music.play("background")
                except Exception as e:
                    print(f"Aviso: Música 'background' não encontrada na pasta 'music/'.")
            elif not sound_enabled:
                try:
                    music.stop()
                except:
                    pass
                
        elif exit_button.collidepoint(pos):
            music.stop()
            sys.exit()
            
    elif game_state == "game_over":
            
        if restart_button.collidepoint(pos):
            hero = Hero((WIDTH // 2, HEIGHT // 2 + 100))
            enemies = [
                Enemy((150, 200), 100, 300),
                Enemy((650, 150), 600, 780),
                Enemy((300, 450), 250, 450),
                Enemy((500, 350), 450, 650)
            ]

            if sound_enabled:
                music.play("background")

            game_state = "playing"

        elif game_over_exit_button.collidepoint(pos):
            music.stop()
            sys.exit()


def update():
    global game_state

    if game_state != "playing":
        return

    hero.update()
    
    if hero.actor.top <= 0:
        if sound_enabled:
            try:
                sounds.victory.play()
            except Exception as e:
                print(f"Erro ao tocar som de vitória: {e}")
        try:
            music.stop()
        except:
            pass        
        game_state = "menu"
        return

    for enemy in enemies:
        enemy.update()

        if hero.actor.colliderect(enemy.actor):
            if sound_enabled:
                try:
                    sounds.game_over.play()
                except:
                    print("Aviso: Som 'game_over' não encontrado na pasta 'sounds/'.")
            try:
                music.stop()
            except:
                pass
            game_state = "game_over"
            return