#include<stdio.h>
#include<stdlib.h>
#include<malloc.h>
#include<string.h>

/* print all permutations of the string provided */
/* usage: ./a.out hello                         */

void permutations(char* head, char* string, int headsize, int bagsize)
{
	char* bag;
	char* top;
	char* pos;
	
	if(bagsize == 0)
	{
		int i;
		for(i=0;i<headsize-1;i++)
		{
			fputc(i[head], stdout);
		}
		fputc(0[string], stdout);
		fputc('\n', stdout);
		return;
	}
		
	bag = malloc(bagsize+1 * sizeof(char));
	if(bag == NULL)
		exit(1);
	top = malloc(headsize+1 * sizeof(char));
	if(top == NULL)
		exit(1);
		
	pos = string;

	while(0[pos] != '\0') 
	{
		char* temp;
		int i;
		i=0;
		temp = string;
		while(0[temp] != '\0') 
		{ /* copy all but current pos to bag */
			if(temp != pos) 
				bag[i++] = 0[temp];
			temp++;
		}
		/* copy head plus pos to top */
		top[headsize]='\0';
		bag[bagsize]='\0';
		for(i=0;i<headsize-1;i++) 
		{
			top[i]=head[i];
		}
		top[headsize-1]=0[pos];

		/* make recursive call */
		/*printf("Head is: %s\n", top);
		printf("Bag  is: %s\n", bag);
		printf("Headsize: %d\nBagsize: %d\n", headsize, bagsize); */
		permutations(top, bag, headsize+1, bagsize-1);
		pos++;

	}	

	free(bag);
	free(top);
}

int main(int argc, char **argv) {
	
	int x=0;
	if(argc != 2)
		exit(1);
	while(argv[1][x] != '\0') 
	{
		x++;
	}
	if(x==1)
	{
		putc(argv[1][0], stdout);
		putc('\n', stdout);
		exit(0);
	}
	permutations(NULL, argv[1],  1, x-1);
	exit(0);
}


