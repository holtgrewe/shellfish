#!/usr/bin/env python3
"""Simple helper for building shell commands from Python.

The main feature is that arbitrary shell interpreters can be used
for containing the source.
"""

__author__ = 'Manuel Holtgrewe <manuel.holtgrewe@bihealth.de>'

import shlex
import subprocess

class Template(object):
    """Template for executing a shell snippet.
    
    >>> tpl = Template(r'''echo "Hello World"
    ...                    ls / \\
    ...                        | grep {pattern}''')
    >>> tpl.values = {'pattern': r'^root$'}
    >>> tpl.capture_stdout = True
    >>> res = tpl.run()
    >>> res.returncode
    0
    >>> print(res.out)
    Hello World
    root
    <BLANKLINE>
    >>> print(res.err)
    None
    """

    def __init__(self, cmd, encoding='ascii', debug=False, values={},
                 shell='bash', capture_stdout=False, capture_stderr=False):
        """Initialize template with the given arguments.

        cmd -- string with command
        encoding -- encoding of string
        debug -- if True then 'set -x;' is prepended to the command
        values -- dict with key/value mapping available in cmd
        shell -- name of the Shell binary to use
        capture_stdout -- True when to capture stdout
        capture_stderr -- True when to capture stderr
        """
        self.shell = shell
        self.cmd = cmd.strip()
        self.debug = debug
        self.encoding = encoding
        self.values = dict(((k, shlex.quote(v)) for k, v in values.items()))
        self.capture_stdout = capture_stdout
        self.capture_stderr = capture_stderr

    def run(self):
        """Run the command and return the resulting ProcessResult."""
        cmd = self.cmd.format(**self.values)
        if self.debug:
            cmd = 'set -x\n' + cmd

        stdout = None if not self.capture_stdout else subprocess.PIPE
        stderr = None if not self.capture_stderr else subprocess.PIPE
        proc = subprocess.Popen(
            [self.shell, '-s'],
            stdin=subprocess.PIPE,
            stdout=stdout,
            stderr=stderr)
        out, err = proc.communicate(bytes(cmd, self.encoding))
        if not out is None:
            out = str(out, self.encoding)
        if not err is None:
            err = str(err, self.encoding)
        return ProcessResult(proc.returncode, out, err)
        return proc


class ProcessResult(object):
    """Returned by Template.run().

    Attributes out and err contain the output to stdout/stderr if they
    were to be captured and None otherwise.
    """

    def __init__(self, returncode, out=None, err=None):
        self.returncode = returncode
        self.out = out
        self.err = err


if __name__ == "__main__":
    import doctest
    doctest.testmod()
