import pygame
import numpy as np

# define game constants

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (204, 204, 204)



# define game display class

class Pong:
    
    def __init__(self, SCREEN_HEIGHT = 640, difficulty = 1):
        
        self.SCREEN_HEIGHT = SCREEN_HEIGHT 
        self.SCREEN_WIDTH = int(self.SCREEN_HEIGHT//19.5*9) # iphone aspect ratio
        self.GRID_SIZE = 40
        self.GRID_COLOR = (50, 50, 50)
        self.LINE_COLOR = (255, 255, 255)
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.SCORE_UP = 0
        self.SCORE_DOWN = 0
        self.difficulty = difficulty
        
        # setup game objects

        self.ball = Ball((self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2), difficulty)
        self.rectangle_up = Rectangle(self.SCREEN_WIDTH, difficulty)
        self.rectangle_down = Rectangle(self.SCREEN_WIDTH, difficulty)
        self.rectangle_down.rectangle.y += self.SCREEN_HEIGHT - self.rectangle_up.rectangle.height*3

        return
    
    # Display elements
    
    def draw_grid(self):
        for x in range(0, self.SCREEN_WIDTH, self.GRID_SIZE):
            pygame.draw.line(self.screen, self.GRID_COLOR, (x+4, 0), (x+4, self.SCREEN_HEIGHT))
        for y in range(0, self.SCREEN_HEIGHT, self.GRID_SIZE):
            pygame.draw.line(self.screen, self.GRID_COLOR, (0, y), (self.SCREEN_WIDTH, y))
       
    
    def draw_center_line(self):
        segment_length = 20
        gap = 20
        x = 0
        while x < self.SCREEN_WIDTH:
            pygame.draw.line(self.screen, self.LINE_COLOR, (x, self.SCREEN_HEIGHT // 2), (x +                                        segment_length,  self.SCREEN_HEIGHT // 2), 4)
            x += segment_length + gap
           
        
    # score function

    def update_score(self, y):
        
        #global ball, SCORE_UP, SCORE_DOWN
        if y < self.ball.radius // 2:
            self.SCORE_DOWN += 1
            
        elif y > self.SCREEN_HEIGHT - self.ball.radius // 2:
            self.SCORE_UP += 1
        
        # start a new round
        self.ball = Ball((self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2), self.difficulty)
        
    def handle_collisions(self):
        # bounce on screen edges
        if self.ball.x > self.SCREEN_WIDTH - self.ball.radius // 2 or self.ball.x < self.ball.radius // 2:
            self.ball.vx *= -1
        # handle score
        
        if self.ball.y > self.SCREEN_HEIGHT - self.ball.radius // 2 or self.ball.y < self.ball.radius // 2:
            self.update_score(self.ball.y)
            #self.vy *= -1
            
        # handle collisions
        collision_rectangle = pygame.Rect(
            self.ball.x - self.ball.radius, self.ball.y - self.ball.radius, self.ball.radius * 2, self.ball.radius * 2)
        
        if pygame.Rect.colliderect(collision_rectangle, self.rectangle_down.rectangle):
            self.ball.vy *= -1
            
        if pygame.Rect.colliderect(collision_rectangle,self.rectangle_up.rectangle):
            self.ball.vy *= -1
        

    # draw score
    
    def draw_score(self):
        # Font setup
        pygame.font.init()
        font = pygame.font.SysFont("Arial", 36)  # Choose any font and size
        SCORE_COLOR = (75, 75, 75) 
        # score elements
        score_text = f"{self.SCORE_UP}:{self.SCORE_DOWN}"
        text_surface = font.render(score_text, True, SCORE_COLOR)
        text_surface = pygame.transform.rotate(text_surface, -90)
        text_rect = text_surface.get_rect(center=(40, self.SCREEN_HEIGHT // 2)) 
        pygame.transform.rotate(text_surface, -90)
        self.screen.blit(text_surface, text_rect)
        
    def get_game_state(self):
        state = [
                self.ball.x, self.ball.y,
                self.ball.vx, self.ball.vy,
                self.rectangle_up.rectangle.x,
                self.rectangle_down.rectangle.x
                ]
        return state
    
    def draw_game(self):
        self.screen.fill(BLACK)
        self.draw_grid()
        self.draw_center_line()
        self.ball.draw(self.screen)
        self.rectangle_down.draw(self.screen)
        self.rectangle_up.draw(self.screen)
        self.draw_score()
        pygame.display.flip()
    
     
    
        

# define Ball class

class Ball:
    def __init__(self, position, difficulty):
        # note position has half the screen dimensions
        self.x = position[0]
        self.y = position[1]
        phi = np.random.uniform(np.pi/4,np.pi/2)
        sign = np.random.choice([-1, 1])
        speed = position[1]/64*(1+difficulty/10)
        self.vx = speed*np.cos(sign*phi)
        self.vy = speed*np.sin(sign*phi)
        self.radius = position[1]//32
        self.SCREEN_WIDTH = 2*position[0]
        self.SCREEN_HEIGHT = 2*position[1]
        
    def move(self):
        self.x += self.vx
        self.y += self.vy
        
    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)
        
    def update(self):
        self.move()
        self.handle_collisions()
            
    #ball movement
    def move_up(self):
        self.rect.y -= self.MOVE_SPEED
        self._keep_in_bounds()

    def move_down(self):
        self.rect.y += self.MOVE_SPEED
        self._keep_in_bounds()

            
       
# define rectangle class

class Rectangle:

    def __init__(self, SCREEN_WIDTH, difficulty):
        self.width = SCREEN_WIDTH//2.6/(1+4/10)
        self.height = SCREEN_WIDTH//20 /(1+4/10)
        self.rectangle = pygame.Rect((SCREEN_WIDTH-self.width)//2, self.height, self.width, self.height)
        self.MOVE_SPEED = SCREEN_WIDTH//60*(1+difficulty/15)#5
        self.SCREEN_WIDTH = SCREEN_WIDTH

    def move_left(self):
        self.rectangle.x -= self.MOVE_SPEED
        self.keep_in_bounds()

    def move_right(self):
        self.rectangle.x += self.MOVE_SPEED
        self.keep_in_bounds()

    def keep_in_bounds(self):
        self.rectangle.x = max(self.rectangle.x, 0)
        self.rectangle.x = min(self.rectangle.x, self.SCREEN_WIDTH - self.rectangle.width)

    def draw(self, screen):
        pygame.draw.rect(
            screen, GRAY, self.rectangle,
        )

        
        