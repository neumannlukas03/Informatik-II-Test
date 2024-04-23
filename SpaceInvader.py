import pygame
import random
import add_ons_PyGame
import time

# Initialisierung von Pygame
pygame.init()

# Bildschirmabmessungen
WIDTH, HEIGHT = 600, 400

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
will_to_play = "y"
# Spieler Eigenschaften
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 20
PLAYER_SPEED = 5
score = 0
highscorelist = [0,0,0,0,0]

# Bild laden und Größe anpassen Spieler 
spielerbild = pygame.image.load('rocket.png')
spielerbild = pygame.transform.scale(spielerbild, (PLAYER_WIDTH, PLAYER_HEIGHT))

# Hintergrundbild laden
background = pygame.image.load('weltall.jpg')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Gegner Eigenschaften
ENEMY_WIDTH, ENEMY_HEIGHT = 30, 30
ENEMY_SPEED = 3
ENEMY_INTERVAL = 60  # Intervall, in dem ein neuer Gegner erscheint

# Initialisierung des Bildschirms
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Weiche den Feinden aus")
clock = pygame.time.Clock()

# Funktion zum Erzeugen eines neuen Gegners
def create_enemy():
    x = random.randint(0, WIDTH - ENEMY_WIDTH)
    y = 0 - ENEMY_HEIGHT
    return pygame.Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)

# Funktion zum Bewegen der Gegner
def move_enemies(enemies):
    for enemy in enemies:
        enemy.y += ENEMY_SPEED

# Funktion zum Zeichnen des Spielers
def draw_player(player):
    screen.blit(spielerbild, (player.x, player.y))

# Funktion zum Zeichnen der Gegner
def draw_enemies(enemies):
    add_ons_PyGame.draw_enemies(enemies, screen)  # Hier die Funktion aus der separaten Datei aufrufen

# Funktion zum Zeichnen der Schüsse
def draw_bullets(bullets):
    for bullet in bullets:
        pygame.draw.rect(screen, RED, pygame.Rect(bullet[0], bullet[1], 5, 10))  # Schuss als einfaches Rechteck zeichnen

# Hauptspiel
def main(score):
    player = pygame.Rect(WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT - 50, PLAYER_WIDTH, PLAYER_HEIGHT)
    enemies = []
    bullets = []
    
    running = True
    while running:
        
        screen.fill(WHITE)
        score = add_ons_PyGame.scorecounting(score,ENEMY_SPEED)
        add_ons_PyGame.drawscore(score,BLACK,screen)
      
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        #Mausposition abrufen 
        mouse_x, mouse_y = pygame.mouse.get_pos() 

        #Spielerpostion basierend auf Mauspostion 
        player.x = max(0, min(mouse_x - PLAYER_WIDTH // 2, WIDTH - PLAYER_WIDTH))
        player.y = max(200, min(mouse_y - PLAYER_HEIGHT // 2, HEIGHT - PLAYER_HEIGHT))

        # Bewege die Schüsse             
        for bullet in bullets:
            bullet[1] -= 10
            if bullet[1] < 0:
                bullets.remove(bullet)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            bullets.append([player.x + PLAYER_WIDTH // 2, player.y])
    
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_LEFT]:
        #     player.x -= PLAYER_SPEED
        # if keys[pygame.K_RIGHT]:
        #     player.x += PLAYER_SPEED

        # Begrenze den Spieler auf den Bildschirm
        player.x = max(0, min(player.x, WIDTH - PLAYER_WIDTH))

        # Bewege die Gegner und füge neue hinzu
        move_enemies(enemies)
        if random.randint(0, ENEMY_INTERVAL) == 0:
            enemies.append(create_enemy())

        # Kollisionserkennung
        for enemy in enemies:
            if player.colliderect(enemy):
                running = False

        # Zeichne Spieler und Gegner
        screen.blit(background, (0,0))
        draw_player(player)
        draw_enemies(enemies)
        draw_bullets(bullets)

        pygame.display.flip()
        clock.tick(60)      
    add_ons_PyGame.gameover(screen,RED)
    add_ons_PyGame.save_highscore(score)
    final_score = add_ons_PyGame.load_highscore
    print(f"your score {final_score}")
    add_ons_PyGame.gameloop
    
    

if __name__ == "__main__":
    
    while will_to_play == "y":
        will_to_play=input("Wanna Play(y/n)")
        if will_to_play == ("y"):
            main(score)
        elif will_to_play == "n":
            pass
        else:
            will_to_play = "y"