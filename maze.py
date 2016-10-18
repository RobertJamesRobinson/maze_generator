import random

#makes a maze, prints the output using ASCII characters
#uses the recursive backtracking algorithm with a while loop and a stack as opposed to actual recursion
class Maze:
    #initialiser takes width and height for the maze to be created. The visited list is a list of x,y coordinates
    def __init__(self,x,y):
        self.maze_width=x
        self.maze_height=y
        self.maze={}
        self.initialise_maze()
        
        #optimization at the expense of functionality here. We "should" be "back tracking" through the visited "list"
        #but, a list is much slower to find values in than a dict. This algorithm is search heavy in the visited list.
        #The resulting mazes are indistinguisable from us using a proper list here, performance gains on large mazes are huge, so going with a dict
        self.visited={}
        self.dead={}
        
    #takes a maze position, returns valid directions we can move to from the given position
    #take into consideration if the target position is outside the maze, or in the visited list
    #returns a list of one of four directions eg ["N","S","E","W"], assumes top left is the origin
    def get_valid_directions_from_position(self,x,y):
        #work out positions of each direction
        directions={"N":[x,y-1],"S":[x,y+1],"E":[x+1,y],"W":[x-1,y]}
        
        #eliminate the ones that are in the visited list
        for dirn in directions.keys():
            if((directions[dirn][0],directions[dirn][1]) in self.visited):
                del directions[dirn]
                    
        #eliminate the ones that are outside the maze area
        for dirn in directions.keys():
            if(directions[dirn][0]<0 or directions[dirn][0]>=self.maze_width or directions[dirn][1]<0 or directions[dirn][1]>=self.maze_height):
                del directions[dirn]
                
        return directions
        
    #initialise the maze, gives us a chance to run this again without making a new object if required
    def initialise_maze(self):
        self.maze={}
        for y in range(self.maze_height):
            for x in range(self.maze_width):
                self.maze[(x,y)]=['N','S','E','W']
        
    #add a new x,y coordinate to the visited list
    def add_to_visited(self,x,y):
        self.visited[(x,y)]=1
        
    #is the given x,y coordinate in the visited list?
    def in_visited(self,x,y):
        return (x,y) in self.visited
        
    #returns a list of the walls at the given location
    def get_maze_at_pos(self,x,y):
        return self.maze[(x,y)]
        
    #remove the wall from the perspective of the starting position, but also from the target position, 
    #the dirn should already be validated, so dont bother to validate the target position, ie, fix the walls blindly
    def remove_wall(self,x,y,dirn):
        #lookup to find position and direction name of second wall
        dir_map={'N':{'x':0,'y':-1,'opp':'S'},'S':{'x':0,'y':1,'opp':'N'},'E':{'x':1,'y':0,'opp':'W'},'W':{'x':-1,'y':0,'opp':'E'}}
        
        #remove first and second positions walls
        self.maze[(x,y)].remove(dirn)
        self.maze[(x+dir_map[dirn]['x'],y+dir_map[dirn]['y'])].remove(dir_map[dirn]['opp'])
        
    #the main part of the algorithm lives here
    def make_maze(self):
        #pick a random spot to start in, and "visit" that position
        x=random.randint(0,self.maze_width-1)
        y=random.randint(0,self.maze_height-1)
        self.add_to_visited(x,y)
        
        #start the main algorithm, stop when we've visited all the maze cells
        while(self.maze_height*self.maze_width>len(self.visited)):
            valid_directions=self.get_valid_directions_from_position(x,y)
            
            #cut away a wall and move to that position, remove the wall from the perspective of the current position
            if(len(valid_directions)>0):
                dir_to_move_to=random.choice(valid_directions.keys())
                self.remove_wall(x,y,dir_to_move_to)
                x=valid_directions[dir_to_move_to][0]
                y=valid_directions[dir_to_move_to][1]
                self.add_to_visited(x,y)
            
            #need to back track, iterate backwards over our visited list until we find a wall we can remove    
            else:
                visited_keys=self.visited.keys()
                position_in_visited=len(visited_keys)-1
                looking=True
                
                #backtrack through the visited list to find a wall into a valid wall
                while(looking and position_in_visited>=0):
                    currentNode=visited_keys[position_in_visited]
                    
                    #optimisation: we keep a list of visited nodes that are known to have 0 valid directions from it
                    while(currentNode in self.dead):
                        position_in_visited-=1
                        currentNode=visited_keys[position_in_visited]
                        
                    #get the valid directions from our previously visited node
                    valid_dirns=self.get_valid_directions_from_position(currentNode[0],currentNode[1])
                    
                    #are there valid directions from this position? or do we need to try again?
                    if len(valid_dirns)>0:
                        dir_to_move_to=random.choice(valid_dirns.keys())
                        self.remove_wall(currentNode[0],currentNode[1],dir_to_move_to)
                        x=valid_dirns[dir_to_move_to][0]
                        y=valid_dirns[dir_to_move_to][1]
                        self.add_to_visited(x,y)
                        looking=False
                    else:
                        self.dead[currentNode]=1
                        position_in_visited-=1
    
    #"pretty" print the maze after i'ts been constructed
    def pretty_print(self):
        result=""
        for y in range(self.maze_height):
            for i in range(3):
                for x in range(self.maze_width):
                    cell=self.get_maze_at_pos(x,y)
                    if i==0:
                        #top row of cells
                        if 'N' in cell:
                            result+=unichr(0x2588)*3
                        else:
                            result+=unichr(0x2588)+" "+unichr(0x2588)
                    elif i==1:
                        #middle row of cells
                        if 'W' in cell:
                            result+=unichr(0x2588)+" "
                        else:
                            result+="  "
                        if 'E' in cell:
                            result+=unichr(0x2588)
                        else:
                            result+=" "
                    elif i==2:
                        #bottom row of cells
                        if 'S' in cell:
                            result+=unichr(0x2588)*3
                        else:
                            result+=unichr(0x2588)+" "+unichr(0x2588)
                result+="\n"
        print result
        

#driver code to make an A4 page size maze using the PIL library
from PIL import Image, ImageDraw, ImageFont
from math import ceil,floor
width=60
height=int(width*0.695)
cell_width=20
cell_height=20
line_width=5
line_colour=(0,0,0)
bg_colour=(255,255,255)
start_font_colour=(0,0,0)
end_font_colour=(0,0,0)
font_size=16
hw=line_width/2
start_pos=[int(floor(width*cell_width*0.1))+hw,int(floor(height*cell_height*0.1))+hw]
end_pos=[int(floor((width-1)*cell_width*0.9))+line_width,int(floor((height-1)*cell_height*0.9))+hw/2]
m=Maze(width,height)
m.make_maze()
img=Image.new("RGB",(width*cell_width+line_width/2-1,height*cell_height+line_width/2-1),bg_colour)
font=ImageFont.truetype("/System/Library/Fonts/AppleSDGothicNeo-Bold.otf",font_size)
draw=ImageDraw.Draw(img)
draw.fontmode="1"

#draw the new image
for y in range(height):
    for x in range(width):
        cell=m.get_maze_at_pos(x,y)
        if 'N' in cell:
            p1=x*cell_width-hw,y*cell_width
            p2=x*cell_width+cell_width+hw,y*cell_width
            draw.line((p1,p2),fill=line_colour,width=line_width)
        if 'S' in cell:
            p1=x*cell_width-hw,y*cell_width+cell_width
            p2=x*cell_width+cell_width+hw,y*cell_width+cell_width
            draw.line((p1,p2),fill=line_colour,width=line_width)
        if 'E' in cell:
            p1=x*cell_width+cell_width,y*cell_width-hw
            p2=x*cell_width+cell_width,y*cell_width+cell_width+hw
            draw.line((p1,p2),fill=line_colour,width=line_width)
        if 'W' in cell:
            p1=x*cell_width,y*cell_width-hw
            p2=x*cell_width,y*cell_width+cell_width+hw
            draw.line((p1,p2),fill=line_colour,width=line_width)
draw.text(start_pos,"S",font=font,fill=start_font_colour)
draw.text(end_pos,"E",font=font,fill=end_font_colour)

img.save("output.jpg",quality=100, optimize=True)
