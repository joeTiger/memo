"""
alias p3='cd ~/python3; source ~/venv/p3/bin/activate; export PYTHONPATH=~/python3'
lsof -i :8081
ps -eaf | grep memo
python memo.py -s &     # start server
python memo.py -r       # restart server
python memo.py ls       # get all ls cmd lines

build binary
------------
cd ~/python3/mydev
python -m PyInstaller memo.py --log-level WARN --onefile

build package deb
-----------------
cd /home/vpnuser/mydev/packaging3
cp -r memo_1.0-1_x64 memo_1.0-3_x64
cp ~/python3/mydev/dist/memo memo_1.0-3_x64/usr/local/bin/
vi memo_1.0-3_x64/DEBIAN/control
dpkg-deb --build memo_1.0-3_x64

install/remove deb
------------------
sudo dpkg -i memo_1.0-3_x64.deb
dpkg -i --force-not-root --root=$HOME memo_1.0-3_x64.deb
sudo dpkg -r memo

build tar gz
------------
tar -czvf memo_1.0-3_x64.tar.gz memo_1.0-3_x64

install tar gz
-------------
cp memo_1.0-3_x64.tar.gz ~/Downloads/
cd ~/Downloads
tar -xvf memo_1.0-3_x64.tar.gz
alias memo='~/Downloads/memo_1.0-3_x64/usr/local/bin/memo'
alias memo='~/Downloads/memo_1.0-3_x64/usr/local/bin/memo > /dev/null 2>&1 &'
alias memo='~/tmp/memo > /dev/null 2>&1'

scenario:
download memo_1.0-3_x64.deb
install it (sudo dpkg -i memo_1.0-3_x64.deb)
will copy it to /usr/local/bin
or
download memo_1.0-3_x64.tar.gz (for ex under ~/Download)
unzip it (tar -xvf memo_1.0-3_x64.tar.gz)
create alias (alias memo='~/Downloads/memo_1.0-3_x64/usr/local/bin/memo')

flow
. install_memo.sh
  =>  ./memo -i [email]

check cron tab and add "memo -c ..." if not exists
* * * * * /homes/mosheh/Downloads/memo_1.0.22/memo -c -d -e email > /tmp/listener.log 2>&1

"memo -c" will run each minute and check that "memo -s" is running in background...
"memo -s" (server) is a process running in background that check history and fill the google sheet
check that PORT is existing (lsof -i :8080)


local mode
1.run memo -i -l (python3 /home/vpnuser/python3/mydev/memo.py -i -l -d)
 a.add cron tab "python3 /home/vpnuser/python3/mydev/memo.py -c...."
 b.add alias memo in .bash_aliases
2.crontab will run memo -c
 a.check lsof for 8081
 b.if not run memo -s &

crontab -l
crontab -e

files used
utils_log.py
utils_systems.py
utils_cron_bash.py
static_helper.py
client_server.py
get_last_lines.py
memo_sheet.py

"""

import argparse
import sys

# appending a path
#sys.path.append('/home/vpnuser/python3')
from static_helper import StaticHelper

sys.path.append('/homes/mosheh/python3')

from client_server import client, server, client_another_email
from utils_systems import check_server, kill_server, show_pids_memo
from utils_cron_bash import init_crontab, remove_memo_from_crontab, remove_alias_from_bashrc
from utils_log import log_debug, set_log_level

__version__ = '1.0.29'


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str, nargs='*')
    parser.add_argument("--init", "-i", action='store_true', help="init memo")
    parser.add_argument("--check", "-c", action='store_true', help="check crontab")
    parser.add_argument("--remove", "-r", action='store_true', help="remove memo from crontab")
    parser.add_argument("--server", "-s", action='store_true', help="start server")
    parser.add_argument("--kill", "-k", action='store_true', help="kill server")
    parser.add_argument("--pids", "-p", action='store_true', help="show pids running for memo")
    parser.add_argument("--debug", "-d", action='store_true', help="set log debug")
    parser.add_argument("--version", "-v", action='store_true', help="print version")
    parser.add_argument("--email", "-e", type=str, help="email for gs")
    parser.add_argument("--local_mode", "-l", action='store_true', help="local mode is False by default")

    # if len(sys.argv)==1:
    #     print('version:{}'.format(__version__))
    #     parser.print_help(sys.stderr)
    #     sys.exit(1)

    args, unknown = parser.parse_known_args()
    program_name  = sys.argv[0]

    set_log_level('debug') if args.debug else set_log_level('critical')

    if args.version:
        print('version:{}'.format(__version__))

    log_debug('args={}'.format(args))
    log_debug('unknown={}'.format(unknown))
    log_debug('program_name={}'.format(program_name))

    if args.init:
        email = args.email
        # check email exists
        if email is None:
            email = StaticHelper.get_user_email()
            if email is None:
                # return error code 1 if not mail found...
                sys.exit(1)
        log_debug('init crontab with "memo -c -d..." if missing...')
        ret = init_crontab(args.local_mode, email)
        # already installed - return error code 255
        if ret == 255:
            sys.exit(255)
        else:
            sys.exit(0)

    if args.pids:
        show_pids_memo(program_name)

    if args.kill:
        kill_server(program_name)

    if args.remove:
        log_debug('remove "memo" from crontab and bashrc...')
        remove_memo_from_crontab()
        remove_alias_from_bashrc()

    if args.check:
        check_server(args.local_mode, program_name, args.email)
        sys.exit(0)

    if args.server:
        server(args.email) # program_name is memo or memo.py

    # search on local email
    if args.pattern and args.email is None:
        log_debug('pattern is <{}>'.format(args.pattern[0]))
        client(args.pattern[0])

    # search on remote email
    if args.email and args.server is False:
        log_debug('search pattern on another email')
        pattern = args.pattern[0] if args.pattern else ' '
        client_another_email(args.email, pattern)

if len(sys.argv) == 1:
        log_debug('no params...')
        client()