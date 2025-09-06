# Email and Password Manager

Um gerenciador de senhas simples e seguro desenvolvido em Python com interface gráfica usando Tkinter. Este aplicativo permite armazenar, gerenciar e organizar suas credenciais de forma segura com criptografia local.

## 🚀 Características

- **Interface Gráfica Intuitiva**: Interface limpa e fácil de usar construída com Tkinter
- **Armazenamento Seguro**: Senhas criptografadas com Base64 e armazenadas localmente
- **CRUD Completo**: Criar, ler, atualizar e deletar entradas
- **Busca e Filtros**: Sistema de busca em tempo real por site, email ou notas
- **Gerador de Senhas**: Gerador de senhas seguras com opções customizáveis
- **Validação de Dados**: Validação para evitar entradas duplicadas e dados inválidos
- **Padrão Observer**: Atualização automática da interface quando dados são modificados
- **Migração Automática**: Sistema de migração automática para manter compatibilidade

## 📋 Requisitos

- Python 3.6+
- Tkinter (geralmente incluído com Python)
- Bibliotecas padrão: `json`, `os`, `base64`, `secrets`, `string`, `datetime`

## 🛠️ Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/password-manager.git
cd password-manager
```

2. Execute o aplicativo:
```bash
python main.py
```

## 📁 Estrutura do Projeto

```
password-manager/
│
├── main.py              # Ponto de entrada da aplicação
├── DataManager.py       # Lógica de negócio e gerenciamento de dados
├── Gui.py              # Interface gráfica do usuário
├── password_data.json   # Arquivo de dados (criado automaticamente)
└── README.md           # Este arquivo
```

## 🎯 Como Usar

### Adicionando uma Nova Entrada
1. Preencha os campos "Site/Service", "Email", "Password" e "Notes" (opcional)
2. Clique em "Add" para salvar a entrada
3. A nova entrada aparecerá na lista automaticamente

### Editando uma Entrada
1. Clique duas vezes na entrada na lista OU selecione e clique em "Edit"
2. Os campos serão preenchidos automaticamente
3. Modifique os dados desejados
4. Clique em "Update" para salvar as alterações

### Gerando Senhas Seguras
1. Clique em "Generate Password"
2. Escolha o comprimento da senha (4-50 caracteres)
3. Decida se deseja incluir símbolos especiais
4. A senha será automaticamente inserida no campo

### Buscando Entradas
1. Use o campo "Search" na parte inferior
2. A busca é realizada em tempo real nos campos: site, email e notas
3. A lista é filtrada automaticamente conforme você digita

### Copiando Senhas
1. Selecione uma entrada na lista
2. Clique em "Copy Password"
3. A senha será copiada para a área de transferência

### Visualizando Senhas
1. Selecione uma entrada na lista
2. Clique em "Show Password"
3. A senha será exibida em um popup

## 🔒 Segurança

- **Criptografia**: As senhas são criptografadas usando Base64 antes de serem salvas
- **Armazenamento Local**: Todos os dados ficam armazenados localmente no seu computador
- **Validação**: Sistema de validação previne entradas duplicadas e dados inválidos
- **Mascaramento**: Senhas são mascaradas na interface principal

## 📊 Funcionalidades Técnicas

### DataManager (Lógica de Negócio)
- **Padrão Observer**: Notifica a interface sobre mudanças nos dados
- **CRUD Operations**: Operações completas de banco de dados
- **Validação de Dados**: Validação robusta de entrada
- **Migração Automática**: Atualiza estrutura de dados automaticamente
- **Gerador de Senhas**: Algoritmo seguro usando `secrets`

### GUI (Interface Gráfica)
- **Layout Responsivo**: Interface que se adapta ao redimensionamento
- **Treeview**: Exibição organizada dos dados em tabela
- **Binding de Eventos**: Integração completa com ações do usuário
- **Tratamento de Erros**: Feedback claro para o usuário

## 🔧 Personalização

### Modificando a Interface
- Edite `Gui.py` para alterar layout, cores ou comportamentos
- Ajuste tamanhos de janela modificando `geometry()` e `minsize()`

### Alterando Validações
- Modifique `_validate_entry()` em `DataManager.py` para suas necessidades
- Customize regras de duplicação em `_entry_exists()`

### Configurando Gerador de Senhas
- Altere caracteres disponíveis em `generate_secure_password()`
- Modifique limites de tamanho conforme necessário

## 🐛 Solução de Problemas

### Arquivo de Dados Corrompido
Se o arquivo `password_data.json` estiver corrompido:
1. Faça backup do arquivo (se possível)
2. Delete o arquivo corrompido
3. Execute o aplicativo (um novo arquivo será criado)

### Problemas de Permissão
Certifique-se de que o aplicativo tem permissão para:
- Ler/escrever no diretório do projeto
- Acessar a área de transferência

### Erro de Importação
Verifique se todas as dependências estão instaladas:
```bash
python -c "import tkinter; print('Tkinter OK')"
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 🔮 Roadmap

- [ ] Criptografia mais robusta (AES)
- [ ] Backup automático
- [ ] Import/Export de dados
- [ ] Temas customizáveis
- [ ] Autenticação por senha mestra
- [ ] Sincronização em nuvem

---

**⚠️ Aviso de Segurança**: Este é um projeto educacional. Para uso em produção, considere implementar criptografia mais robusta e medidas de segurança adicionais.
