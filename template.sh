#!/bin/bash
#SBATCH --nodes=1
#SBATCH --cpus-per-task=20
#SBATCH --ntasks=1
#SBATCH --workdir="/mnt/SCRATCH/"

function cleanup (){
    echo "cleanup tmp data";
    sudo rm -rf $wkdir;
}

input_location="XX_INL_XX"
output_location="XX_OPL_XX"
outputdir_location="XX_OPD_XX"
gdc_id="XX_GDC_XX"
barcode="XX_SM_XX"
picard="quay.io/jeremiahsavage/picard_tool"
fixit="/mnt/fix_it.py"
rna_reheader="/mnt/rna_reheader/rna_reheader.py"
wkdir=`sudo mktemp -d rh.XXXXXXXXXX -p /mnt/SCRATCH/`
sudo chown ubuntu:ubuntu $wkdir

cd $wkdir

/home/ubuntu/.virtualenvs/p2/bin/python \
$rna_reheader \
--input_location $input_location \
--output_location $output_location \
--gdc_id $gdc_id \
--picard $picard \
--fixit $fixit \
--barcode $barcode

sleep 10

trap cleanup EXIT

aws --profile cleversafe --endpoint http://gdc-accessors.osdc.io s3 cp $wkdir $outputdir_location --recursive
