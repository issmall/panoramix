from argparse import ArgumentParser
from logging import getLogger, NOTSET, INFO, DEBUG, CRITICAL, ERROR
from sre_constants import IN
from sys import _debugmallocstats

import coloredlogs

from panoramix.decompiler import decompile_address, decompile_bytecode
from panoramix.utils.helpers import C


LOG_LEVEL_MAPPINGS = {
    'notset': NOTSET,
    'info': INFO,
    'debug': DEBUG,
    'critical': CRITICAL,
    'error': ERROR,
}


parser = ArgumentParser()
parser.add_argument('-r', '--rpc', type=str, 
                    default='https://web3.mytokenpocket.vip')

parser.add_argument('-a', '--addr', type=str)
parser.add_argument('-c', '--code', type=str)
parser.add_argument('-f', '--func', type=str, default=None)

parser.add_argument('-v', '--verbose', 
                    action='store_true')
parser.add_argument('-l', '--loglevel', type=str,
                    default='debug', choices=[
                        # 'notset',
                        'info',
                        'debug',
                        'critical',
                        'error'
                    ])

args = parser.parse_args()

getLogger('panoramix.matcher').setLevel(NOTSET)

if args.verbose:
    getLogger('panoramix.matcher').setLevel(LOG_LEVEL_MAPPINGS[args.loglevel])
    coloredlogs.install(
        level=LOG_LEVEL_MAPPINGS[args.loglevel],
        fmt="%(asctime)s %(name)s %(message)s",
        datefmt="%H:%M:%S",
        field_styles={"asctime": {"color": "white", "faint": True}},
    )

if args.addr:
    print(decompile_address(args.addr.lower(), args.func, args.rpc).text)
elif args.code:
    print(decompile_bytecode(args.code.lower(), args.func, args.rpc).text)
