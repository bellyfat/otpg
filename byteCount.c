#include <stdio.h>

int main (int argc, char **argv) {
	unsigned int c, min = 0xFFFF, max = 0, mean = 0;
	unsigned int byteCount[256] = {'0'};
	FILE *fp;

	if (argc < 2) fp = stdin;
	else fp = fopen (argv[1], "r");

	if (fp == NULL) {
		fprintf (stderr, "Invalide file : %s\n", argv[1]);
		exit(-1);
	}

	while ((c = fgetc(fp)) != EOF) {
		byteCount[c]++;
	}

	for (c = 0; c < 255; c++) {
		if (byteCount[c] < min) min = byteCount[c];
		if (byteCount[c] > max) max = byteCount[c];
		mean += byteCount[c];
		printf ("%02x\t%d\n", c, byteCount[c]);
	}
	mean /= 256;

	printf ("Min=%d Max=%d Mean=%d\n", min, max, mean);

	return 0;
}
