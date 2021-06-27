#!/usr/bin/python3

__doc__ = """Small module to process data and take appropriate action
	from programs that produce output on a line-by-line basis."""

import subprocess, sys, time

def tail_command(command, shell=True):
    result = subprocess.run(command, capture_output=True, shell=shell)
    for line in result.stdout.decode().split('\n'):
        yield line

def tail_f(filename):
    file = open(filename, 'r')
    line = ''
    while True:
        line = file.readline()
        if line:
            yield line
        else:
            time.sleep(0.1)

if __name__ == '__main__':
    for line in tail_command("cat %s" % sys.argv[0]):
        print(line)
    for line in tail_f("/var/log/syslog"):
        print(line, end='')
