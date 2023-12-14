import tkinter as tk
import copy
from time import sleep
import json
import os
import customtkinter as ctk
from BFS import *
from DFS import *
from tkinter import ttk

class GridApp:
    """
    This class represents a grid application with a GUI. It allows the user to create a grid of a specified size,
    add walls, set a start point, set a goal point, and create a maze. The grid can be interacted with using the mouse.
    """
    def __init__(self, root):
        """
        Initializes the grid application with a root window and default settings.
        """
        self.zoom_level = 1.0
        self.agent_square = None
        self.Goal_square = None
        
        # Initialize the root window
        self.root = root
        self.root.configure(bg='#87CEFA')  # Set background color
        self.root.title("Interactive Grid")  # Set window title

        # Initialize variables for grid dimensions
        self.width_var = tk.StringVar()
        self.height_var = tk.StringVar()

        
        # Set default grid dimensions
        self.width_var.set("5")
        self.height_var.set("5")

        # Create the main frame
        self.main_frame = ctk.CTkFrame(master=self.root)
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Create the left frame
        self.left_frame = ctk.CTkFrame(master=self.main_frame)
        self.left_frame.pack(side='left', fill='y', padx=20, pady=20)

        # Create a frame for the canvas and scrollbars
        self.canvas_frame = ctk.CTkFrame(master=self.main_frame)
        self.canvas_frame.pack(side='right', fill='both', expand=True)

        # Create scrollbars
        self.v_scrollbar = tk.Scrollbar(self.canvas_frame, orient='vertical')
        self.v_scrollbar.pack(side='right', fill='y')

        self.h_scrollbar = tk.Scrollbar(self.canvas_frame, orient='horizontal')
        self.h_scrollbar.pack(side='bottom', fill='x')

        # Canvas for the grid
        self.grid_canvas = tk.Canvas(master=self.canvas_frame, bg="#ADD8E6",
                                      xscrollcommand=self.h_scrollbar.set,
                                      yscrollcommand=self.v_scrollbar.set)
        self.grid_canvas.pack(side='left', fill='both', expand=True)

        # Configure the scrollbars to move the canvas
        self.h_scrollbar.config(command=self.grid_canvas.xview)
        self.v_scrollbar.config(command=self.grid_canvas.yview)


        # Label and Entry for grid width
        width_label = ctk.CTkLabel(master=self.left_frame, text="Width:")
        width_label.pack(padx=5, pady=5)

        width_entry = ctk.CTkEntry(master=self.left_frame, textvariable=self.width_var)
        width_entry.pack(padx=5, pady=5)

        # Label and Entry for grid height
        height_label = ctk.CTkLabel(master=self.left_frame, text="Height:")
        height_label.pack(padx=5, pady=5)

        height_entry = ctk.CTkEntry(master=self.left_frame, textvariable=self.height_var)
        height_entry.pack(padx=5, pady=5)

        # Button to create the grid
        create_button = ctk.CTkButton(
            master=self.left_frame, text="Create Grid", command=self.create_grid
        )
        create_button.pack(pady=10)

        # Add your 4 new buttons here
        Walls = ctk.CTkButton(master=self.left_frame, text="Walls" , command=self.walls)
        Walls.pack(pady=10)

        start = ctk.CTkButton(master=self.left_frame, text="start" , command=self.start)
        start.pack(pady=10)

        Goal = ctk.CTkButton(master=self.left_frame, text="Goal" , command=self.Goal)
        Goal.pack(pady=10)

        Create_Maze = ctk.CTkButton(master=self.left_frame, text="Create Maze"  , command=self.solving)
        Create_Maze.pack(pady=10)
        
        Print_Grid = ctk.CTkButton(master=self.left_frame, text="Print Grid", command=self.print_squares)
        Print_Grid.pack(pady=10)

        # Create a style
        style = ttk.Style()
        style.theme_use('default')  # Use the default theme as a base

        # Modify the Combobox's appearance to match the theme
        style.configure('TCombobox', 
                        selectbackground='#ADD8E6',  # Set the background color
                        selectforeground='black') 
        
        # Create the Combobox after the "Print Grid" button
        self.search_technique_var = tk.StringVar()
        self.search_technique_var.set("BFS")  # default value

        self.search_technique_label = ctk.CTkLabel(master=self.left_frame, text="Search Technique:")
        self.search_technique_label.pack(padx=5, pady=5)

        self.search_technique_combobox = ttk.Combobox(master=self.left_frame, textvariable=self.search_technique_var ,  state='readonly')
        self.search_technique_combobox['values'] = ('BFS', 'DFS', 'A*')
        self.search_technique_combobox.pack(padx=5, pady=5)

        # Initialize mode
        self.mode = "normal"
        
    def walls(self):
        """
        Sets the mode to "walls", which allows the user to add walls to the grid.
        """
        self.mode = "walls"
        
    def start(self):
        """
        Sets the mode to "start", which allows the user to set the start point on the grid.
        """
        self.mode = "start"    
        
    def Goal(self):
        """
        Sets the mode to "Goal", which allows the user to set the goal point on the grid.
        """
        self.mode = "Goal"       
    
    def create_grid(self):
        """
        Creates a grid based on the user's input for width and height.
        """
        try:
            # Delete the existing canvas
            self.grid_canvas.delete("all")

            # Reset the squares dictionary, the agent square, and the Goal square
            self.squares = {}
            self.agent_square = None
            self.Goal_square = None

            # Get the width and height from the user inputs
            width = int(self.width_var.get())
            height = int(self.height_var.get())

            # Set the canvas size based on the grid dimensions
            canvas_width = width * 30
            canvas_height = height * 30
            self.grid_canvas.configure(width=canvas_width, height=canvas_height)

            # Dictionary to store the squares
            self.squares = {}
            #self.squares.clear()
            # Draw the grid of squares
            for row in range(height):
                for col in range(width):
                    x1, y1 = col * 30, row * 30
                    x2, y2 = x1 + 30, y1 + 30

                    color = "#ADD8E6"
                    # Create rectangle with custom options
                    rectangle = self.grid_canvas.create_rectangle(
                        x1, y1, x2, y2, fill=color, outline="black", width=2
                    )

                    # Add the square to the dictionary
                    self.squares[(row, col)] = { "rectangle": rectangle , "type":"empty" , "N": True  , "S":True , "W":True , "E":True} 

            # Create event listeners for the squares
            self.create_event_listeners()
            self.update_scroll_region()

        except ValueError:
            return
        
    def print_squares(self):
        """
        Prints the squares in the grid.
        """
        for key, value in self.squares.items():
            print(f"{key}: {value}\n")            
            
    def update_scroll_region(self):
        """
        Updates the scroll region of the canvas to include all items.
        """
        self.grid_canvas.update_idletasks()
        self.grid_canvas.config(scrollregion=self.grid_canvas.bbox('all'))   

    def solving(self):
        self.Maze_Creation()
        self.maze = self.get_maze()
        self.start = copy.deepcopy(self.agent_square)
        self.cell = copy.deepcopy(self.Goal_square)
        self._solving_step()
    
    def Draw_visited(self ):
        if self.x+1 >= len(self.Draw):
            self.Draw_path()
            return
        else:
            self.x+=1
            self.update_maze(  "visited" , self.Draw[self.x])
            self.root.after(20, self.Draw_visited)
    
    def Draw_path(self):
        if self.cell != self.agent_square:
            self.cell = self.Path[self.cell]
            if self.cell != self.agent_square:
                self.grid_canvas.itemconfig(self.squares[self.cell]["rectangle"], fill="black", outline="white", width=2)
                self.squares[self.cell]["type"]="path"    
                self.root.after(20, self.Draw_path)
            
    def _solving_step(self):
            
            current_value = self.search_technique_combobox.get()
            
            if current_value == 'BFS':
                self.Path , self.Draw = BFS(self.maze , self.start , self.Goal_square)
                self.x=0
                self.Draw_visited()
                
            
            if current_value == 'DFS':
                self.Path , self.Draw = DFS(self.maze , self.start , self.Goal_square)
                self.x=0
                self.Draw_visited()
          
    def Maze_Creation(self):
    
    #Creates a maze by checking the surrounding squares of each square in the grid.
    
        for (x, y), square in self.squares.items():
                # Check right square
                if not((x, y+1) in self.squares) or self.squares[(x, y+1)]["type"] == "wall":
                    square["E"] = False
                # Check left square
                if not((x, y-1) in self.squares) or self.squares[(x, y-1)]["type"] == "wall":
                    square["W"] = False
                # Check down square
                if not((x+1, y) in self.squares) or self.squares[(x+1, y)]["type"] == "wall":
                    square["S"] = False
                # Check up square
                if not((x-1, y) in self.squares) or self.squares[(x-1, y)]["type"] == "wall":
                    square["N"] = False

    def get_maze(self):
        self.Maze_copy = copy.deepcopy(self.squares)
        for key in self.Maze_copy:
            self.Maze_copy[key].pop("rectangle", None)
            self.Maze_copy[key].pop("type", None)
        return self.Maze_copy

    def update_maze(self, type, selected):
        if selected != self.agent_square and selected != self.Goal_square:
            self.grid_canvas.itemconfig(self.squares[selected]["rectangle"], fill="#FFFF00", outline="black", width=2)
            self.squares[selected]["type"]=type
        
    def create_event_listeners(self):
        """
        Creates event listeners for each square in the grid.
        """
        # Iterate over all squares
        for (x1, y1), square in self.squares.items():
            # Hover effect
            def on_enter(x, y):
                if self.squares[(x, y)]["type"] == "empty":
                    self.grid_canvas.itemconfig(self.squares[(x, y)]["rectangle"], fill="#B0E0E6", outline="#000", width=3)

            def on_leave(x, y):
                if self.squares[(x, y)]["type"] == "empty":
                    self.grid_canvas.itemconfig(self.squares[(x, y)]["rectangle"], fill ="#ADD8E6", outline="black", width=2)

            def on_click(x, y):
                if self.mode == "walls" and self.squares[(x, y)]["type"] == "empty":
                    self.grid_canvas.itemconfig(self.squares[(x, y)]["rectangle"], fill="dark blue")
                    self.squares[(x, y)]["type"] = "wall"
                if self.mode == "start" and self.squares[(x, y)]["type"] == "empty":
                    if self.agent_square:
                        # Reset the previous agent square
                        self.grid_canvas.itemconfig(self.squares[self.agent_square]["rectangle"], fill="#ADD8E6")
                        self.squares[self.agent_square]["type"] = "empty"
                    # Set the new agent square
                    self.grid_canvas.itemconfig(self.squares[(x, y)]["rectangle"], fill="green")
                    self.squares[(x, y)]["type"] = "agent"
                    self.agent_square = (x, y)
                    
                if self.mode == "Goal" and self.squares[(x, y)]["type"] == "empty" :
                    if self.Goal_square:
                        # Reset the previous Goal square
                        self.grid_canvas.itemconfig(self.squares[self.Goal_square]["rectangle"], fill="#ADD8E6")
                        self.squares[self.Goal_square]["type"] = "empty"
                    # Set the new Goal square
                    self.grid_canvas.itemconfig(self.squares[(x, y)]["rectangle"], fill="red")
                    self.squares[(x, y)]["type"] = "Goal"
                    self.Goal_square = (x, y)

            def create_callback(func, x, y):
                return lambda event: func(x, y)

            # Bind mouse events to the rectangle
            self.grid_canvas.tag_bind(square["rectangle"], "<Button-1>", create_callback(on_click, x1, y1))
            self.grid_canvas.tag_bind(square["rectangle"], "<Enter>", create_callback(on_enter, x1, y1))
            self.grid_canvas.tag_bind(square["rectangle"], "<Leave>", create_callback(on_leave, x1, y1))

        # Bind the on_drag function to the entire canvas
        self.grid_canvas.bind("<B1-Motion>", self.on_drag)
        
    def on_drag(self, event):
        """
        Handles the event when the user drags the mouse over the grid.
        """
        # Get the current scroll position
        x_scroll_pos = self.grid_canvas.canvasx(event.x)
        y_scroll_pos = self.grid_canvas.canvasy(event.y)

        # Calculate the grid coordinates of the square under the mouse
        x = int((x_scroll_pos) // (30))
        y = int((y_scroll_pos) // (30))

        # Check if the coordinates are valid
        if (x, y) in self.squares:
            if self.mode == "walls":
                self.grid_canvas.itemconfig(self.squares[(y, x)]["rectangle"], fill="dark blue")
                self.squares[(y, x)]["type"] = "wall"
