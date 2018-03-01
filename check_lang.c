#include<stdio.h>
#include<stdlib.h>
#include<string.h>

/* Letter frequencies for the English language
 * values from https://en.wikipedia.org/wiki/Letter_frequency.
 */

double eng_charfreqs[29] = {
/* a */ 8.167, 
/* b */	1.492, 
/* c */	2.782, 
/* d */	4.253, 
/* e */	12.702, 
/* f */	2.228, 
/* g */	2.015, 
/* h */	6.094, 
/* i */	6.966, 
/* j */	0.153, 
/* k */	0.772, 
/* l */	4.025, 
/* m */	2.406, 
/* n */	6.749, 
/* o */	7.507, 
/* p */	1.929, 
/* q */	0.095, 
/* r */	5.987, 
/* s */	6.327, 
/* t */	9.056, 
/* u */	2.758, 
/* v */	0.978, 
/* w */	2.360, 
/* x */	0.150, 
/* y */	1.974, 
/* z */ 0.074,
/* extended ASCII */ 0.0,
/* control ASCII */ 0.0,
/* symbols */ 0.0};

/* histogram vector */
double char_hist[29];

double mean_sqr_error() {
	double total = 0.0;
	double temp = 0.0;
	int idx;

	for(idx=0; idx<29; idx++) {
		temp = char_hist[idx] - eng_charfreqs[idx];
		temp *= temp; /* square the error */
		total += temp;
	}

	return total;
}

void test_lang() {
	int i;
	double total = 0.;

	/* normalize histogram */
	for(i=0;i<29;i++) {
		total += char_hist[i];
	}
	if(total <= 0.) { /* histogram was empty */
		total = 1.0;  /* not an English file */
	}
	for(i=0;i<29;i++) {
		char_hist[i] /= total;
		char_hist[i] *= 100.0;
	}

	printf(" %f\n", (float) mean_sqr_error());
}

void count(unsigned char input) {
	if(input >= 65 && input <= 90) { /* upper case */
		char_hist[input-65] += 1.0;	
	} else if (input >= 97 && input <= 122) { /* lower case */
		char_hist[input-97] += 1.0;
	} else if (input > 127) { /* extended ASCII catch */
		char_hist[26] += 1.0;
	} else if (input < 32) { /* control chars */
		char_hist[27] += 1.0;
	} else if (input >= 33 && input <= 47) { /* symbols */
		char_hist[28] += 1.0;
	}
}

void print_usage(char **argv)
{
	printf ("check-lang\n");
	printf ("-----------------------\n\n");
	printf ("Determine if a given file is ASCII English text based on character frequency.\n");
	printf ("usage:\n");
	printf ("%s inputfile\n\n", argv[0]);
	printf ("Program prints the Mean Squared Error.  Lowest value is best match.\n");
	fflush (stdout);
}

int main(int argc, char **argv) {
	
	FILE *in = NULL;
	unsigned char pt;
	
    if(argc != 2) {
		print_usage(argv);
		exit(0);
	}
	if(!strcmp (argv[1], "-h"))
	{
		print_usage(argv);
		exit(0);
	}
	if((in = fopen(argv[1], "rb")) == NULL)
	{
		printf ("Error opening input file %s.\n", argv[1]);
		exit(EXIT_FAILURE);
	}

	while(1) {
		/* read an input block (a single 8-bit byte) */
		if(fread(&pt,1,sizeof(char),in) == 0) { 
				break; /* reached EOF */
			}
		count(pt);
	}

	fclose(in); /* completed reading file */
	
	test_lang();

	return 0;
}

