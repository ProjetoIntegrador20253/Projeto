import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

COLOR_ORANGE = "#F48B2C"
COLOR_GREEN = "#9CC93D"
COLOR_GREY = "#6D6E71"
COLOR_BG_WHITE = "#FFFFFF"   
COLOR_BG_LIGHT = "#FEF5EC"   

COLOR_DARK_BG = "#2E2E2E"      
COLOR_DARK_BG_ALT = "#3A3A3A"  
COLOR_DARK_FG = "#EAEAEA"      

class DataWarehouseApp(tk.Tk):
    
    def __init__(self):
        super().__init__()

        self.title("Painel de Controle DW - Ulabum Buffet")
        self.geometry("900x700")
        self.header_logo_filename = "Logotipo-Oficial-Ulabum_Logotipo-3-Colorido-.png"
        self.menu_logo_filename = "Logotipo-Oficial-Ulabum_Logotipo-2-Colorido-.png"
        self.current_theme = "light"

        self.create_header()

        self.create_scrollable_content()
        
        self.apply_theme_colors()

        self.populate_content()
        
        self.setup_key_bindings()

    def create_header(self):
        
        self.header_frame = tk.Frame(self, bg=COLOR_BG_LIGHT, height=100)
        self.header_frame.pack(side="top", fill="x")
        self.header_frame.pack_propagate(False)

        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(script_dir, self.header_logo_filename)

            if not os.path.exists(image_path):
                self.header_logo_label = tk.Label(
                    self.header_frame, 
                    text="ULABUM (Logo não encontrado)",
                    font=("Arial", 20, "bold"),
                    fg=COLOR_ORANGE,
                    bg=COLOR_BG_LIGHT
                )
                print(f"Erro: Imagem do cabeçalho não encontrada: {image_path}")
            else:
                pil_image = Image.open(image_path)
                w, h = pil_image.size
                new_h = 80
                new_w = int(new_h * (w / h))
                
                pil_image = pil_image.resize((new_w, new_h), Image.Resampling.LANCZOS)
                
                self.logo_tk = ImageTk.PhotoImage(pil_image)
                
                self.header_logo_label = tk.Label(
                    self.header_frame, 
                    image=self.logo_tk, 
                    bg=COLOR_BG_LIGHT
                )
                self.header_logo_label.image = self.logo_tk

            self.header_logo_label.pack(side="left", padx=20, pady=10)

        except Exception as e:
            print(f"Erro ao carregar o logo do cabeçalho: {e}")
            self.header_logo_label = tk.Label(
                self.header_frame, 
                text="ULABUM", 
                font=("Arial", 20, "bold"), 
                fg=COLOR_ORANGE,
                bg=COLOR_BG_LIGHT
            )
            self.header_logo_label.pack(side="left", padx=20, pady=10)

        refresh_button = tk.Button(
            self.header_frame,
            text="Atualizar Dados",
            font=("Arial", 12, "bold"),
            bg=COLOR_GREEN,
            fg="white",
            command=self.refresh_data,
            relief="flat",
            activebackground="#B5E65C",
            activeforeground="white",
            cursor="hand2",
            padx=10,
            pady=5
        )
        refresh_button.pack(side="right", padx=20, pady=10)

    def create_scrollable_content(self):
        
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(self.container, highlightthickness=0)
        
        scrollbar = ttk.Scrollbar(
            self.container, 
            orient="vertical", 
            command=self.canvas.yview
        )
        
        self.scrollable_frame = tk.Frame(self.canvas)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.canvas_window = self.canvas.create_window(
            (0, 0), 
            window=self.scrollable_frame, 
            anchor="nw"
        )
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.bind_all("<MouseWheel>", self._on_mousewheel)
        self.bind_all("<Button-4>", self._on_mousewheel)
        self.bind_all("<Button-5>", self._on_mousewheel)
        
        self.canvas.bind("<Configure>", self.on_canvas_configure)

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        if event.num == 5 or event.delta == -120:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta == 120:
            self.canvas.yview_scroll(-1, "units")

    def populate_content(self):
        
        if self.current_theme == "light":
            bg_main = COLOR_BG_WHITE
            bg_alt = COLOR_BG_LIGHT
            fg_text = COLOR_GREY
        else:
            bg_main = COLOR_DARK_BG
            bg_alt = COLOR_DARK_BG_ALT
            fg_text = COLOR_DARK_FG
            
        self.scrollable_frame.configure(bg=bg_main)

        title_label = tk.Label(
            self.scrollable_frame,
            text="Visão Geral do Data Warehouse",
            font=("Arial", 16, "bold"),
            fg=COLOR_ORANGE,
            bg=bg_main,
            anchor="w"
        )
        title_label.pack(fill="x", padx=10, pady=10)

        for i in range(50):
            bg_color = bg_main if i % 2 == 0 else bg_alt
            
            row_frame = tk.Frame(self.scrollable_frame, bg=bg_color)
            
            label_info = tk.Label(
                row_frame,
                text=f"Informação de Exemplo {i+1} (ex: Tabela 'Eventos' atualizada)",
                font=("Arial", 11),
                fg=fg_text,
                bg=bg_color,
                anchor="w"
            )
            label_info.pack(side="left", fill="x", expand=True, padx=10, pady=5)
            
            btn_details = tk.Button(
                row_frame,
                text="Verificar",
                font=("Arial", 9),
                bg=COLOR_GREY,
                fg="white",
                relief="flat"
            )
            btn_details.pack(side="right", padx=10)

            row_frame.pack(fill="x", expand=True)
            
    def clear_content(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def refresh_data(self):
        print("Iniciando atualização dos dados do DW...")
        
        self.clear_content()
            
        if self.current_theme == "light":
            bg_main = COLOR_BG_WHITE
            fg_text = COLOR_GREY
        else:
            bg_main = COLOR_DARK_BG
            fg_text = COLOR_DARK_FG
        
        loading_label = tk.Label(
            self.scrollable_frame,
            text="Carregando novos dados...",
            font=("Arial", 14, "italic"),
            fg=fg_text,
            bg=bg_main
        )
        loading_label.pack(pady=20)
        
        self.update_idletasks()
        self.after(1500, self.finish_refresh)

    def finish_refresh(self):
        self.clear_content()
        self.populate_content()
        print("Dados atualizados.")

    def setup_key_bindings(self):
        self.bind('<F5>', lambda event=None: self.refresh_data())
        self.bind('<Escape>', lambda event=None: self.open_main_menu())
        
    def close_app(self):
        print("Comando 'Fechar' selecionado. Fechando aplicação...")
        self.destroy()

    def open_main_menu(self):
        
        menu_window = tk.Toplevel(self)
        menu_window.title("Menu")
        menu_window.configure(bg=COLOR_BG_WHITE)
        
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(script_dir, self.menu_logo_filename) 
            
            pil_image = Image.open(image_path)
            w, h = pil_image.size
            new_h = 100
            new_w = int(new_h * (w / h))
            pil_image = pil_image.resize((new_w, new_h), Image.Resampling.LANCZOS)
            
            self.menu_logo_tk = ImageTk.PhotoImage(pil_image) 
            
            logo_label = tk.Label(menu_window, image=self.menu_logo_tk, bg=COLOR_BG_WHITE)
            logo_label.image = self.menu_logo_tk
            logo_label.pack(padx=30, pady=20)

        except Exception as e:
            print(f"Erro ao carregar logo do menu: {e}")
            logo_label = tk.Label(menu_window, text="ULABUM", font=("Arial", 24, "bold"), fg=COLOR_ORANGE, bg=COLOR_BG_WHITE)
            logo_label.pack(padx=30, pady=20)

        button_frame = tk.Frame(menu_window, bg=COLOR_BG_WHITE)
        button_frame.pack(fill="x", padx=20, pady=(0, 20))
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        theme_text = "Ativar Modo Escuro" if self.current_theme == "light" else "Ativar Modo Claro"
        theme_button = tk.Button(
            button_frame,
            text=theme_text,
            font=("Arial", 11),
            bg=COLOR_GREY,
            fg="white",
            relief="flat",
            command=lambda: [self.toggle_theme(), menu_window.destroy()]
        )
        theme_button.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        close_button = tk.Button(
            button_frame,
            text="Fechar Programa",
            font=("Arial", 11),
            bg=COLOR_ORANGE,
            fg="white",
            relief="flat",
            command=self.close_app 
        )
        close_button.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        menu_window.transient(self)
        menu_window.grab_set()
        
        self.update_idletasks()
        main_x = self.winfo_x()
        main_y = self.winfo_y()
        main_w = self.winfo_width()
        main_h = self.winfo_height()
        
        menu_window.update_idletasks()
        menu_w = menu_window.winfo_width()
        menu_h = menu_window.winfo_height()

        center_x = main_x + (main_w // 2) - (menu_w // 2)
        center_y = main_y + (main_h // 2) - (menu_h // 2)
        
        menu_window.geometry(f"+{center_x}+{center_y}")
        menu_window.resizable(False, False)

        self.wait_window(menu_window) 

    
    def apply_theme_colors(self):
        if self.current_theme == "light":
            header_bg = COLOR_BG_LIGHT
            content_bg = COLOR_BG_WHITE
            logo_text_fg = COLOR_ORANGE
        else:
            header_bg = COLOR_DARK_BG_ALT
            content_bg = COLOR_DARK_BG    
            logo_text_fg = COLOR_ORANGE
            
        self.configure(bg=content_bg)

        self.header_frame.configure(bg=header_bg)
        
        self.header_logo_label.configure(bg=header_bg)
        try:
            self.header_logo_label.configure(fg=logo_text_fg)
        except tk.TclError:
            pass 

        self.container.configure(bg=content_bg)
        self.canvas.configure(bg=content_bg)
        self.scrollable_frame.configure(bg=content_bg)

    def toggle_theme(self):
        if self.current_theme == "light":
            self.current_theme = "dark"
            print("Trocando para tema escuro.")
        else:
            self.current_theme = "light"
            print("Trocando para tema claro.")
        
        self.apply_theme_colors() 
        
        self.clear_content()
        self.populate_content()
    

if __name__ == "__main__":
    app = DataWarehouseApp()
    app.mainloop()