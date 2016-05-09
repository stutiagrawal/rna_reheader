import os
import sys
import argparse
import subprocess

def main(args):
    cmd = ['aws',
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
           'O=/dev/stdout'
           '|',
           'tee',
           '>(aws',
           '--profile',
           'cleversafe',
           '--endpoint',
           'http://gdc-accessors.osdc.io',
           's3',
           'cp',
           '- '+str(args.output_location)+')',
           '>(java',
           '-jar',
           '-Xmx2G '+str(args.picard),
           'ValidateSamFile',
           'I=/dev/stdin',
           'VALIDATION_STRINGENCY=LENIENT',
           'O='+str(args.gdc_id)+'.validate',
           '2> '+str(args.gdc_id)+'.validate.log)',
           '>(java',
           '-jar',
           '-Xmx2G '+str(args.picard),
           'BuildBamIndex',
           'I=/dev/stdin',
           'O='+str(args.gdc_id)+'_gdc_realn_rehead.bai',
           '2> '+str(args.gdc_id)+'.buildbamindex.log)',
           '>(md5sum',
           '-',
           '> '+str(args.gdc_id)+'_md5.txt)',
           '>/dev/null']
    shell_cmd = ' '.join(cmd)
    subprocess.call(shell_cmd, shell=True, executable='/bin/bash')

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
