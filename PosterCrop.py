from PIL import Image, ImageTk
import os
import logging
from tkinter import Tk, Button, Checkbutton, IntVar, Label, filedialog, messagebox, ttk

# Set up logging
logging.basicConfig(filename="log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

def crop_image(input_path, output_path, center_x, center_y, width, height):
    """
    Crop an image based on the center coordinates and desired width/height.
    """
    try:
        # Open the image
        img = Image.open(input_path)
        
        # Calculate the left, top, right, and bottom coordinates for cropping
        left = center_x - (width // 2)
        top = center_y - (height // 2)
        right = center_x + (width // 2)
        bottom = center_y + (height // 2)
        
        # Crop the image
        cropped_img = img.crop((left, top, right, bottom))
        
        # Save the cropped image
        cropped_img.save(output_path)
        logging.info(f"Success: Cropped image saved as {output_path}")
        return True
    except Exception as e:
        logging.error(f"Error: {e}")
        messagebox.showerror("Error", str(e))
        return False

def choose_input_image():
    """
    Let the user choose the input image and validate its size.
    """
    global input_image
    input_image = filedialog.askopenfilename(
        title="Select the input image",
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
    )
    
    if not input_image:
        messagebox.showerror("Error", "No input image selected.")
        return
    
    # Validate input image dimensions
    img = Image.open(input_image)
    if img.size != (1024, 1024):
        messagebox.showerror("Error", f"The input image must be 1024x1024 pixels. Your image size is {img.size}.")
        return
    
    # Enable the "Choose Output Folder" button
    output_folder_button.config(state="normal")
    input_status_label.config(text=f"Selected: {os.path.basename(input_image)}", fg="green")

def choose_output_folder():
    """
    Let the user choose the output folder.
    """
    global output_folder
    output_folder = filedialog.askdirectory(title="Select the output folder")
    
    if not output_folder:
        messagebox.showerror("Error", "No output folder selected.")
        return
    
    # Enable the "Start Cropping" button
    start_cropping_button.config(state="normal")
    output_status_label.config(text=f"Selected: {output_folder}", fg="green")

def start_cropping():
    """
    Start the cropping process based on user selections.
    """
    # Get the selected posters
    selected_posters = [i for i, var in enumerate(poster_vars, start=1) if var.get() == 1]
    
    if not selected_posters:
        messagebox.showerror("Error", "No posters selected.")
        return
    
    # Define the cropping parameters (fixed for all crops)
    crops = {
        1: {"output_name": "Poster1.png", "center_x": 778, "center_y": 180, "width": 274, "height": 243},
        2: {"output_name": "Poster2.png", "center_x": 390, "center_y": 802, "width": 411, "height": 364},
        3: {"output_name": "Poster3.png", "center_x": 489, "center_y": 280, "width": 285, "height": 559},
        4: {"output_name": "Poster4.png", "center_x": 171, "center_y": 280, "width": 341, "height": 559},
        5: {"output_name": "Poster5.png", "center_x": 818, "center_y": 656, "width": 372, "height": 672},
    }
    
    # Create a progress window
    progress_root = Tk()
    progress_root.title("Cropping Progress")
    progress = ttk.Progressbar(progress_root, orient="horizontal", length=300, mode="determinate")
    progress.pack(pady=20)
    progress_root.update()

    # Perform the cropping automatically
    total_crops = len(selected_posters)
    for i, poster_num in enumerate(selected_posters):
        crop = crops[poster_num]
        output_path = os.path.join(output_folder, crop["output_name"])
        success = crop_image(
            input_image,
            output_path,
            crop["center_x"],
            crop["center_y"],
            crop["width"],
            crop["height"]
        )
        
        if not success:
            progress_root.destroy()
            return
        
        # Update progress
        progress["value"] = (i + 1) / total_crops * 100
        progress_root.update()

    # Close the progress window
    progress_root.destroy()
    messagebox.showinfo("Success", "All selected crops completed successfully!")

# Create the main window
root = Tk()
root.title("LethalPosters to CustomPosters")
root.geometry("550x500")  # Increased window size

# Add a label for input image selection
Label(root, text="Step 1: Choose a poster png file to crop from LethalPosters", fg="blue").pack(pady=10)

# Add a button to choose the input image
Button(root, text="Choose .png file to crop", command=choose_input_image).pack(pady=5)

# Add a label to show the selected input image
input_status_label = Label(root, text="No file selected", fg="red")
input_status_label.pack(pady=5)

# Add a label for output folder selection
Label(root, text="Step 2: Choose the folder where cropped files should be saved", fg="blue").pack(pady=10)

# Add a button to choose the output folder (initially disabled)
output_folder_button = Button(root, text="Choose Output Folder", command=choose_output_folder, state="disabled")
output_folder_button.pack(pady=5)

# Add a label to show the selected output folder
output_status_label = Label(root, text="No folder selected", fg="red")
output_status_label.pack(pady=5)

# Add checkboxes for poster selection
Label(root, text="Step 3: Select posters to crop", fg="blue").pack(pady=10)
poster_vars = []
for i in range(1, 6):
    var = IntVar()
    Checkbutton(root, text=f"Poster {i}", variable=var).pack(anchor="w")
    poster_vars.append(var)

# Add a "Select All" checkbox
select_all_var = IntVar()
def toggle_select_all():
    for var in poster_vars:
        var.set(select_all_var.get())
Checkbutton(root, text="Select All", variable=select_all_var, command=toggle_select_all).pack(anchor="w")

# Add a "Start Cropping" button (initially disabled)
start_cropping_button = Button(root, text="Start Cropping", command=start_cropping, state="disabled")
start_cropping_button.pack(pady=20)

# Run the main loop
root.mainloop()