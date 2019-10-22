default: f2d d2f

f2d:
	gcc -O2 -Wall f2d.c -o f2d

d2f:
	gcc -O2 -Wall d2f.c -o d2f

clean:
	rm f2d d2f

install: f2d d2f
	cp f2d /usr/local/bin/cpuex_f2d
	chmod 755 /usr/local/bin/cpuex_f2d
	cp d2f /usr/local/bin/cpuex_d2f
	chmod 755 /usr/local/bin/cpuex_d2f
	echo "installed: cpuex_f2d, cpuex_d2f in /usr/bin"

uninstall:
	rm -rf /usr/local/bin/cpuex_f2d
	rm -rf /usr/local/bin/cpuex_d2f
