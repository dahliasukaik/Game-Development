class Timer: 
  def __init__(self, image_list, start_index=0, delta=6, looponce=False): 
    self.image_list = image_list
    self.delta = delta
    self.looponce = looponce
    self.index = start_index
    self.time = 0

  def update_index(self):
    self.time += 1
    if self.time >= self.delta:
      self.index += 1
      self.time = 0
      if self.index > len(self.image_list) - 1 and not self.finished():
        self.index = 0

  def finished(self): 
    finished = self.looponce and self.index >= len(self.image_list) - 1
    return finished
  
  def current_index(self): return self.index

  def current_image(self):     # self.time = 0
    self.update_index()
    return self.image_list[self.index]
  

# TImerDual does NOT inherit from Timer -- instead, it HAS two Timer instances inside of it 
class TimerDual:
  def __init__(self, image_list0, image_list1, start_index0=0, start_index1=0, delta0=6, delta1=6, delta_timers=100, looponce0=False, looponce1=False):
    self.timer0 = Timer(self, image_list=image_list0, start_index=start_index0, delta=delta0, looponce=looponce0)
    self.timer1 = Timer(self, image_list=image_list1, start_index=start_index1, delta=delta1, looponce=looponce1)
    # TODO

  def update_index(self): pass   # TODO -- remove pass and put in your code (if needed)
  
  def finished(self): pass       # TODO -- remove pass and put in your code (if needed)
  
  def current_timer(self): pass  # TODO -- remove pass and put in your code (if needed)
  
  def current_index(self): pass  # TODO -- remove pass and put in your code (if needed)
  
  def current_image(self): pass  # TODO -- remove pass and put in your code (if needed)
  