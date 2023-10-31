import tkinter as tk
from tkinter import ttk
import psutil

def listar_processos():
    process_list.delete(*process_list.get_children())
    processes = []
    filtro = nome_filtro.get().lower()  # Obtém o valor do filtro em letras minúsculas
    for proc in psutil.process_iter(attrs=['pid', 'name', 'status', 'cpu_percent', 'num_threads', 'username', 'nice']):
        process_info = proc.info
        if filtro in process_info['name'].lower():  # Verifica se o filtro está contido no nome do processo
            processes.append(process_info)

    # Ordene a lista de processos com base no uso de CPU (cpu_percent)
    processes.sort(key=lambda x: x['cpu_percent'], reverse=True)

    for proc in processes:
        pid = proc['pid']
        name = proc['name']
        status = proc['status']
        cpu_percent = proc['cpu_percent']
        num_threads = proc['num_threads']
        username = proc['username']
        nice = proc['nice']
        process_list.insert("", "end", values=(pid, name, status, cpu_percent, num_threads, username, nice))

    app.after(5000, listar_processos)  # Atualiza a cada 5 segundos (5000 milissegundos)

def matar_processo():
    selected_item = process_list.selection()
    if selected_item:
        pid = process_list.item(selected_item)['values'][0]
        try:
            process = psutil.Process(pid)
            process.terminate()
        except psutil.NoSuchProcess:
            pass

def parar_continuar_processo(acao):
    selected_item = process_list.selection()
    if selected_item:
        pid = process_list.item(selected_item)['values'][0]
        try:
            process = psutil.Process(pid)
            if acao == 'parar':
                process.suspend()
            elif acao == 'continuar':
                process.resume()
        except psutil.NoSuchProcess:
            pass

def alterar_prioridade():
    pid = pid_entry.get()
    nice = int(prioridade_var.get())  # Obtém o valor da prioridade do menu suspenso
    try:
        process = psutil.Process(int(pid))
        process.nice(nice)
    except (psutil.NoSuchProcess, ValueError):
        pass

def ordenar_por_cpu():
    listar_processos()  # Atualize a lista ao clicar na coluna "CPU%"

app = tk.Tk()
app.title("Gerenciador de Tarefas")

process_list_frame = ttk.Frame(app)
process_list_frame.pack(padx=10, pady=10)
process_list = ttk.Treeview(process_list_frame, columns=("PID", "Nome", "Status", "CPU%", "Threads", "Usuário", "Nice"), show="headings")
process_list.heading("PID", text="PID")
process_list.heading("Nome", text="Nome")
process_list.heading("Status", text="Status")
process_list.heading("CPU%", text="CPU%", command=ordenar_por_cpu)
process_list.heading("Threads", text="Threads")
process_list.heading("Usuário", text="Usuário")
process_list.heading("Nice", text="Nice")
process_list.pack()

filtro_frame = ttk.Frame(app)
filtro_frame.pack(padx=10, pady=10)
nome_filtro = tk.StringVar()  # Variável para armazenar o texto do filtro
filtro_label = ttk.Label(filtro_frame, text="Filtrar por nome:")
filtro_label.pack(side=tk.LEFT)
filtro_entry = ttk.Entry(filtro_frame, textvariable=nome_filtro, width=30)
filtro_entry.pack(side=tk.LEFT)
filtro_button = ttk.Button(filtro_frame, text="Filtrar", command=listar_processos)
filtro_button.pack(side=tk.LEFT)

pid_frame = ttk.Frame(app)
pid_frame.pack(padx=10, pady=10)
pid_label = ttk.Label(pid_frame, text="Digite o PID:")
pid_label.pack(side=tk.LEFT)
pid_entry = ttk.Entry(pid_frame, width=10)
pid_entry.pack(side=tk.LEFT)

prioridade_frame = ttk.Frame(app)
prioridade_frame.pack(padx=10, pady=10)
prioridade_label = ttk.Label(prioridade_frame, text="Nova Prioridade:")
prioridade_label.pack(side=tk.LEFT)
prioridade_var = tk.StringVar()
prioridade_combobox = ttk.Combobox(prioridade_frame, textvariable=prioridade_var, values=["-20", "-10", "0", "10", "20"])
prioridade_combobox.set("0")  # Defina o valor padrão
prioridade_combobox.pack(side=tk.LEFT)

prioridade_button = ttk.Button(prioridade_frame, text="Alterar Prioridade", command=alterar_prioridade)
prioridade_button.pack(side=tk.LEFT)

button_frame = tk.Frame(app)
button_frame.pack(pady=10)
listar_button = tk.Button(button_frame, text="Listar Processos", command=listar_processos)
listar_button.pack(side=tk.LEFT)
matar_button = tk.Button(button_frame, text="Matar Processo", command=matar_processo)
matar_button.pack(side=tk.LEFT)
parar_button = tk.Button(button_frame, text="Parar Processo", command=lambda: parar_continuar_processo('parar'))
parar_button.pack(side=tk.LEFT)
continuar_button = tk.Button(button_frame, text="Continuar Processo", command=lambda: parar_continuar_processo('continuar'))
continuar_button.pack(side=tk.LEFT)

listar_processos()  # Inicialmente, liste os processos
app.mainloop()
