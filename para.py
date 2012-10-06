#!/usr/bin/env python

import sys
import os
import subprocess
import multiprocessing
import re

"""
Para is a parallel for loop.

Para spawns n number of processes (set by $MAXPROCESS) in the background. 
Blocks until a process is done and continues to loop.

license: BSD 
author: https://github.com/ramaro/
"""

in_expr = re.compile(r'(%\w+)\s+in\s+([\S+\s*]+)\s+do:\s*(.+)')

def do_it(what):
    return subprocess.call(what,shell=True)

def usage(exit=0):
    print """usage: para [var] in [element1 element2 element3...] do: \"[command] [var]\" 

Example: para %i in one two three four do: \"echo %i\" 
para spawns n number of processes (set by $MAXPROCESS) in the background. Blocks until a process is done and continues to loop.
Set $MAXPROCESS to 0 for debugging (does not execute)."""
    sys.exit(exit)

def max_processes():
    """
    Returns the number of max processes to put in background. 
    Defaults to the number of cpu cores if env var $MAXPROCESS is not set.
    """
    max = multiprocessing.cpu_count()

    try:
        max = int(os.environ['MAXPROCESS'])
    except KeyError:
        pass
    except ValueError:
        print >> sys.stderr, '[para] $MAXPROCESS not valid. Setting to default (%d)' % (max,)

    return max
    
if __name__ == '__main__':
    m = in_expr.match(' '.join(sys.argv[1:]))

    if not m:
        usage(exit=1)

    try:
        token_key, token_values, command = m.groups()
    except ValueError:
        usage(exit=1)

    token_values = re.split('\s+', token_values)

    maxp = max_processes()
    if maxp <= 0:
        print >> sys.stderr, '[para debug] do:', command
        print >> sys.stderr, '[para debug] on:', token_values

    if maxp > 0:
        pool = multiprocessing.Pool(maxp)
        pool.map(do_it, [command.replace(token_key, token_val) for token_val in token_values])

