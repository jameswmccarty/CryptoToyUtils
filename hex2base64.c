#include<stdio.h>
#include<stdlib.h>
#include<string.h>

#define HI(x) ((x>>4) & 0x0F)
#define LO(x) ((x) & 0x0F)

/* base64 index table */
const static unsigned char b64[64] = {'A', 'B', 'C', 'D', 
	'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 
	'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 
	'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
	'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
	's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1',
	'2', '3', '4', '5', '6', '7', '8', '9', '+', '/'};

/* returns 0xFF on error */
unsigned char b64idx(unsigned char input) {
	unsigned char idx;
	for(idx=0; idx<64; idx++) {
		if(b64[idx] == input) {
			return idx;
		}
	}
	return 0xFF;
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

void hextobase64(unsigned char *hexstr) {
	int b64_idx = 5;
	unsigned char b64_out = 0x00;
	unsigned char tmp;

	int inputidx = 0;
	int inloop;
	while(hexstr[inputidx]) {
		tmp = ascii2hex(hexstr[inputidx]);
		if(tmp == 0xFF) /* error condition */
			return;
		for(inloop=3; inloop>=0; inloop--) {
			if(tmp & (0x01 << inloop)) {
				b64_out |= (0x01 << b64_idx);
			}
			b64_idx--;
			if(b64_idx < 0) { /* packed a full output 6-bits */
				b64_idx = 5;
				(void) fputc(b64[b64_out], stdout);
				b64_out = 0x00;
			}
		}
		inputidx++;
	}

	if(b64_idx != 5) { /* partial state */
		(void) fputc(b64[b64_out], stdout);
	}

	return;
}

void base64tohex(unsigned char *b64str) {
	int hex_idx = 7;
	unsigned char hex_out = 0x00;
	unsigned char tmp;

	int inputidx = 0;
	int inloop;
	while(b64str[inputidx]) {
		tmp = b64idx(b64str[inputidx]); /* pop single input char */
		if(tmp == 0xFF) /* error condition */
			return;
		for(inloop=5; inloop>=0; inloop--) {
			if(tmp & (0x01 << inloop)) {
				hex_out |= (0x01 << hex_idx);

			}
			hex_idx--;
			if(hex_idx < 0) { /* packed full output 8-bits */
				hex_idx = 7;
				(void) fputc(hex2ascii(HI(hex_out)), stdout);
				(void) fputc(hex2ascii(LO(hex_out)), stdout);
				hex_out = 0x00;
			}
		}

		inputidx++;
	}

	return;
}

int main(int argc, char **argv) {

	/*unsigned char hexstr[] = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d";

	unsigned char b64str[] = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t";

	base64tohex(&b64str[0]);
	printf("\n");
	hextobase64(&hexstr[0]);
	printf("\n"); */

	if(argc != 3) {
		printf("Usage: %s -b/-x input\n", argv[0]);
		printf("Flag -b if input is in Base64.  Flag -x in input is Hexadecimal.\n");
		printf("Program outputs coded string to stdout.\n");
		exit(EXIT_FAILURE);
	}
	if(!strcmp("-b", argv[1])) {
		base64tohex((unsigned char *) &argv[2][0]);
	} else if (!strcmp("-x", argv[1])) {
		hextobase64((unsigned char *) &argv[2][0]);
	} else {
		printf("Invalid input flag.\n");
	}

	printf("\n");

	return 0;
}
