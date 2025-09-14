from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import bcrypt
import hashlib
from datetime import datetime
import os
#ACESSO DO ADMINISTRADOR
#admin01
#12345678

#ACESSO DO ADMINISTRADOR
#comum
#12345678

app = Flask(__name__)
app.secret_key = 'python'


db_config = {
    'user': os.getenv("DB_USER", "root"),
    'password': os.getenv("DB_PASSWORD", ""),
    'host': os.getenv("DB_HOST", "localhost"),
    'database': os.getenv("DB_NAME", "db_controle_de_estoque"),
    'port': int(os.getenv("DB_PORT", 3306))
}


def criptografar_senha(senha):
    return generate_password_hash(senha)

def verificar_senha(senha_fornecida, senha_criptografada):
    return check_password_hash(senha_criptografada, senha_fornecida)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login/administrador', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        if not nome or not senha:
            flash('Preencha todos os campos', 'danger')
            return redirect(url_for('login_administrador'))

        conexao = mysql.connector.connect(**db_config)
        cursor = conexao.cursor()

        cursor.execute('SELECT senha FROM administrador WHERE nome = %s', (nome,))
        resultado = cursor.fetchone()
        cursor.close()
        conexao.close()

        if resultado:
            senha_criptografada = resultado[0]
            if verificar_senha(senha, senha_criptografada):
                session['usuario'] = nome
                return redirect(url_for('menu_administrador'))
            else:
                flash('Senha incorreta', 'danger')
        else:
            flash('Usuário não encontrado', 'danger')
    
    return render_template('login_administrador.html')

@app.route('/login/comum', methods=['GET', 'POST'])
def login_comum():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        if not nome or not senha:
            flash('Preencha todos os campos', 'danger')
            return redirect(url_for('login_comum'))

        conexao = mysql.connector.connect(**db_config)
        cursor = conexao.cursor()

        cursor.execute('SELECT senha FROM comum WHERE nome = %s', (nome,))
        resultado = cursor.fetchone()
        cursor.close()
        conexao.close()

        if resultado:
            senha_criptografada = resultado[0]
            if verificar_senha(senha, senha_criptografada):
                session['comum'] = nome
                return redirect(url_for('menu_usuario'))
            else:
                flash('Senha incorreta', 'danger')
        else:
            flash('Usuário não encontrado', 'danger')
    
    return render_template('login_comum.html')

@app.route('/menu_administrador')
def menu_administrador():
    return render_template('menu_administrador.html')

@app.route('/menu_usuario')
def menu_usuario():
    return render_template('menu_usuario.html')

@app.route('/visualizar_estoque')
def visualizar_estoque():
    conexao = mysql.connector.connect(**db_config)
    cursor = conexao.cursor(dictionary=True)
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    for produto in produtos:
        produto['baixo_estoque'] = produto['quantidade'] < produto['quantidade_minima']
    cursor.close()
    conexao.close()
    is_admin = 'usuario' in session
    
    return render_template('estoque.html', produtos=produtos, is_admin=is_admin)

@app.route('/editar_produto/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    conexao = mysql.connector.connect(**db_config)
    cursor = conexao.cursor(dictionary=True)
    
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        quantidade = request.form['quantidade']
        quantidade_minima = request.form['quantidade_minima']
        preco = request.form['preco']
        
        cursor.execute('''
            UPDATE produtos 
            SET nome = %s, descricao = %s, quantidade = %s, quantidade_minima = %s, preco = %s 
            WHERE id = %s
        ''', (nome, descricao, quantidade, quantidade_minima, preco, id))
        conexao.commit()
        cursor.close()
        conexao.close()

        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('visualizar_estoque'))
    
    cursor.execute('SELECT * FROM produtos WHERE id = %s', (id,))
    produto = cursor.fetchone()
    cursor.close()
    conexao.close()
    return render_template('editar_produto.html', produto=produto)

@app.route('/excluir_produto/<int:id>')
def excluir_produto(id):
    conexao = mysql.connector.connect(**db_config)
    cursor = conexao.cursor()
    cursor.execute('DELETE FROM produtos WHERE id = %s', (id,))
    conexao.commit()
    cursor.close()
    conexao.close()
    flash('Produto excluído com sucesso!', 'success')
    return redirect(url_for('visualizar_estoque'))

@app.route('/produtos_baixo_estoque')
def produtos_baixo_estoque():
    conexao = mysql.connector.connect(**db_config)
    cursor = conexao.cursor(dictionary=True)
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    cursor.close()
    conexao.close()
    
    produtos_baixo_estoque = [
        produto for produto in produtos if produto['quantidade'] < produto['quantidade_minima']
    ]
    return render_template('produtos_baixo_estoque.html', produtos=produtos_baixo_estoque)

@app.route('/cadastrar_produto', methods=['GET', 'POST'])
def cadastrar_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        quantidade = request.form['quantidade']
        quantidade_minima = request.form['quantidade_minima']
        preco = request.form['preco']
                
        conexao = mysql.connector.connect(**db_config)
        cursor = conexao.cursor()
        cursor.execute('INSERT INTO produtos (nome, descricao, quantidade, quantidade_minima, preco) VALUES (%s, %s, %s, %s, %s)', (nome, descricao, quantidade, quantidade_minima, preco))
        conexao.commit()
        cursor.close()
        conexao.close()

        flash("Produto cadastrado com sucesso!", "success")
        return redirect(url_for('cadastrar_produto'))
    
    return render_template('cadastrar_produto.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('home'))

@app.route('/cadastro_administrador', methods=['GET', 'POST'])
def cadastro_administrador():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        if not senha.isdigit():
            flash('A senha deve conter apenas números.')
            return redirect(url_for('cadastro_administrador'))
        elif len(senha) < 8:
            flash('A senha deve ter pelo menos 8 caracteres.')
            return redirect(url_for('cadastro_administrador'))
        
        senha_criptografada = generate_password_hash(senha)
        conexao = mysql.connector.connect(**db_config)
        cursor = conexao.cursor()
        cursor.execute('INSERT INTO administrador (nome, senha, tipo) VALUES (%s, %s, %s)', (nome, senha_criptografada, 'administrador'))
        conexao.commit()
        cursor.close()
        conexao.close()

        flash('Cadastro realizado com sucesso!')
        return redirect(url_for('cadastro_administrador'))
    
    return render_template('cadastro_administrador.html')

@app.route('/cadastro_comum', methods=['GET', 'POST'])
def cadastro_comum():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        if not senha.isdigit():
            flash('A senha deve conter apenas números.')
            return redirect(url_for('cadastro_comum'))
        elif len(senha) < 8:
            flash('A senha deve ter pelo menos 8 caracteres.')
            return redirect(url_for('cadastro_comum'))
        
        senha_criptografada = generate_password_hash(senha)
        conexao = mysql.connector.connect(**db_config)
        cursor = conexao.cursor()
        cursor.execute('INSERT INTO comum (nome, senha, tipo) VALUES (%s, %s, %s)', (nome, senha_criptografada, 'comum'))
        conexao.commit()
        cursor.close()
        conexao.close()

        flash('Cadastro realizado com sucesso!')
        return redirect(url_for('cadastro_comum'))

    return render_template('cadastro_comum.html')

from datetime import datetime

@app.route('/entrada_produto/<int:id>', methods=['POST'])
def entrada_produto(id):
    if request.method == 'POST':
        quantidade_entrada = int(request.form['quantidade'])
        
        data_entrada = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        conexao = mysql.connector.connect(**db_config)
        cursor = conexao.cursor()

        cursor.execute('UPDATE produtos SET quantidade = quantidade + %s, data_entrada = %s WHERE id = %s',
                       (quantidade_entrada, data_entrada, id))
        
        conexao.commit()
        cursor.close()
        conexao.close()

        flash(f'{quantidade_entrada} unidades adicionadas ao estoque.')
        return redirect(url_for('visualizar_estoque'))

@app.route('/saida_produto/<int:id>', methods=['POST'])
def saida_produto(id):
    if request.method == 'POST':
        quantidade_saida = int(request.form['quantidade'])
        
        data_saida = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        conexao = mysql.connector.connect(**db_config)
        cursor = conexao.cursor()

        cursor.execute('SELECT quantidade FROM produtos WHERE id = %s', (id,))
        produto = cursor.fetchone()

        if produto and produto[0] >= quantidade_saida:
            cursor.execute('UPDATE produtos SET quantidade = quantidade - %s, data_saida = %s WHERE id = %s',
                           (quantidade_saida, data_saida, id))
            conexao.commit()
            flash(f'{quantidade_saida} unidades removidas do estoque.')
        else:
            flash('Quantidade insuficiente no estoque para essa saída.', 'danger')

        cursor.close()
        conexao.close()

        return redirect(url_for('visualizar_estoque'))


if __name__ == '__main__':
    app.run(debug=True)
