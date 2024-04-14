import customtkinter as ctk
import numpy as np
from PIL import Image, ImageTk
from CTkListbox import *
from CTkMessagebox import CTkMessagebox
import cv2

class Main:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.geometry("1200x720")
        self.app.title("PDI")

        # Configuração do grid geral da janela principal
        self.app.grid_columnconfigure((0, 1), weight=1)
        self.app.grid_rowconfigure(0, weight=2)
        self.app.grid_rowconfigure(1, weight=1)

        self.img_original = None
        self.photo_img = None

        self.img_ratio = 0

        self.img_edit = None
        self.photo_edit = None

        # Janela de espaço de cores
        self.color_conversion_window = None

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

        self.filter_window = None
        self.filter_options = [
            "Nenhum",
            "Média",
            "Gaussiano",
            "Bilateral"
        ]
        self.kernel_size = None
        self.label_kernel_size = None
        self.slider_kernel_size = None

        self.d_size = None
        self.label_d_size = None
        self.slider_d_size = None

        self.sigma_color = None
        self.label_sigma_color = None
        self.slider_sigma_color = None

        self.sigma_space = None
        self.label_sigma_space = None
        self.slider_sigma_space = None

        self.processing_options = [
            "Conversão de cores",
            "Filtros"
        ]

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
            try:
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
            except:
                CTkMessagebox(
                    title="Erro", message="Erro ao abrir imagem!", icon="cancel"
                )

    def btn_save_img_callback(self):
        if self.img_edit is not None:
            img = self.img_edit
            filename = ctk.filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])

            if filename:
                try:
                    img.save(filename)
                    CTkMessagebox(
                        title="Sucesso", message="Imagem salva com sucesso!", icon="check"
                    )
                except:
                    CTkMessagebox(
                        title="Erro", message="Erro ao salvar imagem!", icon="cancel"
                    )

    def on_listbox_select(self, event):
        selected_index = self.listbox.curselection()
        selected_method = self.processing_options[selected_index]

        if self.img_original is not None:
            if selected_method == "Conversão de cores":
                self.open_color_conversion()
            elif selected_method == "Filtros":
                self.open_filter_window()

    def open_color_conversion(self):
        if self.color_conversion_window is None or not self.color_conversion_window.winfo_exists():
            self.color_conversion_window = ctk.CTkToplevel(self.app)
            self.color_conversion_window.geometry("300x720")
            self.color_conversion_window.title("Espaço de cores")

            color_space_var = ctk.StringVar(self.color_conversion_window)
            color_space_var.set("RGB")

            ctk.CTkLabel(self.color_conversion_window, text="Escolha um espaço de cor", font=("Roboto", -18)).pack()

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

    def color_conversion(self, selected_color):
        cv_img = np.array(self.img_edit)
        if selected_color == 'RGB':
            self.photo_edit = self.photo_img
        else:
            cvt_img = cv2.cvtColor(cv_img, self.color_space_options[selected_color])
            self.img_edit = Image.fromarray(cvt_img)
            self.photo_edit = ImageTk.PhotoImage(self.img_edit)

        width, height = self.canvas_edited.winfo_width(), self.canvas_edited.winfo_height()

        self.canvas_edited.create_image(
            int(width / 2), int(height / 2), anchor='center', image=self.photo_edit
        )

    def open_filter_window(self):
        if not (self.filter_window is None or not self.filter_window.winfo_exists()):
            return
        self.filter_window = ctk.CTkToplevel(self.app)
        self.filter_window.geometry("400x720")
        self.filter_window.title("Filtros")

        k_min = 1
        k_max = 15
        steps = int((k_max - k_min) / 2)

        ctk.CTkLabel(self.filter_window, text="Tamanho do Kernel", font=("Roboto", -18)).pack()

        self.label_kernel_size = ctk.CTkLabel(self.filter_window, text="1")
        self.label_kernel_size.pack()

        self.slider_kernel_size = ctk.CTkSlider(
            self.filter_window, from_=k_min, to=k_max, number_of_steps=steps, command=self.handle_kernel_slider
        )
        self.slider_kernel_size.pack()
        self.slider_kernel_size.set(1)

        ctk.CTkLabel(self.filter_window, text="Diametro pixels (bilateral)",  font=("Roboto", -18)).pack()

        self.label_d_size = ctk.CTkLabel(self.filter_window, text="0")
        self.label_d_size.pack()

        self.slider_d_size = ctk.CTkSlider(
            self.filter_window, from_=0, to=30, command=self.handle_d_size_slider
        )
        self.slider_d_size.pack()
        self.slider_d_size.set(0)

        ctk.CTkLabel(self.filter_window, text="Sigma Color",  font=("Roboto", -18)).pack()

        self.label_sigma_color = ctk.CTkLabel(self.filter_window, text="0")
        self.label_sigma_color.pack()

        self.slider_sigma_color = ctk.CTkSlider(
            self.filter_window, from_=0, to=200, command=self.handle_sigma_color_slider
        )
        self.slider_sigma_color.pack()
        self.slider_sigma_color.set(0)

        ctk.CTkLabel(self.filter_window, text="Sigma Space", font=("Roboto", -18)).pack()

        self.label_sigma_space = ctk.CTkLabel(self.filter_window, text="0")
        self.label_sigma_space.pack()

        self.slider_sigma_space = ctk.CTkSlider(
            self.filter_window, from_=0, to=200, command=self.handle_sigma_space_slider
        )
        self.slider_sigma_space.pack()
        self.slider_sigma_space.set(0)

        filter_var = ctk.StringVar(self.filter_window)
        filter_var.set("Nenhum")

        for index, filter in enumerate(self.filter_options):
            if index == 0:
                pady = (20, 10)
            elif index == len(self.color_space_options) - 1:
                pady = (10, 20)
            else:
                pady = (10, 10)
            ctk.CTkRadioButton(
                self.filter_window, text=filter, variable=filter_var, value=filter
            ).pack(pady=pady)

        ctk.CTkButton(
            self.filter_window, text="Confirmar", command=lambda: self.apply_filter(filter_var.get())
        ).pack()

    def handle_kernel_slider(self, value):
        self.label_kernel_size.configure(text=f"{int(value)}")
        self.kernel_size = (int(value), int(value))

    def handle_d_size_slider(self, value):
        self.label_d_size.configure(text=f'{int(value)}')
        self.d_size = int(value)

    def handle_sigma_color_slider(self, value):
        self.label_sigma_color.configure(text=f'{value}')
        self.sigma_color = value

    def handle_sigma_space_slider(self, value):
        self.label_sigma_space.configure(text=f'{value}')
        self.sigma_space = value

    def apply_filter(self, filter_name):
        cv_img = np.array(self.img_edit)
        if filter_name == self.filter_options[0]:
            filtered_img = np.array(self.img_original)
            self.sigma_color = 0
            self.slider_sigma_color.set(0)
            self.label_sigma_color.configure(text=self.sigma_color)

            self.sigma_space = 0
            self.slider_sigma_space.set(0)
            self.label_sigma_space.configure(text=self.sigma_space)

            self.d_size = 0
            self.slider_d_size.set(0)
            self.label_d_size.configure(text=self.d_size)

            self.kernel_size = (0, 0)
            self.slider_kernel_size.set(0)
            self.label_kernel_size.configure(text="0")
        elif filter_name == self.filter_options[1]:
            filtered_img = cv2.blur(cv_img, self.kernel_size)
        elif filter_name == self.filter_options[2]:
            filtered_img = cv2.GaussianBlur(cv_img, self.kernel_size, 0)
        else:
            filtered_img = cv2.bilateralFilter(cv_img, self.d_size, self.sigma_color, self.sigma_space)

        self.img_edit = Image.fromarray(filtered_img)
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

