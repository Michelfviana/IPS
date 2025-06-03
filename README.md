# Image processing Software

![Project Image](src/Screenshot%20from%202024-09-20%2015-26-27.png)

A Python-based software for image processing using a graphical interface built with Tkinter. This application allows users to load images, convert them to grayscale, apply filters, and adjust brightness and contrast. It uses OpenCV for image manipulation and PIL (Pillow) for displaying images. The main features include:

- Loading images from the filesystem and displaying them.
- Converting images to grayscale.
- Applying filters, such as Gaussian Blur, to images.
- Adjusting brightness and contrast using interactive sliders in a separate window.

The user interface includes buttons for each function, a canvas to display the original and processed images, and a label to show basic information about the images.

## Requirements

Make sure you have Python 3.x installed. You can check your Python version with the command:

```bash
python --version
```

You also need to have Tkinter installed:

- **Ubuntu/Debian:**

   ```bash
   sudo apt-get install python3-tk
   ```

- **Fedora:**

   ```bash
   sudo dnf install python3-tkinter
   ```

- **Arch Linux/Manjaro:**

   ```bash
   sudo pacman -S tk
   ```

- **Windows:**

   Tkinter geralmente já vem incluído nas instalações padrão do Python. Se houver problemas, certifique-se de ter instalado o Python oficial do [python.org](https://www.python.org/downloads/).

- **macOS:**

   Tkinter normalmente está incluído no Python fornecido pela Apple ou pelo instalador oficial do Python. Se necessário, instale o Python pelo [python.org](https://www.python.org/downloads/).

## Cloning the Repository

Clone this repository using the `git` command:

```bash
git clone https://github.com/Michelfviana/IPS.git
```

Replace `https://github.com/Michelfviana/IPS.git` with the URL of your repository.

## Environment Setup

1. Navigate to the project directory:

    ```bash
    cd repository-name
    ```

2. Create a virtual environment to isolate the project dependencies:

    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:

    - **Windows:**

       ```bash
       venv\Scripts\activate
       ```

    - **Linux/macOS:**

       ```bash
       source venv/bin/activate
       ```

4. Install the project dependencies listed in the `requirements.txt` file:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Project

With the virtual environment activated and the dependencies installed, you can run the project. Depending on the type of project, the command to run it may vary.

- **For a Python script:**

   ```bash
   python main.py
   ```
