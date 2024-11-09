import argparse
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

def main():
    parser = argparse.ArgumentParser(description="Simulador de Firewall")
    parser.add_argument("--crear_zona", help="Crear una nueva zona")
    parser.add_argument("--crear_regla", nargs=4, metavar=('origen', 'destino', 'accion', 'puerto'), 
                        help="Crear una regla de firewall: origen destino permitir/bloquear puerto")
    parser.add_argument("--configurar_nat", nargs=2, metavar=('ip_interna', 'ip_externa'), 
                        help="Configurar NAT: ip_interna ip_externa")
    parser.add_argument("--simular_trafico", nargs=5, metavar=('origen_ip', 'destino_ip', 'origen_zona', 'destino_zona', 'puerto'), 
                        help="Simular tráfico: origen_ip destino_ip origen_zona destino_zona puerto")
    parser.add_argument("--ver_logs", action="store_true", help="Mostrar registros de tráfico")

    args = parser.parse_args()

    zonas = {}
    nat = NAT()
    registro = Registro()

    if args.crear_zona:
        nombre_zona = args.crear_zona
        if nombre_zona not in zonas:
            zonas[nombre_zona] = Zona(nombre_zona)
            print(f"Zona '{nombre_zona}' creada.")
        else:
            print("La zona ya existe.")

    if args.crear_regla:
        origen, destino, accion, puerto = args.crear_regla
        puerto = int(puerto) if puerto else None

        if origen in zonas and destino in zonas:
            regla = Regla(origen, destino, accion, puerto)
            zonas[origen].reglas.append(regla)
            print(f"Regla creada para tráfico de {origen} a {destino}, acción: {accion}, puerto: {puerto}.")
        else:
            print("Una o ambas zonas no existen.")

    if args.configurar_nat:
        ip_interna, ip_externa = args.configurar_nat
        nat.agregar_NAT(ip_interna, ip_externa)
        print(f"NAT configurado: {ip_interna} -> {ip_externa}")

    if args.simular_trafico:
        origen_ip, destino_ip, origen_zona, destino_zona, puerto = args.simular_trafico
        puerto = int(puerto)

        if origen_zona in zonas and destino_zona in zonas:
            ip_externa = nat.obtener_ip_externa(origen_ip)
            if ip_externa != "NO NAT":
                print(f"IP de origen NAT aplicada: {origen_ip} -> {ip_externa}")
                origen_ip = ip_externa

            accion = verificar_trafico(origen_zona, destino_zona, zonas[origen_zona], zonas[destino_zona], puerto)
            registro.registrar(origen_ip, destino_ip, accion, puerto)
        else:
            print("Una o ambas zonas no existen.")

    if args.ver_logs:
        registro.mostrar_logs()

if __name__ == "__main__":
    main()


"""
python firewall.py --crear_zona ZONA
python firewall.py --crear_regla ORIGEN DESTINO ACCION PUERTO
python firewall.py --configurar_nat IP_INTERNA IP_EXTERNA
python firewall.py --simular_trafico ORIGEN_IP DESTINO_IP ORIGEN_ZONA PUERTO
python firewall.py --ver_logs
"""
"""
Ejemplos de uso en terminal
python firewall.py --crear_zona Interna
python firewall.py --crear_regla Interna Externa permitir 80
python firewall.py --configurar_nat 192.168.0.1 203.0.113.1
python firewall.py --simular_trafico 192.168.0.1 203.0.113.2 Interna Externa 80
python firewall.py --ver_logs
"""




