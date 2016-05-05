import os
import sys
import argparse

def main(args):
    del os.environ['https_proxy']
    del os.environ['http_proxy']
    cmd = ['aws',
           '--profile',
           'cleversafe',
           '--endpoint',
           'http://gdc-accessors.osdc.io',
           's3',
           'cp '+args.input_location,
           '-',
           '| '+args.fixit,
           '--sm',
           'SM',
           '--pl',
           'PL',
           '-',
           '|',
           'java',
           '-jar',
           '-Xmx2G '+args.picard,
           'ValidateSamFile',
           'I=/dev/stdout',
           'O='+args.gdc_id+'.validate',
           '|',
           'java',
           '-jar',
           '-Xmx2G '+args.picard,
           'BuildBamIndex',
           'I=/dev/stdout',
           'O='+args.gdc_id+'_gdc_realn_rehead.bai'
           '|',
           'md5sum',
           '-',
           '> '+args.gdc_id+'_md5.txt',
           'aws',
           '--profile',
           'cleversafe',
           '--endpoint',
           'http://gdc-accessors.osdc.io',
           's3',
           'cp',
           '- '+args.output_location]
    shell_cmd = ' '.join(cmd)
    print shell_cmd

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--input_location',
        help='input_location',
    )
    parser.add_argument('--output_location',
        help='output_location',
    )
    parser.add_argument('--gdc_id',
        help='gdc_id',
    )
    parser.add_argument('--picard',
        help='picard jar file path',
    )
    parser.add_argument('--fixit',
        help='picard jar file path',
    )
    args = parser.parse_args()

    main(args)
