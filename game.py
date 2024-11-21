import pygame
from player import Player
from field import Field

pygame.init()

# Game consts
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

DOWN = 0
UP = 1
LEFT = 2
RIGHT = 3

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
player = Player()
field = Field()

run = True
while run:
  # Run game at 60 FPS
  clock.tick(60)
  
  screen.fill((255,255,255))


# Input Code

  key = pygame.key.get_pressed()
  if key[pygame.K_DOWN] == True:
    player.move(DOWN)
  if key[pygame.K_UP] == True:
    player.move(UP)
  if key[pygame.K_LEFT] == True:
    player.move(LEFT)
  if key[pygame.K_RIGHT] == True:
    player.move(RIGHT)

  if (key[pygame.K_DOWN] == False and key[pygame.K_UP] == False and
  key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False) : 
    player.stop_move()
  

  # Quit Game

  for event in pygame.event.get():

    #Running Mechanic
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LSHIFT:
        player.start_running()
      if event.key == pygame.K_z:
        player.use_tool()
    if event.type == pygame. KEYUP:
      if event.key == pygame.K_LSHIFT:
        player.stop_running()

    if event.type == pygame.QUIT:
      run = False


  # Update Code
  player.update()


  # Drawing Code

  field.draw(screen)
  player.draw(screen)

  pygame.display.flip()
    

pygame.quit()