#!/bin/bash

function cleanup (){
    echo "cleanup tmp data";
    sudo rm -rf $wkdir;
}

unset $http_proxy
unset $https_proxy

input_location="XX_INL_XX"
output_location="XX_OPL_XX"
gdc_id="XX_GDC_XX"
barcode="XX_SM_XX"
picard="/mnt/tools/picard-tools/picard.jar"
fixit="/mnt/fix_it.py"
rna_reheader="/mnt/rna_reheader/rna_reheader.py"
wkdir=`sudo mktemp -d rh.XXXXXXXXXX -p /mnt/SCRATCH/`

cd $wkdir

trap cleanup EXIT

python \
$rna_reheader \
--input_location $input_location \
--output_location $output_location \
--gdc_id $gdc_id \
--picard $picard \
--fixit $fixit \
--barcode $barcode
