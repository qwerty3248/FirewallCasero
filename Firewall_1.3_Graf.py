import tkinter as tk
from tkinter import messagebox

class Zona:
    def __init__(self, nombre):
        self.nombre = nombre
        self.reglas = []

class Regla:
    def __init__(self, origen, destino, accion, puerto=None):
        self.origen = origen
        self.destino = destino
        self.accion = accion
        self.puerto = puerto

class NAT:
    def __init__(self):
        self.tabla_nat = {}

    def agregar_NAT(self, ip_interna, ip_externa):
        self.tabla_nat[ip_interna] = ip_externa

    def obtener_ip_externa(self, ip_interna):
        return self.tabla_nat.get(ip_interna, "NO NAT")

class Registro:
    def __init__(self):
        self.logs = []

    def registrar(self, origen, destino, accion, puerto=None):
        log = f"Tráfico de {origen} a {destino} por puerto {puerto}: {accion}"
        self.logs.append(log)
        return log

    def mostrar_logs(self):
        return "\n".join(self.logs)

def verificar_trafico(origen, destino, zona_origen, zona_destino, puerto):
    for regla in zona_origen.reglas:
        if regla.origen == origen and regla.destino == destino:
            if regla.puerto is None or regla.puerto == puerto:
                return regla.accion
    return "bloqueado"

class FirewallApp:
    def __init__(self, root):
        self.zonas = {}
        self.nat = NAT()
        self.registro = Registro()
        
        self.root = root
        self.root.title("Simulador de Firewall")

        # Widgets para zonas
        self.zona_label = tk.Label(root, text="Nombre de Zona:")
        self.zona_label.pack()
        self.zona_entry = tk.Entry(root)
        self.zona_entry.pack()
        self.zona_button = tk.Button(root, text="Crear Zona", command=self.crear_zona)
        self.zona_button.pack()

        # Widgets para reglas
        self.regla_label = tk.Label(root, text="Regla (Origen, Destino, Acción, Puerto):")
        self.regla_label.pack()
        self.origen_entry = tk.Entry(root)
        self.origen_entry.pack()
        self.destino_entry = tk.Entry(root)
        self.destino_entry.pack()
        self.accion_entry = tk.Entry(root)
        self.accion_entry.pack()
        self.puerto_entry = tk.Entry(root)
        self.puerto_entry.pack()
        self.regla_button = tk.Button(root, text="Crear Regla", command=self.crear_regla)
        self.regla_button.pack()

        # Widgets para NAT
        self.nat_label = tk.Label(root, text="NAT (IP Interna -> IP Externa):")
        self.nat_label.pack()
        self.ip_interna_entry = tk.Entry(root)
        self.ip_interna_entry.pack()
        self.ip_externa_entry = tk.Entry(root)
        self.ip_externa_entry.pack()
        self.nat_button = tk.Button(root, text="Configurar NAT", command=self.configurar_nat)
        self.nat_button.pack()

        # Widgets para simular tráfico
        self.trafico_label = tk.Label(root, text="Simulación de Tráfico (IP Origen, IP Destino, Zona Origen, Zona Destino, Puerto):")
        self.trafico_label.pack()
        self.origen_ip_entry = tk.Entry(root)
        self.origen_ip_entry.pack()
        self.destino_ip_entry = tk.Entry(root)
        self.destino_ip_entry.pack()
        self.zona_origen_entry = tk.Entry(root)
        self.zona_origen_entry.pack()
        self.zona_destino_entry = tk.Entry(root)
        self.zona_destino_entry.pack()
        self.puerto_trafico_entry = tk.Entry(root)
        self.puerto_trafico_entry.pack()
        self.trafico_button = tk.Button(root, text="Simular Tráfico", command=self.simular_trafico)
        self.trafico_button.pack()

        # Botón para ver registros
        self.logs_button = tk.Button(root, text="Ver Registros de Tráfico", command=self.ver_registros)
        self.logs_button.pack()

    def crear_zona(self):
        nombre_zona = self.zona_entry.get()
        if nombre_zona not in self.zonas:
            self.zonas[nombre_zona] = Zona(nombre_zona)
            messagebox.showinfo("Zona Creada", f"Zona '{nombre_zona}' creada.")
        else:
            messagebox.showwarning("Zona Existente", "La zona ya existe.")

    def crear_regla(self):
        origen = self.origen_entry.get()
        destino = self.destino_entry.get()
        accion = self.accion_entry.get()
        puerto = self.puerto_entry.get()
        puerto = int(puerto) if puerto else None

        if origen in self.zonas and destino in self.zonas:
            regla = Regla(origen, destino, accion, puerto)
            self.zonas[origen].reglas.append(regla)
            messagebox.showinfo("Regla Creada", f"Regla creada para tráfico de {origen} a {destino}, acción: {accion}, puerto: {puerto}.")
        else:
            messagebox.showerror("Error", "Una o ambas zonas no existen.")

    def configurar_nat(self):
        ip_interna = self.ip_interna_entry.get()
        ip_externa = self.ip_externa_entry.get()
        self.nat.agregar_NAT(ip_interna, ip_externa)
        messagebox.showinfo("NAT Configurado", f"NAT configurado: {ip_interna} -> {ip_externa}")

    def simular_trafico(self):
        origen_ip = self.origen_ip_entry.get()
        destino_ip = self.destino_ip_entry.get()
        origen_zona = self.zona_origen_entry.get()
        destino_zona = self.zona_destino_entry.get()
        puerto = int(self.puerto_trafico_entry.get())

        if origen_zona in self.zonas and destino_zona in self.zonas:
            ip_externa = self.nat.obtener_ip_externa(origen_ip)
            if ip_externa != "NO NAT":
                origen_ip = ip_externa

            accion = verificar_trafico(origen_zona, destino_zona, self.zonas[origen_zona], self.zonas[destino_zona], puerto)
            log = self.registro.registrar(origen_ip, destino_ip, accion, puerto)
            messagebox.showinfo("Resultado de Tráfico", log)
        else:
            messagebox.showerror("Error", "Una o ambas zonas no existen.")

    def ver_registros(self):
        logs = self.registro.mostrar_logs()
        messagebox.showinfo("Registros de Tráfico", logs)

if __name__ == "__main__":
    root = tk.Tk()
    app = FirewallApp(root)
    root.mainloop()

