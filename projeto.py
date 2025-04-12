import sqlite3

class GerenciadorEstoque:
    def __init__(self, db_name="estoquee.db"):
        self.db_name = db_name
        self.criar_banco()
    
    def conectar(self):
        return sqlite3.connect(self.db_name)
    
    def criar_banco(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE NOT NULL,
                quantidade INTEGER NOT NULL,
                preco REAL NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def produto_existe(self, id):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM produtos WHERE id = ?", (id,))
        existe = cursor.fetchone() is not None
        conn.close()
        return existe

    def adicionar_produto(self, nome, quantidade, preco):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)",
                (nome, quantidade, preco)
            )
            conn.commit()
            print("Produto adicionado com sucesso!")
        except sqlite3.IntegrityError:
            print("Erro: Produto com este nome já existe!")
        finally:
            conn.close()

    def listar_produtos(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produtos")
        produtos = cursor.fetchall()
        conn.close()
        if produtos:
            print(f"\n{'ID':<5} {'Nome':<20} {'Quantidade':<12} {'Preço':<10}")
            print("-" * 50)
            for p in produtos:
                print(f"{p[0]:<5} {p[1]:<20} {p[2]:<12} R${p[3]:.2f}")
        else:
            print("⚠️ Nenhum produto encontrado.")

    def atualizar_produto(self, id):
        if not self.produto_existe(id):
            print("Erro: Produto com este ID não existe.")
            return
        
        while True:
            print("\nOpções de atualização:")
            print("1 - Atualizar Nome")
            print("2 - Atualizar Quantidade")
            print("3 - Atualizar Preço")
            print("4 - Voltar")
            opcao = input("Escolha uma opção: ")

            conn = self.conectar()
            cursor = conn.cursor()

            try:
                if opcao == "1":
                    novo_nome = input("Novo nome: ")
                    cursor.execute("UPDATE produtos SET nome = ? WHERE id = ?", (novo_nome, id))
                elif opcao == "2":
                    nova_quantidade = int(input("Nova quantidade: "))
                    cursor.execute("UPDATE produtos SET quantidade = ? WHERE id = ?", (nova_quantidade, id))
                elif opcao == "3":
                    novo_preco = float(input("Novo preço: "))
                    cursor.execute("UPDATE produtos SET preco = ? WHERE id = ?", (novo_preco, id))
                elif opcao == "4":
                    conn.close()
                    break
                else:
                    print("⚠️ Opção inválida!")
                    continue

                if cursor.rowcount:
                    conn.commit()
                    print("Produto atualizado com sucesso!")
                else:
                    print(" Nenhuma alteração realizada.")
            except Exception as e:
                print("❌ Erro:", e)
            finally:
                conn.close()

    def deletar_produto(self, id):
        if not self.produto_existe(id):
            print(" Erro: Produto com este ID não existe.")
            return

        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produtos WHERE id = ?", (id,))
        conn.commit()
        print("Produto deletado com sucesso!")
        conn.close()

def menu():
    estoque = GerenciadorEstoque()

    while True:
        print("\n📦 Gerenciamento de Estoque 📦")
        print("1 - Adicionar Produto")
        print("2 - Listar Produtos")
        print("3 - Atualizar Produto")
        print("4 - Deletar Produto")
        print("5 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome do produto: ")
            try:
                quantidade = int(input("Quantidade: "))
                preco = float(input("Preço: "))
                estoque.adicionar_produto(nome, quantidade, preco)
            except ValueError:
                print(" Erro: Digite valores válidos para quantidade e preço.")
        elif opcao == "2":
            estoque.listar_produtos()
        elif opcao == "3":
            try:
                id = int(input("ID do produto a atualizar: "))
                estoque.atualizar_produto(id)
            except ValueError:
                print(" Erro: Digite um ID válido.")
        elif opcao == "4":
            try:
                id = int(input("ID do produto a deletar: "))
                estoque.deletar_produto(id)
            except ValueError:
                print(" Erro: Digite um ID válido.")
        elif opcao == "5":
            print(" Saindo...")
            break
        else:
            print(" Opção inválida! Tente novamente.")

# Executa o programa
if __name__ == "__main__":
    menu()

# Teste 1: Adicionar Produto
# Entrada: "Teclado", 10, 120.50
# Saída esperada: Produto adicionado com sucesso!

# Teste 2: Adicionar Produto com Nome Duplicado
# Entrada: "Teclado", 5, 100.00
# Saída esperada: Erro: Produto com este nome já existe!

# Teste 3: Listar Produtos
# Esperado: Lista formatada dos produtos adicionados

# Teste 4: Atualizar Quantidade do Produto ID 1
# Entrada: ID = 1, nova quantidade = 15
# Esperado: Produto atualizado com sucesso!

# Teste 5: Deletar Produto com ID inválido
# Entrada: ID = 999
# Esperado: Erro: Produto com este ID não existe.

