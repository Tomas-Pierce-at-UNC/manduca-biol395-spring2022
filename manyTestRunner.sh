#!/bin/bash

#SBATCH -p general
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem=3g
#SBATCH -t 2-00:00:00

module add python
python3 many_tests.py
