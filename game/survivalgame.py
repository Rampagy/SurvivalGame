import random
import copy
from datetime import datetime

from MyBot import MyBot

TURNS = 1200
HEIGHT = 40
WIDTH = 40
MAX_HEALTH = 2
NEW_APPLE_TURNS = 8
APPLE_POINTS = 20
STATIONARY_POINTS = 1


class Env():
    def __init__(self):
        self.action_space = ['u', 'd', 'l', 'r', 's'] # up down left right stationary
        self.turn = 0
        self.player_pos = (HEIGHT >> 1, WIDTH >> 1)
        self.player_health = MAX_HEALTH
        self.bot1_pos = (0, 0)
        self.bot2_pos = (HEIGHT-1, WIDTH-1)
        self.score = 0
        self.apple_locations = []
        self.game_over = False
        self.map_size = (HEIGHT, WIDTH)

    def reset(self):
        self.turn = 0
        self.player_pos = (HEIGHT >> 1, WIDTH >> 1)
        self.player_health = MAX_HEALTH
        self.bot1_pos = (0, 0)
        self.bot2_pos = (HEIGHT-1, WIDTH-1)
        self.score = 0
        self.apple_locations = []
        self.game_over = False
        self.map_size = (HEIGHT, WIDTH)
        return self.game_state()


    def step(self, action):
        self.game_over = False

        # check if the game is done
        if self.turn >= TURNS:
            # game over
            self.game_over = True
        else:
            self.turn += 1
            # move the bots to their new positions
            self.update_bot_positions()

            # now move the player to their position
            new_player_height = self.player_pos[0]
            new_player_width = self.player_pos[1]
            if action == 'u':
                new_player_height = (new_player_height - 1 + HEIGHT) % HEIGHT
            elif action == 'd':
                new_player_height = (new_player_height + 1 + HEIGHT) % HEIGHT
            elif action == 'l':
                new_player_width = (new_player_width - 1 + WIDTH) % WIDTH
            elif action == 'r':
                new_player_width = (new_player_width + 1 + WIDTH) % WIDTH
            else: # unrecognized or stationary move
                self.score += STATIONARY_POINTS

            # set the new player position
            self.player_pos = (new_player_height, new_player_width)

            # check for collisions with bots
            if self.player_pos in [self.bot1_pos, self.bot2_pos]:
                # reduce player health by 1
                self.player_health -= 1
                if self.player_health <= 0:
                    # game over
                    self.game_over = True

            if self.turn % NEW_APPLE_TURNS == 0  and not self.game_over:
                # spawn a new apple
                self.apple_locations += [(random.randint(0, HEIGHT-1), random.randint(0, WIDTH-1))]

            if not self.game_over:
                # check to see if any apples were collected
                new_apple_list = []
                for apple_location in self.apple_locations:
                    if apple_location == self.player_pos:
                        # add the appropriate points for collecting an apple
                        self.score += APPLE_POINTS
                    else:
                        # add this to the still valid apples
                        new_apple_list += [apple_location]

                # replace the apple list with the now remaining apples
                self.apple_locations = new_apple_list

        return self.game_state()

    def game_state(self):
        return (self.player_pos, self.bot1_pos, self.bot2_pos, self.apple_locations, self.turn, self.player_health, self.score, self.action_space, self.game_over, self.map_size)

    def update_bot_positions(self):
        self.bot1_pos = self.get_bot1_position()
        self.bot2_pos = self.get_bot2_position()

    def get_bot1_position(self):
        # TODO: bot 1 chases the player
        return self.bot1_pos

    def get_bot2_position(self):
        # TODO: bot 2 stands between the player and the apple closest to the player
        return self.bot2_pos




if __name__ == '__main__':
    env = Env()
    new_state = env.reset()

    # initialize game variables
    game_history = []
    player = MyBot.MyBot()

    while new_state[8] == False: # go until the game is over
        state = copy.deepcopy(new_state)
        action = player.get_action(*state)
        # TODO: time players bot, auto exit if exceeds allotted time

        # save the game history
        game_history += [(*state, action)]

        # get the next game state
        new_state = env.step(action)

    game_history += [(*new_state, '')]

    print('{} points in {} turns ({} points / turn)'.format(new_state[6], new_state[4], new_state[6]/new_state[4]))

    # write game history to file
    now = datetime.now()
    with open(now.strftime('%d-%b-%Y_%H-%M-%S.log'), 'w') as f:
        for frame in game_history:
            f.write(frame.__str__() + '\n')
    
