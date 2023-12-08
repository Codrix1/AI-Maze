import tkinter as tk
import customtkinter as ctk

class GridApp:
    def __init__(self, root):
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

        # Bind the mousewheel scroll event
        self.root.bind("<Control-MouseWheel>", self.zoom)

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
        Walls = ctk.CTkButton(master=self.left_frame, text="Walls")
        Walls.pack(pady=10)

        start = ctk.CTkButton(master=self.left_frame, text="start")
        start.pack(pady=10)

        Goal = ctk.CTkButton(master=self.left_frame, text="Goal")
        Goal.pack(pady=10)

        Create_Maze = ctk.CTkButton(master=self.left_frame, text="Create Maze")
        Create Maze.pack(pady=10)

    def create_grid(self):
        try:
            # Delete the existing canvas
            self.grid_canvas.delete("all")

            # Get the width and height from the user inputs
            width = int(self.width_var.get())
            height = int(self.height_var.get())

            # Set the canvas size based on the grid dimensions
            canvas_width = width * 30
            canvas_height = height * 30
            self.grid_canvas.configure(width=canvas_width, height=canvas_height)

            # Dictionary to store the squares
            self.squares = {}

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
                    self.squares[(row, col)] = {"Xpos": row, "Ypos": col, "rectangle": rectangle, "color": color , "type":"empty"} 

            # Create event listeners for the squares
            self.create_event_listeners()
            self.update_scroll_region()

        except ValueError:
            return
        
    def update_scroll_region(self):
        self.grid_canvas.update_idletasks()
        self.grid_canvas.config(scrollregion=self.grid_canvas.bbox('all'))   
         
    def zoom(self, event):
    # Zoom in and out when the ctrl key and mouse wheel are used
        scale = 1.0
        if event.delta > 0:
            # Zoom in
            scale += 0.1
        elif event.delta < 0:
            # Zoom out
            scale -= 0.1
            
            
    def zoom(self, event):
    # Zoom in and out when the ctrl key and mouse wheel are used
        scale = 1.0
        if event.delta > 0:
            # Zoom in
            scale += 0.1
        elif event.delta < 0:
            # Zoom out
            scale -= 0.1

    # Scale the canvas
        self.grid_canvas.scale("all", 0, 0, scale, scale)
        self.update_scroll_region()    
        
            
    def create_event_listeners(self):
        # Iterate over all squares
        for (x1, y1), square in self.squares.items():
            # Hover effect
            def on_enter(event, rectangle=square["rectangle"], color=square["color"]):
                self.grid_canvas.itemconfig(rectangle, fill="#B0E0E6", outline="#000", width=3)
                self.squares[(x1, y1)]["state"] = "hover"

            def on_leave(event, rectangle=square["rectangle"], color=square["color"]):
                self.grid_canvas.itemconfig(rectangle, fill=color, outline="black", width=2)
                self.squares[(x1, y1)]["state"] = "normal"

            def on_click(event, x=x1, y=y1):  # capture current values of x1 and y1
                print(f"Square clicked at grid coordinates ({x},{y})")
                self.squares[(x, y)]["state"] = "clicked"

            # Bind mouse events to the rectangle
            self.grid_canvas.tag_bind(square["rectangle"], "<Enter>", on_enter)
            self.grid_canvas.tag_bind(square["rectangle"], "<Leave>", on_leave)
            self.grid_canvas.tag_bind(square["rectangle"], "<Button-1>", on_click)

if __name__ == "__main__":
    root = tk.Tk()
    app = GridApp(root)
    root.mainloop()  # Start the application's main loop
