"""
https://pypi.org/project/python-crontab/
https://stackoverflow.com/questions/5410757/how-to-delete-from-a-text-file-all-lines-that-contain-a-specific-string

sed -i '/memo/s/^#//' .bashrc         # remove comment
sed -e '/memo/ s/^#*/#/' -i .bashrc   # add comment
"""

import pathlib
import os

from crontab import CronTab

from utils_log import log_debug
from utils_systems import execute_shell_cmd


#
BASHRC_FILE = '.bashrc'
BASH_ALIASES_FILE = '.bash_aliases'


def remove_memo_from_crontab():
    cron = CronTab(user=True)
    iter = cron.find_command('memo')  # matches memo
    for job in iter:
        print('remove job=<{}>'.format(job))
        job.enable(False)
        cron.remove(job)
    cron.write()


def source_bashrc():
    cmd = '. ~/{} &'.format(BASHRC_FILE)
    execute_shell_cmd(cmd)


def remove_alias_from_bashrc():
    cmd = "sed -i '/alias memo/d' ~/{}".format(BASHRC_FILE)
    execute_shell_cmd(cmd)

    cmd = "unalias memo &"
    execute_shell_cmd(cmd)


def export_already_exists(filename, export_line):
    with open(filename) as f:
        for line in f:
            if export_line in line:
                return True
    return False


def line_prepender(filename, export_line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(export_line.rstrip('\r\n') + '\n\n' + content)


# "# Added by memo...\n"
def add_alias_in_bash_file(local_mode):
    log_debug('add_alias_in_bashrc...')
    path_memo = pathlib.Path().absolute()
    log_debug(path_memo)

    #.bashrc
    filename = os.path.expanduser("~/{}".format(BASHRC_FILE))

    # # add at the beginning of the file
    # export_line = "export PROMPT_COMMAND='history -a'"
    # if not export_already_exists(filename, export_line):
    #     line_prepender(filename, export_line)

    export_line_1 = 'export ORIGINAL_PROMPT_COMMAND="${PROMPT_COMMAND}"'
    export_line_2 = 'export PROMPT_COMMAND="history -a; ${ORIGINAL_PROMPT_COMMAND}"'

    if local_mode:
        alias_memo = 'python {}/memo.py'.format(path_memo)
    else:
        alias_memo = '{}/memo'.format(path_memo)

    # add at the end of the file

    with open(filename, "at") as bashrc:
        data = "#alias memo\nalias memo={}\n".format(alias_memo)
        if not export_already_exists(filename, export_line_2):
            data = data + "\n{}\n{}\n".format(export_line_1, export_line_2)
        log_debug(data)
        bashrc.write(data)


def add_cmd_memo_in_cron(cron, local_mode, email=None):
    #job = cron.new(command='/usr/local/bin/memo -c > /tmp/listener.log 2>&1')
    log_debug('add_cmd_memo_in_cron...')
    path_memo = pathlib.Path().absolute()
    log_debug(path_memo)

    if local_mode:
        cmd = 'python {}/memo.py -c -l -d'.format(path_memo)
    else:
        cmd = '{}/memo -c -d'.format(path_memo)

    if email:
        cmd += ' -e {}'.format(email)

    cmd += ' > /tmp/listener.log 2>&1'

    log_debug(cmd)

    job = cron.new(command=cmd)
    job.minute.every(1)
    cron.write()
    log_debug('run job...')
    execute_shell_cmd(cmd+' &')
    log_debug('run job...completed')


def cmd_memo_in_cron(cron):
    for job in cron:
        if 'memo' in job.command:
            log_debug('memo exists in crontab...')
            return True
    return False


def init_crontab(local_mode, email):
    cron = CronTab(user=True)
    if not cmd_memo_in_cron(cron):
        add_cmd_memo_in_cron(cron, local_mode, email)
        add_alias_in_bash_file(local_mode)
        source_bashrc()
        return 0
    print('return 255...')
    return 255
