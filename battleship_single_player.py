import pygame, sys
from pygame.locals import *
import numpy as np
import tkinter as tk
import random

class Board():
	def __init__(self,user):
		self.user = user
		self.size = 10
		self.row_list = ("1","2","3","4","5","6","7","8","9","10")
		self.col_list = ("A","B","C","D","E","F","G","H","I","J")
		self.cellSize = 55
		self.borderSize = 5	
		if (user == "Player"):
			self.start_xpos = 55
			self.start_ypos = 55
		elif (user == "Enemy"):
			self.start_xpos = 670
			self.start_ypos = 55

	def draw_axis_titles(self, window, start_xpos, start_ypos, row_pos, col_pos, color):
		font = pygame.font.SysFont(None, 25)
		for i in self.row_list:
			text = font.render(i, 1, color)
			window.blit(text, (row_pos - (text.get_width()/2), start_ypos))
			row_pos += self.cellSize
		for j in self.col_list:
			text = font.render(j, 1, color)
			window.blit(text, (start_xpos, col_pos - (text.get_width()/2)))
			col_pos += self.cellSize
	
	# Draws the board starting from the top left corner
	def draw_board(self, window, color, text_color):
		start_xpos = self.start_xpos
		start_ypos = self.start_ypos
		line_xpos = self.start_xpos
		line_ypos = self.start_ypos
		end_xpos = start_xpos + (self.cellSize * self.size)
		end_ypos = start_ypos + (self.cellSize * self.size)
		
		# drawing the borders
		pygame.draw.line(window, color, (start_xpos, start_ypos), (start_xpos, end_ypos), self.borderSize)
		pygame.draw.line(window, color, (start_xpos, start_ypos), (end_xpos, start_ypos), self.borderSize)
		pygame.draw.line(window, color, (start_xpos, end_ypos), (end_xpos, end_ypos), self.borderSize)
		pygame.draw.line(window, color, (end_xpos, start_ypos), (end_xpos, end_ypos), self.borderSize)
		
		# drawing the grid
		for i in range(self.size):
			pygame.draw.line(window, color, (line_xpos, start_ypos), (line_xpos, end_ypos))
			pygame.draw.line(window, color, (start_xpos, line_ypos), (end_xpos, line_ypos))
			line_xpos += self.cellSize
			line_ypos += self.cellSize
	
		self.draw_axis_titles(window, start_xpos - 25, start_ypos - 25, start_xpos + 15, start_ypos + 15, BLACK)
		font = pygame.font.SysFont(None, 50)
		str = self.user + "'s Board"
		text = font.render(str, 5, text_color)
		window.blit(text, ((((end_xpos - ((end_xpos - start_xpos)/4)) - text.get_width()), end_ypos + 15)))
		
		pygame.display.update()

class Ships():
	def __init__(self, user, board):
		self.user = user
		self.selected = [] # array to keep track of which cells are selected to be ships
		self.available = ['2', '3', '3', '4', '5']
		self.board = board
	
	def ship_setup(self):
		size = self.board.size
		if (self.user == "Player"):
			root = tk.Tk()
			root.title('Place your ships!')
			root.geometry('260x320')
			frame = tk.Frame(root)
			frame.grid(row = 0, column = 0)
			frame['borderwidth'] = 15
			label = tk.Label(root, text = "Ship Lengths Left: " + ' '.join(str(s) for s in self.available), fg = 'red')
			
			self.btn = [[0 for x in range(size)] for x in range(size)]
			for row in range(size):
				for col in range(size):
					index = row * size + col
					self.btn[row][col] = tk.Button(frame, text = index,  command = lambda x=row, y=col, i = index: self.set_ship(x,y,i))
					self.btn[row][col].grid(row = row, column = col, sticky = "ew")
			label.grid()
			root.mainloop()
		elif (self.user == "Enemy"):
			self.cpu_ships(size)
		
	def set_ship(self,row,col,index):
		if (self.btn[row][col].cget('bg') == 'SystemButtonFace'):
			self.btn[row][col].config(bg ='#008000')
			self.selected.append(index)
		elif (self.btn[row][col].cget('bg') == '#008000'):
			self.btn[row][col].config(bg ='SystemButtonFace')
			self.selected.remove(index)
			
	def draw_ships(self, window, color):
		start_xpos = self.board.start_xpos
		start_ypos = self.board.start_ypos
		cellSize = self.board.cellSize
		size = self.board.size
		selected = np.sort(self.selected)
		for i in selected:
			pygame.draw.rect(window, color, (start_xpos + cellSize * (i % size), start_ypos + cellSize * (i // size),cellSize, cellSize), 0)
		pygame.display.update()

	def cpu_ships(self, size):
		while self.available:
			for x in self.available:
				overlap = False
				orientation = random.randint(0,1) # 0 for horizontal, 1 for vertical
				if (orientation == 0):
					row = random.randint(0,(size-1))
					col = random.randint(0,(size-1)-int(x))
					index = row * size + col
					for i in range(int(x)):
						if (index + i) in self.selected: # check if ship overlaps
							overlap = True
							break
					if (overlap):
						continue
					for i in range(int(x)):
						self.selected.append(index + i)
				else:
					row = random.randint(0,(size-1)-int(x))
					col = random.randint(0,(size-1))
					index = row * size + col
					for i in range(int(x)):
						if (index + i*size) in self.selected:
							overlap = True
							break
					if (overlap):
						continue	
					for i in range(int(x)):
						self.selected.append(index + i*size)
				self.available.remove(x)

class Missiles():
	def __init__(self, user, board, ships, enemy_board, enemy_ships):
		self.user = user
		self.board = board
		self.ships = ships
		self.enemyBoard = enemy_board
		self.enemyShips = enemy_ships
		if (user == "Enemy"):
			self.notattacked = list(range(0,enemy_board.size * enemy_board.size)) # array to keep track of what cells are not hit yet
	
	def attack_ui(self, window, enemyMissiles, turn):
		if (self.user == "Player"):
			size = self.enemyBoard.size
			root = tk.Tk()
			root.title('ATTACK!!!!!')
			root.geometry('260x320')
			frame = tk.Frame(root)
			frame.grid(row = 0, column = 0)
			frame['borderwidth'] = 15
			
			self.btn = [[0 for x in range(size)] for x in range(size)]
			for row in range(size):
				for col in range(size):
					index = row * size + col
					self.btn[row][col] = tk.Button(frame, text = index,  command = lambda x=row, y=col, i = index, win=window, eBoard=self.enemyBoard, eShips=self.enemyShips, eMissiles=enemyMissiles, turn1=turn: self.fire_missile(x,y,i, win, eBoard, eShips, eMissiles, turn))
					self.btn[row][col].grid(row = row, column = col, sticky = "ew")
			root.mainloop()
		elif (self.user == "Enemy"):
			pass
	
	def fire_missile(self, row, col, index, window, enemyBoard, enemyShips, enemyMissiles, turn):
		start_xpos = enemyBoard.start_xpos
		start_ypos = enemyBoard.start_ypos
		cellSize = enemyBoard.cellSize
		size = enemyBoard.size
		if (self.user == "Player" and turn == 0): # Player attack
			if (index in enemyShips.selected):
				pygame.draw.circle(window, (255,0,0), ((start_xpos + cellSize * (index % size)) + cellSize//2, (start_ypos + cellSize * (index // size)) + cellSize//2), cellSize//2, 0)
				enemyShips.selected.remove(index)
				self.btn[row][col].config(bg ='#FF0000', state = tk.DISABLED)
				self.check_win_condition(window)
			else:
				pygame.draw.circle(window, (0,0,0), ((start_xpos + cellSize * (index % size)) + cellSize//2, (start_ypos + cellSize * (index // size)) + cellSize//2), cellSize//2, 0)
				self.btn[row][col].config(bg='#000000', state = tk.DISABLED)
				enemyMissiles.fire_missile(row, col, index, window, self.board, self.ships, self, 1)
		elif (self.user == "Enemy" and turn == 1): # CPU attack
			index = random.choice(self.notattacked)
			if (index in enemyShips.selected):
				pygame.draw.circle(window, (255,0,0), ((start_xpos + cellSize * (index % size)) + cellSize//2, (start_ypos + cellSize * (index // size)) + cellSize//2), cellSize//2, 0)
				enemyShips.selected.remove(index)
				self.fire_missile(row, col, index, window, enemyBoard, enemyShips, self, turn)
				enemyMissiles.check_win_condition(window)
			else:
				pygame.draw.circle(window, (0,0,0), ((start_xpos + cellSize * (index % size)) + cellSize//2, (start_ypos + cellSize * (index // size)) + cellSize//2), cellSize//2, 0)
			self.notattacked.remove(index)
		pygame.display.update()
	
	def check_win_condition(self, window):
		if (self.user == "Player"):
			if not self.ships.selected:
				font = pygame.font.SysFont(None, 80)
				text = font.render("You Lose...",5,(0,0,255))
				window.blit(text,((window.get_width()/2)-(text.get_width()/2),(window.get_height()/2)-150))
				pygame.display.update()
				self.disable_all_buttons()
			elif not self.enemyShips.selected:
				font = pygame.font.SysFont(None, 80)
				text = font.render("You Win!!",5,(0,255,0))
				window.blit(text,((window.get_width()/2)-(text.get_width()/2),(window.get_height()/2)-150))
				pygame.display.update()
				self.disable_all_buttons()
#		elif (self.user == "Enemy"):
#			if not self.ships.selected:
#				font = pygame.font.SysFont(None, 60)
#				text = font.render("You Win!!",5,(0,0,255))
#				window.blit(text,((window.get_width()/2)-(text.get_width()/2),(window.get_height()/2)-150))
#				pygame.display.update()
#				self.disable_all_buttons()
#			elif not self.enemyShips.selected:
#				font = pygame.font.SysFont(None, 50)
#				text = font.render("You Lose...",5,(255,0,0))
#				window.blit(text,((window.get_width()/2)-(text.get_width()/2),(window.get_height()/2)-150))
#				pygame.display.update()
#				self.disable_all_buttons()
	
	def disable_all_buttons(self):
		size = self.enemyBoard.size
		for row in range(size):
				for col in range(size):
					self.btn[row][col].config(state = tk.DISABLED) 
	
if __name__ == "__main__":
	# Initialize program
	pygame.init()
	pygame.font.init()

	# Game Settings
	WHITE = (255,255,255)
	BLACK = (0,0,0)
	RED = (255,0,0)
	GREEN = (0,255,0)
	BLUE = (0,0,255)
	GREY = (128,128,128)

	# Setting up Display Window
	SCREEN_WIDTH = 1280
	SCREEN_HEIGHT = 720

	DISPLAYSURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	DISPLAYSURFACE.fill(WHITE)
	pygame.display.set_caption("Battleship")
	
	turn = random.randint(0,1)
	playerBoard = Board("Player")
	enemyBoard = Board("Enemy")
	playerShip = Ships("Player", playerBoard)
	playerShip.ship_setup()
	enemyShip = Ships("Enemy", enemyBoard)
	enemyShip.ship_setup()
	playerMissiles = Missiles("Player", playerBoard, playerShip, enemyBoard, enemyShip)
	enemyMissiles = Missiles("Enemy", enemyBoard, enemyShip, playerBoard, playerShip)
	
	#=============
	# GAME START
	#=============
	playerBoard.draw_board(DISPLAYSURFACE, BLACK, BLUE)
	enemyBoard.draw_board(DISPLAYSURFACE, BLACK, BLUE)
	playerShip.draw_ships(DISPLAYSURFACE, GREY)
	enemyShip.draw_ships(DISPLAYSURFACE, GREY)
	if (turn == 1):
		enemyMissiles.fire_missile(0, 0, 0, DISPLAYSURFACE, playerBoard, playerShip, playerMissiles, turn)
		turn = 0
	playerMissiles.attack_ui(DISPLAYSURFACE, enemyMissiles, turn)
	
	pygame.quit()