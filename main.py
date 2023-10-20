import tkinter as tk
from tkinter import ttk
import psutil

def listar_processos():
    process_list.delete(*process_list.get_children())
    processes = []
    for proc in psutil.process_iter(attrs=['pid', 'name', 'status', 'cpu_percent', 'num_threads', 'username']):
        processes.append(proc.info)

    # Ordene a lista de processos com base no uso de CPU (cpu_percent)
    processes.sort(key=lambda x: x['cpu_percent'], reverse=True)

    for proc in processes:
        pid = proc['pid']
        name = proc['name']
        status = proc['status']
        cpu_percent = proc['cpu_percent']
        num_threads = proc['num_threads']
        username = proc['username']
        process_list.insert("", "end", values=(pid, name, status, cpu_percent, num_threads, username))

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
    pass

def ordenar_por_cpu():
    # Quando o cabeçalho da coluna "CPU%" for clicado, ordene a lista por uso de CPU
    listar_processos()

app = tk.Tk()
app.title("Gerenciador de Tarefas")

process_list_frame = ttk.Frame(app)
process_list_frame.pack(padx=10, pady=10)
process_list = ttk.Treeview(process_list_frame, columns=("PID", "Nome", "Status", "CPU%", "Threads", "Usuário"), show="headings")
process_list.heading("PID", text="PID")
process_list.heading("Nome", text="Nome")
process_list.heading("Status", text="Status")
process_list.heading("CPU%", text="CPU%", command=ordenar_por_cpu)
process_list.heading("Threads", text="Threads")
process_list.heading("Usuário", text="Usuário")
process_list.pack()

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
