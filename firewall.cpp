#include <gtkmm.h>
#include <string>
#include <unordered_map>
#include <vector>
#include <sstream>

class Regla {
public:
    std::string origen;
    std::string destino;
    std::string accion;
    int puerto;

    Regla(const std::string& origen, const std::string& destino, const std::string& accion, int puerto = -1)
        : origen(origen), destino(destino), accion(accion), puerto(puerto) {}
};

class Zona {
public:
    std::string nombre;
    std::vector<Regla> reglas;

    Zona(const std::string& nombre) : nombre(nombre) {}
};

class NAT {
public:
    std::unordered_map<std::string, std::string> tabla_nat;

    void agregar_NAT(const std::string& ip_interna, const std::string& ip_externa) {
        tabla_nat[ip_interna] = ip_externa;
    }

    std::string obtener_ip_externa(const std::string& ip_interna) const {
        auto it = tabla_nat.find(ip_interna);
        return it != tabla_nat.end() ? it->second : "NO NAT";
    }
};

class Registro {
public:
    std::vector<std::string> logs;

    void registrar(const std::string& origen, const std::string& destino, const std::string& accion, int puerto = -1) {
        std::stringstream log;
        log << "Tráfico de " << origen << " a " << destino << " por puerto " << puerto << ": " << accion;
        logs.push_back(log.str());
    }

    std::string mostrar_logs() const {
        std::stringstream all_logs;
        for (const auto& log : logs) {
            all_logs << log << "\n";
        }
        return all_logs.str();
    }
};

std::string verificar_trafico(const std::string& origen, const std::string& destino, const Zona& zona_origen, const Zona& zona_destino, int puerto) {
    for (const auto& regla : zona_origen.reglas) {
        if (regla.origen == origen && regla.destino == destino && (regla.puerto == -1 || regla.puerto == puerto)) {
            return regla.accion;
        }
    }
    return "bloqueado";
}

class FirewallApp : public Gtk::Window {
public:
    FirewallApp() {
        set_title("Simulador de Firewall");
        set_default_size(300, 300);

        zona_button.set_label("Crear Zona");
        regla_button.set_label("Crear Regla");
        nat_button.set_label("Configurar NAT");
        trafico_button.set_label("Simular Tráfico");
        logs_button.set_label("Ver Registros");

        vbox.pack_start(zona_button);
        vbox.pack_start(regla_button);
        vbox.pack_start(nat_button);
        vbox.pack_start(trafico_button);
        vbox.pack_start(logs_button);
        
        add(vbox);
        zona_button.signal_clicked().connect(sigc::mem_fun(*this, &FirewallApp::crear_zona));
        regla_button.signal_clicked().connect(sigc::mem_fun(*this, &FirewallApp::crear_regla));
        nat_button.signal_clicked().connect(sigc::mem_fun(*this, &FirewallApp::configurar_nat));
        trafico_button.signal_clicked().connect(sigc::mem_fun(*this, &FirewallApp::simular_trafico));
        logs_button.signal_clicked().connect(sigc::mem_fun(*this, &FirewallApp::ver_registros));

        show_all_children();
    }

protected:
    void crear_zona() {
        Gtk::MessageDialog dialog(*this, "Zona creada", false, Gtk::MESSAGE_INFO);
        dialog.set_secondary_text("Zona creada.");
        dialog.run();
    }

    void crear_regla() {
        Gtk::MessageDialog dialog(*this, "Regla creada", false, Gtk::MESSAGE_INFO);
        dialog.set_secondary_text("Regla creada.");
        dialog.run();
    }

    void configurar_nat() {
        Gtk::MessageDialog dialog(*this, "NAT configurado", false, Gtk::MESSAGE_INFO);
        dialog.set_secondary_text("NAT configurado.");
        dialog.run();
    }

    void simular_trafico() {
        Gtk::MessageDialog dialog(*this, "Simulación de tráfico", false, Gtk::MESSAGE_INFO);
        dialog.set_secondary_text("Simulación realizada.");
        dialog.run();
    }

    void ver_registros() {
        Gtk::MessageDialog dialog(*this, "Registros de tráfico", false, Gtk::MESSAGE_INFO);
        dialog.set_secondary_text("Mostrando registros.");
        dialog.run();
    }

private:
    Gtk::Box vbox{Gtk::ORIENTATION_VERTICAL};
    Gtk::Button zona_button, regla_button, nat_button, trafico_button, logs_button;

    std::unordered_map<std::string, Zona> zonas;
    NAT nat;
    Registro registro;
};

int main(int argc, char* argv[]) {
    auto app = Gtk::Application::create(argc, argv, "org.gtkmm.example");
    FirewallApp firewallApp;
    return app->run(firewallApp);
}

