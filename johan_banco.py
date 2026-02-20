import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# ------------------ DATOS ------------------

dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
gastos = {dia: [] for dia in dias}
ingresos = 0

# ------------------ FUNCIONES --------------------------

def agregar_gasto():
    dia = combo_dia.get()
    valor = entry_valor.get()

    if valor == "":
        messagebox.showerror("Error", "Ingrese un valor")
        return

    try:
        valor = float(valor)
    except ValueError:
        messagebox.showerror("Error", "Ingrese un número válido")
        return

    gastos[dia].append(valor)
    actualizar_tabla()
    actualizar_balance()
    entry_valor.delete(0, tk.END)

def eliminar_gasto():
    dia = combo_dia.get()
    lista = gastos[dia]

    if not lista:
        messagebox.showinfo("Eliminar", f"No hay gastos en {dia}")
        return

    texto = f"Gastos en {dia}:\n\n"
    for i, gasto in enumerate(lista, 1):
        texto += f"{i}. ${gasto:,.2f}\n"

    texto += "\nIngrese el número del gasto que desea eliminar:"

    numero = simpledialog.askinteger("Eliminar gasto", texto)

    if numero is None:
        return

    if 1 <= numero <= len(lista):
        eliminado = lista.pop(numero - 1)
        messagebox.showinfo("Éxito", f"Se eliminó el gasto ${eliminado:,.2f}")
        actualizar_tabla()
        actualizar_balance()
    else:
        messagebox.showerror("Error", "Número inválido")

def agregar_ingreso():
    global ingresos
    valor = entry_ingreso.get()

    if valor == "":
        messagebox.showerror("Error", "Ingrese un ingreso")
        return

    try:
        valor = float(valor)
    except ValueError:
        messagebox.showerror("Error", "Número inválido")
        return

    ingresos += valor
    entry_ingreso.delete(0, tk.END)
    actualizar_balance()

def actualizar_tabla():
    for fila in tabla.get_children():
        tabla.delete(fila)

    for dia in dias:
        total_dia = sum(gastos[dia])
        tabla.insert("", "end", values=(dia, f"${total_dia:,.2f}"))

def ver_gastos_dia():
    dia = combo_dia.get()
    lista = gastos[dia]

    if not lista:
        messagebox.showinfo("Gastos", f"No hay gastos registrados en {dia}")
        return

    texto = f"Gastos en {dia}:\n\n"
    for i, gasto in enumerate(lista, 1):
        texto += f"{i}. ${gasto:,.2f}\n"

    messagebox.showinfo("Detalle de gastos", texto)

def ver_balance_semanal():
    total_gastos = sum(sum(lista) for lista in gastos.values())
    balance = ingresos - total_gastos

    texto = f"""
Ingresos totales: ${ingresos:,.2f}
Gastos totales: ${total_gastos:,.2f}
--------------------------
Balance semanal: ${balance:,.2f}
"""
    messagebox.showinfo("Balance semanal", texto)

def actualizar_balance():
    total_gastos = sum(sum(lista) for lista in gastos.values())
    balance = ingresos - total_gastos
    label_balance.config(text=f"Balance actual: ${balance:,.2f}")

# ------------------ VENTANA ------------------

ventana = tk.Tk()
ventana.title("Sistema Financiero Semanal")
ventana.geometry("800x600")
ventana.config(bg="#1C1C2E")

style = ttk.Style()
style.theme_use("clam")

style.configure("Treeview",
                background="#2A2A40",
                foreground="white",
                rowheight=25,
                fieldbackground="#2A2A40")

# ------------------ TÍTULO ------------------

tk.Label(ventana,
         text="SISTEMA DE CONTROL FINANCIERO",
         font=("Arial", 22, "bold"),
         bg="#1C1C2E",
         fg="white").pack(pady=20)

# ------------------ FRAME ENTRADAS ------------------

frame_inputs = tk.Frame(ventana, bg="#2A2A40", padx=20, pady=20)
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="Día:", bg="#2A2A40", fg="white").grid(row=0, column=0, padx=10)
combo_dia = ttk.Combobox(frame_inputs, values=dias, state="readonly")
combo_dia.grid(row=0, column=1)
combo_dia.current(0)

tk.Label(frame_inputs, text="Gasto:", bg="#2A2A40", fg="white").grid(row=1, column=0, padx=10)
entry_valor = tk.Entry(frame_inputs)
entry_valor.grid(row=1, column=1)

tk.Button(frame_inputs, text="Agregar Gasto",
          bg="#4E73DF", fg="white",
          command=agregar_gasto).grid(row=2, column=0, columnspan=2, pady=5)

tk.Button(frame_inputs, text="Ver gastos del día",
          bg="#17A673", fg="white",
          command=ver_gastos_dia).grid(row=3, column=0, columnspan=2, pady=5)

tk.Button(frame_inputs, text="Eliminar gasto del día",
          bg="#E74A3B", fg="white",
          command=eliminar_gasto).grid(row=4, column=0, columnspan=2, pady=5)

# ------------------ INGRESOS ------------------

tk.Label(frame_inputs, text="Ingreso:", bg="#2A2A40", fg="white").grid(row=5, column=0, padx=10)
entry_ingreso = tk.Entry(frame_inputs)
entry_ingreso.grid(row=5, column=1)

tk.Button(frame_inputs, text="Agregar Ingreso",
          bg="#36B9CC", fg="white",
          command=agregar_ingreso).grid(row=6, column=0, columnspan=2, pady=5)

# ------------------ TABLA ------------------

tabla = ttk.Treeview(ventana, columns=("Día", "Total Gastado"), show="headings", height=7)
tabla.heading("Día", text="Día")
tabla.heading("Total Gastado", text="Total Gastado")
tabla.column("Día", anchor="center", width=200)
tabla.column("Total Gastado", anchor="center", width=200)
tabla.pack(pady=20)

# ------------------ BALANCE  ------------------

label_balance = tk.Label(ventana,
                         text="Balance actual: $0.00",
                         font=("Arial", 16, "bold"),
                         bg="#1C1C2E",
                         fg="#00FFAA")
label_balance.pack(pady=10)
 #BUENA NOCHES ZDF

tk.Button(ventana,
          text="Ver Balance Semanal",
          bg="#F6C23E",
          fg="black",
          command=ver_balance_semanal).pack(pady=5)

tk.Button(ventana,
          text="Salir",
          bg="#E74A3B",
          fg="white",
          command=ventana.quit).pack(pady=10)

actualizar_tabla()


ventana.mainloop()