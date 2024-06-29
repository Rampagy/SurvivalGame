import random


# rename this class for your specific bot
class MyBot():
    def __init__(self):
        # Put any bot initializations here
        pass

    # DO NOT rename this function
    def get_action(self, player_pos, bot1_pos, bot2_pos, apple_locations, turn, player_health, score, action_space, game_over, map_size):
        # Add your bot logic here
        return random.choice(action_space)

    def get_name():
        return 'ExampleBot'