import subprocess
import os


def cmd_run(command):
    fnull = open(os.devnull, 'w')
    subprocess.Popen([command], shell=True,
                     stdin=None, stdout=fnull, stderr=None, close_fds=False)
