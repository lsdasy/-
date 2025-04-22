import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import time
import threading

def simulate_calculation():
    for i in range(101):
        progress_var.set(i)
        time.sleep(0.02)  # Имитация длительного расчета
    root.after(0, show_results)

def show_results():
    try:
        lambda_val = float(entry_lambda.get())
        mu_val = float(entry_mu.get())
        
        if lambda_val <= 0 or mu_val <= 0:
            messagebox.showerror("Ошибка", "Значения должны быть положительными!")
            return
        
        rho = lambda_val / mu_val
        p0 = 1 / (1 + rho)
        p_refuse = rho / (1 + rho)
        q = 1 - p_refuse
        a = lambda_val * q
        
        result_text.set(
            f"Вероятность отказа: {p_refuse:.4f}\n"
            f"Относительная пропускная способность: {q:.4f}\n"
            f"Абсолютная пропускная способность: {a:.4f} покупателей/час"
        )
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные числовые значения!")
    finally:
        progress_frame.pack_forget()
        result_frame.pack(fill="x", pady=10)

def calculate_metrics():
    # Скрываем результаты и показываем прогресс-бар
    result_frame.pack_forget()
    progress_frame.pack(fill="x", pady=10)
    progress_var.set(0)
    
    # Запускаем расчет в отдельном потоке
    thread = threading.Thread(target=simulate_calculation)
    thread.daemon = True
    thread.start()

# Создаем главное окно с темной темой
root = ttk.Window(themename="darkly")
root.title("СМО: Магазин одежды")
root.geometry("500x450")
root.resizable(False, False)

# Основной фрейм
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(expand=True, fill="both")

# Заголовок
title_label = ttk.Label(
    main_frame,
    text="Магазин одежды: Анализ СМО",
    font=("Helvetica", 16, "bold"),
    foreground="#ffffff",
    anchor="center"
)
title_label.pack(pady=10)

# Фрейм для ввода
input_frame = ttk.LabelFrame(
    main_frame, 
    text="Входные параметры", 
    padding=10,
    style='dark.TLabelframe'
)
input_frame.pack(fill="x", pady=10)

# Поля ввода
ttk.Label(
    input_frame, 
    text="Интенсивность потока (λ, покупателей/час):",
    foreground="#ffffff"
).grid(row=0, column=0, sticky="w", pady=5)
entry_lambda = ttk.Entry(input_frame, width=20, style='dark.TEntry')
entry_lambda.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(
    input_frame, 
    text="Интенсивность обслуживания (μ, покупателей/час):",
    foreground="#ffffff"
).grid(row=1, column=0, sticky="w", pady=5)
entry_mu = ttk.Entry(input_frame, width=20, style='dark.TEntry')
entry_mu.grid(row=1, column=1, padx=10, pady=5)

# Кнопка расчета
calculate_button = ttk.Button(
    main_frame,
    text="Рассчитать",
    command=calculate_metrics,
    style="primary.TButton"
)
calculate_button.pack(pady=20)

# Фрейм для прогресс-бара
progress_frame = ttk.Frame(main_frame)
progress_var = ttk.DoubleVar()

progress_label = ttk.Label(
    progress_frame,
    text="Выполняется расчет...",
    foreground="#ffffff"
)
progress_label.pack(pady=5)

progress_bar = ttk.Progressbar(
    progress_frame,
    variable=progress_var,
    maximum=100,
    style='success.Horizontal.TProgressbar',
    length=400
)
progress_bar.pack(pady=5)

# Фрейм для вывода с прокруткой
result_frame = ttk.LabelFrame(
    main_frame, 
    text="Результаты", 
    padding=10,
    style='dark.TLabelframe'
)

# Добавляем прокрутку
canvas = ttk.Canvas(result_frame)
scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Текстовое поле для результатов
result_text = ttk.StringVar()
result_label = ttk.Label(
    scrollable_frame,
    textvariable=result_text,
    font=("Helvetica", 10),
    foreground="#ffffff",
    justify="left",
    wraplength=350
)
result_label.pack(pady=5, padx=5)

# Запускаем приложение
root.mainloop()