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
        self.bot1_pos = (2, 2)
        self.bot2_pos = (HEIGHT-1, WIDTH-1)
        self.score = 0
        self.apple_locations = []
        self.game_over = False
        self.map_size = (HEIGHT, WIDTH)

    def reset(self):
        self.turn = 0
        self.player_pos = (HEIGHT >> 1, WIDTH >> 1)
        self.player_health = MAX_HEALTH
        self.bot1_pos = (2, 2)
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
        self.update_bot1_position()
        self.update_bot2_position()

    def update_bot1_position(self):
        # bot 1 chases the player

        # check all directions and see which one is the closest to the player
        direction = self.get_closest_direction_to_target(self.bot1_pos, self.player_pos)

        # calculate the new position
        newy = self.bot1_pos[0]
        newx = self.bot2_pos[1]
        if direction == 'u':
            newy = (self.bot1_pos[0] - 1 + HEIGHT) % HEIGHT
        elif direction == 'd':
            newy = (self.bot1_pos[0] + 1 + HEIGHT) % HEIGHT
        elif direction == 'l':
            newx = (self.bot1_pos[1] - 1 + WIDTH) % WIDTH
        elif direction == 'r':
            newx = (self.bot1_pos[1] + 1 + WIDTH) % WIDTH

        self.bot1_pos = (newy, newx)

    def update_bot2_position(self):
        # TODO: bot 2 stands between the player and the apple closest to the player
        self.bot2_pos = self.bot2_pos
    
    def get_closest_direction_to_target(self, position, target):
        # check the four direction and go to the one that is closest to the target
        direction = 's'
        min_distance = 99999
        for ymod, xmod, dir in [(-1, 0, 'u'), (1, 0, 'd'), (0, 1, 'r'), (0, -1, 'l')]:
            dx = abs(position[1] + xmod - target[1])
            if (dx > (self.map_size[1]>>1)):
                dx = self.map_size[1] - dx

            dy = abs(position[0] + ymod - target[0])
            if dy > (self.map_size[0]>>1):
                dy = self.map_size[0] - dy

            distance = dx + dy
            if distance < min_distance:
                min_distance = distance
                direction = dir

        return direction




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
    
