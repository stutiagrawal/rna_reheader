import os
import subprocess
import signal
from cdis_pipe_utils import pipe_util
from cdis_pipe_utils import time_util

def get_header(bam, outheader, logger):
    """ extract the header from bam file """

    if os.path.isfile(bam) and os.path.isdir(os.path.dirname(outheader)):


        cmd = 'samtools view -H %s > %s' %(bam, outheader)

        output = pipe_util.do_shell_command(cmd, logger)
        metrics = time_util.parse_time(output)
        return metrics
    else:
        error_msg = "Invalid bam file %s or output directory %s" %(bam, os.path.diranme(outheader))
        logger.error(error_msg)
        raise Exception(error_msg)

def modify_header(header, newheader, sample, library):
    "add the sample and library to the header """

    if sample == "":
        raise Exception("sample name cannot be empty")
    if library == "":
        raise Exception("libary cannot be empty")

    if os.path.isfile(header) and os.path.isdir(os.path.dirname(newheader)):
    f = open(header, "r")
    out = open(newheader, "w")

    for line in f:

        if line.startswith("@RG"):
            newline = ""
            line = line.split("\t")
            newline = newline += "%s\tSM:%s\tLB:%s\n" %(line[0], sample, library)
            out.write(newline)
        else:
            out.write(line)
    return newheader


def reheader(bam, header, outbam, logger):
    """ reheader bam with a new header """

    if not os.path.isdir(os.path.dirname(outbam)):
        raise Exception("Invalid directory %s for output bam" %(os.path.dirname(outbam)))

    if os.path.isfile(bam) and os.path.isfile(header):

        cmd = 'samtools reheader %s %s > %s' %(bam, header, outbam)

        output = pipe_util.do_shell_command(cmd, logger)
        metrics = time_util.parse_time(output)
        return metrics

    else:
        error_msg = "Invalid BAM file %s or header file %s. Please check the file exists and the path is correct." %(bam, header)
        logger.error(error_msg)
        raise Exception(error_msg)

