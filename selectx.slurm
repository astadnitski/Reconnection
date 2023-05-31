#!/bin/bash -l
###SBATCH -M ukko
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:09:00
#SBATCH --mem-per-cpu=28G
#SBATCH --partition=short
#SBATCH --output=%x_%j.log
#SBATCH --job-name=SelectX

module load Python
../miniconda/bin/python3.10 SelectX.py
