import os

host = "34.85.44.253"
user = "root"
passwd = ""

def shell_run(cmd):
    return os.system(cmd)

if __name__ == "__main__":
    '''
    Sync develop data with remote machine.
    '''
    shell_run("ssh %s@%s" % (user, host))
    # waiting for enter passwd
    