#include <stdio.h>
#include <stdlib.h>

struct matrix_struct {
	float **matrix;
	int columns;
	int lines;
} matrix_s;
typedef struct matrix_struct matrix_t;

struct sparse_matrix_struct {
	float *values;
	int *rows;
	int *columns;
} sparse_matrix_s;
typedef struct sparse_matrix_struct sparse_matrix_t;

unsigned long int sizeof_matrix(matrix_t *m)
{
	if (NULL != m)
	{
		return sizeof(m->matrix)*columns*lines;
	}
	return 0;
}

unsigned long int sizeof_sparse_matrix(sparse_matrix_t *m)
{
	if (NULL != m)
	{
		return sizeof(m->values)/sizeof(float) + (sizeof(rows)+sizeof(columns))/sizeof(int);
	}
	return 0;
}

void set_value_matrix(matrix_t *m,int row, int column, float value)
{
	if ((row > 0) && (row <= m->lines) && (column > 0) && (column <= m->columns)) {
		if (NULL != m[row][column])
		{
			m[row][column] = value;
		}
	}	
}

float **matrix(int l, int c)
{
	float **rows = (float **)calloc(l,sizeof(float *));
	int i = 0;
	for(i = 0; i < c; i++)
	{
		rows[i] = (float *)calloc(c,sizeof(float));
	}

	return rows;
}

float **sparsematrix(int l,int c)
{

}

void print_matrix(float **m)
{

}

int main(int argc, char *argv[])
{
	int lines = 0, columns = 0;
	int i = 0, j = 0;
	float **m = NULL;
	
	scanf("%d %d",&lines,&columns);
	
	printf("Creating matrix with %dx%d\n",lines,columns);

	m = matrix(lines,columns);

	printf("%d",sizeof(m)*lines*columns);

	
	for(i = 0; i < lines; i++)
	{
		for(j = 0; j < columns; j++)
		{
			if (i == j || i == (j-1) || i == (j+1) || j == (i-1) || j == (i+1))
			{
				m[i][j] = 1;
			}
		}
	}

	return 0;
}
