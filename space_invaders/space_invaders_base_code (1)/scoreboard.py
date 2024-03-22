import pygame as pg
import pygame.font 
from pygame.sprite import Group
from ship import Ship


class Scoreboard:
  def __init__(self, game):
      self.game = game 
      self.screen = game.screen 
      self.screen_rect = game.screen.get_rect() 
      self.settings = game.settings 
      self.stats = game.stats

      self.text_color = (30, 30, 30)
      self.font = pg.font.SysFont(None, 48)
      self.prep()
      self.prep_high_score()

  def prep(self):
      self.prep_score()
      self.prep_level()
      self.prep_ships()

  def prep_score(self):
     rounded_score = round(self.stats.score, -1)
     s = f'Current: {rounded_score:,}'
     
     self.score_image = self.font.render(s, True, self.text_color, self.settings.bg_color)
     self.score_rect = self.score_image.get_rect()
     self.score_rect.right = self.screen_rect.right - 20
     self.score_rect.top += 20

  def prep_high_score(self):
    high_score = round(self.stats.high_score, -1)
    high_score_str = f"High: {high_score:,}"

    self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

    self.high_score_rect = self.high_score_image.get_rect()
    self.high_score_rect.centerx = self.screen_rect.centerx
    self.high_score_rect.top = self.score_rect.top

  def prep_level(self):
    level_str = f'L {self.stats.level}'


    self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

    self.level_rect = self.level_image.get_rect()
    self.level_rect.right = self.score_rect.right
    self.level_rect.top = self.score_rect.bottom + 10

  def save_high_score(self):
    with open('high_score.txt', 'w') as f:
        f.write(str(self.stats.high_score))

  def show_high_score(self):
    
    self.screen.fill(self.settings.bg_color)  # Clear screen or set a background
    high_scores = self.load_high_score()  # Load or get high scores
    title_font = pg.font.SysFont(None, 56)
    font = pg.font.SysFont(None, 36)

    # Render title
    title_surface = title_font.render("High Scores", True, self.text_color)
    title_rect = title_surface.get_rect(center=(self.screen_rect.centerx, 50))
    self.screen.blit(title_surface, title_rect)

    # Render high scores
    start_y = 100  # Starting Y position for the first high score
    if not high_scores:  # This checks for an empty list as well as None, but None should not occur
      print("No high scores to display.")
      return
    for index, score in enumerate(high_scores):
        score_surface = font.render(f"{index + 1}. {score}", True, self.text_color)
        score_rect = score_surface.get_rect(center=(self.screen_rect.centerx, start_y + index * 40))
        self.screen.blit(score_surface, score_rect)

   



  

  def load_high_score(self):
    try:
        with open('high_score.txt', 'r') as f:
            self.stats.high_score = int(f.readline())
            self.prep_high_score()
    except FileNotFoundError:
        self.stats.high_score = 0

  def prep_ships(self):
    self.ships = Group()
    for ship_number in range(self.stats.ships_left):
      ship = Ship(self.game)
      ship.rect.x = 10 + ship_number * ship.rect.width
      ship.rect.y = 10
      self.ships.add(ship)

  def check_high_score(self):
    if self.stats.score > self.stats.high_score:
        self.stats.high_score = self.stats.score
        self.prep_high_score()
        self.save_high_score()

  def update(self): 
    self.draw()

  def draw(self):
     self.screen.blit(self.score_image, self.score_rect)
     self.screen.blit(self.high_score_image, self.high_score_rect)
     self.screen.blit(self.level_image, self.level_rect)
     self.ships.draw(self.screen)
  
    