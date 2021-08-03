# https://pypi.org/project/python-crontab/
# https://stackoverflow.com/questions/65597453/how-to-store-private-and-public-key-into-pem-file-generated-by-rsa-module-of-pyt

import sys
import subprocess
import re

import rsa
import base64

from utils_log import log_debug

PORT = 8081         # Make sure it's within the > 1024 $$ <65535 range


def licence_key_is_valid(email):
    try:
        with open('license_pubkey.txt','r') as f:
            data = f.read()
            log_debug(f'read from file...license_pubkey.txt...{data[32:50]}')
            # Import public key in PKCS#1 format, PEM encoded
            pubkey = rsa.PublicKey.load_pkcs1(data.encode('utf8'))
            with open('license.txt','rb') as f:
                s = f.read()
                signature = base64.b64decode(s)
                try:
                    rsa.verify(email.encode('utf-8'), signature, pubkey)
                    log_debug('Valid license key....')
                    return True
                except rsa.VerificationError:
                    log_debug('invalid license key - refuse to start...')
                    return False
    except IOError as e:
        log_debug("Couldn't open file (%s)." % e)
        return False


def execute_shell_cmd(cmd, background=False):
    log_debug(100 * '-')
    log_debug('cmd --------------- <{}>'.format(cmd))
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if background:
        return
    stdout, stderr = process.communicate()
    stdout = stdout.decode("utf-8") if stdout else ''
    #if process.returncode != 0:
    log_debug('returncode--------- <{}>'.format(process.returncode))
    log_debug('stdout ------------ <{}>'.format(stdout))
    log_debug('stderr ------------ <{}>'.format(stderr))
    return stdout, process.returncode, stderr


def kill_pids(out):
    log_debug('extract pid from console response...')
    pattern = r'(\d+)\s.*'
    pids = []
    for line in out.splitlines():
        #print('line=<{}>'.format(line))
        try:
            line = line.strip()
            pid = re.search(pattern, line).group(1)
            if pid in pids:
                continue
            else:
                pids.append(pid)
            log_debug('kill pid={}...'.format(pid))
            cmd = 'kill -9 {}'.format(pid)
            execute_shell_cmd(cmd)
            if ret != 0:
                log_debug('kill failed...cmd={}'.format(cmd))
        except:
            log_debug('pid not found in console line={}'.format(line))

    return 0


def get_ps_memo(program_name):
    extension = '.py' if '.py' in program_name else ''
    out, ret, err = execute_shell_cmd('ps -eaf | grep "[m]emo{} -s"'.format(extension))
    return out, ret


def show_pids_memo(program_name):
    log_debug('show_pids_memo...')
    out, ret = get_ps_memo(program_name)
    print(out)
    out, ret, err = execute_shell_cmd('lsof -i :{}'.format(PORT))
    print(out)


def kill_server(program_name):
    log_debug('kill server...')
    out, ret = get_ps_memo(program_name)
    if out:
        kill_pids(out)

    # lsof -i :8081
    out, ret, err = execute_shell_cmd('lsof -i :{}'.format(PORT))
    if out:
        kill_pids(out)


def check_memo_already_exists(program_name):
    out, ret = get_ps_memo(program_name)
    return True if ret == 0 else False


def check_memo_already_running():
    out, ret, err = execute_shell_cmd('lsof -i :{}'.format(PORT))
    return True if ret == 0 else False


def check_server(local_mode, program_name, email=None):
    log_debug('called by crontab...')

    # not work.....
    # # need to set this export in order to
    # # Flush commands to bash history immediately
    # # http://www.aloop.org/2012/01/19/flush-commands-to-bash-history-immediately/
    # cmd = "export PROMPT_COMMAND='history -a'"
    # log_debug(cmd)
    # _, ret = execute_shell_cmd(cmd)

    log_debug('check if <memo -s [-e email] &> is running ...')

    # if check_memo_already_running():
    #     log_debug('8080 running ...exit')
    #     sys.exit(0)

    if check_memo_already_exists(program_name):
        log_debug('<memo -s [-e email] &> is ALREADY existing ...exit')
        sys.exit(0)

    log_debug('run <memo.py -s [-e email] &>...')

    cmd = '{} -s -d '.format(program_name)

    if email:
        cmd += '-e {} '.format(email)

    if local_mode:
        cmd = 'python ' + cmd

    cmd += ' > /tmp/listener2.log 2>&1 &'

    log_debug(cmd)

    execute_shell_cmd(cmd)
    log_debug('finito')

