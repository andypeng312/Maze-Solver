import pygame, random

def make_maze(size,cellsize,algo):
	cellsx = size[0]//cellsize
	cellsy = size[1]//cellsize
	cells = cellsx*cellsy
	if algo==0:
		#recursive depth-first
		maze = [[[1 for i in xrange(4)] for j in xrange(cellsy)] for k in xrange(cellsx)]
		def algo0(col,row):
			if (col,row)==(cellsx-1,cellsy-1):
				return
			else:
				poss_dir = range(4)
				poss_moves = [(0,-1),(1,0),(0,1),(-1,0)]
				while len(poss_dir)>0:
					dir_move = poss_dir.pop(random.randint(0,len(poss_dir)-1))
					move = poss_moves[dir_move]
					next_col = col+move[0]
					next_row = row+move[1]
					if (next_col>=0 and next_col<cellsx and next_row>=0 and next_row<cellsy):
						if sum(maze[next_col][next_row])==4:
							maze[col][row][dir_move] = 0
							maze[next_col][next_row][(dir_move+2)%4] = 0
							algo0(next_col,next_row)
						else:
							continue
					else:
						continue
				return
		algo0(0,0)
	elif algo==1:
		#iterized depth-first
		maze = [[[1 for i in xrange(4)] for j in xrange(cellsy)] for k in xrange(cellsx)]
		col = 0
		row = 0
		visited_stack = []
		while True:
			if (col,row)==(cellsx-1,cellsy-1):
				if len(visited_stack)>0:
					col,row = visited_stack.pop()
					continue
				else:
					break
			else:
				poss_dir = range(4)
				poss_moves = [(0,-1),(1,0),(0,1),(-1,0)]
				popstack=True
				while len(poss_dir)>0:
					dir_move = poss_dir.pop(random.randint(0,len(poss_dir)-1))
					move = poss_moves[dir_move]
					next_col = col+move[0]
					next_row = row+move[1]
					if (next_col>=0 and next_col<cellsx and next_row>=0 and next_row<cellsy):
						if sum(maze[next_col][next_row])==4:
							maze[col][row][dir_move] = 0
							maze[next_col][next_row][(dir_move+2)%4] = 0
							visited_stack.append((col,row))
							col,row = next_col,next_row
							popstack = False
							break
						else:
							continue
					else:
						continue
				if len(visited_stack)>0 and popstack:
					col,row = visited_stack.pop()
					continue
				elif popstack:
					break
				else:
					continue
	elif algo==2:
		maze = [[[1 for i in xrange(4)] for j in xrange(cellsy)] for k in xrange(cellsx)]
		walls = range((cellsx*2-1)*cellsy-cellsx)
		set2cell = {r*cellsx+c:[(c,r)] for c in xrange(cellsx) for r in xrange(cellsy)}
		cell2set = {(c,r):r*cellsx+c for c in xrange(cellsx) for r in xrange(cellsy)}
		poss_moves = [(0,-1),(1,0),(0,1),(-1,0)]
		while len(set2cell.keys())>1:
			rand_wall=walls.pop(random.randint(0,len(walls)-1))
			row = rand_wall//(cellsx*2-1)
			col = (rand_wall%(cellsx*2-1))//(1 if (row==(cellsy-1)) else 2)
			wall = (rand_wall%(cellsx*2-1))%(1 if (row==(cellsy-1)) else 2)+1+(col==(cellsx-1))
			row2 = row + poss_moves[wall][1]
			col2 = col + poss_moves[wall][0]
			new_set = cell2set[(col,row)]
			if new_set != cell2set[(col2,row2)]:
				old_set = cell2set[(col2,row2)]
				set2cell[new_set]+=set2cell.pop(old_set)
				for cell in set2cell[new_set]:
					cell2set[cell] = new_set
				maze[col][row][wall] = 0
				maze[col2][row2][(wall+2)%4] = 0
	return maze


def draw_cell(screen, color, upperleft, cellsize, wall_array):
	for n in xrange(len(wall_array)):
		if wall_array[n]>0:
			x1 = upperleft[0] + (n%3 > 0)*cellsize
			x2 = upperleft[0] + (n < 2)*cellsize
			y1 = upperleft[1] + (n > 1)*cellsize
			y2 = upperleft[1] + (n%3 > 0)*cellsize
			pygame.draw.line(screen,color, (x1,y1), (x2,y2))

def advance_solve_maze(size, cellsize, solve_algo, maze, path, spath, sobj = {}):
	cellsx = size[0]//cellsize
	cellsy = size[1]//cellsize
	last_point = (path[-1][0]-(cellsize//2))/cellsize, (path[-1][1]-(cellsize//2))/cellsize
	poss_moves = [(0,-1),(1,0),(0,1),(-1,0)]
	if solve_algo == 0:
		#depth-first solve
		for move in xrange(len(poss_moves)):
			if maze[last_point[0]][last_point[1]][move]==0:
				maze[last_point[0]][last_point[1]][move] = -1
				next_col = last_point[0]+poss_moves[move][0]
				next_row = last_point[1]+poss_moves[move][1]
				maze[next_col][next_row][(move+2)%4] = -1
				test_move = next_col,next_row
				test_move_c = (test_move[0]*cellsize+(cellsize//2)),(test_move[1]*cellsize+(cellsize//2))
				path.append(test_move_c)
				spath.append(test_move_c)
				if test_move != (cellsx-1,cellsy-1):
					return False
				else:
					return True
		spath.pop()
		path2 = []
		for ind in xrange(-2,-len(path)-1,-1):
			path2.append((path[ind][0],path[ind][1]))
			point = (path[ind][0]-(cellsize//2))/cellsize, (path[ind][1]-(cellsize//2))/cellsize
			for move in xrange(len(poss_moves)):
				if maze[point[0]][point[1]][move]==0:
					test_move = (point[0]+poss_moves[move][0]),(point[1]+poss_moves[move][1])
					test_move_c = (test_move[0]*cellsize+(cellsize//2)),(test_move[1]*cellsize+(cellsize//2))
					path+=path2
					path.append(test_move_c)
					spath.append(test_move_c)
					if test_move != (cellsx-1,cellsy-1):
						return False
					else:
						return True
			if path[ind] == spath[-1]:
				spath.pop()
	elif solve_algo == 1:
		#A*
		#h_x = lambda p: cellsx+cellsy-2-p[1]-p[0]
		h_x = lambda p: ((cellsx-1-p[0])**2+(cellsy-1-p[1])**2)**0.5
		f_x = lambda p: sobj["priorityQ"][p]["g"]+sobj["priorityQ"][p]["h"]
		if sobj=={}:
			sobj["cameFrom"] = {}
			sobj["priorityQ"] = {last_point:{"g":0,"h":h_x(last_point),"use":False}}
		cf = sobj["cameFrom"]
		pq = sobj["priorityQ"]
		for move in xrange(len(poss_moves)):
			if maze[last_point[0]][last_point[1]][move]==0:
				next_col = last_point[0]+poss_moves[move][0]
				next_row = last_point[1]+poss_moves[move][1]
				next_point = next_col,next_row
				if not pq.has_key(next_point):
					cf[next_point]=last_point
					pq[next_point]={"g":1+pq[last_point]["g"],"h":h_x(next_point),"use":True}
		smallestf = {"p":next_point,"f":f_x(next_point)}
		for node in pq:
			if pq[node]["use"] and f_x(node)<smallestf["f"] or (not pq[smallestf["p"]]["use"]):
				smallestf = {"p":node,"f":f_x(node)}
		pq[smallestf["p"]]["use"]=False
		path2 = []
		while cf[smallestf["p"]] != last_point:
			last_point_c = path[-1-len(path2)]
			last_point = (last_point_c[0]-(cellsize//2))/cellsize, (last_point_c[1]-(cellsize//2))/cellsize
			path2.append(last_point_c)
			
		path+=path2
		smallestfp_c = smallestf["p"][0]*cellsize+(cellsize//2),smallestf["p"][1]*cellsize+(cellsize//2)
		path.append(smallestfp_c)
		if smallestf["p"]!=(cellsx-1,cellsy-1):
			return False
		else:
			p = smallestf["p"]
			p_c = smallestfp_c
			spath2 = [p_c]
			while cf[p] != (0,0):
				p = cf[p]
				p_c = p[0]*cellsize+(cellsize//2),p[1]*cellsize+(cellsize//2)
				spath2 = [p_c] + spath2
			spath += spath2
			return True

	return False

def run_gui():
	algo=input("Choose a maze generation algorithm: ")
	pygame.init()
	clock = pygame.time.Clock()

	size = width, height = 600, 800
	cellsize = 25
	black = 0, 0, 0
	white = 255, 255, 255
	red = 255, 0, 0
	green = 0, 255, 0

	maze = make_maze(size,cellsize,algo)
	path = [(cellsize//2,cellsize//2)]
	spath = [(cellsize//2,cellsize//2)]

	screen = pygame.display.set_mode(size)
	running = True
	solver = False
	solved = False
	while running:
		clock.tick(100)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		screen.fill(white)
		for col in xrange(len(maze)):
			for row in xrange(len(maze[col])):
				draw_cell(screen,black,(col*cellsize,row*cellsize),cellsize,maze[col][row])
		if len(path)>1:
			pygame.draw.lines(screen,red,False,path)
		if solved:
			pygame.draw.lines(screen,green,False,spath)
		pygame.display.flip()
		if not solver:
			solve_algo = input("Choose a maze solving algorithm: ")
			solver = True
		elif not solved:
			solved = advance_solve_maze(size, cellsize, solve_algo, maze, path, spath)

if __name__=="__main__":
	random.seed()
	run_gui()