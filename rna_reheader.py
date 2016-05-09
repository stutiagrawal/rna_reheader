import os
import sys
import argparse
import subprocess

def main(args):
    step_dir = os.getcwd()
    base_name = os.path.basename(args.output_location)
    fixed_bam = os.path.join(step_dir, base_name)
    cmd1 = ['aws',
           '--profile',
           'cleversafe',
           '--endpoint',
           'http://gdc-accessors.osdc.io',
           's3',
           'cp '+str(args.input_location),
           '-',
           '| '+str(args.fixit),
           '--sm '+str(args.barcode),
           '--pl',
           'ILLUMINA',
           '-',
           '|',
           'java',
           '-jar',
           '-Xmx2G '+str(args.picard),
           'FixMateInformation',
           'I=/dev/stdin',
           'O='+fixed_bam,
           '2> '+str(args.gdc_id)+'.fixmateinfo.log']
    cmd2 = ['java',
           '-jar',
           '-Xmx2G '+str(args.picard),
           'ValidateSamFile',
           'I='+fixed_bam,
           'VALIDATION_STRINGENCY=LENIENT',
           'O='+str(args.gdc_id)+'.validate',
           '2> '+str(args.gdc_id)+'.validate.log',
           '|',
           'java',
           '-jar',
           '-Xmx2G '+str(args.picard),
           'BuildBamIndex',
           'I='+fixed_bam,
           'O='+str(args.gdc_id)+'_gdc_realn_rehead.bai',
           '2> '+str(args.gdc_id)+'.buildbamindex.log',
           '|',
           'md5sum',
           fixed_bam,
           '> '+str(args.gdc_id)+'_md5.txt',
           '>/dev/null']
    shell_cmd1 = ' '.join(cmd1)
    subprocess.call(shell_cmd1, shell=True, executable='/bin/bash')
    shell_cmd2 = ' '.join(cmd2)
    subprocess.call(shell_cmd2, shell=True, executable='/bin/bash')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--input_location',
        required=True,
        help='input_location',
    )
    parser.add_argument('--output_location',
        required=True,
        help='output_location',
    )
    parser.add_argument('--gdc_id',
        required=True,
        help='gdc_id',
    )
    parser.add_argument('--barcode',
        required=True,
        help='barcode',
    )
    parser.add_argument('--picard',
        required=True,
        help='picard jar file path',
    )
    parser.add_argument('--fixit',
        required=True,
        help='picard jar file path',
    )
    args = parser.parse_args()

    main(args)
