#!/bin/bash
# since Bash v4
for i in {10..500..10}
do
     ./blas $i data
done
