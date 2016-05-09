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
           '|',
           '/home/ubuntu/.virtualenvs/p2/bin/python',
           str(args.fixit),
           '--sm',
           str(args.barcode),
           '--pl',
           'ILLUMINA',
           '-',
           '>',
           fixed_bam]
    shell_cmd1 = ' '.join(cmd1)
    subprocess.call(shell_cmd1, shell=True, executable='/bin/bash')

    cmd2 = ['docker',
           'run',
           '-i',
           '-v',
           step_dir+':'+step_dir,
           '-v',
           '/mnt/SCRATCH/:/tmp',
           str(args.picard),
           'java',
           '-jar',
           '-Xmx4G',
           '-Djava.io.tmpdir=/tmp/job_tmp',
           'tools/picard-tools/picard.jar',
           'ValidateSamFile',
           'I='+fixed_bam,
           'VALIDATION_STRINGENCY=LENIENT',
           'O='+os.path.join(step_dir, str(args.gdc_id))+'.validate',
           '2> '+os.path.join(step_dir, str(args.gdc_id))+'.validate.log']
    shell_cmd2 = ' '.join(cmd2)
    subprocess.call(shell_cmd2, shell=True, executable='/bin/bash')

    cmd3 = ['docker',
           'run',
           '-i',
           '-v',
           step_dir+':'+step_dir,
           '-v',
           '/mnt/SCRATCH/:/tmp',
           str(args.picard),
           'java',
           '-jar',
           '-Xmx4G',
           '-Djava.io.tmpdir=/tmp/job_tmp',
           'tools/picard-tools/picard.jar',
           'BuildBamIndex',
           'I='+fixed_bam,
           'VALIDATION_STRINGENCY=LENIENT',
           'O='+os.path.join(step_dir, str(args.gdc_id))+'_gdc_realn_rehead.bai',
           '2> '+os.path.join(step_dir, str(args.gdc_id))+'.buildbamindex.log']
    shell_cmd3 = ' '.join(cmd3)
    subprocess.call(shell_cmd3, shell=True, executable='/bin/bash')

    cmd4 =['md5sum',
           fixed_bam,
           '> '+str(args.gdc_id)+'_md5.txt']
    shell_cmd4 = ' '.join(cmd4)
    subprocess.call(shell_cmd4, shell=True, executable='/bin/bash')

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
        help='picard docker',
    )
    parser.add_argument('--fixit',
        required=True,
        help='picard jar file path',
    )
    args = parser.parse_args()

    main(args)
