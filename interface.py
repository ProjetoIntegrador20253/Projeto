import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import psycopg2
from dotenv import load_dotenv
import locale
from datetime import datetime

try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except:
    locale.setlocale(locale.LC_ALL, '')

load_dotenv()
DB_SETTINGS = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

COLOR_ORANGE = "#F48B2C"
COLOR_GREEN = "#9CC93D"
COLOR_GREY = "#6D6E71"
COLOR_RED = "#E74C3C"
COLOR_BLUE = "#3498DB"
COLOR_BG_WHITE = "#FFFFFF"   
COLOR_BG_LIGHT = "#FEF5EC"   

COLOR_DARK_BG = "#2E2E2E"       
COLOR_DARK_BG_ALT = "#3A3A3A"   
COLOR_DARK_FG = "#EAEAEA"       

class DataWarehouseApp(tk.Tk):
    
    def __init__(self):
        super().__init__()

        self.title("Painel de Controle & Gestão - Ulabum Buffet")
        self.geometry("1150x900") 
        self.header_logo_filename = "Logotipo-Oficial-Ulabum_Logotipo-3-Colorido-.png"
        self.menu_logo_filename = "Logotipo-Oficial-Ulabum_Logotipo-2-Colorido-.png"
        self.current_theme = "light"

        self.create_header()
        self.create_scrollable_content()
        self.apply_theme_colors()
        self.populate_content()
        self.setup_key_bindings()

    def get_db_connection(self):
        try:
            conn = psycopg2.connect(**DB_SETTINGS)
            return conn
        except Exception as e:
            messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ao banco:\n{e}")
            return None

    def fetch_kpis(self):
        conn = self.get_db_connection()
        if not conn: return (0, 0, 0)
        try:
            cursor = conn.cursor()
            query = """
                SELECT 
                    COALESCE(SUM(faturamento), 0), 
                    COALESCE(SUM(lucro_total), 0),
                    COUNT(*)
                FROM fato_evento 
                WHERE status = 'Confirmado'
            """
            cursor.execute(query)
            result = cursor.fetchone()
            conn.close()
            return result
        except Exception as e:
            print(f"Erro ao buscar KPIs: {e}")
            return (0, 0, 0)

    def fetch_funnel(self):
        conn = self.get_db_connection()
        if not conn: return []
        try:
            cursor = conn.cursor()
            query = """
                SELECT status, COUNT(*), SUM(faturamento) 
                FROM fato_evento 
                GROUP BY status 
                ORDER BY SUM(faturamento) DESC
            """
            cursor.execute(query)
            result = cursor.fetchall()
            conn.close()
            return result
        except:
            return []

    def fetch_pending_events(self):
        conn = self.get_db_connection()
        if not conn: return []
        try:
            cursor = conn.cursor()
            query = """
                SELECT 
                    f.sk_evento, p.nome, v.nome, f.faturamento, f.tipo_evento, t.data,
                    f.qtd_adultos, f.qtd_criancas
                FROM fato_evento f
                JOIN dim_prospect p ON f.fk_prospect = p.id_prospect
                JOIN dim_vendedor v ON f.fk_vendedor = v.id_vendedor
                JOIN dim_tempo t ON f.fk_tempo = t.id_tempo
                WHERE f.status = 'Pendente'
                ORDER BY t.data ASC
            """
            cursor.execute(query)
            result = cursor.fetchall()
            conn.close()
            return result
        except Exception as e:
            print(e)
            return []

    def fetch_confirmed_events(self):
        conn = self.get_db_connection()
        if not conn: return []
        try:
            cursor = conn.cursor()
            query = """
                SELECT 
                    f.sk_evento, p.nome, v.nome, f.faturamento, f.tipo_evento, t.data,
                    f.qtd_adultos, f.qtd_criancas
                FROM fato_evento f
                JOIN dim_prospect p ON f.fk_prospect = p.id_prospect
                JOIN dim_vendedor v ON f.fk_vendedor = v.id_vendedor
                JOIN dim_tempo t ON f.fk_tempo = t.id_tempo
                WHERE f.status = 'Confirmado'
                ORDER BY t.data DESC
                LIMIT 20
            """
            cursor.execute(query)
            result = cursor.fetchall()
            conn.close()
            return result
        except Exception as e:
            print(e)
            return []

    def update_event_status(self, sk_evento, new_status):
        conn = self.get_db_connection()
        if not conn: return
        try:
            cursor = conn.cursor()
            query = "UPDATE fato_evento SET status = %s WHERE sk_evento = %s"
            cursor.execute(query, (new_status, sk_evento))
            conn.commit()
            conn.close()
            self.refresh_data() 
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao atualizar status:\n{e}")

    def update_event_details(self, sk_evento, novo_faturamento, novos_adultos, novas_criancas):
        conn = self.get_db_connection()
        if not conn: return
        try:
            cursor = conn.cursor()
            faturamento_float = float(novo_faturamento)
            novo_custo = faturamento_float * 0.60
            novo_lucro = faturamento_float - novo_custo
            novo_total_pessoas = int(novos_adultos) + int(novas_criancas)

            query = """
                UPDATE fato_evento 
                SET faturamento = %s, 
                    qtd_adultos = %s, 
                    qtd_criancas = %s,
                    custo = %s,
                    lucro_total = %s,
                    total_pessoas = %s
                WHERE sk_evento = %s
            """
            cursor.execute(query, (faturamento_float, novos_adultos, novas_criancas, novo_custo, novo_lucro, novo_total_pessoas, sk_evento))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Dados do evento atualizados com sucesso!")
            self.refresh_data()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar dados:\n{e}")

    def open_edit_window(self, evento_data):
        sk_evento, cliente, vendedor, valor, tipo, data, qtd_adultos, qtd_criancas = evento_data
        
        edit_window = tk.Toplevel(self)
        edit_window.title(f"Editar Evento #{sk_evento} - {cliente}")
        edit_window.geometry("400x400")
        edit_window.configure(bg=COLOR_BG_WHITE)
        
        lbl_font = ("Arial", 10, "bold")
        entry_font = ("Arial", 10)
        
        tk.Label(edit_window, text=f"Editando: {cliente}", font=("Arial", 14, "bold"), fg=COLOR_ORANGE, bg=COLOR_BG_WHITE).pack(pady=15)

        form_frame = tk.Frame(edit_window, bg=COLOR_BG_WHITE)
        form_frame.pack(padx=20, pady=10, fill="x")

        tk.Label(form_frame, text="Faturamento (R$):", font=lbl_font, bg=COLOR_BG_WHITE).grid(row=0, column=0, sticky="w", pady=5)
        entry_valor = tk.Entry(form_frame, font=entry_font)
        entry_valor.insert(0, str(valor))
        entry_valor.grid(row=0, column=1, sticky="ew", pady=5)

        tk.Label(form_frame, text="Qtd. Adultos:", font=lbl_font, bg=COLOR_BG_WHITE).grid(row=1, column=0, sticky="w", pady=5)
        entry_adultos = tk.Entry(form_frame, font=entry_font)
        entry_adultos.insert(0, str(qtd_adultos))
        entry_adultos.grid(row=1, column=1, sticky="ew", pady=5)

        tk.Label(form_frame, text="Qtd. Crianças:", font=lbl_font, bg=COLOR_BG_WHITE).grid(row=2, column=0, sticky="w", pady=5)
        entry_criancas = tk.Entry(form_frame, font=entry_font)
        entry_criancas.insert(0, str(qtd_criancas))
        entry_criancas.grid(row=2, column=1, sticky="ew", pady=5)

        form_frame.columnconfigure(1, weight=1)

        def save_action():
            try:
                v = float(entry_valor.get())
                a = int(entry_adultos.get())
                c = int(entry_criancas.get())
                self.update_event_details(sk_evento, v, a, c)
                edit_window.destroy()
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")

        btn_save = tk.Button(edit_window, text="💾 Salvar Alterações", bg=COLOR_GREEN, fg="white", font=("Arial", 11, "bold"), command=save_action)
        btn_save.pack(pady=20, fill="x", padx=20)

    def create_header(self):
        self.header_frame = tk.Frame(self, bg=COLOR_BG_LIGHT, height=100)
        self.header_frame.pack(side="top", fill="x")
        self.header_frame.pack_propagate(False)

        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(script_dir, self.header_logo_filename)
            if not os.path.exists(image_path):
                self.header_logo_label = tk.Label(self.header_frame, text="ULABUM DW", font=("Arial", 20, "bold"), fg=COLOR_ORANGE, bg=COLOR_BG_LIGHT)
            else:
                pil_image = Image.open(image_path)
                w, h = pil_image.size
                new_h = 80
                new_w = int(new_h * (w / h))
                pil_image = pil_image.resize((new_w, new_h), Image.Resampling.LANCZOS)
                self.logo_tk = ImageTk.PhotoImage(pil_image)
                self.header_logo_label = tk.Label(self.header_frame, image=self.logo_tk, bg=COLOR_BG_LIGHT)
                self.header_logo_label.image = self.logo_tk
            self.header_logo_label.pack(side="left", padx=20, pady=10)
        except:
            self.header_logo_label = tk.Label(self.header_frame, text="ULABUM", font=("Arial", 20, "bold"), fg=COLOR_ORANGE, bg=COLOR_BG_LIGHT)
            self.header_logo_label.pack(side="left", padx=20, pady=10)

        refresh_button = tk.Button(
            self.header_frame, text="Atualizar", font=("Arial", 12, "bold"),
            bg=COLOR_GREEN, fg="white", command=self.refresh_data, relief="flat",
            cursor="hand2", padx=15, pady=5
        )
        refresh_button.pack(side="right", padx=20, pady=10)

    def create_scrollable_content(self):
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True, padx=10, pady=10)
        self.canvas = tk.Canvas(self.container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def populate_content(self):
        if self.current_theme == "light":
            bg_main = COLOR_BG_WHITE
            bg_card = "#F9F9F9"
            fg_title = COLOR_ORANGE
            fg_text = COLOR_GREY
            fg_value = "#333333"
        else:
            bg_main = COLOR_DARK_BG
            bg_card = COLOR_DARK_BG_ALT
            fg_title = COLOR_ORANGE
            fg_text = "#AAAAAA"
            fg_value = COLOR_DARK_FG
            
        self.scrollable_frame.configure(bg=bg_main)

        faturamento, lucro, qtd_vendas = self.fetch_kpis()
        funnel_data = self.fetch_funnel()
        pending_events = self.fetch_pending_events()
        confirmed_events = self.fetch_confirmed_events()

        kpi_frame = tk.Frame(self.scrollable_frame, bg=bg_main)
        kpi_frame.pack(fill="x", padx=10, pady=10)
        kpi_frame.columnconfigure(0, weight=1)
        kpi_frame.columnconfigure(1, weight=1)
        kpi_frame.columnconfigure(2, weight=1)

        self.create_kpi_card(kpi_frame, "Faturamento Confirmado", self.format_money(faturamento), COLOR_BLUE, bg_card, fg_text, fg_value, 0)
        self.create_kpi_card(kpi_frame, "Lucro Realizado", self.format_money(lucro), COLOR_GREEN, bg_card, fg_text, fg_value, 1)
        self.create_kpi_card(kpi_frame, "Contratos Fechados", str(qtd_vendas), COLOR_ORANGE, bg_card, fg_text, fg_value, 2)

        tk.Label(self.scrollable_frame, text="Funil de Vendas", font=("Arial", 14, "bold"), fg=fg_title, bg=bg_main, anchor="w").pack(fill="x", padx=20, pady=(30, 10))
        
        funnel_frame = tk.Frame(self.scrollable_frame, bg=bg_main)
        funnel_frame.pack(fill="x", padx=20)

        for status, count, total_val in funnel_data:
            row = tk.Frame(funnel_frame, bg=bg_card, pady=5)
            row.pack(fill="x", pady=2)
            
            tk.Label(row, text=status, font=("Arial", 11, "bold"), width=15, anchor="w", bg=bg_card, fg=fg_value).pack(side="left", padx=10)
            tk.Label(row, text=f"{count}", font=("Arial", 10), width=5, anchor="w", bg=bg_card, fg=fg_text).pack(side="left")
            
            total_base = faturamento + sum(x[2] for x in funnel_data if x[0] != 'Confirmado')
            bar_width = min(int(total_val / (total_base + 1) * 400), 400) 
            
            bar_color = COLOR_GREEN if status == 'Confirmado' else (COLOR_RED if status == 'Cancelado' else COLOR_ORANGE)
            tk.Frame(row, bg=bar_color, height=12, width=bar_width).pack(side="left", padx=10)
            
            tk.Label(row, text=self.format_money(total_val), font=("Arial", 10, "bold"), bg=bg_card, fg=fg_value).pack(side="right", padx=10)

        tk.Label(self.scrollable_frame, text="⚠️ Gestão de Eventos Pendentes", font=("Arial", 14, "bold"), fg=COLOR_RED, bg=bg_main, anchor="w").pack(fill="x", padx=20, pady=(20, 10))
        
        if not pending_events:
            tk.Label(self.scrollable_frame, text="Nenhum evento pendente.", font=("Arial", 11, "italic"), fg=fg_text, bg=bg_main, anchor="w").pack(padx=20)
        else:
            header_pend = tk.Frame(self.scrollable_frame, bg=COLOR_GREY)
            header_pend.pack(fill="x", padx=20)
            cols = ["Data", "Cliente", "Vendedor", "Valor", "Ações"]
            widths = [15, 25, 20, 15, 30]
            for col, w in zip(cols, widths):
                tk.Label(header_pend, text=col, font=("Arial", 10, "bold"), bg=COLOR_GREY, fg="white", width=w, anchor="w").pack(side="left", padx=5, pady=5)

            for row_data in pending_events:
                sk_evento, cliente, vendedor, valor, tipo, data, adultos, criancas = row_data
                
                bg_row = bg_card
                row_frame = tk.Frame(self.scrollable_frame, bg=bg_row, pady=2)
                row_frame.pack(fill="x", padx=20)
                
                data_fmt = data.strftime('%d/%m/%Y') if data else "-"
                
                tk.Label(row_frame, text=data_fmt, font=("Arial", 10), bg=bg_row, fg=fg_text, width=widths[0], anchor="w").pack(side="left", padx=5)
                tk.Label(row_frame, text=cliente, font=("Arial", 10, "bold"), bg=bg_row, fg=fg_value, width=widths[1], anchor="w").pack(side="left", padx=5)
                tk.Label(row_frame, text=vendedor, font=("Arial", 10), bg=bg_row, fg=fg_text, width=widths[2], anchor="w").pack(side="left", padx=5)
                tk.Label(row_frame, text=self.format_money(valor), font=("Arial", 10), bg=bg_row, fg=fg_value, width=widths[3], anchor="w").pack(side="left", padx=5)
                
                action_frame = tk.Frame(row_frame, bg=bg_row, width=widths[4])
                action_frame.pack(side="left", padx=5)
                
                btn_edit = tk.Button(action_frame, text="✏️ Editar", font=("Arial", 9), bg=COLOR_BLUE, fg="white", relief="flat", cursor="hand2", command=lambda d=row_data: self.open_edit_window(d))
                btn_edit.pack(side="left", padx=2)

                btn_conf = tk.Button(action_frame, text="✅", font=("Arial", 9), bg=COLOR_GREEN, fg="white", relief="flat", cursor="hand2", command=lambda id=sk_evento: self.update_event_status(id, 'Confirmado'))
                btn_conf.pack(side="left", padx=2)
                
                btn_canc = tk.Button(action_frame, text="❌", font=("Arial", 9), bg=COLOR_RED, fg="white", relief="flat", cursor="hand2", command=lambda id=sk_evento: self.update_event_status(id, 'Cancelado'))
                btn_canc.pack(side="left", padx=2)

        tk.Label(self.scrollable_frame, text="✅ Eventos Confirmados (Últimos 20)", font=("Arial", 14, "bold"), fg=COLOR_GREEN, bg=bg_main, anchor="w").pack(fill="x", padx=20, pady=(30, 10))
        
        if not confirmed_events:
             tk.Label(self.scrollable_frame, text="Nenhum evento confirmado ainda.", font=("Arial", 11, "italic"), fg=fg_text, bg=bg_main, anchor="w").pack(padx=20)
        else:
            header_conf = tk.Frame(self.scrollable_frame, bg=COLOR_ORANGE)
            header_conf.pack(fill="x", padx=20)
            cols = ["Data", "Cliente", "Vendedor", "Valor", "Ações"]
            widths = [15, 25, 20, 15, 25]
            for col, w in zip(cols, widths):
                tk.Label(header_conf, text=col, font=("Arial", 10, "bold"), bg=COLOR_ORANGE, fg="white", width=w, anchor="w").pack(side="left", padx=5, pady=5)

            for row_data in confirmed_events:
                sk_evento, cliente, vendedor, valor, tipo, data, adultos, criancas = row_data
                
                bg_row = bg_main
                row_frame = tk.Frame(self.scrollable_frame, bg=bg_row, pady=2)
                row_frame.pack(fill="x", padx=20)
                
                data_fmt = data.strftime('%d/%m/%Y') if data else "-"
                
                tk.Label(row_frame, text=data_fmt, font=("Arial", 10), bg=bg_row, fg=fg_text, width=widths[0], anchor="w").pack(side="left", padx=5)
                tk.Label(row_frame, text=cliente, font=("Arial", 10, "bold"), bg=bg_row, fg=fg_value, width=widths[1], anchor="w").pack(side="left", padx=5)
                tk.Label(row_frame, text=vendedor, font=("Arial", 10), bg=bg_row, fg=fg_text, width=widths[2], anchor="w").pack(side="left", padx=5)
                tk.Label(row_frame, text=self.format_money(valor), font=("Arial", 10, "bold"), bg=bg_row, fg=COLOR_GREEN, width=widths[3], anchor="w").pack(side="left", padx=5)
                
                action_frame = tk.Frame(row_frame, bg=bg_row, width=widths[4])
                action_frame.pack(side="left", padx=5)
                
                btn_edit = tk.Button(action_frame, text="✏️ Editar", font=("Arial", 9), bg=COLOR_BLUE, fg="white", relief="flat", cursor="hand2", command=lambda d=row_data: self.open_edit_window(d))
                btn_edit.pack(side="left", padx=2)
                
                btn_canc = tk.Button(action_frame, text="❌ Cancelar", font=("Arial", 9), bg=COLOR_RED, fg="white", relief="flat", cursor="hand2", command=lambda id=sk_evento: self.update_event_status(id, 'Cancelado'))
                btn_canc.pack(side="left", padx=5)


    def create_kpi_card(self, parent, title, value, accent_color, bg_color, fg_title, fg_val, col_idx):
        card = tk.Frame(parent, bg=bg_color, padx=15, pady=15, highlightbackground=accent_color, highlightthickness=1)
        card.grid(row=0, column=col_idx, sticky="ew", padx=10)
        tk.Label(card, text=title, font=("Arial", 10, "bold"), fg=fg_title, bg=bg_color).pack(anchor="w")
        tk.Label(card, text=value, font=("Arial", 18, "bold"), fg=accent_color, bg=bg_color).pack(anchor="w", pady=(5,0))

    def format_money(self, value):
        try:
            return locale.currency(value, grouping=True)
        except:
            return f"R$ {value:,.2f}"

    def clear_content(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def refresh_data(self):
        self.clear_content()
        bg_main = COLOR_BG_WHITE if self.current_theme == "light" else COLOR_DARK_BG
        fg_text = COLOR_GREY if self.current_theme == "light" else COLOR_DARK_FG
        
        loading_label = tk.Label(self.scrollable_frame, text="Recarregando dados...", font=("Arial", 14, "italic"), fg=fg_text, bg=bg_main)
        loading_label.pack(pady=50)
        
        self.update_idletasks()
        self.after(300, self.finish_refresh)

    def finish_refresh(self):
        self.clear_content()
        self.populate_content()

    def setup_key_bindings(self):
        self.bind('<F5>', lambda event=None: self.refresh_data())
        self.bind('<Escape>', lambda event=None: self.open_main_menu())
        
    def close_app(self):
        self.destroy()

    def open_main_menu(self):
        menu_window = tk.Toplevel(self)
        menu_window.title("Menu")
        menu_window.configure(bg=COLOR_BG_WHITE)
        tk.Label(menu_window, text="MENU", font=("Arial", 20, "bold"), bg=COLOR_BG_WHITE, fg=COLOR_ORANGE).pack(pady=20)
        tk.Button(menu_window, text="Alternar Tema", command=lambda: [self.toggle_theme(), menu_window.destroy()], bg=COLOR_GREY, fg="white").pack(fill="x", padx=20, pady=5)
        tk.Button(menu_window, text="Fechar", command=self.close_app, bg=COLOR_RED, fg="white").pack(fill="x", padx=20, pady=5)

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
        self.header_logo_label.configure(bg=header_bg, fg=logo_text_fg)
        self.container.configure(bg=content_bg)
        self.canvas.configure(bg=content_bg)
        self.scrollable_frame.configure(bg=content_bg)

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme_colors()
        self.refresh_data()

if __name__ == "__main__":
    app = DataWarehouseApp()
    app.mainloop()