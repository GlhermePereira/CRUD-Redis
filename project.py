import redis
import json
from datetime import datetime

# Configuração de conexão com o Redis
client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Função para gerar ID único sequencial para cada tarefa
def generate_task_id():
    return client.incr("tarefa_id")

# Funções CRUD

# Criar nova tarefa
def create_task(title, description):
    if not title or not description:
        print("Título e descrição são obrigatórios.")
        return
    task_id = generate_task_id()
    task_data = {
        "id": task_id,
        "titulo": title,
        "descricao": description,
        "data_criacao": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "status": "Pendente"
    }
    client.hset(f'tarefa:{task_id}', mapping=task_data)
    print(f"Tarefa criada com sucesso! ID: {task_id}")

# Ler tarefa pelo ID
def read_task(task_id):
    task_data = client.hgetall(f'tarefa:{task_id}')
    if task_data:
        return task_data
    else:
        print("Tarefa não encontrada.")
        return None

# Listar todas as tarefas
def list_tasks():
    keys = client.keys('tarefa:*')
    tasks = [client.hgetall(key) for key in keys]
    return tasks if tasks else print("Nenhuma tarefa encontrada.")

# Atualizar tarefa
def update_task(task_id, field, new_value):
    task_key = f'tarefa:{task_id}'
    if not client.exists(task_key):
        print("Tarefa não encontrada.")
        return
    if field not in ["titulo", "descricao", "status"]:
        print("Campo inválido. Campos permitidos: titulo, descricao, status.")
        return
    client.hset(task_key, field, new_value)
    print(f"Tarefa {task_id} atualizada com sucesso.")

# Deletar tarefa
def delete_task(task_id):
    task_key = f'tarefa:{task_id}'
    if client.exists(task_key):
        client.delete(task_key)
        print("Tarefa deletada com sucesso.")
    else:
        print("Tarefa não encontrada.")

# Interface do usuário
def menu():
    while True:
        print("\nSistema de Gerenciamento de Tarefas")
        print("1. Criar nova tarefa")
        print("2. Visualizar tarefa")
        print("3. Listar todas as tarefas")
        print("4. Atualizar tarefa")
        print("5. Deletar tarefa")
        print("6. Sair")
        choice = input("Escolha uma opção: ")

        if choice == "1":
            title = input("Título da tarefa: ").strip()
            description = input("Descrição da tarefa: ").strip()
            create_task(title, description)

        elif choice == "2":
            task_id = input("ID da tarefa: ").strip()
            task = read_task(task_id)
            if task:
                print(json.dumps(task, indent=4, ensure_ascii=False))

        elif choice == "3":
            tasks = list_tasks()
            if tasks:
                for task in tasks:
                    print(json.dumps(task, indent=4, ensure_ascii=False))

        elif choice == "4":
            task_id = input("ID da tarefa: ").strip()
            field = input("Campo a ser atualizado (titulo, descricao, status): ").strip()
            new_value = input("Novo valor: ").strip()
            update_task(task_id, field, new_value)

        elif choice == "5":
            task_id = input("ID da tarefa: ").strip()
            delete_task(task_id)

        elif choice == "6":
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida. Tente novamente.")

# Executar o sistema
if __name__ == '__main__':
    menu()

