from argparse import ArgumentParser
from parser import TildeAthInterp


if __name__ == '__main__':
    cmdparser = ArgumentParser(
        description='A fanmade ~ATH interpreter.',
        )
    cmdparser.add_argument(
        'script',
        help='The ~ATH file to run.',
        metavar='scr_name',
        )
    cmdargs = cmdparser.parse_args()
    with open(cmdargs.script, 'r') as codefile:
        script = codefile.read()
        TildeAthInterp.execute(script)
