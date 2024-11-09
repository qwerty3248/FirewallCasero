#include <iostream>
#include <unordered_map>
#include <vector>
#include <string>

class Regla {
public:
    std::string origen;
    std::string destino;
    std::string accion; // "permitir" o "bloquear"
    int puerto;

    Regla(const std::string& origen, const std::string& destino, const std::string& accion, int puerto = -1)
        : origen(origen), destino(destino), accion(accion), puerto(puerto) {}
};

class Zona {
public:
    std::string nombre;
    std::vector<Regla> reglas;
    
    Zona() = default;
    Zona(const std::string& nombre) : nombre(nombre) {}

    void agregar_regla(const Regla& regla) {
        reglas.push_back(regla);
    }
};

class NAT {
private:
    std::unordered_map<std::string, std::string> tabla_nat;

public:
    void agregar_NAT(const std::string& ip_interna, const std::string& ip_externa) {
        tabla_nat[ip_interna] = ip_externa;
    }

    std::string obtener_ip_externa(const std::string& ip_interna) {
        return tabla_nat.count(ip_interna) ? tabla_nat[ip_interna] : "NO NAT";
    }
};

class Registro {
private:
    std::vector<std::string> logs;

public:
    void registrar(const std::string& origen, const std::string& destino, const std::string& accion, int puerto = -1) {
        std::string log = "Tráfico de " + origen + " a " + destino + " por puerto " + std::to_string(puerto) + ": " + accion;
        logs.push_back(log);
        std::cout << log << std::endl;
    }

    void mostrar_logs() {
        std::cout << "\nRegistros de tráfico:\n";
        for (const auto& log : logs) {
            std::cout << log << std::endl;
        }
    }
};

std::string verificar_trafico(const Zona& zona_origen, const std::string& origen, const std::string& destino, int puerto) {
    for (const auto& regla : zona_origen.reglas) {
        if (regla.origen == origen && regla.destino == destino) {
            if (regla.puerto == -1 || regla.puerto == puerto) {
                return regla.accion;
            }
        }
    }
    return "bloqueado";
}

int main(int argc, char* argv[]) {
    std::unordered_map<std::string, Zona> zonas;
    NAT nat;
    Registro registro;

    if (argc > 1) {
        std::string comando = argv[1];

        if (comando == "--crear_zona" && argc == 3) {
            std::string nombre_zona = argv[2];
            if (zonas.find(nombre_zona) == zonas.end()) {
                zonas[nombre_zona] = Zona(nombre_zona);
                std::cout << "Zona '" << nombre_zona << "' creada." << std::endl;
            } else {
                std::cout << "La zona ya existe." << std::endl;
            }
        }
        else if (comando == "--crear_regla" && argc == 6) {
            std::string origen = argv[2];
            std::string destino = argv[3];
            std::string accion = argv[4];
            int puerto = std::stoi(argv[5]);

            if (zonas.find(origen) != zonas.end() && zonas.find(destino) != zonas.end()) {
                Regla regla(origen, destino, accion, puerto);
                zonas[origen].agregar_regla(regla);
                std::cout << "Regla creada para tráfico de " << origen << " a " << destino 
                          << ", acción: " << accion << ", puerto: " << puerto << "." << std::endl;
            } else {
                std::cout << "Una o ambas zonas no existen." << std::endl;
            }
        }
        else if (comando == "--configurar_nat" && argc == 4) {
            std::string ip_interna = argv[2];
            std::string ip_externa = argv[3];
            nat.agregar_NAT(ip_interna, ip_externa);
            std::cout << "NAT configurado: " << ip_interna << " -> " << ip_externa << std::endl;
        }
        else if (comando == "--simular_trafico" && argc == 7) {
            std::string origen_ip = argv[2];
            std::string destino_ip = argv[3];
            std::string origen_zona = argv[4];
            std::string destino_zona = argv[5];
            int puerto = std::stoi(argv[6]);

            if (zonas.find(origen_zona) != zonas.end() && zonas.find(destino_zona) != zonas.end()) {
                std::string ip_externa = nat.obtener_ip_externa(origen_ip);
                if (ip_externa != "NO NAT") {
                    std::cout << "IP de origen NAT aplicada: " << origen_ip << " -> " << ip_externa << std::endl;
                    origen_ip = ip_externa;
                }

                std::string accion = verificar_trafico(zonas[origen_zona], origen_zona, destino_zona, puerto);
                registro.registrar(origen_ip, destino_ip, accion, puerto);
            } else {
                std::cout << "Una o ambas zonas no existen." << std::endl;
            }
        }
        else if (comando == "--ver_logs") {
            registro.mostrar_logs();
        }
    } else {
        std::cout << "Uso incorrecto de argumentos." << std::endl;
    }

    return 0;
}


/* Ejemplo de uso
./firewall --crear_zona Interna
./firewall --crear_regla Interna Externa permitir 80
./firewall --configurar_nat 192.168.0.1 203.0.113.1
./firewall --simular_trafico 192.168.0.1 203.0.113.2 Interna Externa 80
./firewall --ver_logs
*/


