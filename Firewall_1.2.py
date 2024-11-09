import random

class Zona:
    def __init__(self, nombre):
        self.nombre = nombre
        self.reglas = []

class Regla:
    def __init__(self, origen, destino, accion, puerto=None):
        self.origen = origen
        self.destino = destino
        self.accion = accion  # 'permitir' o 'bloquear'
        self.puerto = puerto  # Opcional: permite reglas basadas en puertos

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
        print(log)

    def mostrar_logs(self):
        print("\nRegistros de tráfico:")
        for log in self.logs:
            print(log)
        print()

def verificar_trafico(origen, destino, zona_origen, zona_destino, puerto):
    for regla in zona_origen.reglas:
        if regla.origen == origen and regla.destino == destino:
            if regla.puerto is None or regla.puerto == puerto:
                return regla.accion
    return "bloqueado"

def menu_principal():
    zonas = {}
    nat = NAT()
    registro = Registro()

    while True:
        print("\n--- Simulador de Firewall ---")
        print("1. Crear zona")
        print("2. Crear regla de firewall")
        print("3. Configurar NAT")
        print("4. Simular tráfico")
        print("5. Ver registros de tráfico")
        print("6. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            nombre_zona = input("Nombre de la zona: ")
            if nombre_zona not in zonas:
                zonas[nombre_zona] = Zona(nombre_zona)
                print(f"Zona '{nombre_zona}' creada.")
            else:
                print("La zona ya existe.")

        elif opcion == "2":
            origen = input("Zona de origen: ")
            destino = input("Zona de destino: ")
            accion = input("Acción (permitir/bloquear): ")
            puerto = input("Puerto (opcional, presiona Enter para omitir): ")
            puerto = int(puerto) if puerto else None

            if origen in zonas and destino in zonas:
                regla = Regla(origen, destino, accion, puerto)
                zonas[origen].reglas.append(regla)
                print(f"Regla creada para tráfico de {origen} a {destino}, acción: {accion}, puerto: {puerto}.")
            else:
                print("Una o ambas zonas no existen.")

        elif opcion == "3":
            ip_interna = input("IP interna: ")
            ip_externa = input("IP externa: ")
            nat.agregar_NAT(ip_interna, ip_externa)
            print(f"NAT configurado: {ip_interna} -> {ip_externa}")

        elif opcion == "4":
            origen_ip = input("IP de origen: ")
            destino_ip = input("IP de destino: ")
            origen_zona = input("Zona de origen: ")
            destino_zona = input("Zona de destino: ")
            puerto = int(input("Puerto: "))

            if origen_zona in zonas and destino_zona in zonas:
                ip_externa = nat.obtener_ip_externa(origen_ip)
                if ip_externa != "No NAT":
                    print(f"IP de origen NAT aplicada: {origen_ip} -> {ip_externa}")
                    origen_ip = ip_externa

                accion = verificar_trafico(origen_zona, destino_zona, zonas[origen_zona], zonas[destino_zona], puerto)
                registro.registrar(origen_ip, destino_ip, accion, puerto)
            else:
                print("Una o ambas zonas no existen.")

        elif opcion == "5":
            registro.mostrar_logs()

        elif opcion == "6":
            print("Saliendo del simulador de firewall.")
            break

        else:
            print("Opción inválida. Por favor, intenta de nuevo.")

if __name__ == "__main__":
    menu_principal()

