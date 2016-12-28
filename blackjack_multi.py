import random 
import sys

class TABLE():
	def __init__(self, deck, dealer, players):
		self.deck    = deck    # a deck class
		self.dealer  = dealer  # a player class
		self.players = players # a list of player clases
		self.discard = []      # used for discarded cards after each game
		self.num_games = 0
	
	def all_players(self):
		return [self.dealer] + self.players # return a list of all players including dealer

	def deal(self, player, num_cards=1):
		for i in range(num_cards):
			player.add_card( self.deck.get_card() )

	def get_table_state(self):
		return { "cards_remaining"      : self.deck.cards_remaining(),
				 "dealer_visible_card"  : self.dealer.get_visible_card(),
				 "discarded_cards"      : self.discard
				}

	def setup_game(self):		
		self.num_games += 1
		for p in self.all_players():
			self.discard += p.discard() # discard current hand
			self.deal(p, 2)				# deal new starting hand

	def run_game(self):
		for p in self.all_players():
			while p.play( self.get_table_state() ) == 'hit':
				self.deal(p)

	def check_if_winner(self, player):
		dealer_value = self.dealer.get_hand_value()
		player_value = player.get_hand_value()
		if player_value <= 21 and  dealer_value > 21:
			return True
		if player_value <= 21 and player_value > dealer_value:
			return True
		return False

	def score_game(self):
		dealer_value = self.dealer.get_hand_value()
		for p in self.players:
			if self.check_if_winner(p):
				p.num_wins += 1

	def print_game(self):
		# print player, hand_value, hand, win
		print '\nGAME NUMBER:',self.num_games
		print self.dealer.name, self.dealer.get_hand_value(), self.dealer.get_hand()
		for p in self.players:
			print p.name, p.get_hand_value(), p.hand, self.check_if_winner(p)

	def print_summary(self):
		print '\nTOTAL GAMES', self.num_games
		for p in self.players:
			print '-'
			print 'name  : ', p.name
			print 'wins  : ', p.num_wins
			print 'win % : ',100.0*p.num_wins/self.num_games
			
		


class DECK():
	def __init__(self, num_decks=1):
		self.cards = self.build_deck(num_decks)

	def build_deck(self, num_decks=1):
		d = []
		for val in ['A','2','3','4','5','6','7','8','9','T','J','Q','K']:
			for suit in ['H','D','S','C']:
				d.append(val+suit)
		d *= num_decks # replicate array to generate multiple decks
		random.shuffle(d)
		return d

	def cards_remaining(self):
		return len(self.cards)

	def get_card(self):
		try:
			return self.cards.pop()
		except:
			print ' ! ERROR - Deck out of cards'
			sys.exit()

		
class PLAYER():
	def __init__(self, name):
		self.hand     = []
		self.name     = name
		self.num_wins = 0

	def add_card(self, c):
		self.hand.append(c)

	def add_cards(self, cards):
		for c in cards:
			self.add_card(c)

	def get_hand(self):
		return self.hand

	def get_hand_value(self):
		card_values = {'A':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'T':10,'J':10,'Q':10,'K':10}
		hand_values = [card_values[c[0]] for c in self.hand]
		total = sum(hand_values)

		# use ace as 11 unless bust
		if 1 in hand_values and total + 10 <=21:
			return total + 10
		else:
			return total

	def discard(self):
		discarded = self.hand
		self.hand = []
		return discarded

	def get_visible_card(self):
		if self.hand != []:
			return self.hand[0]
		else:
			return ''


# class DEALER():
# 	def __init__(self, dealer_player, num_decks=1, verbose=True):
# 		self.deck    = DECK(num_decks)
# 		self.dealer  = dealer_player
# 		self.players = []
# 		self.score   = {}
# 		self.game_num= 0
# 		self.verbose = verbose

# 	## PLAYER BASED METHODS ##
# 	def add_player(self, player):
# 		self.players.append(player)

# 	def all_players(self):
# 		return [self.dealer] + self.players

# 	def deal_cards(self, player, n):
# 		player.add_cards( self.deck.deal(n) )

# 	def get_hand_value(self, player):
# 		# assume ace = 1 then try to improve hand by adding 10
# 		card_values = {'A':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'T':10,'J':10,'Q':10,'K':10}
# 		hand_values = [card_values[c[0]] for c in player.get_hand()]
# 		total       = sum(hand_values)
		
# 		if 1 in hand_values and total + 10 <=21:
# 			return total + 10
# 		else:
# 			return total

# 	def get_dealer_visible_card(self):
# 		return self.dealer.get_hand()[0]

# 	## GAME BASED METHODS ##		
# 	def play_one_game(self):
# 		self.game_num += 1
# 		for p in self.all_players():
# 			self.deal_cards(p, 2) # deal starting hand of 2 cards
# 			# run the player to let them decide to hit/stay			
# 			action = p.play(self.get_dealer_visible_card())
# 			while action != 'stay':
# 				self.deal_cards(p, 1)
# 				action = p.play(self.get_dealer_visible_card())

# 	def discard_pile(self):
# 		return self.deck.discard_pile()

# 	def reset(self):
# 		self.deck.dealt_to_discard()
# 		for p in self.all_players():
# 			p.reset()

# 	def find_winner(self):
# 		print 'game #', self.game_num

# 		d_value = self.dealer.get_hand_value()
# 		print d_value, self.dealer.name,  self.dealer.hand

		
# 		for p in self.players:		
# 			p_value = self.get_hand_value(p)
# 			print p_value, p.name, p.hand,
# 			if p_value <= 21 and d_value > 21:
# 				self.score[p.name] += 1
# 				print '*WIN*'
# 			elif p_value <= 21 and p_value > d_value:
# 				self.score[p.name] += 1
# 				print '*WIN*'
# 			else:
# 				print '*LOSS*'
# 		print self.score
		

# 	def print_results(self):
# 		print '\n#### RESULTS ####'
# 		for p in self.players:
# 			print p.name, self.score[p.name], 'wins', self.score[p.name]*100.0 / self.game_num, '%'

# 	def initialize_score(self):
# 		for p in self.players:
# 			self.score[p.name] = 0


# 	def run(self):
# 		self.initialize_score()
# 		while self.deck.cards_remaining() > 20:
# 			self.play_one_game()
# 			self.find_winner()
# 			self.reset()
# 			print '----'
# 		self.print_results()
