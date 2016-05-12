import logging
import os
import setupLog
import reheader
import argparse
from cdis_pipe_utils import postgres

class REHEAD(postgres.ToolTypeMixin, postgres.Base):

    __tablename__ = 'rehead_metrics'


if __name__=="__main__":

    parser = argparse.ArgumentParser(description="Raw counts using reheader")
    required = parser.add_argument_group("Required input paramters")
    required.add_argument("--bam", default=None, help="path to BAM file", required=True)
    required.add_argument("--case_id", default='unknown', help="gdc case id", required=True)
    required.add_argument("--gdc_id", default='unknown', help="gdc id for bam file", required=True)
    required.add_argument("--outdir", default="./", help="path to output directory")
    required.add_argument("--library", default="unknown", help="library name", required=True)
    required.add_argument("--sample", default="unknown", help="sample name", required=True)
    required.add_argument("--readgroup", default="unknown". help="readgroup name")

    database = parser.add_argument_group("database paramters")
    database.add_argument("--record_metrics", default=0, help="record metrics for runs")
    database.add_argument("--drivername", default="postgres", help="drivername for database")
    database.add_argument("--host", default="pgreadwrite.osdc.io", help="hostname for database")
    database.add_argument("--port", default="5432", help="port number for connection")
    database.add_argument("--username", default=None, help="username for connection")
    database.add_argument("--password", default=None, help="password for connection")
    database.add_argument("--database", default="prod_bioinfo", help="name of database")

    args = parser.parse_args()

    if not os.path.isdir(args.outdir):
        os.mkdir(args.outdir)

    log_file = "%s.reheader.log" % os.path.join(args.outdir, args.id)
    logger = setupLog.setup_logging(logging.INFO, args.id, log_file)

    bam = args.bam
    if not os.path.isfile(args.bam):
        raise Exception("Cannot find bam file %s. Please check that the file exists and is in the correct path" %bam)

    #get reheader counts
    metrics = reheader.get_header(bam, outheader, logger)
    newheader = reheader.modify_header(header, newheader, args.sample, args.library)
    outbam = reheader.reheader(bam, newheader, outbam, logger)

    if not metrics['exit_status']:

        if int(args.record_metrics):

            database = {
                    'drivername':args.drivername,
                    'host': args.host,
                    'port': args.port,
                    'username' : args.username,
                    'password' : args.password,
                    'database' : args.database
            }

            engine = postgres.db_connect(database)

            met = reheader(case_id = args.case_id,
                        tool = 'reheader',
                        files = [args.gdc_id],
                        systime = metrics['system_time'],
                        usertime =  metrics['user_time'],
                        elapsed = metrics['wall_clock'],
                        cpu = metrics['percent_of_cpu'],
                        max_resident_time = metrics['maximum_resident_set_size'])

            postgres.create_table(engine, met)
            postgres.add_metrics(engine, met)



