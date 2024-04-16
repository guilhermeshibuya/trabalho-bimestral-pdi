import customtkinter as ctk
import numpy as np
from PIL import Image, ImageTk
from CTkListbox import *
from CTkMessagebox import CTkMessagebox
import cv2

class Main:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.geometry("1280x720")
        self.app.title("PDI")

        # Configuração do grid geral da janela principal
        self.app.grid_columnconfigure(0, weight=0)
        self.app.grid_columnconfigure((1, 2), weight=5)
        self.app.grid_rowconfigure(0, weight=3)
        self.app.grid_rowconfigure(1, weight=1)

        self.img_original = None
        self.photo_img = None

        self.img_ratio = 0

        self.img_edit = None
        self.photo_edit = None

        self.history = []
        self.redo_history = []

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

        self.color_conversion_applied = False

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

        self.sobel_window = None
        self.sobel_ksize = None
        self.label_sobel_ksize = None

        self.laplace_window = None
        self.laplace_ksize = None
        self.label_laplace_ksize = None

        self.processing_options = [
            "Conversão de cores",
            "Filtros",
            "Sobel",
            "Laplace"
        ]

        # Canvas para as imagens
        self.canvas_original = ctk.CTkCanvas(
            self.app, background='black', bd=0, highlightthickness=0, relief='flat'
        )
        self.canvas_original.grid(row=0, column=1, stick='nsew', padx=5, pady=(10, 5))
        self.canvas_original.bind('<Configure>', self.fill_img)

        self.canvas_edited = ctk.CTkCanvas(
            self.app, background='black', bd=0, highlightthickness=0, relief='flat'
        )
        self.canvas_edited.grid(row=0, column=2, stick='nsew', padx=(5, 10), pady=(10, 5))
        self.canvas_edited.bind('<Configure>', self.fill_img)

        # Container para as opções
        self.frame_options = ctk.CTkFrame(self.app)
        self.frame_options.grid(row=1, column=1, columnspan=2, sticky="nsew", padx=10, pady=(5, 10))
        self.frame_options.grid_columnconfigure(0, weight=5)
        self.frame_options.grid_columnconfigure(1, weight=3)
        self.frame_options.grid_rowconfigure(0, weight=1)

        # Botões
        self.frame_btns = ctk.CTkFrame(self.app)
        self.frame_btns.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=(10, 5), rowspan=2)
        self.frame_btns.grid_columnconfigure(0, weight=1)

        self.load_img_icon = ctk.CTkImage(
            dark_image=Image.open('icons/file_open.png'),
            size=(36, 36)
        )
        self.btn_load_img = ctk.CTkButton(
            self.frame_btns, text="", image=self.load_img_icon,
            command=self.btn_load_img_callback, width=40, height=40
        )
        self.btn_load_img.grid(row=0, column=0, padx=10, pady=(10, 5))

        self.btn_save_img_icon = ctk.CTkImage(
            dark_image=Image.open('icons/file_save.png'),
            size=(36, 36)
        )
        self.btn_save_img = ctk.CTkButton(
            self.frame_btns, text="", image=self.btn_save_img_icon,
            command=self.btn_save_img_callback, width=40, height=40
        )
        self.btn_save_img.grid(row=1, column=0, padx=10, pady=5)

        self.btn_undo_icon = ctk.CTkImage(
            dark_image=Image.open('icons/undo.png'),
            size=(36, 36)
        )
        self.btn_undo = ctk.CTkButton(
            self.frame_btns, text="", image=self.btn_undo_icon,
            command=self.undo_preprocessing, width=40, height=40
        )
        self.btn_undo.grid(row=2, column=0, padx=10, pady=5)

        self.btn_redo_icon = ctk.CTkImage(
            dark_image=Image.open('icons/redo.png'),
            size=(36, 36)
        )
        self.btn_redo = ctk.CTkButton(
            self.frame_btns, text="", image=self.btn_redo_icon,
            command=self.redo_preprocessing, width=40, height=40
        )
        self.btn_redo.grid(row=3, column=0, padx=10, pady=5)

        # Listbox
        self.listbox = CTkListbox(self.frame_options)
        self.listbox.grid(row=0, column=0,  sticky="nsew", padx=5, pady=5)
        self.listbox.bind("<<ListboxSelect>>", self.on_listbox_select)

        for option in self.processing_options:
            self.listbox.insert("end", option)

        # Listbox histórico
        self.history_listbox = CTkListbox(self.frame_options)
        self.history_listbox.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Setando aparência e tema do aplicativo
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.operations_types = ["color conversion", "filter", "edge detection"]

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
                self.color_conversion_applied = False
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
                self.history.append({
                    'image': self.img_edit.copy(),
                    'operation': 'Imagem aberta'
                })
                self.update_history_listbox()
            except:
                CTkMessagebox(
                    title="Erro", message="Erro ao abrir imagem!", icon="cancel"
                )

    def btn_save_img_callback(self):
        if self.img_edit is not None:
            img = self.img_edit
            filename = ctk.filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])

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
            elif selected_method == "Sobel":
                self.open_sobel_window()
            elif selected_method == "Laplace":
                self.open_laplace_window()
                
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
        if self.color_conversion_applied:
            CTkMessagebox(
                title="Erro", message="Conversão já aplicada", icon="cancel"
            )
            return

        cv_img = np.array(self.img_edit)
        if selected_color == 'RGB':
            self.photo_edit = self.photo_img
        else:
            cvt_img = cv2.cvtColor(cv_img, self.color_space_options[selected_color])
            self.img_edit = Image.fromarray(cvt_img)
            self.photo_edit = ImageTk.PhotoImage(self.img_edit)

        self.update_canvas()

        self.color_conversion_applied = True
        self.history.append({
            'image': self.img_edit.copy(),
            'operation': f'Espaço de cor - {selected_color}',
            'type': self.operations_types[0]
        })
        self.redo_history.clear()
        self.update_history_listbox()

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

        self.update_canvas()
        self.history.append({
            'image': self.img_edit.copy(),
            'operation': filter_name,
            'type': self.operations_types[1]
        })
        self.redo_history.clear()
        self.update_history_listbox()

    def open_sobel_window(self):
        if not (self.sobel_window is None or not self.sobel_window.winfo_exists()):
            return
        self.sobel_window = ctk.CTkToplevel(self.app)
        self.sobel_window.geometry("300x720")
        self.sobel_window.title("Sobel")

        k_min = 1
        k_max = 15
        steps = int((k_max - k_min) / 2)

        ctk.CTkLabel(self.sobel_window, text="Tamanho do Kernel", font=("Roboto", -18)).pack()

        self.label_sobel_ksize = ctk.CTkLabel(self.sobel_window, text="1")
        self.label_sobel_ksize.pack()

        self.slider_kernel_size = ctk.CTkSlider(
            self.sobel_window, from_=k_min, to=k_max, number_of_steps=steps, command=self.handle_sobel_ksize_slider
        )
        self.slider_kernel_size.pack()
        self.slider_kernel_size.set(1)

        ctk.CTkLabel(self.sobel_window, text="Direção", font=("Roboto", -18)).pack()

        direction_var = ctk.StringVar(self.sobel_window)
        direction_var.set("x")

        ctk.CTkRadioButton(
            self.sobel_window, text="x", variable=direction_var, value="x"
        ).pack()
        ctk.CTkRadioButton(
            self.sobel_window, text="y", variable=direction_var, value="y"
        ).pack()

        ctk.CTkButton(
            self.sobel_window, text="Confirmar", command=lambda: self.apply_sobel(direction_var.get())
        ).pack()

    def apply_sobel(self, direction):
        cv_img = np.array(self.img_edit)

        if direction == "x":
            edit_img = cv2.Sobel(cv_img, cv2.CV_8U, 1, 0, self.sobel_ksize)
        else:
            edit_img = cv2.Sobel(cv_img, cv2.CV_8U, 0, 1, self.sobel_ksize)

        self.img_edit = Image.fromarray(edit_img)
        self.photo_edit = ImageTk.PhotoImage(self.img_edit)

        self.update_canvas()
        self.history.append({
            'image': self.img_edit.copy(),
            'operation': 'Sobel',
            'type': self.operations_types[2]
        })
        self.redo_history.clear()
        self.update_history_listbox()

    def open_laplace_window(self):
        if not (self.laplace_window is None or not self.laplace_window.winfo_exists()):
            return
        self.laplace_window = ctk.CTkToplevel(self.app)
        self.laplace_window.geometry("300x720")
        self.laplace_window.title("Sobel")

        k_min = 1
        k_max = 15
        steps = int((k_max - k_min) / 2)

        ctk.CTkLabel(self.laplace_window, text="Tamanho do Kernel", font=("Roboto", -18)).pack()

        self.label_laplace_ksize = ctk.CTkLabel(self.laplace_window, text="1")
        self.label_laplace_ksize.pack()

        self.slider_kernel_size = ctk.CTkSlider(
            self.laplace_window, from_=k_min, to=k_max, number_of_steps=steps, command=self.handle_laplace_ksize_slider
        )
        self.slider_kernel_size.pack()
        self.slider_kernel_size.set(1)

        ctk.CTkLabel(self.laplace_window, text="Direção", font=("Roboto", -18)).pack()

        ctk.CTkButton(
            self.laplace_window, text="Confirmar", command=self.apply_laplace
        ).pack()

    def apply_laplace(self):
        cv_img = np.array(self.img_edit)

        edit_img = cv2.Laplacian(cv_img, cv2.CV_16S, ksize=self.laplace_ksize)

        self.img_edit = Image.fromarray(edit_img)
        self.photo_edit = ImageTk.PhotoImage(self.img_edit)

        self.update_canvas()
        self.history.append({
            'image': self.img_edit.copy(),
            'operation': 'Laplace',
            'type': self.operations_types[2]
        })
        self.redo_history.clear()
        self.update_history_listbox()

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

    def handle_sobel_ksize_slider(self, value):
        self.label_sobel_ksize.configure(text=f'{int(value)}')
        self.sobel_ksize = int(value)

    def handle_laplace_ksize_slider(self, value):
        self.label_laplace_ksize.configure(text=f'{int(value)}')
        self.laplace_ksize = int(value)

    def update_canvas(self):
        width, height = self.canvas_edited.winfo_width(), self.canvas_edited.winfo_height()

        self.canvas_edited.create_image(
            int(width / 2), int(height / 2), anchor='center', image=self.photo_edit
        )

    def update_history_listbox(self):
        self.history_listbox.delete(0, "end")
        for index, item in enumerate(self.history):
            self.history_listbox.insert("end", f"{index + 1} - Processamento: {item['operation']}")

    def undo_preprocessing(self):
        if len(self.history) > 1:
            last = self.history.pop()
            self.redo_history.append(last)

            if last['type'] == self.operations_types[0]:
                self.color_conversion_applied = False
            self.img_edit = self.history[-1]['image'].copy()
            self.photo_edit = ImageTk.PhotoImage(self.img_edit)
            self.update_canvas()
            self.update_history_listbox()

    def redo_preprocessing(self):
        if self.redo_history:
            self.history.append(self.redo_history.pop())
            self.img_edit = self.history[-1]['image'].copy()
            self.photo_edit = ImageTk.PhotoImage(self.img_edit)
            self.update_canvas()
            self.update_history_listbox()

    def start_app(self):
        self.app.mainloop()


if __name__ == "__main__":
    app = Main()
    app.start_app()

