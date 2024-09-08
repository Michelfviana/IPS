from tkinter import Tk, Canvas, Label, Button, Frame, filedialog, Toplevel, Scale, HORIZONTAL, NW
import cv2
from PIL import Image, ImageTk

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Software de Processamento de Imagens")
        self.root.configure(bg='lightgray')  # Definir a cor de fundo da janela principal

        # Variáveis para armazenar a imagem original e a imagem processada
        self.original_image = None
        self.processed_image = None

        # Frame para organizar os botões
        button_frame = Frame(root, bg='lightgray')
        button_frame.grid(row=0, column=0, columnspan=2, pady=10)

        # Botão para carregar a imagem
        self.load_button = Button(button_frame, text="Carregar Imagem", command=self.load_image, bg='white')
        self.load_button.grid(row=0, column=0, padx=5)

        # Botão para conversão para tons de cinza
        self.grayscale_button = Button(button_frame, text="Converter para Tons de Cinza", command=self.convert_to_grayscale, bg='white')
        self.grayscale_button.grid(row=0, column=1, padx=5)

        # Botão para aplicar filtro
        self.filter_button = Button(button_frame, text="Aplicar Filtro", command=self.apply_filter, bg='white')
        self.filter_button.grid(row=0, column=2, padx=5)

        # Botão para ajustar brilho/contraste
        self.contrast_button = Button(button_frame, text="Ajustar Brilho/Contraste", command=self.adjust_contrast, bg='white')
        self.contrast_button.grid(row=0, column=3, padx=5)

        # Área para exibir a imagem carregada
        self.original_canvas = Canvas(root, width=300, height=400, bg='white')
        self.original_canvas.grid(row=1, column=0, padx=10, pady=10)

        # Área para exibir a imagem processada
        self.processed_canvas = Canvas(root, width=300, height=400, bg='white')
        self.processed_canvas.grid(row=1, column=1, padx=10, pady=10)

        # Label para exibir informações da imagem
        self.info_label = Label(root, text="", bg='lightgray')
        self.info_label.grid(row=2, column=0, columnspan=2, pady=10)

    def load_image(self):
        """Carregar uma imagem do sistema de arquivos e redimensioná-la."""
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")])
        if file_path:
            self.original_image = cv2.imread(file_path)
            self.original_image = self.resize_image(self.original_image, 0.3)  # Redimensiona a imagem para 30%
            self.display_image(self.original_image, self.original_canvas)
            self.display_image_info(self.original_image)

    def display_image(self, image, canvas):
        """Exibir a imagem em um Canvas Tkinter."""
        # Converte a imagem para RGB e depois para o formato compatível com o Tkinter
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_tk = ImageTk.PhotoImage(image_pil)
        canvas.create_image(0, 0, anchor=NW, image=image_tk)
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

    def apply_filter(self):
        """Aplicar filtros espaciais na imagem."""
        if self.original_image is not None:
            # Exemplo de filtro de média
            filtered_image = cv2.GaussianBlur(self.original_image, (15, 15), 0)
            self.processed_image = filtered_image
            self.display_image(filtered_image, self.processed_canvas)

    def adjust_contrast(self):
        """Ajustar o brilho e o contraste da imagem."""
        if self.original_image is not None:
            # Abre uma nova janela para ajustar o brilho/contraste
            window = Toplevel(self.root)
            window.title("Ajuste de Brilho/Contraste")
            window.configure(bg='lightgray')  # Definir a cor de fundo da nova janela
            
            def update(val):
                """Função de callback para atualizar o brilho e contraste."""
                alpha = contrast_slider.get() / 100
                beta = brightness_slider.get() - 50
                adjusted_image = cv2.convertScaleAbs(self.original_image, alpha=alpha, beta=beta)
                self.display_image(adjusted_image, self.processed_canvas)

            contrast_slider = Scale(window, from_=0, to=100, orient=HORIZONTAL, label="Contraste", command=update, bg='lightgray')
            contrast_slider.set(50)
            contrast_slider.pack(pady=5)

            brightness_slider = Scale(window, from_=0, to=100, orient=HORIZONTAL, label="Brilho", command=update, bg='lightgray')
            brightness_slider.set(50)
            brightness_slider.pack(pady=5)

    def resize_image(self, image, scale):
        """Redimensionar a imagem para uma versão menor."""
        width = int(image.shape[1] * scale)
        height = int(image.shape[0] * scale)
        dim = (width, height)
        resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        return resized_image

if __name__ == "__main__":
    root = Tk()
    app = ImageProcessorApp(root)
    root.mainloop()