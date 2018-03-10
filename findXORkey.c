#include<stdio.h>
#include<stdlib.h>
#include<malloc.h>

#define HI(x) ((x>>4) & 0x0F)
#define LO(x) ((x) & 0x0F)

/* histogram vector */
double char_hist[29];

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

double test_lang() {
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

	return mean_sqr_error();
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

/* returns 0xFF on error */
unsigned char hex2ascii(unsigned char input) {
	switch (input) {
		case 0 :
			return '0';
		case 1 :
			return '1';
		case 2 :
			return '2';
		case 3 :
			return '3';
		case 4:
			return '4';
		case 5 :
			return '5';
		case 6 :
			return '6';
		case 7 :
			return '7';
		case 8 :
			return '8';
		case 9 :
			return '9';
		case 10 :
			return 'a';
		case 11 :
			return 'b';
		case 12 :
			return 'c';
		case 13 :
			return 'd';
		case 14 :
			return 'e';
		case 15 :
			return 'f';
		default :
			return 255;
	}
}

/* returns 0xFF on error */
unsigned char ascii2hex(unsigned char input) {
	switch (input) {
		case '0' :
			return 0x00;
		case '1' :
			return 0x01;
		case '2' :
			return 0x02;
		case '3' :
			return 0x03;
		case '4' :
			return 0x04;
		case '5' :
			return 0x05;
		case '6' :
			return 0x06;
		case '7' :
			return 0x07;
		case '8' :
			return 0x08;
		case '9' :
			return 0x09;
		case 'a' :
		case 'A' :
			return 0x0A;
		case 'b' :
		case 'B' :
			return 0x0B;
		case 'c' :
		case 'C' :
			return 0x0C;
		case 'd' :
		case 'D' :
			return 0x0D;
		case 'e' :
		case 'E' :
			return 0x0E;
		case 'f' :
		case 'F' :
			return 0x0F;
		default :
			return 255;
	}
}

/* number of bits different between streams */
int hamming_dist(char *str1, char *str2, int len) {
	int idx = 0;
	int dist = 0;
	int shift;
	unsigned char mask;
	for(idx=0; idx<len; idx++) {
		for(shift=7;shift>=0;shift--) {
			mask = 0x00;
			mask |= 0x01 << shift;
			if((str1[idx] & mask) ^ (str2[idx] & mask))
				dist++;
		}
	}
	return dist;
}

/* provided an raw char string, and a trial keysize  *
 * report the hamming distance of taking the first   *
 * keysize bytes and checking against the next       *
 * keysize bytes.                                    */
int check_keysize(char *instr, int guess) {
	char *blk1;
	char *blk2;
	int dist = 0;

	int idx, glblidx = 0;

	blk1 = malloc(guess * sizeof(char));
	if(blk1 == NULL) {
		printf("Malloc failed.\n");
		exit(EXIT_FAILURE);
	}
	blk2 = malloc(guess * sizeof(char));
	if(blk2 == NULL) {
		printf("Malloc failed.\n");
		exit(EXIT_FAILURE);
	}

	for(idx=0;idx<guess;idx++)
		blk1[idx] = instr[glblidx++];

	for(idx=0;idx<guess;idx++)
		blk2[idx] = instr[glblidx++];

	/* return hamming_dist(&blk1[0], &blk2[0]); */
	dist = hamming_dist(&blk1[0], &blk2[0], guess);

	free(blk1);
	free(blk2);
	return dist;

}

/* normalized edit distance (edit dist divided by keylen) */
double norm_edit_dist(char *instr, int filelen, int size) {
	int i,sets = 0;
	double total = 0.0;
	for(i=0; i<(filelen/size); i+=size) {
		total += (double) check_keysize(&instr[i], size);
		sets += 1;
	}
	total /= (double)size;
	total /= (double)sets;
	return total;
}

int guess_keysize(char *instr, int filelen, int max_guess) {
	double mintrial = 1000.0; 
	double currenttrial;
	int best_guess = 0;
	int current_guess;
	
	for(current_guess=2;current_guess<max_guess;current_guess++) {
		currenttrial = norm_edit_dist(instr, filelen, current_guess);
		/* printf("Guess Key Size: %d Guess Error: %f.\n", current_guess, (float) currenttrial); */ 
		if(currenttrial<mintrial) {
			mintrial = currenttrial;
			best_guess = current_guess;
		}
	}

	return best_guess;
}

void rebuild_key(char *input, unsigned int insize, int keylen) {
	int inidx, keyidx, tidx, i;
	char *transpose;
	char *fullkey;
	double minerr, currenterr;
	char bestkey, tmp;

	int key;

	/* room for every n-th char of raw input */	

	fullkey = calloc(keylen, sizeof(char));
	if(fullkey == NULL) {
		printf("Malloc failed.\n");
		exit(EXIT_FAILURE);
	}

	for(keyidx=0; keyidx<keylen; keyidx++) {
		tidx=0;
		bestkey=0;
		minerr=1000000.;

		transpose = calloc(((insize/keylen)+keylen), sizeof(char));
		if(transpose == NULL ) {
			printf("Calloc failed.\n");
			exit(EXIT_FAILURE);
		}

		for(inidx=keyidx; inidx<insize;inidx+=keylen) {
			transpose[tidx++] = input[inidx];
		} /* copy every nth byte to transpose */
		for(key=0;key<256;key++) { /* for all possible keys */
			for(i=0;i<29;i++) { /* reset histogram */
				char_hist[i] = 0.;
			}
			for(i=0;i<tidx;i++) { /* for all in transpose array */
				/* xor with trial key, add to histogram */
				count(transpose[i] ^ (unsigned char) key);
			}
			currenterr = test_lang(); /* score histogram */
			if(currenterr < minerr) { /* better match */
				minerr = currenterr;
				bestkey = (unsigned char) key;
			}
		} /* found min error key */
		fputc(hex2ascii(HI(bestkey)), stdout);
		fputc(hex2ascii(LO(bestkey)), stdout);
		fullkey[keyidx] = bestkey;
		free(transpose);
	}

	fputc('\n', stdout);

	keyidx=0;
	for(i=0;i<insize;i++) {
		tmp = input[i] ^ fullkey[keyidx];
		keyidx++; keyidx %= keylen;
		fputc(tmp, stdout);
	} /* dump output */

	free(fullkey);

} 

int main(int argc, char **argv) {

	FILE *in      = NULL;
	unsigned int size;
	char *rawbytes = NULL;
	int readidx = 0;
	char inlo, inhi;

	int keysize;

	if((in = fopen(argv[1], "rb")) == NULL)
	{
		printf ("Error opening input file %s.\n", argv[1]);
		exit(EXIT_FAILURE);
	}
	fseek(in, 0, SEEK_END); 
	size = ftell(in); 
	fseek(in, 0, SEEK_SET);

	size /= 2;

	rawbytes = malloc(size * sizeof(char));
	if(rawbytes == NULL) {
		printf("Malloc failed.\n");
		exit(EXIT_FAILURE);
	}

	while(1) {
			
			if(fread(&inhi,1,sizeof(char),in) == 0) { /* reached EOF */
				break;
			}
			if(fread(&inlo,1,sizeof(char),in) == 0) { /* reached EOF */
				break;
			}
		rawbytes[readidx] = ascii2hex(inhi) << 4 | ascii2hex(inlo);
		readidx++;
	}
	fclose(in);

	keysize = guess_keysize(rawbytes, size, 40);
	printf("Guess Size: %d.\n", keysize);
	printf("Key: ");
	rebuild_key(rawbytes, size, keysize);
	fputc('\n', stdout);	
	free(rawbytes);
	return 0;
	
}
