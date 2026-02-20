import tkinter as tk
from tkinter import ttk, messagebox

# ------------------ VENTANA PRINCIPAL ------------------
ventana = tk.Tk()
ventana.title("Sistema Escuela de Fútbol")
ventana.geometry("900x600")
ventana.config(bg="#0f3057")

# ------------------ LOGO ------------------
canvas_logo = tk.Canvas(ventana, width=100, height=100, bg="#0f3057", highlightthickness=0)
canvas_logo.pack(pady=5)

canvas_logo.create_oval(10, 10, 90, 90, fill="white", outline="black", width=2)
canvas_logo.create_polygon(50,25, 65,45, 58,70, 42,70, 35,45, fill="black")

titulo = tk.Label(
    ventana,
    text="SISTEMA DE GESTIÓN - ESCUELA DE FÚTBOL",
    font=("Arial", 18, "bold"),
    bg="#0f3057",
    fg="white"
)
titulo.pack(pady=5)

# ------------------ NOTEBOOK (PESTAÑAS) ------------------
notebook = ttk.Notebook(ventana)
notebook.pack(expand=True, fill="both", padx=20, pady=20)

# =========================================================
# =================== PESTAÑA JUGADORES ===================
# =========================================================

frame_jugadores = tk.Frame(notebook, bg="white")
notebook.add(frame_jugadores, text="Jugadores")

# ----- FUNCIONES JUGADORES -----
def agregar_jugador():
    nombre = entry_nombre_j.get()
    edad = entry_edad_j.get()
    categoria = combo_categoria_j.get()

    if nombre == "" or edad == "" or categoria == "":
        messagebox.showwarning("Error", "Complete todos los campos")
    else:
        tabla_jugadores.insert("", "end", values=(nombre, edad, categoria))
        entry_nombre_j.delete(0, tk.END)
        entry_edad_j.delete(0, tk.END)
        combo_categoria_j.set("")

# ----- FORMULARIO JUGADORES -----
frame_form_j = tk.LabelFrame(frame_jugadores, text="Registro de Jugador", padx=20, pady=20)
frame_form_j.pack(padx=20, pady=10, fill="x")

tk.Label(frame_form_j, text="Nombre:").grid(row=0, column=0, padx=10, pady=5)
entry_nombre_j = tk.Entry(frame_form_j, width=30)
entry_nombre_j.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_form_j, text="Edad:").grid(row=1, column=0, padx=10, pady=5)
entry_edad_j = tk.Entry(frame_form_j, width=30)
entry_edad_j.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame_form_j, text="Categoría:").grid(row=2, column=0, padx=10, pady=5)
combo_categoria_j = ttk.Combobox(frame_form_j, width=27,
                                 values=["Sub-8", "Sub-10", "Sub-12", "Sub-15", "Juvenil"])
combo_categoria_j.grid(row=2, column=1, padx=10, pady=5)

tk.Button(frame_form_j, text="Agregar Jugador",
          bg="#28a745", fg="white",
          command=agregar_jugador).grid(row=3, column=0, columnspan=2, pady=10)

# ----- TABLA JUGADORES -----
columnas_j = ("Nombre", "Edad", "Categoría")
tabla_jugadores = ttk.Treeview(frame_jugadores, columns=columnas_j, show="headings")

for col in columnas_j:
    tabla_jugadores.heading(col, text=col)
    tabla_jugadores.column(col, anchor="center")

tabla_jugadores.pack(padx=20, pady=10, fill="both", expand=True)

# =========================================================
# =================== PESTAÑA ENTRENADORES =================
# =========================================================

frame_entrenadores = tk.Frame(notebook, bg="white")
notebook.add(frame_entrenadores, text="Entrenadores")

# ----- FUNCIONES ENTRENADORES -----
def agregar_entrenador():
    nombre = entry_nombre_e.get()
    especialidad = entry_especialidad_e.get()
    experiencia = entry_experiencia_e.get()

    if nombre == "" or especialidad == "" or experiencia == "":
        messagebox.showwarning("Error", "Complete todos los campos")
    else:
        tabla_entrenadores.insert("", "end", values=(nombre, especialidad, experiencia))
        entry_nombre_e.delete(0, tk.END)
        entry_especialidad_e.delete(0, tk.END)
        entry_experiencia_e.delete(0, tk.END)

# ----- FORMULARIO ENTRENADORES -----
frame_form_e = tk.LabelFrame(frame_entrenadores, text="Registro de Entrenador", padx=20, pady=20)
frame_form_e.pack(padx=20, pady=10, fill="x")

tk.Label(frame_form_e, text="Nombre:").grid(row=0, column=0, padx=10, pady=5)
entry_nombre_e = tk.Entry(frame_form_e, width=30)
entry_nombre_e.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_form_e, text="Especialidad:").grid(row=1, column=0, padx=10, pady=5)
entry_especialidad_e = tk.Entry(frame_form_e, width=30)
entry_especialidad_e.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame_form_e, text="Años de Experiencia:").grid(row=2, column=0, padx=10, pady=5)
entry_experiencia_e = tk.Entry(frame_form_e, width=30)
entry_experiencia_e.grid(row=2, column=1, padx=10, pady=5)

tk.Button(frame_form_e, text="Agregar Entrenador",
          bg="#007bff", fg="white",
          command=agregar_entrenador).grid(row=3, column=0, columnspan=2, pady=10)

# ----- TABLA ENTRENADORES -----
columnas_e = ("Nombre", "Especialidad", "Experiencia")
tabla_entrenadores = ttk.Treeview(frame_entrenadores, columns=columnas_e, show="headings")

for col in columnas_e:
    tabla_entrenadores.heading(col, text=col)
    tabla_entrenadores.column(col, anchor="center")

tabla_entrenadores.pack(padx=20, pady=10, fill="both", expand=True)

# ------------------ EJECUTAR ------------------
ventana.mainloop()