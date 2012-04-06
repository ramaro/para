#!/usr/bin/env python

import sys
import os
import subprocess
import multiprocessing

"""
para spawns n number of processes (set by $MAXPROCESS) in the background. Blocks until a process is done and continues to loop.

author: ricardo.amaro@gmail.com
"""

def do_it(what):
	return subprocess.call(what,shell=True)

if __name__ == '__main__':

	if len(sys.argv) <= 5:
		print """Usage: para [var] in [element1 element2 element3...] do: \"[command] [var]\" 
Example: para %i in one two three four do: \"echo %i\" 

para spawns n number of processes (set by $MAXPROCESS) in the background. Blocks until a process is done and continues to loop.
Set $MAXPROCESS to 0 for debugging (does not execute).
					""" 
		sys.exit(1)

	max_processes = multiprocessing.cpu_count()
	try:
		max_processes = int(os.environ['MAXPROCESS'])
	except KeyError:
		pass
	except ValueError:
		print >> sys.stderr, '[para] $MAXPROCESS not valid. Setting to default (%d)' % (max_processes, )

	pool = multiprocessing.Pool(max_processes)
		
	token_key = sys.argv[1]
	token_values = []


	if sys.argv[2] == 'in':
		do_from=None
		for n,v in enumerate(sys.argv[3:]):
			if v == 'do:':
				token_values = sys.argv[3:3+n]
				do_from=n
				break

		do_what = ' '.join(sys.argv[4+do_from:])

		if max_processes <= 0:
			print >> sys.stderr, '[para debug] do:', do_what
			print >> sys.stderr, '[para debug] on:', token_values

		if max_processes > 0:
			pool.map(do_it, [do_what.replace(token_key, token_val) for token_val in token_values])	

