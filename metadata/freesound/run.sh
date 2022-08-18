#!/bin/bash


for (( c=1; c<=$1; c++ ))
do
  	sbatch /scratch/tyz/marl-demandresponse/job.sh
done