import os
import sys
import argparse

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
           '--sm',
           'SM',
           '--pl',
           'PL',
           '-',
           '|',
           'java',
           '-jar',
           '-Xmx2G '+str(args.picard),
           'ValidateSamFile',
           'I=/dev/stdin',
           'O='+str(args.gdc_id)+'.validate',
           '|',
           'java',
           '-jar',
           '-Xmx2G '+str(args.picard),
           'BuildBamIndex',
           'I=/dev/stdin',
           'O='+str(args.gdc_id)+'_gdc_realn_rehead.bai'
           '|',
           'md5sum',
           '-',
           '> '+str(args.gdc_id)+'_md5.txt',
           '|',
           'aws',
           '--profile',
           'cleversafe',
           '--endpoint',
           'http://gdc-accessors.osdc.io',
           's3',
           'cp',
           '- '+str(args.output_location)]
    shell_cmd = ' '.join(cmd)
    os.system(shell_cmd)

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
