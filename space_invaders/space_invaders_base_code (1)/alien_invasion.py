import sys, time
import pygame as pg
from settings import Settings 
from ship import Ship
from aliens import Aliens, Alien
from vector import Vector
from game_stats import GameStats
from button import Button
from barrier import Barrier, Barriers
from scoreboard import Scoreboard
from sound import Sound



class Game:
  key_velocity = {pg.K_RIGHT: Vector(1, 0), pg.K_LEFT: Vector(-1,  0),
                  pg.K_UP: Vector(0, -1), pg.K_DOWN: Vector(0, 1)}

  def __init__(self):
    pg.init()
    self.settings = Settings()
    self.screen = pg.display.set_mode(
      (self.settings.screen_width, self.settings.screen_height))
    pg.display.set_caption("Alien Invasion")


    self.aliens = None
    self.stats = GameStats(game=self)
    self.sound = Sound()
    self.sb = Scoreboard(game=self)
    self.sb.load_high_score()
    

  
    
    self.ship = Ship(game=self)
    self.aliens = Aliens(game=self)  



    self.ship.set_aliens(self.aliens)
    self.ship.set_sb(self.sb)

    self.barrier = Barriers(game=self)
    self.ufo = Aliens(game=self)
    
    self.game_active = False              # MUST be before Button is created
    self.first = True
    self.play_button = Button(game=self, text='Play Game', position=(30, 300))
    self.Scores_button = Button(game=self, text='High Scores', position=(30, 200))

   
   
  

  def check_events(self):
    for event in pg.event.get():
      type = event.type
      if type == pg.KEYUP: 
        key = event.key 
        if key == pg.K_SPACE: self.ship.cease_fire()
        elif key in Game.key_velocity: self.ship.all_stop()
      elif type == pg.QUIT: 
        pg.quit()
        sys.exit()
      elif type == pg.KEYDOWN:
        key = event.key
        if key == pg.K_SPACE: 
          self.ship.fire_everything()
        elif key == pg.K_p: 
          self.play_button.select(True)
          self.play_button.press()
        elif key in Game.key_velocity: 
          self.ship.add_speed(Game.key_velocity[key])
      elif type == pg.MOUSEBUTTONDOWN:
        b = self.play_button
        x, y = pg.mouse.get_pos()
        if b.rect.collidepoint(x, y):
          b.press()
      elif type == pg.MOUSEMOTION:
        b = self.play_button
        x, y = pg.mouse.get_pos()
        
        b.select(b.rect.collidepoint(x, y))
    
  def restart(self):
    self.screen.fill(self.settings.bg_color)
    self.ship.reset()
    self.aliens.reset()
    self.barrier.reset()
    self.settings.initialize_dynamic_settings()

  def game_over(self):
    print('Game Over !')
    pg.mouse.set_visible(True)
    self.play_button.change_text('Play again?')
    self.play_button.show()
    self.launch_screen()
    self.first = True
    self.game_active = False
    self.sound.play_game_over()
    self.stats.reset()
    self.restart()

  def activate(self): 
    self.game_active = True
    self.first = False
    self.sound.play_music("sounds/i_just_need.wav")

  def launch_screen(self):
    self.screen.fill((0, 0, 0))

    launch_image = pg.image.load('images/launch.png')
    launch_image_scaled = pg.transform.scale(launch_image, (self.settings.screen_width, self.settings.screen_height))
    launch_image_rect = launch_image_scaled.get_rect()
    launch_image_rect.center = self.screen.get_rect().center
    self.screen.blit(launch_image_scaled, launch_image_rect)
  

    self.Scores_button.draw()
    self.play_button.draw()
 
  
    pg.display.flip()

    input_waiting = True
    
    while input_waiting and not self.game_active:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos_x, mouse_pos_y = pg.mouse.get_pos()
                if self.play_button.rect.collidepoint(mouse_pos_x, mouse_pos_y):
                    self.activate()
                    input_waiting = False
                elif self.Scores_button.rect.collidepoint(mouse_pos_x, mouse_pos_y):
                    self.sb.show_high_score()
                    pg.display.flip()
                    waiting_for_high_scores_return = True
                    while waiting_for_high_scores_return:
                        for return_event in pg.event.get():
                            if return_event.type == pg.KEYDOWN or return_event.type == pg.MOUSEBUTTONDOWN:
                                waiting_for_high_scores_return = False

    

  def play(self):
    finished = False
    self.launch_screen()
    self.screen.fill(self.settings.bg_color)

    while not finished:
      self.check_events()    # exits if Cmd-Q on macOS or Ctrl-Q on other OS

      if self.game_active or self.first:
        self.first = False
        self.screen.fill(self.settings.bg_color)
        self.ship.update()
        self.ufo.update_ufo()
        
        self.aliens.update()   # when we have aliens

        self.sb.update()
        self.barrier.update()
        
      else:
        self.play_button.update() 
        self.Scores_button.update() 
      
      pg.display.flip()
      time.sleep(0.02)


if __name__ == '__main__':
  g = Game()
  g.play()

