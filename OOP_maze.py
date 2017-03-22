import pygame, random, pickle

class Drawer(object):
	#class to draw display

	#rgb color codes
	black = (0,0,0)
	white = (255,255,255)
	red = (255,0,0)
	green = (0,255,0)
	blue = (0,0,255)

	def __init__(self, display, maze, cell_size, tick_interval=10):
		pygame.init()
		self.clock = pygame.time.Clock()
		self.tick_interval = tick_interval
		self.canvas = display
		self.cell_size = cell_size
		self.maze = maze
		self.path_start_frame = None
		self.frame_number = None
		self.running = False

	def draw_walls(self):
		for wall in self.maze.get_cell_walls():
			if wall.get_state()>0:
				p = wall.end_points()
				pygame.draw.line(self.canvas, Drawer.black, p[0], p[1],2)

	def draw_path(self, redraw_all=False, animate=True, path_speed=1):
		#path_speed is one update per number of frames (smaller = faster)
		if (self.frame_number != None) and (animate):
			if not self.maze.is_solved():
				self.maze.solve()
			if self.path_start_frame == None:
				self.path_start_frame = self.frame_number
			path_frame = self.frame_number-self.path_start_frame
			path_o = self.maze.get_solution_path()
			path = []
			for p in xrange(len(path_o)):
				path.append(((path_o[p][0]*self.cell_size+cellsize//2),(path_o[p][1]*self.cell_size+cellsize//2)))
			step = path_frame//path_speed
			if redraw_all:
				pygame.draw.lines(self.canvas,Drawer.red,False,path[:min(step+2,len(path))])
				pygame.draw.circle(self.canvas,Drawer.blue,path[min(((step+1),len(path)-1))],max(self.cell_size//4,2))
				if step >= len(path)-1:
					self.draw_optimal()
			elif (self.frame_number%path_speed == 0) and (step<(len(path)-1)):
				pygame.draw.line(self.canvas,Drawer.red,path[step:step+2][0],path[step:step+2][1])
			elif step == len(path)-1:
				self.draw_optimal()
		elif (not animate):
			if redraw_all or (not redraw_all and self.path_start_frame == None):
				if self.path_start_frame == None:
					self.path_start_frame = self.frame_number
				pygame.draw.lines(self.canvas,Drawer.red,False,path)

	def draw_optimal(self):
		if not self.maze.is_solved():
			self.maze.solve()
		path_o = self.maze.get_optimum_path()
		path = []
		for p in xrange(len(path_o)):
			path.append(((path_o[p][0]*self.cell_size+cellsize//2),(path_o[p][1]*self.cell_size+cellsize//2)))
		pygame.draw.lines(self.canvas,Drawer.green,False,path)

	def draw(self, redraw_all=False):
		self.running = True
		while self.running:
			self.clock.tick(self.tick_interval)
			if self.frame_number == None:
				self.frame_number = 0
			else:
				self.frame_number+=1
			if (self.frame_number == 0) or (redraw_all):
				self.canvas.fill(Drawer.white)
				self.draw_walls()
			if (self.frame_number > 0):
				self.draw_path(redraw_all)
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					self.running = False

class Cell(object):
	def __init__(self, w, h, r, c, cellrow, cellcol):
		self.row = cellrow
		self.col = cellcol
		self.size = w/c
		self.xy = (w*cellcol/c),(h*cellrow/r)
		self.walls = {"top":None, "right":None,"bottom":None, "left":None}
		if cellrow == 0:
			self.walls["top"] = Wall(self,self,2,"top")
		elif cellrow == r-1:
			self.walls["bottom"] = Wall(self,self,2,"bottom")
		if cellcol == 0:
			self.walls["left"] = Wall(self,self,2,"left")
		elif cellcol == c-1:
			self.walls["right"] = Wall(self,self,2,"right")
		self.visited = False
		self.connected = []

	def connect(self,direc,other_cell,wall=1):
		pair = {"top":"bottom","bottom":"top","left":"right","right":"left"}
		if other_cell != None:
			if other_cell not in self.connected:
				self.connected.append(other_cell)
			if self not in other_cell.connected:
				other_cell.connected.append(self)
			if self.walls[direc]==None and other_cell.walls[pair[direc]]!=None:
				self.walls[direc] = other_cell.walls[direc]
			elif self.walls[direc]!=None and other_cell.walls[pair[direc]]==None:
				other_cell.walls[direc] = self.walls[direc]
			else:
				wall = Wall(self, other_cell, wall, direc)
				self.walls[direc] = other_cell.walls[pair[direc]] = wall
				return wall
	
	def get_corner_xy(self, corner):
		if corner == "tl":
			return self.xy
		elif corner == "tr":
			return ((self.xy[0]+self.size),self.xy[1])
		elif corner == "bl":
			return ((self.xy[0],self.xy[1]+self.size))
		elif corner == "br":
			return ((self.xy[0]+self.size,self.xy[1]+self.size))

	def get_walls(self,boundary=True):
		walls = []
		for wall in self.walls.values():
			if wall!=None and (wall.state==2)==boundary:
				walls.append(wall)
		return walls

	def is_visited(self):
		return self.visited

	def visit(self):
		self.visited = True

class Wall(object):
	def __init__(self, cell1, cell2, state,direc):
		self.cells = [cell1, cell2]
		self.state = state
		self.set_points(direc)

	def set_points(self,dir1):
		cell1 = self.cells[0]
		cell2 = self.cells[1]
		if dir1=="top":
			self.p1 = cell1.get_corner_xy("tl")
			self.p2 = cell1.get_corner_xy("tr")
		elif dir1 == "right":
			self.p1 = cell1.get_corner_xy("tr")
			self.p2 = cell1.get_corner_xy("br")
		elif dir1 == "bottom":
			self.p1 = cell1.get_corner_xy("br")
			self.p2 = cell1.get_corner_xy("bl")
		elif dir1 == "left":
			self.p1 = cell1.get_corner_xy("bl")
			self.p2 = cell1.get_corner_xy("tl")

	def end_points(self):
		return self.p1,self.p2

	def set_state(self, state):
		if self.state != 2:
			self.state = state
		return self.state

	def get_state(self):
		return self.state

class Maze(object):
	def __init__(self, w, h, r, c, maze_setup=None, algo=None, solve_algo=None):
		if maze_setup == None:
			self.generate(algo, w, h, r, c)
		else:
			self.maze = maze_setup
		self.solution_path = []
		self.optimum_path = []
		self.solved = False
		self.solve_algo = solve_algo
		self.c = c
		self.r = r

	def is_solved(self):
		return self.solved

	def generate_maze_templ(self, w, h, r, c, default):
		walls = {}
		cells = {}
		for col in xrange(c):
			for row in xrange(r):
				cell = Cell(w, h, r, c, row, col)
				cells.update({(col,row):cell})
				for wall in cell.get_walls():
					if walls.has_key(((col,row),0)):
						walls.update({((col,row),1):wall})
					else:
						walls.update({((col,row),0):wall})
				if col>0:
					(c2,r2) = (col-1,row)
					wall = cell.connect("left",cells.get((c2,r2)),default)
					if wall != None:
						walls.update({((col,row),(c2,r2)):wall})
				if row>0:
					(c2,r2) = (col,row-1)
					wall = cell.connect("top",cells.get((c2,r2)),default)
					if wall != None:
						walls.update({((col,row),(c2,r2)):wall})
		self.maze = {"walls":walls,"cells":cells}

	def generate(self, algo, w, h, r, c):
		self.generate_maze_templ(w, h, r, c, 1)
		if algo==0:
			self._bintree()
		elif algo==1:
			self._depthfirst0(w, h, r, c)
		elif algo==1.1:
			self._depthfirstrand(w, h, r, c)
		elif algo==2:
			self._kruskal(w, h, r, c)
		elif algo==3:
			self._prim0(w, h, r, c)
		elif algo==3.1:
			self._primrand(w, h, r, c)

	def _bintree(self):
		for cell in self.maze["cells"].values():
			choices = ["top", "left"]
			if (cell.walls[choices.pop(random.randint(0,1))].set_state(0) != 0):
				cell.walls[choices.pop()].set_state(0)

	def _depthfirst0(self, w, h, r, c):
		self._depthfirst(w, h, r, c, (0,0))

	def _depthfirstrand(self, w, h, r, c):
		self._depthfirst(w, h, r, c, random.choice(self.maze["cells"].keys()))

	def _depthfirst(self, w, h, r, c, start):
		started = False
		stack = []
		cell = self.maze["cells"][start]
		while ((len(stack)>0) or (started==False)):
			if not started:
				started = True
			cell.visit()
			cellwalls = cell.get_walls(False)
			unvisited = False
			while (len(cellwalls)>0) and (not unvisited):
				wall = cellwalls.pop(random.randint(0,len(cellwalls)-1))
				for c in wall.cells:
					if not c.is_visited():
						next_cell = c
						unvisited = True
			if not unvisited:
				cell = self.maze["cells"][stack.pop()]
			else:
				stack.append((cell.col,cell.row))
				wall.set_state(0)
				cell = next_cell
		for cell in self.maze["cells"].values():
			cell.visited = False

	def _kruskal(self, w, h, r, c):
		cell_list = self.maze["cells"].keys()
		cell2set = {cell_list[i]:i for i in xrange(len(cell_list))}
		wall_list = self.maze["walls"].values()
		while len(wall_list)>0:
			wall = wall_list.pop(random.randint(0,len(wall_list)-1))
			cell1,cell2 = wall.cells
			cell1xy = cell1.col, cell1.row
			cell2xy = cell2.col, cell2.row
			if cell2set[cell1xy] != cell2set[cell2xy]:
				oldset = cell2set[cell2xy]
				newset = cell2set[cell1xy]
				for key in cell_list:
					if cell2set[key] == oldset:
						cell2set[key] = newset
				wall.set_state(0)

	def _prim0(self, w, h, r, c):
		self._prim(w, h, r, c, (0,0))

	def _primrand(self, w, h, r, c):
		self._prim(w, h, r, c, random.choice(self.maze["cells"].keys()))

	def _prim(self, w, h, r, c, start):
		self.maze["cells"][start].visit()
		wall_list = self.maze["cells"][start].get_walls(False)
		while len(wall_list) > 0:
			wall = wall_list.pop(random.randint(0,len(wall_list)-1))
			for cell in wall.cells:
				if not cell.is_visited():
					wall.set_state(0)
					cell.visit()
					wall_list+=cell.get_walls(False)
		for cell in self.maze["cells"].values():
			cell.visited = False

	def solve(self):
		c = self.c
		r = self.r
		if self.solve_algo == None:
			self.solve_algo = input("Choose a maze solving algorithm: ")
		if self.solve_algo==0:
			started = False
			start = (0,0)
			end = (c-1,r-1)
			stack = []
			path = []
			cell = self.maze["cells"][start]
			while ((len(stack)>0) or (started==False)) and (len(path)==0 or (path[-1] != end)):
				if not started:
					started = True
				cell.visit()
				path.append((cell.col,cell.row))
				cellwalls = cell.get_walls(False)
				unvisited = False
				while (len(cellwalls)>0) and (not unvisited):
					wall = cellwalls.pop()
					if (wall.get_state() == 0):
						for c in wall.cells:
							if not c.is_visited():
								next_cell = c
								unvisited = True
				if (not unvisited) and (path[-1] != end):
					cell = self.maze["cells"][stack.pop()]
				else:
					stack.append((cell.col,cell.row))
					cell = next_cell
			self.solution_path = path
			self.optimum_path = stack
			self.solved = True


	def get_solution_path(self):
		return self.solution_path

	def get_optimum_path(self):
		return self.optimum_path

	def get_cell_walls(self):
		return self.maze["walls"].values()

if __name__=="__main__":
	random.seed()
	algo=input("Choose a maze generation algorithm: ")
	size = width, height = 600, 800
	cellsize = 25
	rows = height//cellsize
	cols = width//cellsize

	display = pygame.display.set_mode(size)
	maze = Maze(width,height,rows,cols,algo=algo)
	pygame.init()
	draw = Drawer(display, maze, cellsize,50)
	draw.draw(True)

