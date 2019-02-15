#include <stdio.h>
#include <gsl/gsl_blas.h>
#include <gsl/gsl_vector.h>
#include <time.h>
#include <sys/time.h>
#include <unistd.h>
#include <string.h>


#define MAX_RAND 1000
#define SAMPLES_NUM 10 

double  count_time(struct timeval start,struct timeval end){
	return (end.tv_sec-start.tv_sec)+(end.tv_usec-start.tv_usec)/1000000.0;
}

void naive_multiplication(int **A,int **B,int **C,int size){
	for(int i=0;i<size;i++)
		for(int j=0;j<size;j++)
			for (int k=0;k<size;k++)
				C[j][i]=C[j][i]+A[j][k]*B[k][i];
}

void better_multiplication(int **A,int **B,int **C,int size){
	for(int i=0;i<size;i++)
		for(int j=0;j<size;j++)
			for (int k=0;k<size;k++)
				C[j][k]=C[j][k]+A[j][i]*B[i][k];
}

void csv_file(char *filename,char*exp_name,int dim,double samples[SAMPLES_NUM]){
	FILE *fp;
	
	if(access(filename,F_OK)==-1){
		fp=fopen(filename,"w");
		fprintf(fp,"Method,Size,Time\n");
	}else{
		fp=fopen(filename,"a");
	}
	int i;
	for(i=0;i<SAMPLES_NUM-1;i++)
		fprintf(fp,"%s,%d,%lf\n",exp_name,dim,samples[i]);    	
	fclose(fp);
}

int main(int argc, char **argv)
{    
	size_t size = (size_t) atoi(argv[1]);
	char*filename = strcat(argv[2],".csv");

	gsl_matrix* matrixA = gsl_matrix_alloc(size,size);
	gsl_matrix* matrixB = gsl_matrix_alloc(size,size);
	gsl_matrix* matrixC = gsl_matrix_alloc(size,size);
	int**A = calloc(size,sizeof(int*));
	int**B = calloc(size,sizeof(int*));
	int**C = calloc(size,sizeof(int*));
	for(int i=0;i<size;i++){
		A[i] = calloc(size,sizeof(int));
		B[i] = calloc(size,sizeof(int));
		C[i] = calloc(size,sizeof(int));
		for(int j=0;j<size;j++){
			A[i][j]=rand()%MAX_RAND;
			B[i][j]=rand()%MAX_RAND;
			gsl_matrix_set(matrixA,i,j,A[i][j]);
			gsl_matrix_set(matrixB,i,j,B[i][j]);
		}
			
	}

	struct timeval start,end;
	double naive_samples[SAMPLES_NUM];
	double better_samples[SAMPLES_NUM];
	double blas_samples[SAMPLES_NUM];
	
	for(int i=0;i<SAMPLES_NUM;i++){
		gettimeofday(&start, 0);
		naive_multiplication(A,B,C,size);
		gettimeofday(&end, 0);
		naive_samples[i]=count_time(start,end);

		gettimeofday(&start, 0);
		better_multiplication(A,B,C,size);
		gettimeofday(&end, 0);
		better_samples[i]=count_time(start,end);

		gettimeofday(&start,0);
		gsl_blas_dgemm(CblasNoTrans,CblasNoTrans,1.0,matrixA,matrixB,0.0,matrixC);
		gettimeofday(&end,0);
		blas_samples[i]=count_time(start,end);	
	}
	
	csv_file(filename,"naive",size,naive_samples);
	csv_file(filename,"better",size,better_samples); 
	csv_file(filename,"blas",size,blas_samples); 
	return 0;
}