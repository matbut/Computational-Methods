CC=gcc
CFLAGS=-Wall 
PROGNAME=blas

compile:
	$(CC) $(CFLAGS) $(PROGNAME).c -lgsl -lgslcblas  -lm -o $(PROGNAME)
	chmod +x ./$(PROGNAME)
clean:
	rm -rf *.o $(PROGNAME)
