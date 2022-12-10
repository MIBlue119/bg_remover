import os
import tkinter as tk
from tkinter import ttk
from pathlib import Path
import glob
from tkinter import filedialog
from rembg import remove
from PIL import Image


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Background Remover")

        self.padding = 10
        self.geometry(f"700x300+{self.padding}+{self.padding}")
        self.frame_object = tk.Frame()
        self.frame_object.pack(fill=tk.BOTH, expand=True)
        # Create a variable that will store the selected directory path
        self.directory_path = tk.StringVar()
        # Create a variable that will store the selected file path
        self.file_path = tk.StringVar()
        # Create a variable that will store the selected mode (directory or file)
        self.mode = tk.StringVar()
        # Set the default mode to "Directory"
        self.mode.set("Directory")
        self.create_widgets()
        self.mode_changed()

    # Create a function that will be called when the user
    # changes the selected mode (directory or file)
    def mode_changed(
        self,
    ):
        # Check which mode is selected
        if self.mode.get() == "Directory":
            # If the directory mode is selected, show the directory selection
            # widgets and hide the file selection widgets
            self.directory_button.pack(
                anchor=tk.W, padx=self.padding, pady=self.padding
            )
            self.directory_label.pack(anchor=tk.W, padx=self.padding, pady=self.padding)
            self.file_button.pack_forget()
            self.file_label.pack_forget()
        elif self.mode.get() == "File":
            # If the file mode is selected, show the file selection
            # widgets and hide the directory selection widgets
            self.file_button.pack(anchor=tk.W, padx=self.padding, pady=self.padding)
            self.file_label.pack(anchor=tk.W, padx=self.padding, pady=self.padding)
            self.directory_button.pack_forget()
            self.directory_label.pack_forget()

    def create_widgets(self):
        # Creat a text label to describe the mode selection
        self.mode_label = tk.Label(self.frame_object, text="選取處理[資料夾]或是[檔案]:")
        self.mode_label.pack(anchor=tk.NW, padx=self.padding, pady=self.padding)
        self.directory_mode = tk.Radiobutton(
            self.frame_object,
            text="資料夾",
            variable=self.mode,
            value="Directory",
            command=self.mode_changed,
        )

        self.directory_mode.pack(anchor=tk.NW, padx=self.padding, pady=self.padding)
        self.file_mode = tk.Radiobutton(
            self.frame_object,
            text="檔案",
            variable=self.mode,
            value="File",
            command=self.mode_changed,
        )

        self.file_mode.pack(anchor=tk.NW, padx=self.padding, pady=self.padding)

        # Create a button that will call the select_directory() function
        # when clicked
        self.directory_button = tk.Button(
            self.frame_object, text="Select Directory", command=self.select_directory
        )

        # Add the button to the root window
        self.directory_button.pack(anchor=tk.W, padx=self.padding, pady=self.padding)
        # Create a label that will show the selected directory path
        self.directory_label = tk.Label(
            self.frame_object, textvariable=self.directory_path
        )
        self.directory_label["text"] = f"Selected directory:{self.directory_path.get()}"

        # Add the label to the root window
        self.directory_label.pack(
            anchor=tk.W, side="top", padx=self.padding, pady=self.padding
        )

        # Create a button that will call the select_file() function
        # when clicked
        self.file_button = tk.Button(
            self.frame_object, text="Select File", command=self.select_file
        )

        # Add the button to the root window
        self.file_button.pack(anchor=tk.W, padx=self.padding, pady=self.padding)

        # Create a label that will show the selected file path
        self.file_label = tk.Label(self.frame_object, textvariable=self.file_path)

        self.file_label.pack(
            anchor=tk.W, side="top", padx=self.padding, pady=self.padding
        )
        self.file_label["text"] = f"Selected file:{self.file_path.get()}"
        # Append a reset button to the root window
        # Use the reset function as the command
        self.reset_button = tk.Button(
            self.frame_object, text="Reset", command=self.reset
        )
        self.reset_button.pack(
            anchor=tk.E, side="right", padx=self.padding, pady=self.padding
        )
        self.process_button = tk.Button(
            self.frame_object, text="Process", command=self.process
        )
        self.process_button.pack(
            anchor=tk.E, side="right", padx=self.padding, pady=self.padding
        )

        # Append a process status label to the root window
        self.process_status = tk.Label(self.frame_object, text="處理進度: 等待選取檔案或資料夾")
        # Set the default process status to "Idle"
        self.process_status["text"] = "處理進度: 等待選取檔案或資料夾"
        self.process_status.pack(
            anchor=tk.SW, side="bottom", padx=self.padding, pady=self.padding
        )

        # Set a label to show the output path
        self.output_path_label = tk.Label(self.frame_object, text="輸出檔案位置:")
        self.output_path_label.pack(
            anchor=tk.SW, side="bottom", padx=self.padding, pady=self.padding
        )

    def remove_img_background(self, input_path: str, output_path: str):
        try:
            # Open the jpeg file
            image = Image.open(input_path)
            # Remove the background
            result = remove(image)
            # Save the image
            result.save(output_path, "PNG")
        except Exception as e:
            print(e)

    def remove_background(
        self, input_path: str, output_format: str = "png", process_status_callback=None
    ):
        # Check if the input path is a directory
        if os.path.isdir(input_path):
            # Get the directory name
            directory_name = Path(input_path).name
            # Create a directory to store the processed images
            output_path = os.path.join(
                Path(input_path).parent, f"{directory_name}-processed"
            )
            # Show the output path in the output path label
            self.output_path_label["text"] = f"輸出檔案位置: {output_path}"
            os.makedirs(output_path, exist_ok=True)

            # Use glob to get all the picture files in the directory
            files = glob.glob(os.path.join(input_path, "*"))
            total_files_count = len(files)
            count = 0
            # Loop through the files
            for file in files:
                count += 1
                # Check if the file is a picture file
                if file.endswith((".jpg", ".jpeg", ".png")):
                    # Get the file name
                    file_name = Path(file).stem
                    # Call the remove_img_background() function
                    self.remove_img_background(
                        file, os.path.join(output_path, f"{file_name}.{output_format}")
                    )
                    # Update the progress bar
                    if process_status_callback:
                        process_status_callback(count, total_files_count)
        # Check if the input path is a file
        elif os.path.isfile(input_path):
            # Get the file name
            file_name = Path(input_path).stem
            # Get the directory path
            directory_path = Path(input_path).parent
            output_path = os.path.join(
                directory_path, f"{file_name}_processed.{output_format}"
            )
            # Show the output path in the output path label
            self.output_path_label["text"] = f"輸出檔案位置: {output_path}"
            # Call the remove_img_background() function
            self.remove_img_background(input_path, output_path)
            # Update the progress bar
            if process_status_callback:
                process_status_callback(1, 1)

    # Create a function that will be called when the user
    # clicks on the "Select Directory" button
    def select_directory(self):
        # Use filedialog.askdirectory() to prompt the user to select a directory
        directory = filedialog.askdirectory()
        # Set the directory_path variable to the selected directory
        self.directory_path.set(directory)
        # Set the directory_path text to the selected file
        # convert the StringVar self.directory_path to a string
        dir_string = self.directory_path.get()
        self.directory_label["text"] = f"選取的資料夾: {dir_string}"

    # Create a function that will be called when the user
    # clicks on the "Select File" button
    def select_file(self):
        # Use filedialog.askopenfilename() to prompt the user to select a file
        file = filedialog.askopenfilename()
        # Set the file_path variable to the selected file
        self.file_path.set(file)
        # Set the file_path text to the selected file
        file_str = self.file_path.get()
        self.file_label["text"] = f"選取的檔案: {file_str}"

    # Create a function that will be called when the user
    # clicks on the "Process" button
    def process(self, process_status_callback=None):
        if process_status_callback is None:
            process_status_callback = self.update_process_status
        # Freeze the process button
        self.process_button["state"] = "disabled"

        # Reset the progress bar
        self.process_status["text"] = "處理進度:  0%"
        # Reset the output path label
        self.output_path_label["text"] = "輸出檔案位置:"
        # Check which mode is selected (directory or file)
        if self.mode.get() == "Directory":
            # If the directory mode is selected, get the selected directory
            directory = self.directory_path.get()
            # Check if a directory was selected
            if directory:
                # Use the remove_background() function from the rembg package
                # to remove the background from all the images in the selected directory
                # and save the processed images as PNG files
                self.remove_background(
                    directory,
                    output_format="png",
                    process_status_callback=process_status_callback,
                )
            else:
                self.process_status["text"] = f"處理進度: 沒有選擇資料夾"
        elif self.mode.get() == "File":
            # If the file mode is selected, get the selected file
            file = self.file_path.get()
            # Check if a file was selected
            if file:
                # Use the remove_background() function from the rembg package
                # to remove the background from the selected file
                # and save the processed image as a PNG file
                self.remove_background(
                    file,
                    output_format="png",
                    process_status_callback=process_status_callback,
                )
            else:
                self.process_status["text"] = f"處理進度: 沒有選擇檔案"
        # Unfreeze the process button
        self.process_button["state"] = "normal"
        # Remove the selected file or directory
        # Reset the directory path variable
        self.directory_path.set("")
        # Reset the file path variable
        self.file_path.set("")

    # Create a function that will be called by the remove_background() function
    # to update the process status
    def update_process_status(self, count, total):
        # Calculate the percentage of the progress
        percentage = count / total * 100
        # Update the process status label
        self.process_status["text"] = f"處理進度: {percentage:.2f}%"

    def reset(self):
        # Reset the progress bar
        self.process_status["text"] = "處理進度: 等待選取檔案或資料夾"
        # Reset the output path label
        self.output_path_label["text"] = "輸出檔案位置:"
        # Reset the directory path variable
        self.directory_path.set("")
        # Reset the file path variable
        self.file_path.set("")


if __name__ == "__main__":

    # Create the application
    app = App()
    # Run the application
    app.mainloop()
