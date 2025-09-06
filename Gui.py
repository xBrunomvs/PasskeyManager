import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from ttkthemes import ThemedTk, ThemedStyle
from DataManager import DataManager


class PasswordManagerGUI:
    """Classe responsável pela interface gráfica com suporte a temas"""

    def __init__(self, root=None):
        # Se não foi passado um root, criar um ThemedTk
        if root is None:
            self.root = ThemedTk(theme="arc")  # Tema padrão moderno
        else:
            self.root = root

        self.root.title("Email and Password Manager")
        self.root.geometry("900x650")
        self.root.minsize(700, 500)

        # Configurar estilo se não for ThemedTk
        if not isinstance(self.root, ThemedTk):
            self.style = ThemedStyle(self.root)
            self.style.set_theme("arc")  # Tema padrão
        else:
            self.style = None

        # Instanciar gerenciador de dados e se registrar como observador
        self.manager = DataManager()
        self.manager.add_observer(self._update_list)

        self.selected_entry_id = None
        self._create_interface()
        self._update_list()

    def change_theme(self, theme_name):
        """Muda o tema da aplicação"""
        try:
            if isinstance(self.root, ThemedTk):
                self.root.set_theme(theme_name)
            elif self.style:
                self.style.set_theme(theme_name)

            # Forçar atualização da interface
            self.root.update()
            messagebox.showinfo("Theme Changed", f"Theme changed to: {theme_name}")
        except Exception as e:
            messagebox.showerror("Theme Error", f"Could not apply theme '{theme_name}': {str(e)}")

    def _get_available_themes(self):
        """Retorna lista de temas disponíveis"""
        try:
            if isinstance(self.root, ThemedTk):
                return self.root.get_themes()
            elif self.style:
                return self.style.theme_names()
            else:
                return ["default", "clam", "alt", "classic"]
        except:
            return ["arc", "equilux", "adapta", "yaru", "breeze", "aqua"]

    def _create_interface(self):
        """Cria toda a interface gráfica"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Título e seleção de tema
        self._create_header(main_frame)
        self._create_entry_frame(main_frame)
        self._create_list_frame(main_frame)
        self._configure_resizing(main_frame)

    def _create_header(self, parent):
        """Cria o cabeçalho com título e seletor de tema"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))

        # Título
        ttk.Label(header_frame, text="Email and Password Manager",
                  font=("Arial", 16, "bold")).grid(row=0, column=0, sticky=tk.W)

        # Frame para seletor de tema
        theme_frame = ttk.Frame(header_frame)
        theme_frame.grid(row=0, column=1, sticky=tk.E)

        ttk.Label(theme_frame, text="Theme:").grid(row=0, column=0, padx=(0, 5))

        self.theme_var = tk.StringVar()
        theme_combo = ttk.Combobox(theme_frame, textvariable=self.theme_var,
                                   values=self._get_available_themes(),
                                   state="readonly", width=15)
        theme_combo.grid(row=0, column=1, padx=(0, 10))
        theme_combo.bind("<<ComboboxSelected>>", lambda e: self.change_theme(self.theme_var.get()))

        # Definir tema atual
        current_theme = "arc"  # padrão
        if isinstance(self.root, ThemedTk):
            try:
                current_theme = self.root.tk.call("ttk::style", "theme", "use")
            except:
                current_theme = "arc"
        self.theme_var.set(current_theme)

        # Configurar peso das colunas do header
        header_frame.columnconfigure(0, weight=1)
        header_frame.columnconfigure(1, weight=0)

    def _create_entry_frame(self, parent):
        """Cria o frame de entrada de dados"""
        entry_frame = ttk.LabelFrame(parent, text="Add/Edit Entry", padding="10")
        entry_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))

        # Variáveis de controle
        self.site_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.notes_var = tk.StringVar()

        # Campos de entrada com melhor layout
        fields = [
            ("Site/Service:", self.site_var, 20),
            ("Email:", self.email_var, 25),
            ("Password:", self.password_var, 20),
            ("Notes:", self.notes_var, 25)
        ]

        for i, (label, var, width) in enumerate(fields):
            row, col = i // 2, (i % 2) * 2

            # Label com estilo
            label_widget = ttk.Label(entry_frame, text=label)
            label_widget.grid(row=row, column=col, sticky=tk.W,
                              padx=(0 if col == 0 else 20, 5), pady=5)

            # Entry com estilo
            entry = ttk.Entry(entry_frame, textvariable=var, width=width, font=("Arial", 9))
            if label == "Password:":
                entry.config(show="*")
            entry.grid(row=row, column=col + 1, padx=5, pady=5, sticky=(tk.W, tk.E))

        self._create_entry_buttons(entry_frame)

        # Configurar expansão das colunas
        entry_frame.columnconfigure(1, weight=1)
        entry_frame.columnconfigure(3, weight=1)

    def _create_entry_buttons(self, parent):
        """Cria os botões do frame de entrada com estilos aprimorados"""
        btn_frame = ttk.Frame(parent)
        btn_frame.grid(row=3, column=0, columnspan=4, pady=15)

        buttons_config = [
            ("Add", self._add_entry, "normal", "Accent.TButton"),
            ("Update", self._update_entry, "disabled", "Accent.TButton"),
            ("Generate Password", self._generate_password, "normal", "TButton"),
            ("Clear", self._clear_fields, "normal", "TButton")
        ]

        self.entry_buttons = {}
        for i, (text, command, state, style) in enumerate(buttons_config):
            try:
                btn = ttk.Button(btn_frame, text=text, command=command,
                                 state=state, style=style)
            except:
                # Fallback se o estilo não existir
                btn = ttk.Button(btn_frame, text=text, command=command, state=state)

            btn.grid(row=0, column=i, padx=8, pady=5, sticky=(tk.W, tk.E))
            self.entry_buttons[text.lower().replace(" ", "_")] = btn

            # Configurar expansão
            btn_frame.columnconfigure(i, weight=1)

    def _create_list_frame(self, parent):
        """Cria o frame da lista de senhas"""
        list_frame = ttk.LabelFrame(parent, text="Saved Passwords", padding="10")
        list_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))

        self._create_search(list_frame)  # Busca no topo
        self._create_treeview(list_frame)
        self._create_list_buttons(list_frame)

    def _create_search(self, parent):
        """Cria o campo de busca no topo"""
        search_frame = ttk.Frame(parent)
        search_frame.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky=(tk.W, tk.E))

        ttk.Label(search_frame, text="🔍 Search:", font=("Arial", 9, "bold")).grid(row=0, column=0, padx=(0, 5))

        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self._update_list())

        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30, font=("Arial", 9))
        search_entry.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))

        # Botão para limpar busca
        clear_search_btn = ttk.Button(search_frame, text="✕", width=3,
                                      command=lambda: self.search_var.set(""))
        clear_search_btn.grid(row=0, column=2, padx=5)

        search_frame.columnconfigure(1, weight=1)

    def _create_treeview(self, parent):
        """Cria o treeview para exibir as senhas com estilo aprimorado"""
        # Frame para treeview e scrollbar
        tree_frame = ttk.Frame(parent)
        tree_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

        columns = ("ID", "Site", "Email", "Password", "Notes", "Created Date")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)

        # Configurar colunas com melhor layout
        column_config = {
            "ID": (50, tk.CENTER),
            "Site": (150, tk.W),
            "Email": (200, tk.W),
            "Password": (100, tk.CENTER),
            "Notes": (150, tk.W),
            "Created Date": (120, tk.CENTER)
        }

        for col in columns:
            width, anchor = column_config.get(col, (100, tk.W))
            self.tree.heading(col, text=col, anchor=tk.W)
            self.tree.column(col, width=width, anchor=anchor, minwidth=50)

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)

        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Grid layout
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))

        # Configurar expansão
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        # Bind duplo clique e seleção
        self.tree.bind("<Double-1>", lambda e: self._edit_entry())
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

    def _on_tree_select(self, event):
        """Callback para seleção no treeview"""
        pass  # Pode adicionar comportamentos futuros aqui

    def _create_list_buttons(self, parent):
        """Cria os botões do frame da lista com melhor layout"""
        btn_list_frame = ttk.Frame(parent)
        btn_list_frame.grid(row=2, column=0, columnspan=2, pady=10)

        buttons_config = [
            ("📝 Edit", self._edit_entry, "TButton"),
            ("🗑️ Delete", self._delete_entry, "TButton"),
            ("📋 Copy Password", self._copy_password, "TButton"),
            ("👁️ Show Password", self._show_password, "TButton")
        ]

        for i, (text, command, style) in enumerate(buttons_config):
            try:
                btn = ttk.Button(btn_list_frame, text=text, command=command, style=style)
            except:
                btn = ttk.Button(btn_list_frame, text=text, command=command)

            btn.grid(row=0, column=i, padx=5, pady=2, sticky=(tk.W, tk.E))
            btn_list_frame.columnconfigure(i, weight=1)

    def _configure_resizing(self, main_frame):
        """Configura o redimensionamento da janela"""
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

    def _get_selected_entry_id(self):
        """Obtém o ID da entrada selecionada na lista"""
        selection = self.tree.selection()
        if selection:
            return self.tree.item(selection[0])['values'][0]
        return None

    def _execute_operation(self, operation, success_message, **kwargs):
        """Executa uma operação com tratamento de erro padronizado"""
        try:
            result = operation(**kwargs)
            if success_message:
                messagebox.showinfo("✅ Success", success_message)
            return result
        except ValueError as e:
            messagebox.showwarning("⚠️ Warning", str(e))
        except Exception as e:
            messagebox.showerror("❌ Error", str(e))
        return None

    def _add_entry(self):
        """Adiciona nova entrada"""
        self._execute_operation(
            self.manager.add_entry,
            "Entry added successfully!",
            site=self.site_var.get(),
            email=self.email_var.get(),
            password=self.password_var.get(),
            notes=self.notes_var.get()
        )
        self._clear_fields()

    def _update_entry(self):
        """Atualiza entrada existente"""
        if not self.selected_entry_id:
            messagebox.showwarning("⚠️ Warning", "No entry selected!")
            return

        self._execute_operation(
            self.manager.update_entry,
            "Entry updated successfully!",
            entry_id=self.selected_entry_id,
            site=self.site_var.get(),
            email=self.email_var.get(),
            password=self.password_var.get(),
            notes=self.notes_var.get()
        )
        self._clear_fields()

    def _delete_entry(self):
        """Deleta entrada selecionada"""
        entry_id = self._get_selected_entry_id()
        if not entry_id:
            messagebox.showwarning("⚠️ Warning", "Select an entry to delete!")
            return

        if messagebox.askyesno("🗑️ Confirm Delete", f"Delete entry ID {entry_id}?\n\nThis action cannot be undone."):
            self._execute_operation(
                self.manager.delete_entry,
                "Entry deleted successfully!",
                entry_id=entry_id
            )
            self._clear_fields()

    def _edit_entry(self):
        """Carrega dados da entrada selecionada para edição"""
        entry_id = self._get_selected_entry_id()
        if not entry_id:
            messagebox.showwarning("⚠️ Warning", "Select an entry to edit!")
            return

        entry = self.manager.find_by_id(entry_id)
        if entry:
            self.selected_entry_id = entry_id
            self.site_var.set(entry['site'])
            self.email_var.set(entry['email'])
            self.password_var.set(entry['password'])
            self.notes_var.set(entry['notes'])

            self.entry_buttons['add'].config(state="disabled")
            self.entry_buttons['update'].config(state="normal")

    def _generate_password(self):
        """Gera uma senha segura com interface melhorada"""
        length = simpledialog.askinteger("🔐 Generate Password",
                                         "Password length (4-50):",
                                         minvalue=4, maxvalue=50, initialvalue=12)
        if length:
            include_symbols = messagebox.askyesno("🔐 Generate Password",
                                                  "Include special symbols?\n\n" +
                                                  "Yes = More secure\nNo = Only letters and numbers")
            password = self.manager.generate_secure_password(length, include_symbols)
            self.password_var.set(password)
            messagebox.showinfo("🔐 Password Generated",
                                f"Generated password: {password}\n\n" +
                                "Password has been filled in the form!")

    def _copy_password(self):
        """Copia senha para área de transferência"""
        entry_id = self._get_selected_entry_id()
        if entry_id:
            entry = self.manager.find_by_id(entry_id)
            if entry:
                self.root.clipboard_clear()
                self.root.clipboard_append(entry['password'])
                messagebox.showinfo("📋 Success", "Password copied to clipboard!")

    def _show_password(self):
        """Mostra senha em popup"""
        entry_id = self._get_selected_entry_id()
        if entry_id:
            entry = self.manager.find_by_id(entry_id)
            if entry:
                messagebox.showinfo("👁️ Password", f"Password for {entry['site']}:\n\n{entry['password']}")

    def _clear_fields(self):
        """Limpa todos os campos de entrada"""
        for var in [self.site_var, self.email_var, self.password_var, self.notes_var]:
            var.set("")
        self.selected_entry_id = None
        self.entry_buttons['add'].config(state="normal")
        self.entry_buttons['update'].config(state="disabled")

    def _update_list(self):
        """Atualiza a lista exibida (chamada automaticamente pelo padrão Observer)"""
        # Limpar lista atual
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Obter dados filtrados
        entries = self.manager.filter_entries(self.search_var.get())

        # Adicionar entradas à lista com cores alternadas
        for i, entry in enumerate(entries):
            # Verificar se todos os campos necessários existem
            entry_id = entry.get('id', 'N/A')
            site = entry.get('site', 'N/A')
            email = entry.get('email', 'N/A')
            password = entry.get('password', '')
            notes = entry.get('notes', '')
            created_date = entry.get('created_date', entry.get('data', 'N/A'))

            masked_password = "•" * min(len(password), 8) if password else ""

            # Inserir item com tag para cores alternadas
            item = self.tree.insert("", "end", values=(
                entry_id, site, email, masked_password, notes, created_date
            ), tags=('evenrow' if i % 2 == 0 else 'oddrow',))

        # Configurar tags de cores (se suportado pelo tema)
        try:
            self.tree.tag_configure('evenrow', background='#f0f0f0')
            self.tree.tag_configure('oddrow', background='white')
        except:
            pass  # Nem todos os temas suportam

