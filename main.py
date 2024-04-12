import customtkinter as ctk
import numpy as np
from PIL import Image, ImageTk
from CTkListbox import *
from CTkMessagebox import CTkMessagebox
import cv2
from _socket import herror


class Main:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.geometry("1200x720")
        self.app.title("PDI")

        # Configuração do grid geral da janela principal
        self.app.grid_columnconfigure((0, 1), weight=1)
        self.app.grid_rowconfigure(0, weight=2)
        self.app.grid_rowconfigure(1, weight=1)

        # Janela de espaço de cores
        self.color_conversion_window = None

        self.img_original = None
        self.photo_img = None

        self.img_ratio = 0

        self.img_edit = None
        self.photo_edit = None

        self.processing_options = [
            "Conversão de cores",
            "Média"
        ]

        # Opções de espaço de cores
        self.color_space_options = {
            'RGB': '',
            'Gray': cv2.COLOR_RGB2GRAY,
            'HSV': cv2.COLOR_RGB2HSV,
            'XYZ': cv2.COLOR_RGB2XYZ,
            'Luv': cv2.COLOR_RGB2Luv,
            'Lab': cv2.COLOR_RGB2Lab,
            'YCrCb': cv2.COLOR_RGB2YCrCb
        }

        # Canvas para as imagens
        self.canvas_original = ctk.CTkCanvas(
            self.app, background='black', bd=0, highlightthickness=0, relief='flat'
        )
        self.canvas_original.grid(row=0, column=0, stick='nsew', padx=(10, 5), pady=(10, 5))
        self.canvas_original.bind('<Configure>', self.fill_img)

        self.canvas_edited = ctk.CTkCanvas(
            self.app, background='black', bd=0, highlightthickness=0, relief='flat'
        )
        self.canvas_edited.grid(row=0, column=1, stick='nsew', padx=(10, 5), pady=(10, 5))
        self.canvas_edited.bind('<Configure>', self.fill_img)

        # Container para as opções, botões
        self.frame_options = ctk.CTkFrame(self.app)
        self.frame_options.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=(5, 10))
        self.frame_options.grid_columnconfigure(0, weight=1)
        self.frame_options.grid_columnconfigure(1, weight=5)
        self.frame_options.grid_columnconfigure(2, weight=3)
        self.frame_options.grid_rowconfigure(0, weight=1)

        # Botões
        self.frame_btns = ctk.CTkFrame(self.frame_options)
        self.frame_btns.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.frame_btns.grid_columnconfigure(0, weight=1)

        self.btn_load_img = ctk.CTkButton(
            self.frame_btns, text="Carregar Imagem", command=self.btn_load_img_callback, font=("Roboto", -18)
        )
        self.btn_load_img.grid(row=0, column=0, padx=20, pady=(10, 5), sticky="ew")

        self.btn_save_img = ctk.CTkButton(
            self.frame_btns, text="Salvar Imagem", command=self.btn_save_img_callback, font=("Roboto", -18)
        )
        self.btn_save_img.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        # Listbox
        self.listbox = CTkListbox(self.frame_options)
        self.listbox.grid(row=0, column=1,  sticky="nsew", padx=5, pady=5)
        self.listbox.bind("<<ListboxSelect>>", self.on_listbox_select)

        for option in self.processing_options:
            self.listbox.insert("end", option)

        # Setando aparência e tema do aplicativo
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.app.update()

    def fill_img(self, event):
        if not self.img_original:
            return
        canvas_ratio = event.width / event.height

        if canvas_ratio > self.img_ratio:
            height = int(event.height)
            width = int(height * self.img_ratio)
        else:
            width = int(event.width)
            height = int(width / self.img_ratio)

        resized_img = self.img_original.resize((width, height))
        resized_photo = ImageTk.PhotoImage(resized_img)
        self.canvas_original.create_image(
            int(event.width / 2),
            int(event.height / 2),
            anchor='center',
            image=resized_photo
        )
        # self.photo_img = resized_photo

    def btn_load_img_callback(self):
        filename = ctk.filedialog.askopenfilename()
        if filename:
            self.img_original = Image.open(filename).convert("RGB")
            self.img_edit = self.img_original
            self.img_ratio = self.img_original.size[0] / self.img_original.size[1]

            photo_img = ImageTk.PhotoImage(self.img_original)

            width, height = self.canvas_original.winfo_width(), self.canvas_original.winfo_height()

            self.canvas_original.create_image(
                int(width / 2), int(height / 2), anchor='center', image=photo_img
            )
            self.photo_img = photo_img

            self.canvas_edited.create_image(
                int(width / 2), int(height / 2), anchor='center', image=photo_img
            )
            self.photo_edit = photo_img

    def btn_save_img_callback(self):
        if self.img_edit is not None:
            img = self.img_edit
            filename = ctk.filedialog.asksaveasfilename(defaultextension=".jpg",filetypes=[("JPEG files", "*.jpg")])

            if filename:
                try:
                    img.save(filename)
                    CTkMessagebox(
                        title="Sucesso", message="Imagem salva com sucesso!", icon="check"
                    )
                except Exception as e:
                    CTkMessagebox(
                        title="Erro", message="Erro ao salvar imagem!", icon="cancel"
                    )

    def on_listbox_select(self, event):
        selected_index = self.listbox.curselection()
        selected_method = self.processing_options[selected_index]

        if self.img_original is not None:
            if selected_method == "Conversão de cores":
                self.open_color_conversion()
            elif selected_method == "Média":
                print("blur")

    def open_color_conversion(self):
        if self.color_conversion_window is None or not self.color_conversion_window.winfo_exists():
            self.color_conversion_window = ctk.CTkToplevel(self.app)
            self.color_conversion_window.geometry("200x720")
            self.color_conversion_window.title("Espaço de cores")

            color_space_var = ctk.StringVar(self.color_conversion_window)
            color_space_var.set("RGB")

            ctk.CTkLabel(self.color_conversion_window, text="Escolha um espaço de cor").pack()

            for index, opt in enumerate(self.color_space_options.keys()):
                if index == 0:
                    pady = (20, 10)
                elif index == len(self.color_space_options) - 1:
                    pady = (10, 20)
                else:
                    pady = (10, 10)
                ctk.CTkRadioButton(
                    self.color_conversion_window, text=opt, variable=color_space_var, value=opt
                ).pack(pady=pady)

            ctk.CTkButton(
                self.color_conversion_window, text="Confirmar", command=lambda: self.color_conversion(color_space_var.get())
            ).pack()

    def open_filter_window(self):
        print("")

    def color_conversion(self, selected_color):
        if selected_color == 'RGB':
            self.photo_edit = self.photo_img
        else:
            cv_img = np.array(self.img_original)
            cvt_img = cv2.cvtColor(cv_img, self.color_space_options[selected_color])
            self.img_edit = Image.fromarray(cvt_img)
            self.photo_edit = ImageTk.PhotoImage(self.img_edit)

        width, height = self.canvas_edited.winfo_width(), self.canvas_edited.winfo_height()

        self.canvas_edited.create_image(
            int(width / 2), int(height / 2), anchor='center', image=self.photo_edit
        )

    def start_app(self):
        self.app.mainloop()


if __name__ == "__main__":
    app = Main()
    app.start_app()

