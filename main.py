import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import ImageTk, Image
import numpy as np
import matplotlib.pyplot as plt

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Software de Processamento de Imagens")
        self.root.configure(bg="lightgray")

        # Frame para botões de controle
        button_frame = tk.Frame(self.root, bg="lightgray")
        button_frame.pack(side="left", fill="y")

        # Botões para cada funcionalidade
        tk.Button(button_frame, text="Carregar Imagem", command=self.load_image).pack(pady=5)
        tk.Button(button_frame, text="Converter para Tons de Cinza", command=self.convert_to_grayscale).pack(pady=5)
        tk.Button(button_frame, text="Filtros Espaciais", command=self.open_filter_window).pack(pady=5)
        tk.Button(button_frame, text="Ajuste de Contraste", command=self.adjust_contrast).pack(pady=5)
        tk.Button(button_frame, text="Operações Morfológicas", command=self.morphological_operations).pack(pady=5)
        tk.Button(button_frame, text="Segmentação e Contornos", command=self.segment_and_find_contours).pack(pady=5)
        tk.Button(button_frame, text="Filtros Personalizados", command=self.open_custom_filter_window).pack(pady=5)
        tk.Button(button_frame, text="Exibir Histograma", command=self.display_histogram).pack(pady=5)
        tk.Button(button_frame, text="Equalizar Histograma", command=self.equalize_histogram).pack(pady=5)

        # Canvas para exibição de imagens
        self.original_canvas = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.original_canvas.pack(side="left", padx=10, pady=10)
        self.processed_canvas = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.processed_canvas.pack(side="left", padx=10, pady=10)

        # Label para informações da imagem
        self.info_label = tk.Label(self.root, text="", bg="lightgray")
        self.info_label.pack(pady=5)

        self.original_image = None
        self.processed_image = None

    def load_image(self):
        """Carregar uma imagem do sistema de arquivos."""
        file_path = tk.filedialog.askopenfilename(
            filetypes=[("Arquivos de Imagem", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if file_path:
            self.original_image = cv2.imread(file_path)
            self.original_image = self.resize_image(self.original_image, 0.5)  # Redimensionar a imagem para 50%
            self.display_image(self.original_image, self.original_canvas)
            self.display_image_info(self.original_image)

    def display_image(self, image, canvas):
        """Exibir a imagem no Canvas do Tkinter."""
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_tk = ImageTk.PhotoImage(image_pil)
        canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)
        canvas.image = image_tk  # Armazena a referência para evitar coleta de lixo

    def display_image_info(self, image):
        """Exibir informações básicas da imagem."""
        height, width, channels = image.shape
        info_text = f"Dimensões: {width}x{height}, Canais: {channels}"
        self.info_label.config(text=info_text)

    def convert_to_grayscale(self):
        """Converter a imagem para tons de cinza."""
        if self.original_image is not None:
            gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            self.processed_image = gray_image
            self.display_image(cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR), self.processed_canvas)

    def open_filter_window(self):
        """Abrir uma nova janela para aplicar filtros espaciais."""
        if self.original_image is not None:
            window = tk.Toplevel(self.root)
            window.title("Filtros Espaciais")
            window.configure(bg="lightgray")

            def apply_filter(filter_type):
                kernel_size = int(kernel_size_slider.get())
                if filter_type == "media":
                    filtered_image = cv2.blur(self.original_image, (kernel_size, kernel_size))
                elif filter_type == "gaussiano":
                    filtered_image = cv2.GaussianBlur(self.original_image, (kernel_size, kernel_size), 0)
                elif filter_type == "mediana":
                    filtered_image = cv2.medianBlur(self.original_image, kernel_size)
                elif filter_type == "laplaciano":
                    gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
                    filtered_image = cv2.Laplacian(gray_image, cv2.CV_64F)
                    filtered_image = cv2.convertScaleAbs(filtered_image)
                elif filter_type == "sobel":
                    gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
                    sobelx = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=kernel_size)
                    sobely = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=kernel_size)
                    filtered_image = cv2.convertScaleAbs(cv2.sqrt(sobelx ** 2 + sobely ** 2))
                self.processed_image = filtered_image
                self.display_image(filtered_image if len(filtered_image.shape) == 3 else cv2.cvtColor(filtered_image, cv2.COLOR_GRAY2BGR), self.processed_canvas)

            kernel_size_slider = tk.Scale(window, from_=3, to=15, orient=tk.HORIZONTAL, label="Tamanho do Kernel", bg="lightgray")
            kernel_size_slider.set(3)
            kernel_size_slider.pack(pady=5)

            tk.Button(window, text="Filtro de Média", command=lambda: apply_filter('media')).pack(pady=5)
            tk.Button(window, text="Filtro Gaussiano", command=lambda: apply_filter('gaussiano')).pack(pady=5)
            tk.Button(window, text="Filtro Mediana", command=lambda: apply_filter('mediana')).pack(pady=5)
            tk.Button(window, text="Filtro Laplaciano", command=lambda: apply_filter('laplaciano')).pack(pady=5)
            tk.Button(window, text="Filtro Sobel", command=lambda: apply_filter('sobel')).pack(pady=5)

    def adjust_contrast(self):
        """Ajustar brilho e contraste usando sliders."""
        if self.original_image is not None:
            window = tk.Toplevel(self.root)
            window.title("Ajuste de Brilho/Contraste")
            window.configure(bg="lightgray")

            def update(val):
                alpha = contrast_slider.get() / 100
                beta = brightness_slider.get() - 50
                adjusted_image = cv2.convertScaleAbs(self.original_image, alpha=alpha, beta=beta)
                self.display_image(adjusted_image, self.processed_canvas)

            contrast_slider = tk.Scale(window, from_=0, to=100, orient=tk.HORIZONTAL, label="Contraste", command=update, bg="lightgray")
            contrast_slider.set(50)
            contrast_slider.pack(pady=5)

            brightness_slider = tk.Scale(window, from_=0, to=100, orient=tk.HORIZONTAL, label="Brilho", command=update, bg="lightgray")
            brightness_slider.set(50)
            brightness_slider.pack(pady=5)

    def resize_image(self, image, scale):
        """Redimensionar a imagem para uma versão menor."""
        width = int(image.shape[1] * scale)
        height = int(image.shape[0] * scale)
        dim = (width, height)
        resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        return resized_image

    def apply_morphological_operation(self, operation, kernel_size):
        """Aplicar operações morfológicas como erosão, dilatação, etc."""
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
        """Abrir uma nova janela para aplicar operações morfológicas."""
        if self.original_image is not None:
            window = tk.Toplevel(self.root)
            window.title("Operações Morfológicas")
            window.configure(bg="lightgray")

            def apply(operation):
                kernel_size = int(kernel_size_slider.get())
                self.apply_morphological_operation(operation, kernel_size)

            kernel_size_slider = tk.Scale(window, from_=3, to=15, orient=tk.HORIZONTAL, label="Tamanho do Kernel", bg="lightgray")
            kernel_size_slider.set(3)
            kernel_size_slider.pack(pady=5)

            tk.Button(window, text="Erosão", command=lambda: apply('erosion')).pack(pady=5)
            tk.Button(window, text="Dilatação", command=lambda: apply('dilation')).pack(pady=5)
            tk.Button(window, text="Abertura", command=lambda: apply('opening')).pack(pady=5)
            tk.Button(window, text="Fechamento", command=lambda: apply('closing')).pack(pady=5)
            tk.Button(window, text="Gradiente", command=lambda: apply('gradient')).pack(pady=5)

    def segment_and_find_contours(self):
        """Segmentar a imagem e encontrar contornos."""
        if self.original_image is not None:
            window = tk.Toplevel(self.root)
            window.title("Segmentação e Contornos")
            window.configure(bg="lightgray")

            def apply_segmentation():
                threshold_value = threshold_slider.get()
                gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
                _, thresholded = cv2.threshold(gray_image, threshold_value, 255, cv2.THRESH_BINARY)
                contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                contour_image = self.original_image.copy()
                cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)
                self.display_image(contour_image, self.processed_canvas)

            threshold_slider = tk.Scale(window, from_=0, to=255, orient=tk.HORIZONTAL, label="Threshold", bg="lightgray")
            threshold_slider.set(128)
            threshold_slider.pack(pady=5)

            tk.Button(window, text="Aplicar", command=apply_segmentation).pack(pady=5)

    def open_custom_filter_window(self):
        """Abrir uma nova janela para aplicar um filtro personalizado."""
        if self.original_image is not None:
            window = tk.Toplevel(self.root)
            window.title("Filtro Personalizado")
            window.configure(bg="lightgray")

            def apply_filter():
                kernel = np.array([
                    [int(entry_00.get()), int(entry_01.get()), int(entry_02.get())],
                    [int(entry_10.get()), int(entry_11.get()), int(entry_12.get())],
                    [int(entry_20.get()), int(entry_21.get()), int(entry_22.get())]
                ], dtype=np.float32)
                custom_filtered_image = cv2.filter2D(self.original_image, -1, kernel)
                self.display_image(custom_filtered_image, self.processed_canvas)

            entries = []
            for i in range(3):
                row = []
                for j in range(3):
                    entry = tk.Entry(window, width=5)
                    entry.grid(row=i, column=j, padx=5, pady=5)
                    row.append(entry)
                entries.append(row)

            entry_00, entry_01, entry_02 = entries[0]
            entry_10, entry_11, entry_12 = entries[1]
            entry_20, entry_21, entry_22 = entries[2]

            tk.Button(window, text="Aplicar Filtro", command=apply_filter).grid(row=3, columnspan=3, pady=10)

    def display_histogram(self):
        """Exibir o histograma da imagem."""
        if self.processed_image is not None:
            # Se a imagem for em tons de cinza, mostra um único histograma
            if len(self.processed_image.shape) == 2:
                histogram = cv2.calcHist([self.processed_image], [0], None, [256], [0, 256])
                plt.plot(histogram, color='black')
                plt.xlim([0, 256])
            else:
                # Exibir histograma para cada canal de cor
                for i, color in enumerate(['b', 'g', 'r']):
                    histogram = cv2.calcHist([self.processed_image], [i], None, [256], [0, 256])
                    plt.plot(histogram, color=color)
                    plt.xlim([0, 256])
            plt.show()

    def equalize_histogram(self):
        """Equalizar o histograma da imagem."""
        if self.processed_image is not None:
            if len(self.processed_image.shape) == 2:  # Tons de cinza
                equalized_image = cv2.equalizeHist(self.processed_image)
            else:  # Imagem colorida, converter para YCrCb e equalizar o canal Y
                ycrcb = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2YCrCb)
                ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
                equalized_image = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)
            self.display_image(equalized_image, self.processed_canvas)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
