import status_postgres
import argparse
import os

def is_nat(x):
    '''
    Checks that a value is a natural number.
    '''
    if int(x) > 0:
        return int(x)
    raise argparse.ArgumentTypeError('%s must be positive, non-zero' % x)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="GATK HaplotypeCaller Pipeline")
    required = parser.add_argument_group("Required input parameters")
    required.add_argument("--config", default=None, help="path to config file", required=True)
    required.add_argument("--outdir", default="./", help="otuput directory for slurm scripts")

    db = parser.add_argument_group("Database parameters")
    db.add_argument("--host", default=None, help='hostname for db')
    db.add_argument("--database", default='prod_bioinfo', help='name of the database')

    args = parser.parse_args()

    if not os.path.isdir(args.outdir):
        raise Exception("Cannot find output directory: %s" %args.outdir)

    if not os.path.isfile(args.config):
        raise Exception("Cannot find config file: %s" %args.config)


    s = open(args.config, 'r').read()
    config = eval(s)

    DATABASE = {
        'drivername': 'postgres',
        'host' : args.host,
        'port' : '5432',
        'username': config['username'],
        'password' : config['password'],
        'database' : args.database
    }

    engine = postgres.db_connect(DATABASE)

    cases = postgres.get_all_inputs(engine, 'rnaseq_for_reheader')

    for case in cases:
        slurm = open(os.path.join(args.outdir, "rh.%s.sh" %(cases[case][0])), "w")
        temp = open("template.sh", "r")
        for line in temp:
            if "XX_INL_XX" in line:
                line = line.replace("XX_INL_XX", str(cases[case][2]))

            if "XX_OPL_XX" in line:
                line = line.replace("XX_OPL_XX", str(cases[case][3]))

            if "XX_GDC_XX" in line:
                line = line.replace("XX_GDC_XX", str(cases[case][0]))

            if "XX_SM_XX" in line:
                line = line.replace("XX_SM_XX", str(cases[case][1]))
            slurm.write(line)
        slurm.close()
        temp.close()
