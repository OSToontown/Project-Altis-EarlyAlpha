"Shell command line completion support"
from __future__ import print_function
import os
import sys


def bash_completion(parser):
    """Command line completion for bash shell

    To use, register the subcommand with bash a the command line completion
    function for this program.

        $ complete -o default -C '%(prog)s _bash_completion' %(prog)s

    Bash will now call this subcommand when attempting shell completion of
    arguments.
    """
    partial = sys.argv[-2]
    comp_line = os.environ.get('COMP_LINE').split()[1:-1]
    import pdb; pdb.set_trace()
    print(repr(comp_line))
    print('XXX')
    print('YYY')
    print('ZZZ')


SHELL_COMPLETION = {
        '__bash__': bash_completion
}
