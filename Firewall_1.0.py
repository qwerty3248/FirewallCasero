
#Define las zonas de la red 
class Zona:
	def __init__(self,nombre):
		self.nombre = nombre
		self.reglas = []
	
#Define las reglas para el firewall	
class Regla:
	def __init__(self,origen,destino,accion):
		self.origen = origen
		self.destino = destino
		self.accion = accion #Permitir o bloquear una accion
#Traducir las IPs privadas a una publica	
class NAT:
	def __init__(self):
		self.tabla_nat = {} #Mapear IPs internas a IPs externas
	
	def agregar_NAT(self,ip_interna,ip_externa):
		self.tabla_nat[ip_interna] = ip_externa
		
	def obtener_ip_externa(self,ip_interna):
		return self.tabla_nat.get(ip_interna,"NO NAT")
#Captura un resgistro de las conexiones que se han intentado o que lo han coseguido		
class Registro:
	def __init__(self):
		self.logs = []
	
	def registrar(self,origen,destino,accion):
		log = f"Trafico de {origen} a {destino}: {accion}"
		self.logs.append(log)
		print(log) #El log primero vemos si funciona y luego vemos si lo pasamos a un archivo


#Funcion que puede ayudar a simular algo de trafico		
def verificar_trafico(origen,destino,zona_origen,zona_destino):
	for regla in zona_origen.reglas:
		if regla.origen == origen and regla.destino == destino:
			return regla.accion
	return "Bloqueado"
	
	





if __name__=="__main__":
	
	#Aqui tenemos mis zonas y mis reglas
	zona_interna = Zona("Interna")
	zona_externa = Zona("Externa")
	
	regla1 = Regla("Interna","Externa","Permitir")
	regla2 = Regla("Externa","Interna","Bloquear")
	
	zona_interna.reglas.append(regla1)
	zona_externa.reglas.append(regla2)
	
	#Creamos NAT y registros
	nat = NAT()
	registro = Registro()
	nat.agregar_NAT("192.168.1.10","200.0.113.5")
	
	#Ahora en esta parte simularemos el trafico
	origen_ip = "192.168.1.10"
	destino_ip = "200.0.113.5"
	origen = "Interna"
	destino = "Externa"
	accion = verificar_trafico(origen,destino,zona_interna,zona_externa)
	registro.registrar(origen,destino,accion)
	
	
	
	
	
	


														
