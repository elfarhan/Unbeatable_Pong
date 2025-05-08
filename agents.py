from assets import *
import pygame


# setup game agents

def perform_action(player, action):
    if action == -1: # left
        player.move_left()
    elif action == 1: # right
        player.move_right()
    elif action == 0: # stay
        pass  
    
def human_agent(keys, player):
    human_action = 0
    if keys[pygame.K_LEFT]:
        human_action = -1
    elif keys[pygame.K_RIGHT]:
        human_action = 1
    perform_action(player, human_action)
    

def move_towards_the_ball(game_state, player):
    """moves the centre of the paddle to the predicted 
       intersection point of ball and side of the screen
       args: state = [
                game.ball.x, game.ball.y,
                game.ball.vx, game.ball.vy,
                game.rectangle_up.rectangle.x,
                game.rectangle_down.rectangle.x
                game.screen_height
                ]"""
    width = player.width #rectangle_width
    # x = x0 + vx *(screen_height -y0) / vy
    x_intersect_down = game_state[0] + game_state[2]/game_state[3] * (game_state[-1]-game_state[1])
    x_intersect_up = game_state[0] + game_state[2]/game_state[3] * (0-game_state[1])
    
    if x_intersect_up < game_state[4] - width/2:
        action = -1
        
    elif x_intersect_up > game_state[4] + width/2:
        action = 1
        
    else:
        action = -1
        
    perform_action(player, action)
    
    