#!/bin/bash
### to add parameter to be replace in sbatch file add @name@ to it and use in the runs.toml add thing to replace it
################################################################################################
### sbatch configuration parameters must start with #SBATCH and must precede any other commands.
### To ignore, just add another # - like so: ##SBATCH
################################################################################################

#SBATCH --partition rtx3090
#SBATCH --time 0-24:30:00
#SBATCH --job-name inverse_transformer
#SBATCH --output ../logs/job-%A-%a.out
#SBATCH --gpus=1

#SBATCH --qos=ZenCoat
#SBATCH --array=0-3
# Note: the following 4 lines are commented out
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
source activate attn
python main.py "configs/templet/confs/$SLURM_ARRAY_TASK_ID.toml"