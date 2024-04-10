import customtkinter as ctk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import cv2


class Main:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.geometry("1200x720")

        self.app.grid_columnconfigure((0, 1), weight=1)
        self.app.grid_rowconfigure(0, weight=2)
        self.app.grid_rowconfigure(1, weight=1)

        self.frame_img1 = ctk.CTkFrame(self.app)
        self.frame_img1.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=(10, 5))

        self.label_img = ctk.CTkLabel(self.frame_img1, text="")
        self.label_img.grid(row=0, column=0, sticky="nsew")

        self.frame_img2 = ctk.CTkFrame(self.app)
        self.frame_img2.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=(10, 5))

        self.frame_options = ctk.CTkFrame(self.app)
        self.frame_options.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=(5, 10))
        self.frame_options.grid_columnconfigure(0, weight=1)
        self.frame_options.grid_columnconfigure(1, weight=5)
        self.frame_options.grid_rowconfigure(0, weight=1)

        self.frame_btns = ctk.CTkFrame(self.frame_options)
        self.frame_btns.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.frame_btns.grid_columnconfigure(0, weight=1)

        self.btn_load_img = ctk.CTkButton(
            self.frame_btns, text="Carregar Imagem", command=self.btn_load_img_callback, font=("Roboto", -18)
        )
        self.btn_load_img.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")


    def btn_load_img_callback(self):
        filename = ctk.filedialog.askopenfilename()
        if filename:
            img = Image.open(filename)
            img.thumbnail((self.frame_img1.winfo_width(), self.frame_img1.winfo_height()))
            img = ImageTk.PhotoImage(img)
            self.label_img.configure(image=img)
            self.label_img.image = img

    def start_app(self):
        self.app.mainloop()


if __name__ == "__main__":
    app = Main()
    app.start_app()

