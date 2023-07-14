
# Just a stub for now

def add_cpsat_args(parser):
    parser.add_argument('--log_period', type=int, default=100000, dest="sat_LogPeriod")
    parser.add_argument('--seed', type=int, default=4, dest="sat_RandomSeed")
