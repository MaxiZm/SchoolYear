import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg




def create_class_tab(notebook, class_name, weekly_data):
    # Create a Frame for each class
    class_frame = ttk.Frame(notebook)
    notebook.add(class_frame, text=class_name)

    # For each day of the week (assuming data is per day in a week)
    for day_index, day_data in enumerate(weekly_data):
        # Create a LabelFrame for each day inside the tab
        day_frame = ttk.LabelFrame(class_frame, text=f'Day {day_index + 1}')
        day_frame.grid(row=0, column=day_index, padx=10, pady=10, sticky="nsew")
        day_frame.columnconfigure(0, weight=1)  # Make the column within day_frame expand to fill available space

        # Populate the day's frame with subjects
        for lesson_index, lesson in enumerate(day_data):
            lesson_info = f"{lesson['subject']} - {lesson['teacher']}"
            label = ttk.Label(day_frame, text=lesson_info, wraplength=150, anchor="center")
            label.grid(row=lesson_index, column=0, sticky="ew", padx=5, pady=2)
            label.config(relief="solid", borderwidth=1)  # Add a border to make it look like a box


def generate_plot(frame, x, y):
    # Generate a simple plot with passed x and y data points
    fig, ax = plt.subplots(figsize=(5, 4))  # Adjust the figure size as needed
    ax.plot(x, y)  # Plot with line and markers
    ax.set_xlabel('Generation')
    ax.set_ylabel('Fitness')
    ax.set_title('Fitness over Gen')

    # Embed the plot in the Tkinter frame
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

def main(class_data, x, y):
    root = tk.Tk()
    root.title("Class Schedule and Fitness Viewer")
    root.geometry("1200x600")  # Adjust the window size as needed

    container = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
    container.pack(fill=tk.BOTH, expand=True)

    notebook_frame = ttk.Frame(container)
    container.add(notebook_frame, weight=1)
    notebook = ttk.Notebook(notebook_frame)
    notebook.pack(expand=True, fill="both", side=tk.LEFT)

    plot_frame = ttk.Frame(container)
    container.add(plot_frame, weight=1)

    # Assuming the creation of class tabs as before
    for class_name, weekly_data in class_data.items():
        create_class_tab(notebook, class_name, weekly_data)

    generate_plot(plot_frame, x, y)

    root.mainloop()


