import customtkinter as ctk
import random


class GridApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grid of Squares")

        # Initialize variables for grid dimensions, zoom factor, and slider value
        self.width_var = ctk.StringVar()
        self.height_var = ctk.StringVar()
        self.zoom_factor = 1.0

        # Set default grid dimensions
        self.width_var.set("5")
        self.height_var.set("5")

        # Create the main frame
        self.main_frame = ctk.CTkFrame(master=self.root)
        self.main_frame.pack(padx=20, pady=20)

        # Canvas for the grid
        self.grid_canvas = ctk.CTkCanvas(master=self.root)
        self.grid_canvas.pack(padx=20, pady=20)

        # Label and Entry for grid width
        width_label = ctk.CTkLabel(master=self.main_frame, text="Width:")
        width_label.pack(padx=5, pady=5)

        width_entry = ctk.CTkEntry(master=self.main_frame, textvariable=self.width_var)
        width_entry.pack(padx=5, pady=5)

        # Label and Entry for grid height
        height_label = ctk.CTkLabel(master=self.main_frame, text="Height:")
        height_label.pack(padx=5, pady=5)

        height_entry = ctk.CTkEntry(master=self.main_frame, textvariable=self.height_var)
        height_entry.pack(padx=5, pady=5)


        # Button to create the grid
        create_button = ctk.CTkButton(
            master=self.main_frame, text="Create Grid", command=self.create_grid
        )
        create_button.pack(pady=10)

    def validate_input(self, new_text):
        return new_text.isdigit() or new_text == ""

    
    def create_grid(self):
        try:
            # Delete the existing canvas
            self.grid_canvas.delete("all")

            width = int(self.width_var.get())
            height = int(self.height_var.get())

            # Set the canvas size based on the grid dimensions and zoom factor
            canvas_width = int(width * 30 * self.zoom_factor)
            canvas_height = int(height * 30 * self.zoom_factor)
            self.grid_canvas.configure(width=canvas_width, height=canvas_height)

            # Draw the grid of squares with color variations and hover effects
            for row in range(height):
                for col in range(width):
                    x1, y1 = col * 30 * self.zoom_factor, row * 30 * self.zoom_factor
                    x2, y2 = x1 + 30 * self.zoom_factor, y1 + 30 * self.zoom_factor

                    
                    color = "#f5f5f5"
                    # Create rectangle with custom options and event bindings
                    rectangle = self.grid_canvas.create_rectangle(
                        x1, y1, x2, y2, fill=color, outline="black", width=2
                    )

                    # Hover effect
                    def on_enter(event):
                        self.grid_canvas.itemconfig(rectangle, fill="#eee", outline="#000", width=3)

                    def on_leave(event):
                        self.grid_canvas.itemconfig(rectangle, fill=color, outline="black", width=2
                    )
                    def on_click(event):
                        print(f"Square clicked at ({x1},{y1})")

                    self.grid_canvas.tag_bind(rectangle, "<Button-1>", on_click)

                    # Bind mouse events to the rectangle
                    self.grid_canvas.tag_bind(rectangle, "<Enter>", on_enter)
                    self.grid_canvas.tag_bind(rectangle, "<Leave>", on_leave)

        except ValueError:
            return

    def update_zoom_ui(self):
        # Update zoom factor based on the slider's value
        self.create_grid()


if __name__ == "__main__":
    root = ctk.CTk()
    app = GridApp(root)
    root.mainloop()