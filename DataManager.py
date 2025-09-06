import json
import os
import base64
import secrets
import string
from datetime import datetime
class DataManager:
    """Classe responsável pelo gerenciamento dos dados (CRUD operations)"""

    def __init__(self, data_file="password_data.json"):
        self.data_file = data_file
        self.data = self._load_data()
        self._observers = []  # Lista de callbacks para notificar mudanças

    def add_observer(self, callback):
        """Adiciona um observador para mudanças nos dados"""
        self._observers.append(callback)

    def _notify_observers(self):
        """Notifica todos os observadores sobre mudanças"""
        for callback in self._observers:
            callback()

    def _load_data(self):
        """Carrega dados do arquivo JSON"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                    # Migração automática: adicionar IDs se não existirem
                    for i, item in enumerate(data):
                        if 'password' in item:
                            item['password'] = base64.b64decode(item['password'].encode()).decode()

                        # Adicionar ID se não existir
                        if 'id' not in item:
                            item['id'] = i + 1

                        # Adicionar campos de data se não existirem
                        if 'created_date' not in item:
                            item['created_date'] = item.get('data', datetime.now().strftime("%d/%m/%Y"))
                        if 'modified_date' not in item:
                            item['modified_date'] = item.get('data', datetime.now().strftime("%d/%m/%Y"))

                        # Garantir que notes existe
                        if 'notes' not in item:
                            item['notes'] = ""

                    # Salvar dados migrados
                    if data:
                        self._save_migrated_data(data)

                    return data
            except Exception as e:
                print(f"Error loading data: {e}")
        return []

    def _save_migrated_data(self, data):
        """Salva dados migrados temporariamente (usado durante carregamento)"""
        try:
            data_to_save = []
            for item in data:
                item_copy = item.copy()
                item_copy['password'] = base64.b64encode(item['password'].encode()).decode()
                data_to_save.append(item_copy)

            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving migrated data: {e}")

    def _save_data(self):
        """Salva dados no arquivo JSON"""

        try:
            data_to_save = []
            for item in self.data:
                item_copy = item.copy()
                item_copy['password'] = base64.b64encode(item['password'].encode()).decode()
                data_to_save.append(item_copy)

            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            raise Exception(f"Error saving data: {e}")

    def _generate_id(self):
        """Gera um ID único para nova entrada"""
        return max((entry.get('id', 0) for entry in self.data), default=0) + 1

    def _validate_entry(self, site, email, password):
        """Valida os dados de entrada"""
        if not site or not site.strip():
            raise ValueError("Site is required!")
        if not email or not email.strip():
            raise ValueError("Email is required!")
        if not password or not password.strip():
            raise ValueError("Password is required!")

    def _entry_exists(self, site, email, exclude_id=None):
        """Verifica se uma combinação site/email já existe"""
        for entry in self.data:
            if (entry.get('id') != exclude_id and
                    entry['site'].lower() == site.lower() and
                    entry['email'].lower() == email.lower()):
                return True
        return False

    def add_entry(self, site, email, password, notes=""):
        """Adiciona uma nova entrada"""
        self._validate_entry(site, email, password)

        if self._entry_exists(site, email):
            raise ValueError("This site and email combination already exists!")

        new_entry = {
            'id': self._generate_id(),
            'site': site.strip(),
            'email': email.strip(),
            'password': password.strip(),
            'notes': notes.strip(),
            'created_date': datetime.now().strftime("%d/%m/%Y %H:%M"),
            'modified_date': datetime.now().strftime("%d/%m/%Y %H:%M")
        }

        self.data.append(new_entry)
        self._save_data()
        self._notify_observers()
        return new_entry

    def update_entry(self, entry_id, **kwargs):
        """Atualiza uma entrada existente"""
        entry = self.find_by_id(entry_id)
        if not entry:
            raise ValueError("Entry not found!")

        # Extrair valores para validação
        site = kwargs.get('site', entry['site'])
        email = kwargs.get('email', entry['email'])
        password = kwargs.get('password', entry['password'])

        self._validate_entry(site, email, password)

        if self._entry_exists(site, email, entry_id):
            raise ValueError("This site and email combination already exists!")

        # Atualizar campos
        entry.update({
            'site': site.strip(),
            'email': email.strip(),
            'password': password.strip(),
            'notes': kwargs.get('notes', entry['notes']).strip(),
            'modified_date': datetime.now().strftime("%d/%m/%Y %H:%M")
        })

        self._save_data()
        self._notify_observers()
        return entry

    def delete_entry(self, entry_id):
        """Deleta uma entrada"""
        entry = self.find_by_id(entry_id)
        if not entry:
            raise ValueError("Entry not found!")

        self.data.remove(entry)
        self._save_data()
        self._notify_observers()
        return True

    def find_by_id(self, entry_id):
        """Busca entrada por ID"""
        for entry in self.data:
            if entry.get('id') == entry_id:
                return entry
        return None

    def filter_entries(self, search_term=""):
        """Filtra entradas por termo de busca"""
        if not search_term:
            return self.data.copy()

        term = search_term.lower()
        return [entry for entry in self.data
                if (term in entry['site'].lower() or
                    term in entry['email'].lower() or
                    term in entry['notes'].lower())]

    def get_all_entries(self):
        """Retorna todas as entradas"""
        return self.data.copy()

    def generate_secure_password(self, length=12, include_symbols=True):
        """Gera uma senha segura"""
        length = max(4, min(50, length))
        characters = string.ascii_letters + string.digits
        if include_symbols:
            characters += "!@#$%^&*"
        return ''.join(secrets.choice(characters) for _ in range(length))

