import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from DataManager import DataManager

class PasswordManagerGUI:
    """Classe responsável pela interface gráfica"""

    def __init__(self, root):
        self.root = root
        self.root.title("Email and Password Manager")
        self.root.geometry("900x650")
        self.root.minsize(700, 500)

        # Instanciar gerenciador de dados e se registrar como observador
        self.manager = DataManager()
        self.manager.add_observer(self._update_list)

        self.selected_entry_id = None
        self._create_interface()
        self._update_list()

    def _create_interface(self):
        """Cria toda a interface gráfica"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Título
        ttk.Label(main_frame, text="Email and Password Manager",
                  font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 20))

        self._create_entry_frame(main_frame)
        self._create_list_frame(main_frame)
        self._configure_resizing(main_frame)

    def _create_entry_frame(self, parent):
        """Cria o frame de entrada de dados"""
        entry_frame = ttk.LabelFrame(parent, text="Add/Edit Entry", padding="10")
        entry_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))

        # Variáveis de controle
        self.site_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.notes_var = tk.StringVar()

        # Campos de entrada
        fields = [
            ("Site/Service:", self.site_var, 20),
            ("Email:", self.email_var, 25),
            ("Password:", self.password_var, 20),
            ("Notes:", self.notes_var, 25)
        ]

        for i, (label, var, width) in enumerate(fields):
            row, col = i // 2, (i % 2) * 2
            ttk.Label(entry_frame, text=label).grid(
                row=row, column=col, sticky=tk.W, padx=(0 if col == 0 else 10, 5)
            )
            entry = ttk.Entry(entry_frame, textvariable=var, width=width)
            if label == "Password:":
                entry.config(show="*")
            entry.grid(row=row, column=col + 1, padx=5, pady=2)

        self._create_entry_buttons(entry_frame)

    def _create_entry_buttons(self, parent):
        """Cria os botões do frame de entrada"""
        btn_frame = ttk.Frame(parent)
        btn_frame.grid(row=2, column=0, columnspan=4, pady=10)

        buttons = [
            ("Add", self._add_entry, "normal"),
            ("Update", self._update_entry, "disabled"),
            ("Generate Password", self._generate_password, "normal"),
            ("Clear", self._clear_fields, "normal")
        ]

        self.entry_buttons = {}
        for i, (text, command, state) in enumerate(buttons):
            btn = ttk.Button(btn_frame, text=text, command=command, state=state)
            btn.grid(row=0, column=i, padx=5)
            self.entry_buttons[text.lower().replace(" ", "_")] = btn

    def _create_list_frame(self, parent):
        """Cria o frame da lista de senhas"""
        list_frame = ttk.LabelFrame(parent, text="Saved Passwords", padding="10")
        list_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))

        self._create_treeview(list_frame)
        self._create_list_buttons(list_frame)
        self._create_search(list_frame)

    def _create_treeview(self, parent):
        """Cria o treeview para exibir as senhas"""
        columns = ("ID", "Site", "Email", "Password", "Notes", "Created Date")
        self.tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)

        # Configurar colunas
        widths = [50, 150, 200, 100, 150, 120]
        for col, width in zip(columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)

        # Scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Bind duplo clique
        self.tree.bind("<Double-1>", lambda e: self._edit_entry())

    def _create_list_buttons(self, parent):
        """Cria os botões do frame da lista"""
        btn_list_frame = ttk.Frame(parent)
        btn_list_frame.grid(row=1, column=0, columnspan=2, pady=10)

        buttons = [
            ("Edit", self._edit_entry),
            ("Delete", self._delete_entry),
            ("Copy Password", self._copy_password),
            ("Show Password", self._show_password)
        ]

        for i, (text, command) in enumerate(buttons):
            ttk.Button(btn_list_frame, text=text, command=command).grid(row=0, column=i, padx=5)

    def _create_search(self, parent):
        """Cria o campo de busca"""
        search_frame = ttk.Frame(parent)
        search_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))

        ttk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self._update_list())
        ttk.Entry(search_frame, textvariable=self.search_var, width=30).grid(row=0, column=1, padx=5)

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
                messagebox.showinfo("Success", success_message)
            return result
        except ValueError as e:
            messagebox.showwarning("Warning", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))
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
            messagebox.showwarning("Warning", "No entry selected!")
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
            messagebox.showwarning("Warning", "Select an entry to delete!")
            return

        if messagebox.askyesno("Confirm", f"Delete entry ID {entry_id}?"):
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
            messagebox.showwarning("Warning", "Select an entry to edit!")
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
        """Gera uma senha segura"""
        length = simpledialog.askinteger("Generate Password", "Length (4-50):",
                                         minvalue=4, maxvalue=50, initialvalue=12)
        if length:
            include_symbols = messagebox.askyesno("Generate Password", "Include special symbols?")
            password = self.manager.generate_secure_password(length, include_symbols)
            self.password_var.set(password)

    def _copy_password(self):
        """Copia senha para área de transferência"""
        entry_id = self._get_selected_entry_id()
        if entry_id:
            entry = self.manager.find_by_id(entry_id)
            if entry:
                self.root.clipboard_clear()
                self.root.clipboard_append(entry['password'])
                messagebox.showinfo("Success", "Password copied to clipboard!")

    def _show_password(self):
        """Mostra senha em popup"""
        entry_id = self._get_selected_entry_id()
        if entry_id:
            entry = self.manager.find_by_id(entry_id)
            if entry:
                messagebox.showinfo("Password", f"Password for {entry['site']}:\n{entry['password']}")

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

        # Adicionar entradas à lista
        for entry in entries:
            # Verificar se todos os campos necessários existem
            entry_id = entry.get('id', 'N/A')
            site = entry.get('site', 'N/A')
            email = entry.get('email', 'N/A')
            password = entry.get('password', '')
            notes = entry.get('notes', '')
            created_date = entry.get('created_date', entry.get('data', 'N/A'))

            masked_password = "*" * len(password) if password else ""

            self.tree.insert("", "end", values=(
                entry_id, site, email, masked_password, notes, created_date
            ))


