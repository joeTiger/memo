import subprocess
import os
import re
import time

from mydev.utils_log import log_debug


class StaticHelper:
    """
    This static class contains various general helpers
    """

    # region mail functions
    @staticmethod
    def get_user_email(user=os.environ.get('USER')):
        """
        Check that a user name is valid and returns its orcam email
        :param user: network user name
        :return: Corresponding email.  None if the user does not exist or has no mail
        """
        email = None
        try:
            log_debug('user is {}'.format(user))
            if not user:
                raise
            regex = re.compile(r"(?P<user>\w+):x:\d{4}:\d{4}:(?P<first_name>\w+) (?P<last_name>[\w-]+).*:"
                               r"(?P<home_dir>[\S]+):(?P<bin_bash_dir>[\S]+)")
            proc_args = ['getent', 'passwd', user]
            p = subprocess.Popen(proc_args, stdout=subprocess.PIPE, universal_newlines=True)
            p_out, p_err = p.communicate()
            log_debug(f'p_out=<{p_out}>\n p_err=<{p_err}>')
            match = re.search(regex, p_out)
            if match:
                try:
                    email = '{}.{}@orcam.com'.format(match.group('first_name').lower(), match.group('last_name').lower())
                except:
                    log_debug('get_user_email user not found...')
                    email = None
            else:
                email = None
        except Exception as ex:
            log_debug(f'get_user_email...failed...<{ex}>')
        return email
