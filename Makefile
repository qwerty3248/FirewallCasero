

ALL:	
	g++ firewall.cpp -o firewall `pkg-config --cflags --libs gtkmm-3.0`
	g++ -o firewall2 firewall2.cpp



clean:
	rm -rf firewall
	rm -rf firewall2
