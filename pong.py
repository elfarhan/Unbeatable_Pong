import pygame
import numpy as np
from assets import *
from agents import *

def main():
    pygame.init()
    game = Pong(SCREEN_HEIGHT=899,difficulty=8)
    
    # setup game window
    
    screen = game.screen
    pygame.display.set_caption("PONG")
    clock = pygame.time.Clock()
    close_window = False #close window event

    # draw the game window   
    
    while not close_window:
        
        # set framerate and background
        
        clock.tick(60)
        
        # draw objects
        
        game.draw_game()
        
        # update game state
        
        game.ball.move()
        game.handle_collisions()
        
        
        # get input
        state = game.get_game_state()
        events = pygame.event.get()
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.QUIT:
                close_window = True
        
        # human player
        human_agent(keys, game.rectangle_down)
        ai_action = move_towards_the_ball(state, game.rectangle_up)
        #perform_action(game.rectangle_up, ai_action)
        
        
        if keys[pygame.K_ESCAPE]:
            close_window = True
            pygame.quit()
    return 

#main()
    