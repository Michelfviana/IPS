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
    Entry,
)
import cv2
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")
        self.root.configure(bg="lightgray")

        # Create a frame for the buttons
        button_frame = Frame(self.root, bg="lightgray")
        button_frame.pack(side="left", fill="y")

        # Add buttons for each functionality
        Button(button_frame, text="Load Image", command=self.load_image).pack(pady=5)
        Button(button_frame, text="Convert to Grayscale", command=self.convert_to_grayscale).pack(pady=5)
        Button(button_frame, text="Apply Filter", command=self.apply_filter).pack(pady=5)
        Button(button_frame, text="Adjust Contrast", command=self.adjust_contrast).pack(pady=5)
        Button(button_frame, text="Morphological Operations", command=self.morphological_operations).pack(pady=5)
        Button(button_frame, text="Segment and Find Contours", command=self.segment_and_find_contours).pack(pady=5)
        Button(button_frame, text="Apply Custom Filter", command=self.apply_custom_filter).pack(pady=5)
        Button(button_frame, text="Display Histogram", command=self.display_histogram).pack(pady=5)

        # Create canvases for displaying images
        self.original_canvas = Canvas(self.root, width=400, height=400, bg="white")
        self.original_canvas.pack(side="left", padx=10, pady=10)
        self.processed_canvas = Canvas(self.root, width=400, height=400, bg="white")
        self.processed_canvas.pack(side="left", padx=10, pady=10)

        # Label to display image information
        self.info_label = Label(self.root, text="", bg="lightgray")
        self.info_label.pack(pady=5)

        self.original_image = None
        self.processed_image = None

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

    def apply_morphological_operation(self, operation, kernel_size):
        """Apply morphological operations like erosion, dilation, etc."""
        if self.original_image is not None:
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
            if operation == 'erosion':
                processed_image = cv2.erode(self.original_image, kernel)
            elif operation == 'dilation':
                processed_image = cv2.dilate(self.original_image, kernel)
            elif operation == 'opening':
                processed_image = cv2.morphologyEx(self.original_image, cv2.MORPH_OPEN, kernel)
            elif operation == 'closing':
                processed_image = cv2.morphologyEx(self.original_image, cv2.MORPH_CLOSE, kernel)
            elif operation == 'gradient':
                processed_image = cv2.morphologyEx(self.original_image, cv2.MORPH_GRADIENT, kernel)
            self.display_image(processed_image, self.processed_canvas)

    def morphological_operations(self):
        """Open a new window to apply morphological operations."""
        if self.original_image is not None:
            window = Toplevel(self.root)
            window.title("Morphological Operations")
            window.configure(bg="lightgray")

            def apply_operation(operation):
                kernel_size = int(kernel_size_slider.get())
                self.apply_morphological_operation(operation, kernel_size)

            kernel_size_slider = Scale(window, from_=1, to=10, orient=HORIZONTAL, label="Kernel Size", bg="lightgray")
            kernel_size_slider.set(3)
            kernel_size_slider.pack(pady=5)

            Button(window, text="Erosion", command=lambda: apply_operation('erosion')).pack(pady=5)
            Button(window, text="Dilation", command=lambda: apply_operation('dilation')).pack(pady=5)
            Button(window, text="Opening", command=lambda: apply_operation('opening')).pack(pady=5)
            Button(window, text="Closing", command=lambda: apply_operation('closing')).pack(pady=5)
            Button(window, text="Gradient", command=lambda: apply_operation('gradient')).pack(pady=5)

    def segment_and_find_contours(self):
        """Segment the image and find contours."""
        if self.original_image is not None:
            window = Toplevel(self.root)
            window.title("Segment and Find Contours")
            window.configure(bg="lightgray")

            def apply_segmentation():
                threshold_value = int(threshold_slider.get())
                self.segment_and_find_contours(threshold_value)

            threshold_slider = Scale(window, from_=0, to=255, orient=HORIZONTAL, label="Threshold", bg="lightgray")
            threshold_slider.set(128)
            threshold_slider.pack(pady=5)

            Button(window, text="Apply", command=apply_segmentation).pack(pady=5)

    def apply_custom_filter(self):
        """Open a new window to apply a custom filter."""
        if self.original_image is not None:
            window = Toplevel(self.root)
            window.title("Custom Filter")
            window.configure(bg="lightgray")

            def apply_filter():
                kernel = [
                    [int(entry_00.get()), int(entry_01.get()), int(entry_02.get())],
                    [int(entry_10.get()), int(entry_11.get()), int(entry_12.get())],
                    [int(entry_20.get()), int(entry_21.get()), int(entry_22.get())]
                ]
                self.apply_custom_filter(kernel)

            entries = []
            for i in range(3):
                row = []
                for j in range(3):
                    entry = Entry(window, width=5)
                    entry.grid(row=i, column=j, padx=5, pady=5)
                    row.append(entry)
                entries.append(row)

            entry_00, entry_01, entry_02 = entries[0]
            entry_10, entry_11, entry_12 = entries[1]
            entry_20, entry_21, entry_22 = entries[2]

            Button(window, text="Apply Filter", command=apply_filter).grid(row=3, columnspan=3, pady=10)

    def display_histogram(self):
        """Display the histogram of the image."""
        if self.processed_image is not None:
            for i, color in enumerate(['b', 'g', 'r']):
                histogram = cv2.calcHist([self.processed_image], [i], None, [256], [0, 256])
                plt.plot(histogram, color=color)
                plt.xlim([0, 256])
            plt.show()

    def equalize_histogram(self):
        """Equalize the histogram of the image."""
        if self.processed_image is not None:
            gray_image = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
            equalized_image = cv2.equalizeHist(gray_image)
            self.display_image(cv2.cvtColor(equalized_image, cv2.COLOR_GRAY2BGR), self.processed_canvas)

if __name__ == "__main__":
    root = Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
    