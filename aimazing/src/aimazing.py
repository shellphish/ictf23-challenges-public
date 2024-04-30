#!/usr/bin/env python3

# MAZE GAME INSPIRED BY: https://replit.com/talk/learn/Build-Your-Own-Maze-Game-in-Python/78799

import argparse
import itertools
import networkx as nx
import os
import pickle
import random
import signal
import sys
import termios
import time
import zlib

from rich.console import Console
from rich.syntax import Syntax
from rich.rule import Rule
from rich.prompt import IntPrompt

from os import system
from pyfiglet import Figlet


############################################################
# GLOBALS
############################################################
TIMEOUT = 180
embed = lambda c: "wasdx .#F".index(c)
reverse_embed = lambda i: "wasdx .#F"[i]


############################################################
# UTILS
############################################################
def replace_string(text,index,substring):
	new = list(text)
	new[index] = substring
	return ''.join(new)

def colorize(string):
		return string.replace(" ","  ")\
			.replace("#","\u001b[47;1m  \u001b[0m")\
			.replace("F","\u001b[42;1m  \u001b[0m")\
			.replace("C","\u001b[46;1m  \u001b[0m")

def raw_input(f):
	if not os.isatty(sys.stdin.fileno()):
		return f
	def wrapper(*args, **kwargs):
		old_settings = termios.tcgetattr(sys.stdin)
		new_settings = termios.tcgetattr(sys.stdin)
		new_settings[3] = new_settings[3] & ~termios.ICANON
		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, new_settings)
		try:
			return f(*args, **kwargs)
		finally:
			termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
	return wrapper

# @raw_input
def getch():
	return os.read(sys.stdin.fileno(), 1).decode()

# @raw_input
def long_input(prompt=""):
	return input(prompt)


############################################################
class Maze:
	def __init__(self, ascii_maze, curr_pos, end_pos, timeout=TIMEOUT):
		self.map = [[c for c in line] for line in ascii_maze.splitlines()]
		self.curr_pos = curr_pos
		self.end_pos = end_pos

		self.height = len(self.map)
		self.width = len(self.map[0])

		self.greeting = "WASD to move, Q to quit. Get to the green target!"
		self.congrats = "Congratulations! You made it to the end!"

		self.action_log = []
		self.visited = {curr_pos,}
		self.visible = set()
		
		self.input_mode = None
		self.model = None
		self.recorded_moves = None

		self.timeout = timeout

	@staticmethod
	def from_text(text):
		# get ascii art text (only # and spaces)
		# figlet_text = Figlet(font="banner3-D").renderText(text).replace("'", " ").replace(".", " ").replace(":", " ")
		figlet_text = Figlet(font="3-d").renderText(text)\
			.replace("*", "#")\
			.replace("/", " ")
		lines = ("\n"+figlet_text).splitlines()

		# normalize line width
		height = len(lines)
		width = max(len(s) for s in lines)
		lines = [l + ' ' * (width - len(l)) for l in lines]

		# add vertical obstructions (" # ") every 15 columns
		skip = itertools.cycle([height-1, 0])
		skip_pairs = [(i, next(skip)) for i in range(15, width, 15)]
		for i in range(15, width, 15):
			for j in range(0, height):
				if (i, j) in skip_pairs:
					continue
				lines[j] = lines[j][:i] + "#" + lines[j][i:]

		# add border
		height = len(lines)
		width = max(len(s) for s in lines)
		tmp = ['#' + '#' * width + '#']
		for s in lines:
			tmp.append('#' + (s + ' ' * width)[:width] + '#')
		tmp.append('#' + '#' * width + '#')
		lines = tmp

		# place player
		height = len(lines)
		width = max(len(s) for s in lines)
		for i, j in [(i,j) for j in range(width) for i in range(height)]:
			if lines[i][j] == ' ':
				curr_pos = (i, j)
				break

		# place finish line
		for i, j in [(i,j) for j in range(width) for i in range(height)][::-1]:
			if lines[i][j] == ' ':
				end_pos = (i, j)
				break

		ascii_maze = '\n'.join(lines)
		return Maze(ascii_maze, curr_pos, end_pos)
	
	############################################################
	# MOVEMENT / MAP HELPERS
	############################################################
	def get_move_from_nodes(self, source_node, target_node):
		# wasd to move
		if source_node[0] > target_node[0]:
			return "w"
		elif source_node[0] < target_node[0]:
			return "s"
		elif source_node[1] > target_node[1]:
			return "a"
		elif source_node[1] < target_node[1]:
			return "d"
				
	def up(self):
		self.curr_pos = (self.curr_pos[0]-1, self.curr_pos[1])

	def down(self):
		self.curr_pos = (self.curr_pos[0]+1, self.curr_pos[1])

	def left(self):
		self.curr_pos = (self.curr_pos[0], self.curr_pos[1]-1)

	def right(self):
		self.curr_pos = (self.curr_pos[0], self.curr_pos[1]+1)

	def inspect_surroundings(self, n=1):
		r, c = self.curr_pos

		# get everything n blockS from current position
		surroundings = ""
		for i in range(-n, n+1):
			for j in range(-n, n+1):
				# if out of bound, just add a wall
				if r+i < 0 or r+i >= self.height or c+j < 0 or c+j >= self.width:
					surroundings += "#"
				# if current position, skip
				# elif i == 0 and j == 0:
				# 	pass
				# 	surroundings += "."
				# if visited, add a dot
				elif (r+i, c+j) in self.visited:
					surroundings += "."
				else:
					surroundings += self.map[r+i][c+j]
		return surroundings

	############################################################
	# GAME LOOP
	############################################################
	def print(self):
		# ONLY PRINT THE PART OF THE MAZE THAT WAS DISCOVERED, PLUS THE FINAL TARGET
		for i, line in enumerate(self.map):
			for j, c in enumerate(line):
				if (i, j) == self.curr_pos:
					print(colorize("C"), end="")
				elif (i, j) == self.end_pos:
					print(colorize("F"), end="")
				elif (i, j) in self.visible:
					print(colorize(c), end="")
				else:
					print(colorize(" "), end="")
			print("\n", end="")

	def update_visible_area(self):
		# set up visible area
		for i, line in enumerate(self.map):
			for j, _ in enumerate(line):
				# first and last rows are always visible
				if i == 0 or i == self.height-1:
					self.visible.add((i, j))
				# first and last columns are always visible
				if j == 0 or j == self.width-1:
					self.visible.add((i, j))
			# everything within 10 columns of the player is visible
			_, col = self.curr_pos
			for j in range(0, col+10):
				self.visible.add((i, j))

	def _get_x(self, with_embeddings=False):
		surroundings = self.inspect_surroundings()
		previous_answer = self.action_log[-1][1] if len(self.action_log) > 0 else "x"
		x = (previous_answer,)+tuple(c for c in surroundings)
		if with_embeddings:
			x = tuple(embed(c) for c in x)
		return x

	def do_move(self, answer):
		x = self._get_x()

		# move player, or quit
		row, col = self.curr_pos
		if answer == "w" and self.map[row-1][col]!="#":
			self.up()
		elif answer == "s" and self.map[row+1][col]!="#":
			self.down()
		elif answer == "a" and self.map[row][col-1]!="#":
			self.left()
		elif answer=="d" and self.map[row][col+1]!="#":
			self.right()
		elif answer == "q":
			Maze.quit("Bye!", self.action_log)
		else:
			return False

		# log game action (pre-move)
		self.action_log.append((x, answer))
		# update visited
		self.visited.add(self.curr_pos)
		
		return True

	@staticmethod
	def quit(message, action_log=None):
		print(message)
		if action_log is not None:
			print("\nAction log (serialized - see help message):")
			action_log_serialized = zlib.compress(pickle.dumps(action_log))
			print(action_log_serialized.hex())

		exit(1)
	
	@staticmethod
	def timeout(*args, **kwargs):
		Maze.quit("Do you even need AI?")

	############################################################
	# INPUT MODES
	############################################################
	def input_mode_player(self):
		answer = getch().lower()
		return answer

	def input_mode_ai(self):
		self.greeting = "CTRL-C to quit. Get to the green target!"
		x = [self._get_x(with_embeddings=True),]
		
		# pick with probability proba
		proba = self.model.predict_proba(x)[0]
		y = random.choices(self.model.classes_, weights=proba, k=1)[0]

		y = reverse_embed(y)
		
		time.sleep(0.25)
		return y
	
	def input_mode_recorded(self):
		self.greeting = "CTRL-C to quit."
		self.congrats = "That's how it's done!"
		# pop moves from self.recorded_moves
		if len(self.recorded_moves) == 0:
			raise Exception("No more recorded moves")
		answer = self.recorded_moves.pop(0)
		time.sleep(0.25)
		return answer

	############################################################
	# UTILS
	############################################################
	def as_graph(self):
		# for each pair of nodes, add edge if they are adjacent (and not walls)
		G = nx.Graph()
		for i, line in enumerate(self.map):
			for j, c in enumerate(line):
				if c == "#":
					continue
				if i > 0 and self.map[i-1][j] != "#":
					G.add_edge((i, j), (i-1, j))
				if i < len(self.map)-1 and self.map[i+1][j] != "#":
					G.add_edge((i, j), (i+1, j))
				if j > 0 and self.map[i][j-1] != "#":
					G.add_edge((i, j), (i, j-1))
				if j < len(line)-1 and self.map[i][j+1] != "#":
					G.add_edge((i, j), (i, j+1))
		return G

	def run(self):
		signal.signal(signal.SIGALRM, Maze.timeout)
		signal.alarm(self.timeout)
		answer = None
		while True:
			self.update_visible_area()

			system("clear")
			self.print()
			print(self.greeting)

			print(f"Last move: {answer}")

			if self.curr_pos == self.end_pos:
				Maze.quit(self.congrats, self.action_log)

			# read input
			answer = self.input_mode()

			if not self.do_move(answer):
				continue


############################################################
# FLAG AND TRAIN SENTENCES
############################################################
FLAG = None
LOREM_IPSUM = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
# all 3 consecutive words in LOREM_IPSUM.split
TRAIN_SENTENCES = [f"ictf{{{' '.join(LOREM_IPSUM.split()[i:i+3])}}}" for i in range(len(LOREM_IPSUM.split())-2)]


############################################################
# MAIN
############################################################
def main():
	# clear screen
	system("clear")

	console = Console()

	# select input mode
	console.print("I built this fantastic command line maze game, do you think you can solve it? [red]Train[white] mode does [red]NOT[white] show the real flag.")
	# console.print("Possible actions:")
	console.print("  1. [red][Train][white] Just Train")
	console.print("  2. [red][Train][white] Watch a Pro")
	console.print("  3. [green][Play][white]  Play with AI")
	console.print("  4. Show Help")
	try:
		while True:
			choice = IntPrompt.ask("Your choice")
			if choice in [1, 2, 3, 4, 5]:
				break
			else:
				console.print("[red]Invalid choice, please try again.")
	except KeyboardInterrupt:
		Maze.quit("Bye!")

	if choice == 1:
		text = random.choice(TRAIN_SENTENCES)
		maze = Maze.from_text(text)
		maze.input_mode = maze.input_mode_player
	elif choice == 2:
		while True:
			text = random.choice(TRAIN_SENTENCES)
			maze = Maze.from_text(text)
			maze.input_mode = maze.input_mode_recorded

			graph = maze.as_graph()

			source_node = maze.curr_pos
			target_node = maze.end_pos
			try:
				path = nx.bidirectional_shortest_path(graph, source_node, target_node)
				break
			except nx.exception.NetworkXNoPath:
				continue

		maze.recorded_moves = []
		for source_node, target_node in zip(path[:-1], path[1:]):
			answer = maze.get_move_from_nodes(source_node, target_node)
			maze.recorded_moves.append(answer)
	elif choice == 3:
		text = FLAG
		maze = Maze.from_text(text)
		compressed_model = long_input("Please input your serialized scikit-learn model (see help message):")
		# TODO: harden pickle
		maze.model = pickle.loads(zlib.decompress(bytes.fromhex(compressed_model)))
		# maze.model must have a predict method
		if not hasattr(maze.model, "predict_proba") or not callable(maze.model.predict_proba):
			Maze.quit("Invalid model. Your model must have a predict_proba method.")
		maze.input_mode = maze.input_mode_ai
	elif choice == 4:
		console.print(Rule("Help"))
		console.print(Rule("Input Modes"))
		console.print("  1. (Just Train)   The player can move around the maze using WASD. [bold]The maze does NOT show the real flag.")
		console.print("  2. (Watch a Pro)  Show a recorded (optimal) game. [bold]The maze does NOT show the real flag.")
		console.print("  3. (Play with AI) The player uploads a trained scikit-learn model. Given the input features, the model will predict the next movement and navigate the maze. [bold]The maze shows the real flag.")
		console.print(Rule("Action Log"))
		console.print("At the end of each game, the action log is serialized and shown to the player. The player can then use the action log to train their model.")
		console.print("The action log consists in a list of tuples (x, y) where x represents the input features and y the next movement. The input features are a tuple of 10 characters (previous movement + 9 cells around the player - left to right, top to bottom). The next movement is one of 'wasd'. For example:")

		SYMBOLS = f"""
[bold][orange1]w[white]: movement up       [orange1]d[white]: movement right     [orange1].[white]: visited cell
[bold][orange1]a[white]: movement left     [orange1]x[white]: no movement        [orange1]#[white]: wall
[bold][orange1]s[white]: movement down     [orange1] [white]: empty cell         [orange1]F[white]: finish
		"""
		console.print(SYMBOLS)

		print(colorize("###"))
		print(colorize("#C "))
		print(colorize("#↓ #"))
		console.print("Action: (('x', '#', '#', '#', '#', '.', ' ', '#', ' ', '#'), 's')")

		print()
		print(colorize("#↓ #"))
		print(colorize("#C →"))
		print(colorize("###"))
		console.print("Action: (('s', '#', '.', '#', '#', '.', ' ', '#', '#', '#'), 'd')")

		print()
		console.print("The action log is then serialized and deserialized using:")

		SERIALIZATION = """c_actions = zlib.compress(pickle.dumps(actions)).hex()
actions = pickle.loads(zlib.decompress(bytes.fromhex(c_actions)))"""
		console.print(Syntax(SERIALIZATION, "python", theme="ansi_dark", line_numbers=True, indent_guides=True, background_color="default"))
		# console.print(Syntax("c_actions = zlib.compress(pickle.dumps(actions)).hex()", "python"))
		# console.print(Syntax("pickle.loads(zlib.decompress(bytes.fromhex(c_actions)))", "python"))

		console.print(Rule("Training your model"))
		console.print("The player can train and play with any scikit-learn classification model. When training a model, the player must use the provided embeddings:\n")

		TRAINING = f"""import pickle
import zlib

embed = lambda c: "wasdx .#F".index(c)

c_actions = "789c6b6099aac90001b153347a182ba6f4302a4fc96002c11e463d204f01c463c9602a01b253a6b44d49d403004ff00e7d"
actions = pickle.loads(zlib.decompress(bytes.fromhex(c_actions)))
X, Y = zip(*actions)
X = [[embed(c) for c in x] for x in X]
Y = [embed(y) for y in Y]

# train any scikit-learn classification model
# import sklearn.tree
# clf = sklearn.tree.DecisionTreeClassifier()
# clf.fit(X, Y)

cmodel = zlib.compress(pickle.dumps(clf)).hex()
print(cmodel)"""
		
		console.print(Syntax(TRAINING, "python", theme="ansi_dark", line_numbers=True, indent_guides=True, background_color="default"))

		console.print(Rule())
		exit(0)
	
	maze.run()

# def dump_random_game():
# 	text = random.choice(TRAIN_SENTENCES)
# 	maze = Maze.from_text(text)
# 	maze.input_mode = maze.input_mode_recorded

# 	graph = maze.as_graph()

# 	source_node = maze.curr_pos
# 	target_node = maze.end_pos

# 	# find shortest path from start to mid
# 	while True:
# 		try:
# 			# pick a random node that's not a wall or finish
# 			mid_node = random.choice([(i, j) for i in range(maze.height) for j in range(maze.width) if (i, j) in graph.nodes and (i, j) != target_node])
# 			path = nx.bidirectional_shortest_path(graph, source_node, mid_node)
# 			break
# 		except nx.exception.NetworkXNoPath:
# 			print("Bad random node, retrying...")
# 			continue

# 	# get there (this will record visited and action log)
# 	for s, t in zip(path[:-1], path[1:]):
# 		answer = maze.get_move_from_nodes(s, t)
# 		maze.do_move(answer)

# 	# reset the action log
# 	maze.action_log = []

# 	# find shortest path from mid to finish
# 	path = nx.bidirectional_shortest_path(graph, mid_node, target_node)

# 	# get there
# 	for s, t in zip(path[:-1], path[1:]):
# 		answer = maze.get_move_from_nodes(s, t)
# 		maze.do_move(answer)

# 	# compress and dump action log to ./training/<hash(compressed_action_log)>
# 	action_log_serialized = zlib.compress(pickle.dumps(maze.action_log))
# 	filename = f"./training/{sha256(action_log_serialized.encode()).hexdigest()}.hex"
# 	with open(filename, "w") as f:
# 		f.write(action_log_serialized)

if __name__ == "__main__":
	try:
		parser = argparse.ArgumentParser()
		parser.add_argument("--flag", type=str, help="Flag")
		parser.add_argument("--debug", action="store_true", help="Debug mode")
		# parser.add_argument("--play", action="store_true", help="Play the game")
		# parser.add_argument("--training", type=int, help="Dump N random games.")
		args = parser.parse_args()

		if args.flag:
			FLAG = args.flag
		else:
			raise Exception("No flag provided. Please use --flag <flag>")
		
		if args.debug:
			text = FLAG
			maze = Maze.from_text(text)
			maze.input_mode = maze.input_mode_player
			maze.run()

		# if args.play:
		# 	main()
		# elif args.training is not None:
		# 	for _ in range(args.training):
		# 		dump_random_game()
		# else:
		# 	parser.print_help()

		main()

	except KeyboardInterrupt:
		Maze.quit("Bye!")
