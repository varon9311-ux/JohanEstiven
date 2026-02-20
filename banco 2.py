import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

# ------------------ DATOS ------------------
dias = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
gastos = {dia: [] for dia in dias}
ingresos = 0
colchon = 0  # Colchón de ahorro

# Variables para animación
anim_ingresos = []
anim_gastos = []
anim_colchon = []

# ------------------ FUNCIONES ------------------
def agregar_gasto():
    dia = combo_dia.get()
    valor = entry_gasto.get()
    if not valor:
        messagebox.showerror("Error","Ingrese un valor")
        return
    try:
        valor = float(valor)
    except:
        messagebox.showerror("Error","Valor inválido")
        return
    fecha = datetime.now().strftime("%d/%m/%Y")
    gastos[dia].append((valor,fecha))
    entry_gasto.delete(0,tk.END)
    actualizar_tabla()
    actualizar_historial()
    actualizar_balance()

def agregar_ingreso():
    global ingresos
    valor = entry_ingreso.get()
    if not valor:
        messagebox.showerror("Error","Ingrese un valor")
        return
    try:
        valor = float(valor)
    except:
        messagebox.showerror("Error","Valor inválido")
        return
    ingresos += valor
    entry_ingreso.delete(0,tk.END)
    actualizar_balance()

def agregar_colchon():
    global ingresos, colchon
    if ingresos <= 0:
        messagebox.showinfo("Info","No tienes saldo para mover al colchón")
        return
    valor = simpledialog.askfloat("Colchón","Ingrese monto a guardar en el colchón:")
    if valor is None or valor <=0:
        return
    if valor > ingresos:
        messagebox.showerror("Error","No puedes apartar más de tu balance")
        return
    ingresos -= valor
    colchon += valor
    actualizar_balance()
    messagebox.showinfo("Éxito",f"${valor:,.2f} guardados en el colchón")

def retirar_colchon():
    global ingresos, colchon
    if colchon <=0:
        messagebox.showinfo("Info","No hay dinero en el colchón")
        return
    valor = simpledialog.askfloat("Retirar del colchón","Ingrese monto a retirar:")
    if valor is None or valor <=0:
        return
    if valor > colchon:
        messagebox.showerror("Error","No puedes retirar más de lo disponible")
        return
    colchon -= valor
    ingresos += valor
    actualizar_balance()
    messagebox.showinfo("Éxito",f"${valor:,.2f} retirados del colchón")

def eliminar_gasto():
    dia = combo_dia.get()
    lista = gastos[dia]
    if not lista:
        messagebox.showinfo("Info","No hay gastos en este día")
        return
    texto = "Gastos:\n"
    for i,(v,f) in enumerate(lista,1):
        texto += f"{i}. ${v:,.2f} ({f})\n"
    numero = simpledialog.askinteger("Eliminar gasto", texto)
    if numero and 1<=numero<=len(lista):
        confirmar = messagebox.askyesno("Confirmar","¿Eliminar este gasto?")
        if confirmar:
            lista.pop(numero-1)
            actualizar_tabla()
            actualizar_historial()
            actualizar_balance()

def reiniciar_semana():
    global ingresos, colchon
    confirmar = messagebox.askyesno("Confirmar","¿Desea reiniciar toda la semana?")
    if confirmar:
        ingresos = 0
        colchon = 0
        for dia in dias:
            gastos[dia] = []
        actualizar_tabla()
        actualizar_historial()
        actualizar_balance()

def actualizar_tabla():
    for fila in tabla_resumen.get_children():
        tabla_resumen.delete(fila)
    for dia in dias:
        total = sum([v[0] for v in gastos[dia]])
        tabla_resumen.insert("", "end", values=(dia,f"${total:,.2f}"))

def actualizar_historial():
    for fila in tabla_historial.get_children():
        tabla_historial.delete(fila)
    for dia in dias:
        for valor,fecha in gastos[dia]:
            tabla_historial.insert("", "end", values=(dia,fecha,f"${valor:,.2f}"))

def actualizar_balance():
    global anim_ingresos, anim_gastos, anim_colchon
    total_gastos = sum([v[0] for lista in gastos.values() for v in lista])
    balance = ingresos - total_gastos
    color = "#4DD0E1" if balance>=0 else "#FF5252"  # Azul positivo, rojo negativo
    label_balance.config(text=f"Balance actual: ${balance:,.2f} | Colchón: ${colchon:,.2f}", fg=color)
    anim_ingresos = generar_animacion_datos(ingresos)
    anim_gastos = generar_animacion_datos(total_gastos)
    anim_colchon = generar_animacion_datos(colchon)
    dibujar_grafico_animado(0)

def generar_animacion_datos(valor_final, pasos=20):
    return [valor_final*i/pasos for i in range(pasos+1)]

def dibujar_grafico_animado(paso):
    canvas.delete("all")
    margen_x = 50
    margen_y = 30
    ancho = 700
    alto = 250
    pasos_totales = 20

    canvas.create_rectangle(0,0,ancho+2*margen_x, alto+2*margen_y, fill="white", outline="")
    canvas.create_text(ancho//2 + margen_x, 15, text="Evolución semanal de ingresos, gastos y colchón",
                       font=("Arial",14,"bold"), fill="#333333")

    canvas.create_line(margen_x, margen_y, margen_x, alto + margen_y, fill="#888888", width=2)
    canvas.create_line(margen_x, alto + margen_y, ancho + margen_x, alto + margen_y, fill="#888888", width=2)

    acumulado_gastos = []
    suma_gas = 0
    for dia in dias:
        gasto_dia = sum([v[0] for v in gastos[dia]])
        suma_gas += gasto_dia
        acumulado_gastos.append(suma_gas * anim_gastos[paso]/(anim_gastos[-1] or 1))

    ing_anim = anim_ingresos[paso]
    colchon_anim = anim_colchon[paso]

    max_val = max(ing_anim, max(acumulado_gastos) if acumulado_gastos else 1, colchon_anim, 1)

    def escala_y(valor):
        return alto + margen_y - (valor/max_val)*alto

    paso_x = ancho / (len(dias)-1)

    puntos_ing = []
    for i in range(len(dias)):
        x = margen_x + i*paso_x
        y = escala_y(ing_anim)
        puntos_ing.extend([x,y])
    canvas.create_line(*puntos_ing, fill="#4DD0E1", width=3, smooth=True)

    puntos_gas = []
    for i in range(len(dias)):
        x = margen_x + i*paso_x
        y = escala_y(acumulado_gastos[i])
        puntos_gas.extend([x,y])
    canvas.create_line(*puntos_gas, fill="#FF5252", width=3, smooth=True)

    puntos_colchon = []
    for i in range(len(dias)):
        x = margen_x + i*paso_x
        y = escala_y(colchon_anim)
        puntos_colchon.extend([x,y])
    canvas.create_line(*puntos_colchon, fill="#FFD700", width=3, smooth=True)

    for i,dia in enumerate(dias):
        x = margen_x + i*paso_x
        canvas.create_text(x, alto+margen_y+15, text=dia[:3], font=("Arial",9), fill="#333333")

    leyendas = [("#4DD0E1", "Ingresos"), ("#FF5252", "Gastos"), ("#FFD700", "Colchón")]
    for i,(color, texto) in enumerate(leyendas):
        canvas.create_rectangle(ancho-150, margen_y + 10 + i*30, ancho-110, margen_y + 30 + i*30, fill=color, outline="")
        canvas.create_text(ancho-100, margen_y + 20 + i*30, text=texto, anchor="w", font=("Arial",10), fill=color)

    if paso < 20:
        canvas.after(40, lambda: dibujar_grafico_animado(paso+1))

# ------------------ VENTANA ------------------
root = tk.Tk()
root.title("Sistema Financiero Organizado y Gráfico Animado")
root.geometry("950x700")
root.configure(bg="#1E1E2F")

# TÍTULO GENERAL
tk.Label(root, text="Sistema Financiero Organizado y Gráfico Animado",
         font=("Arial",20,"bold"), bg="#1E1E2F", fg="#FFD700").pack(pady=12)

# FRAME PRINCIPAL
frame_main = tk.Frame(root, bg="#2A2A50")
frame_main.pack(expand=True, fill="both", padx=15, pady=10)

# ------------------ SECCIÓN INGRESOS ------------------
frame_ingresos = tk.LabelFrame(frame_main, text="Ingresos", bg="#2A2A50", fg="white",
                               font=("Arial",12,"bold"), padx=15,pady=15)
frame_ingresos.pack(side="top", fill="x", pady=8)

tk.Label(frame_ingresos, text="Monto ingreso:", bg="#2A2A50", fg="white").grid(row=0,column=0,padx=10,pady=5)
entry_ingreso = tk.Entry(frame_ingresos)
entry_ingreso.grid(row=0,column=1,pady=5)
tk.Button(frame_ingresos,text="Agregar Ingreso",bg="#4DD0E1",fg="white",command=agregar_ingreso).grid(row=0,column=2,padx=10,pady=5)

# ------------------ SECCIÓN GASTOS ------------------
frame_gastos = tk.LabelFrame(frame_main, text="Gastos", bg="#2A2A50", fg="white",
                             font=("Arial",12,"bold"), padx=15,pady=15)
frame_gastos.pack(side="top", fill="x", pady=8)

tk.Label(frame_gastos, text="Día:", bg="#2A2A50", fg="white").grid(row=0,column=0,padx=10,pady=5)
combo_dia = ttk.Combobox(frame_gastos, values=dias, state="readonly")
combo_dia.grid(row=0,column=1,pady=5)
combo_dia.current(0)

tk.Label(frame_gastos, text="Monto gasto:", bg="#2A2A50", fg="white").grid(row=1,column=0,padx=10,pady=5)
entry_gasto = tk.Entry(frame_gastos)
entry_gasto.grid(row=1,column=1,pady=5)

tk.Button(frame_gastos,text="Agregar Gasto",bg="#FF5252",fg="white",command=agregar_gasto).grid(row=1,column=2,padx=10,pady=5)
tk.Button(frame_gastos,text="Eliminar Gasto",bg="#F6C23E",fg="black",command=eliminar_gasto).grid(row=2,column=0,columnspan=3,pady=5)

# ------------------ SECCIÓN COLCHÓN ------------------
frame_colchon = tk.LabelFrame(frame_main, text="Colchón (Ahorro Apartado)", bg="#2A2A50", fg="white",
                              font=("Arial",12,"bold"), padx=15,pady=15)
frame_colchon.pack(side="top", fill="x", pady=8)

tk.Button(frame_colchon,text="Guardar en Colchón",bg="#FFD700",fg="black",command=lambda:[agregar_colchon(), actualizar_balance()]).grid(row=0,column=0,padx=10,pady=5)
tk.Button(frame_colchon,text="Retirar del Colchón",bg="#FFD700",fg="black",command=lambda:[retirar_colchon(), actualizar_balance()]).grid(row=0,column=1,padx=10,pady=5)

# ------------------ BOTÓN REINICIAR ------------------
tk.Button(frame_main,text="Reiniciar Semana",bg="#9C27B0",fg="white",command=reiniciar_semana).pack(pady=10)

# ------------------ TABLA RESUMEN ------------------
frame_tabla = tk.LabelFrame(frame_main, text="Resumen Semanal", bg="#2A2A50", fg="white", font=("Arial",12,"bold"), padx=15,pady=15)
frame_tabla.pack(side="left", fill="both", expand=True, padx=10, pady=10)

tabla_resumen = ttk.Treeview(frame_tabla, columns=("Día","Total"), show="headings", height=10)
tabla_resumen.heading("Día", text="Día")
tabla_resumen.heading("Total", text="Total Gastado")
tabla_resumen.pack(expand=True, fill="both")

# ------------------ TABLA HISTORIAL ------------------
frame_historial = tk.LabelFrame(frame_main, text="Historial de Gastos", bg="#2A2A50", fg="white", font=("Arial",12,"bold"), padx=15,pady=15)
frame_historial.pack(side="right", fill="both", expand=True, padx=10, pady=10)

tabla_historial = ttk.Treeview(frame_historial, columns=("Día","Fecha","Monto"), show="headings", height=10)
tabla_historial.heading("Día", text="Día")
tabla_historial.heading("Fecha", text="Fecha")
tabla_historial.heading("Monto", text="Monto")
tabla_historial.pack(expand=True, fill="both")

# ------------------ BALANCE Y GRÁFICO ------------------
frame_balance = tk.Frame(root, bg="#2A2A50")
frame_balance.pack(fill="both", padx=20, pady=10)

label_balance = tk.Label(frame_balance, text="Balance actual: $0.00 | Colchón: $0.00", font=("Arial",16,"bold"), bg="#2A2A50", fg="#4DD0E1")
label_balance.pack(pady=5)

canvas = tk.Canvas(frame_balance,width=800,height=320,bg="white", highlightthickness=0)
canvas.pack(pady=10)

# ------------------ INICIALIZAR ------------------
actualizar_tabla()
actualizar_historial()
actualizar_balance()

root.mainloop()