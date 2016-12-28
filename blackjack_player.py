from blackjack import * # Note: aces are always 11, will fix later
import random


class DEALER_PLAYER(PLAYER):
	def play(self, table_state):
		if self.get_hand_value() < 16:
			return 'hit'
		else:
			return 'stay'

class RANDOM_PLAYER(PLAYER):
	def play(self, table_state):
		return random.choice( ['hit','stay'] )

class AWESOME_PLAYER(PLAYER):
	def play(self, table_state):
		if self.get_hand_value() < 16:
			return 'hit'
		else:
			return 'stay'

# create the dealer by passing a playertype and the size of the deck
deck    = DECK(10)
dealer  = DEALER_PLAYER('Dealer')
players = [ RANDOM_PLAYER('Jonathan'),
			AWESOME_PLAYER('Kristen')
		  ]	

T = TABLE(deck, dealer, players)

while T.get_table_state()['cards_remaining'] > 20:
	T.setup_game()
	T.run_game()
	T.score_game()
	T.print_game()
T.print_summary()
