from tkinter import (
    Tk,
    Canvas,
    Label,
    Button,
    Frame,
    filedialog,
    Toplevel,
    Scale,
    HORIZONTAL,
    NW,
)
import cv2
from PIL import Image, ImageTk


class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing Software")
        self.root.configure(
            bg="lightgray"
        )  # Set the background color of the main window

        # Variables to store the original and processed images
        self.original_image = None
        self.processed_image = None

        # Frame to organize the buttons
        button_frame = Frame(root, bg="lightgray")
        button_frame.grid(row=0, column=0, columnspan=2, pady=10)

        # Button to load the image
        self.load_button = Button(
            button_frame, text="Load Image", command=self.load_image, bg="white"
        )
        self.load_button.grid(row=0, column=0, padx=5)

        # Button to convert to grayscale
        self.grayscale_button = Button(
            button_frame,
            text="Convert to Grayscale",
            command=self.convert_to_grayscale,
            bg="white",
        )
        self.grayscale_button.grid(row=0, column=1, padx=5)

        # Button to apply filter
        self.filter_button = Button(
            button_frame, text="Apply Filter", command=self.apply_filter, bg="white"
        )
        self.filter_button.grid(row=0, column=2, padx=5)

        # Button to adjust brightness/contrast
        self.contrast_button = Button(
            button_frame,
            text="Adjust Brightness/Contrast",
            command=self.adjust_contrast,
            bg="white",
        )
        self.contrast_button.grid(row=0, column=3, padx=5)

        # Area to display the loaded image
        self.original_canvas = Canvas(root, width=300, height=400, bg="white")
        self.original_canvas.grid(row=1, column=0, padx=10, pady=10)

        # Area to display the processed image
        self.processed_canvas = Canvas(root, width=300, height=400, bg="white")
        self.processed_canvas.grid(row=1, column=1, padx=10, pady=10)

        # Label to display image information
        self.info_label = Label(root, text="", bg="lightgray")
        self.info_label.grid(row=2, column=0, columnspan=2, pady=10)

    def load_image(self):
        """Load an image from the file system and resize it."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if file_path:
            self.original_image = cv2.imread(file_path)
            self.original_image = self.resize_image(
                self.original_image, 0.3
            )  # Resize the image to 30%
            self.display_image(self.original_image, self.original_canvas)
            self.display_image_info(self.original_image)

    def display_image(self, image, canvas):
        """Display the image on a Tkinter Canvas."""
        # Convert the image to RGB and then to the format compatible with Tkinter
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_tk = ImageTk.PhotoImage(image_pil)
        canvas.create_image(0, 0, anchor=NW, image=image_tk)
        canvas.image = image_tk  # Store the reference to avoid garbage collection

    def display_image_info(self, image):
        """Display basic information about the image."""
        height, width, channels = image.shape
        info_text = f"Dimensions: {width}x{height}, Channels: {channels}"
        self.info_label.config(text=info_text)

    def convert_to_grayscale(self):
        """Convert the image to grayscale."""
        if self.original_image is not None:
            gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            self.processed_image = gray_image
            self.display_image(
                cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR), self.processed_canvas
            )

    def apply_filter(self):
        """Apply spatial filters to the image."""
        if self.original_image is not None:
            # Example of a mean filter
            filtered_image = cv2.GaussianBlur(self.original_image, (15, 15), 0)
            self.processed_image = filtered_image
            self.display_image(filtered_image, self.processed_canvas)

    def adjust_contrast(self):
        """Adjust the brightness and contrast of the image."""
        if self.original_image is not None:
            # Open a new window to adjust brightness/contrast
            window = Toplevel(self.root)
            window.title("Brightness/Contrast Adjustment")
            window.configure(bg="lightgray")  # Set the background color of the new window

            def update(val):
                """Callback function to update brightness and contrast."""
                alpha = contrast_slider.get() / 100
                beta = brightness_slider.get() - 50
                adjusted_image = cv2.convertScaleAbs(
                    self.original_image, alpha=alpha, beta=beta
                )
                self.display_image(adjusted_image, self.processed_canvas)

            contrast_slider = Scale(
                window,
                from_=0,
                to=100,
                orient=HORIZONTAL,
                label="Contrast",
                command=update,
                bg="lightgray",
            )
            contrast_slider.set(50)
            contrast_slider.pack(pady=5)

            brightness_slider = Scale(
                window,
                from_=0,
                to=100,
                orient=HORIZONTAL,
                label="Brightness",
                command=update,
                bg="lightgray",
            )
            brightness_slider.set(50)
            brightness_slider.pack(pady=5)

    def resize_image(self, image, scale):
        """Resize the image to a smaller version."""
        width = int(image.shape[1] * scale)
        height = int(image.shape[0] * scale)
        dim = (width, height)
        resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        return resized_image


if __name__ == "__main__":
    root = Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
