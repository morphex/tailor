#!/usr/bin/python3.7

__doc__ = """Small module to process data and take appropriate action
	from programs that produce output on a line-by-line basis."""

import subprocess, sys, time, re, os, shlex

ansi_re = re.compile("\x1b\[[0-9;]*[mGKHF]")

def filter_ansi(string_):
    return ansi_re.sub("", string_)

def tail_command_old(command):
    stdout = tempfile.mktemp()
    stderr = tempfile.mktemp()
    command = "/bin/sh -c '%s 1> %s 2> %s &'" % (command, stdout, stderr)
    result = subprocess.run(command, shell=True)
    stdout_f = open(stdout, 'r')
    stderr_f = open(stderr, 'r')
    while True:
        line = stdout_f.readline()
        if line:
            yield line
        else:
            time.sleep(0.01)

def tail_command(command):
    command = shlex.split(command)
    result = subprocess.Popen(command, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
    count = 0
    while True:
        line = result.stdout.readline().decode()
        if line:
            yield line
        else:
            count += 1
            if result.returncode == None:
                if count % 10:
                    time.sleep(0.01)
                else:
                    if os.system("ps -%s > /dev/null " % result.pid):
                        return
            else:
                return

class GotEOF(Exception):
    "Exception raised when EOF of file is found, by empty readline"
    pass

def tail(filename):
    return tail_f(filename, follow=False)

def tail_f(filename, follow=True):
    file = open(filename, 'r')
    try:
        for line in _tail_f(file, follow=follow, signal_wait=True):
            yield line
    except GotEOF:
        for line in _tail_f(file, follow=follow):
            yield line

def _tail_f(file, follow=True, signal_wait=False):
    line = ''
    while True:
        line = file.readline()
        if line:
            yield line
        else:
            if not follow: return
            if signal_wait:
                raise GotEOF()
            time.sleep(0.1)

def get_tail_of_tail_f(filename, follow=True, tail_size=10):
    file = open(filename, 'r')
    lines = []
    try:
        for line in _tail_f(file, follow=follow, signal_wait=True):
            lines.append(line)
    except GotEOF:
        for line in lines[len(lines) - tail_size:]:
            yield line
    # If it's a huuuge file with lots of lines, free up that memory as this
    # function may run "forever".
    del lines
    for line in _tail_f(file, follow=follow):
        yield line

class Listener:
    """Instances of this 'listen' to each line produced by tail commands."""

    def __init__(self):
        self.lines = []

    def add(self, line):
        self.lines.append(time.time(), line)

if __name__ == '__main__':
    #for line in tail_command("cat %s" % sys.argv[0]):
    #    print(line)
    for line in tail_command("ls --color -l"):
        print(filter_ansi(line))
    for line in tail_command("./output_ansi.py"):
        print(filter_ansi(line))
    for line in get_tail_of_tail_f("/var/log/syslog"):
        print(line, end='')
