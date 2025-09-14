# Controle de Estoque - Flask Application 🛠️📦
Este projeto é uma aplicação web para controle de estoque, desenvolvida com Flask, que permite a gestão de produtos, entrada/saída de mercadorias, e gerenciamento de usuários com permissões específicas. Existem dois tipos de usuários: Administrador e Usuário Comum, com permissões diferenciadas.

## Fluxo do Sistema 🔄

### 1. Início
- 🌐 Início: O sistema começa com a página inicial (home), onde o usuário é direcionado para a tela de login.

 -------------------------------------------

### 2. Login de Usuário
- Login de Usuário: O usuário deve fazer o login para acessar o sistema. A validação do login é realizada com base nas credenciais cadastradas:
- Usuário Comum: O login é validado com os dados na tabela comum no banco de dados.
- Administrador: O login é validado com os dados na tabela administrador.

 -------------------------------------------

### 3. Menu Usuário
- 📋 Menu Usuário: Após o login, o usuário será redirecionado para a tela inicial de seu perfil, com as opções baseadas nas permissões do tipo de usuário.
#### 🧑‍💻 Usuário Comum:
- Visualizar Estoque: O usuário pode consultar os produtos disponíveis no estoque.
- Logout: O usuário pode se desconectar.
  
 -------------------------------------------

#### 👨‍💼 Administrador:
- Cadastro de Produtos: O administrador pode cadastrar novos produtos no sistema.
- Editar / Excluir Produtos: O administrador pode editar as informações dos produtos cadastrados ou excluí-los.
- Visualizar Estoque: O administrador também pode visualizar os produtos no estoque.
- Entrada / Saída dos Produtos: O administrador pode registrar entradas e saídas de produtos no estoque.
- Logout: O administrador pode se desconectar.

----------------------------------

## Funcionalidades


### 🔑 Autenticação de Usuários:
**Administrador:** Pode visualizar, editar, excluir produtos, cadastrar novos produtos, e gerenciar a entrada e saída de mercadorias.
**Usuário Comum:** Pode apenas visualizar os produtos em estoque.


**Cadastro e Gestão de Produtos:**
Administrador pode cadastrar novos produtos informando nome, descrição, quantidade, preço e quantidade mínima.
Administrador pode editar e excluir produtos existentes.
   
### 📈 Gestão de Estoque:

Administrador pode registrar entradas e saídas de produtos no estoque.
Usuário Comum pode visualizar apenas os produtos cadastrados, sem a capacidade de modificar.

### 🔑 Segurança:

As senhas de todos os usuários (administradores e comuns) são armazenadas de forma criptografada utilizando a biblioteca werkzeug.security.


----------------------------------
## Tecnologias Utilizadas
🐍 Back-end: Python 3.x com Flask
💾 Banco de Dados: MySQL para armazenar as informações de produtos e usuários
🎨 Frontend: HTML, CSS para a interface de usuário


## Configuração do Banco de Dados 💾
```bash
create database db_controle_de_estoque;

use db_controle_de_estoque;

SELECT * FROM comum;
SELECT * FROM administrador;
SELECT * FROM produtos;

CREATE TABLE administrador (
	id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    tipo VARCHAR(255) NOT NULL
);

CREATE TABLE comum (
	id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    tipo VARCHAR(255) NOT NULL
);

CREATE TABLE produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    quantidade INT DEFAULT 0,
    quantidade_minima INT DEFAULT 0,
    preco DECIMAL(10, 2) NOT NULL
);

ALTER TABLE produtos ADD COLUMN data_entrada DATETIME;
ALTER TABLE produtos ADD COLUMN data_saida DATETIME;


DESCRIBE produtos;
