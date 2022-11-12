#!/bin/bash
### to add parameter to be replace in sbatch file add @name@ to it and use in the runs.toml add thing to replace it
################################################################################################
### sbatch configuration parameters must start with #SBATCH and must precede any other commands.
### To ignore, just add another # - like so: ##SBATCH
################################################################################################

#SBATCH --partition @PARTITION@
#SBATCH --time @TIME@
#SBATCH --job-name @JOB-NAME@
#SBATCH --output @OUTPUT@
#SBATCH --gpus=1

#SBATCH --qos=@QOS@
#SBATCH --array=@RANGE@
# Note: the following 3 lines are commented out
##SBATCH --mail-user=@MAIL@
##SBATCH --mail-type=ALL                        ### conditions for sending the email. ALL,BEGIN,END,FAIL, REQUEU, NONE
##SBATCH --mem=24G                              ### ammount of RAM memory, allocating more than 60G requires IT team's permission

### Print some data to output file ###
echo `date`
echo -e "\nSLURM_JOBID:\t\t" $SLURM_JOBID
echo -e "running configs/testrun/confs/$SLURM_ARRAY_TASK_ID.toml config"
echo -e "SLURM_JOB_NODELIST:\t" $SLURM_JOB_NODELIST "\n\n"

### Start your code below ####
module load anaconda
source activate @CONDA_ENV@
python main.py "@CONF_PATH@/$SLURM_ARRAY_TASK_ID.toml"