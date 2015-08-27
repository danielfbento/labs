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
		return sizeof(m->matrix)*(m->columns)*(m->lines);
	}
	return 0;
}

unsigned long int sizeof_sparse_matrix(sparse_matrix_t *m)
{
	if (NULL != m)
	{
		return sizeof(m->values)/sizeof(float) +
			   (sizeof(m->rows) + sizeof(m->columns))/sizeof(int);
	}
	return 0;
}

unsigned int nnz(matrix_t *m)
{
	unsigned int count = 0;
	for (int l = 0; l < m->lines; l++)
	{
		for (int c = 0; c < m->columns; c++)
		{
			if (abs(m->matrix[l][c]) > 0) {
				count++;
			}
		}
	}

	return count;
}

unsigned int numel(matrix_t *m)
{
	return m->lines * m->columns;
}

float density(matrix_t *m)
{
	return nnz(m)/numel(m);
}

void set_value_matrix(matrix_t *m, int row, int column, float value)
{
	if ((row >= 0) && (row < m->lines) && (column >= 0) && (column < m->columns)) {
		if (NULL != &m->matrix[row][column])
		{
			m->matrix[row][column] = value;
		}
	}	
}

float **matrix_data_alloc(int l, int c)
{
	float **rows = (float **)calloc(l,sizeof(float *));
	int i = 0;
	for(i = 0; i < c; i++)
	{
		rows[i] = (float *)calloc(c,sizeof(float));
	}

	return rows;
}

matrix_t *init_matrix(int l, int c)
{
	matrix_t *matrix;
	matrix = (matrix_t *)calloc(1, sizeof(matrix_t));
	matrix->matrix = matrix_data_alloc(l, c);
	matrix->lines = l;
	matrix->columns = c;
	return matrix;
}

float **sparsematrix(int l,int c)
{

}

void print_matrix(float **m, int lines, int cols)
{
	for (int l = 0; l < lines; l++) {
		printf("[ ");
		for (int c = 0; c < cols; c++) {
			printf("%f ", m[l][c]);
		}
		printf(" ]\n");
	}
}

int main(int argc, char *argv[])
{
	int lines = 0, columns = 0;
	int i = 0, j = 0;
	float **m = NULL;
	matrix_t *matrix = NULL;
	
	scanf("%d %d",&lines,&columns);
	
	printf("Creating matrix with %dx%d\n",lines,columns);

	m = matrix_data_alloc(lines,columns);
	matrix = init_matrix(lines, columns);

	printf("m Size: %d bytes\n",sizeof(m)*lines*columns);
	printf("matrix Size: %d bytes\n",sizeof_matrix(matrix));
	
	for(i = 0; i < lines; i++)
	{
		for(j = 0; j < columns; j++)
		{
			if (i == j || i == (j-1) || i == (j+1) || j == (i-1) || j == (i+1))
			{
				m[i][j] = 1;
				set_value_matrix(matrix, i, j, 1);
			}
		}
	}

	printf("nnz(m) = %d | numel(m) = %d | density(m) = %f\n", nnz(matrix), numel(matrix), density(matrix));

	return 0;
}
