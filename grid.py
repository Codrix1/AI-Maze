import tkinter as tk
import customtkinter as ctk

class GridApp:
    def __init__(self, root):
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

        Create_Maze = ctk.CTkButton(master=self.left_frame, text="Create Maze"  , command=self.Maze_Creation)
        Create_Maze.pack(pady=10)
        
        Print_Grid = ctk.CTkButton(master=self.left_frame, text="Print Grid", command=self.print_squares)
        Print_Grid.pack(pady=10)
        # Initialize mode
        self.mode = "normal"
        
    def walls(self):
        self.mode = "walls"
        
    def start(self):
        self.mode = "start"    
        
    def Goal(self):
        self.mode = "Goal"       
    
        
    def create_grid(self):
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
                    self.squares[(row, col)] = { "rectangle": rectangle , "type":"empty" , "Up": True  , "Down":True , "Left":True , "Right":True} 

            # Create event listeners for the squares
            self.create_event_listeners()
            self.update_scroll_region()

        except ValueError:
            return
        
        
    def print_squares(self):
        for key, value in self.squares.items():
            print(f"{key}: {value}\n")
    def update_scroll_region(self):
        self.grid_canvas.update_idletasks()
        self.grid_canvas.config(scrollregion=self.grid_canvas.bbox('all'))   

  
    def Maze_Creation(self):
        for (x, y), square in self.squares.items():
            if square["type"] == "empty":
                # Check right square
                if (x, y+1) in self.squares and self.squares[(x, y+1)]["type"] == "wall":
                    square["Right"] = False
                # Check left square
                if (x, y-1) in self.squares and self.squares[(x, y-1)]["type"] == "wall":
                    square["Left"] = False
                # Check down square
                if (x+1, y) in self.squares and self.squares[(x+1, y)]["type"] == "wall":
                    square["Down"] = False
                # Check up square
                if (x-1, y) in self.squares and self.squares[(x-1, y)]["type"] == "wall":
                    square["Up"] = False

    def create_event_listeners(self):
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

if __name__ == "__main__":
    root = tk.Tk()
    app = GridApp(root)
    root.mainloop()  # Start the application's main loop
