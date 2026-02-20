import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from datetime import datetime
import pandas as pd # Para Excel
from reportlab.lib.pagesizes import letter # Para PDF
from reportlab.pdfgen import canvas as pdf_canvas

# ------------------ DATOS ------------------
dias = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
gastos = {dia: [] for dia in dias}
ingresos = 0
colchon = 0  

# ------------------ NUEVAS FUNCIONES DE EXPORTACIÓN ------------------

def exportar_excel():
    datos_exportar = []
    for dia in dias:
        for valor, fecha in gastos[dia]:
            datos_exportar.append({"Día": dia, "Fecha": fecha, "Monto": valor})
    
    if not datos_exportar:
        messagebox.showwarning("Atención", "No hay datos para exportar")
        return

    filepath = filedialog.asksaveasfilename(defaultextension=".xlsx", 
                                            filetypes=[("Excel files", "*.xlsx")])
    if filepath:
        df = pd.DataFrame(datos_exportar)
        df.to_excel(filepath, index=False)
        messagebox.showinfo("Éxito", "Archivo Excel guardado correctamente")

def exportar_pdf():
    filepath = filedialog.asksaveasfilename(defaultextension=".pdf", 
                                            filetypes=[("PDF files", "*.pdf")])
    if not filepath:
        return

    c = pdf_canvas.Canvas(filepath, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "Reporte de Gastos Semanales")
    
    c.setFont("Helvetica", 12)
    y = 720
    c.drawString(100, y, f"Fecha de reporte: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    y -= 30
    
    total_gral = 0
    for dia in dias:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, y, f"--- {dia} ---")
        y -= 20
        c.setFont("Helvetica", 10)
        
        if not gastos[dia]:
            c.drawString(120, y, "Sin gastos")
            y -= 15
        else:
            for valor, fecha in gastos[dia]:
                c.drawString(120, y, f"{fecha}: ${valor:,.2f}")
                total_gral += valor
                y -= 15
                if y < 50: # Nueva página si se acaba el espacio
                    c.showPage()
                    y = 750
        y -= 10

    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, y, f"TOTAL GASTADO: ${total_gral:,.2f}")
    c.drawString(100, y-20, f"SALDO EN COLCHÓN: ${colchon:,.2f}")
    
    c.save()
    messagebox.showinfo("Éxito", "Archivo PDF guardado correctamente")

# ------------------ FUNCIONES EXISTENTES (SIN CAMBIOS) ------------------
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
    total_gastos = sum([v[0] for lista in gastos.values() for v in lista])
    balance = ingresos - total_gastos
    color = "#4DD0E1" if balance>=0 else "#FF5252"
    label_balance.config(text=f"Balance actual: ${balance:,.2f} | Colchón: ${colchon:,.2f}", fg=color)
    dibujar_grafico_animado(0)

def dibujar_grafico_animado(paso):
    # (Se mantiene tu lógica de dibujo original aquí)
    canvas.delete("all")
    # ... (resto del código del canvas igual al tuyo) ...
    pass

# ------------------ VENTANA ------------------
root = tk.Tk()
root.title("Sistema Financiero Pro")
root.geometry("1000x800")
root.configure(bg="#1E1E2F")

# ... (Tus secciones de Ingresos, Gastos y Colchón se mantienen igual) ...

# ------------------ NUEVA SECCIÓN: EXPORTACIÓN ------------------
frame_export = tk.LabelFrame(root, text="Exportar Datos", bg="#2A2A50", fg="white", 
                             font=("Arial",12,"bold"), padx=15, pady=10)
frame_export.pack(fill="x", padx=15, pady=5)

btn_excel = tk.Button(frame_export, text="Exportar a Excel", bg="#28a745", fg="white", 
                      font=("Arial",10,"bold"), command=exportar_excel)
btn_excel.pack(side="left", padx=20, expand=True, fill="x")

btn_pdf = tk.Button(frame_export, text="Exportar a PDF", bg="#dc3545", fg="white", 
                    font=("Arial",10,"bold"), command=exportar_pdf)
btn_pdf.pack(side="left", padx=20, expand=True, fill="x")

# --- (El resto de tu código de tablas y canvas va aquí abajo) ---

root.mainloop()