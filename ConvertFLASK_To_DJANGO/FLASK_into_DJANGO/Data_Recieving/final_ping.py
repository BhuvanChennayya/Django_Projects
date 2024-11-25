import platform
import sys, subprocess, shlex
import os


class Popen2(subprocess.Popen):
    """Context manager for Python2"""

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.stdout:
            self.stdout.close()
        if self.stderr:
            self.stderr.close()
        if self.stdin:
            self.stdin.close()
        self.wait()


def os_command(command, print_output=True, shell=False):
    ENCODING = 'UTF-8'
    if isinstance(command, str):
        command = shlex.split(command)
    if sys.version_info < (3, 2):
        Popen = Popen2
    else:
        Popen = subprocess.Popen
    with Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=shell) as process:
        empty_arr_test = []
        # count =0 
        # count +=1
        print('LINES:', process.stdout.readline().rstrip())
        line = process.stdout.readline().rstrip()
        if len(line) > 0:
            empty_arr_test.append(str(line)[2:-5])
        # if len(empty_arr_test) >= 2:
        #     break
        # if count > 2:
        #     break
        return empty_arr_test


def run_os_command(command, print_output=True, shell=False):
    r = os_command(command, print_output=print_output, shell=shell)
    if len(r) != 0:
        return '\n'.join(r)
    else:
        return None


def os_get(command, shell=False):
    # print("command===",command)
    check_return = run_os_command(command, print_output=False, shell=shell)
    if check_return is not None:
        # print("check_return ---",check_return)
        return check_return
    else:
        return None


def parsing_the_bytes_to_sting(sting_1):
    sumne_data = sting_1
    all_data = sumne_data.split('\n')
    while '' in all_data:
        all_data.remove('')
    try:
        if platform.system() == 'Windows':
            if 'TTL=' in all_data[-1]:
                return True
            else:
                return False
        elif platform.system() == 'Linux':
            if 'ttl=' in all_data[-1]:
                return True
            else:
                return False
    except Exception as error:
        # print(' checking ping --- ingore it ', error)
        try:
            if platform.system() == 'Windows':
                if 'TTL=' in all_data[-1] or 'TTL=' in all_data[0]:
                    return True
                else:
                    return False
            elif platform.system() == 'Linux':
                if 'ttl=' in all_data[-1] or 'ttl=' in all_data[0]:
                    return True
                else:
                    return False
        except Exception as error2:
            return False


def final_ping(ipaddress):
    # print("entered ping ip ===",ipaddress)
    os_type = platform.system()
    final_return = None
    final_output = False
    if os_type is not None:
        if os_type == 'Windows':
            final_return = os_get('ping -n 1 ' + str(ipaddress))
        elif os_type == 'Linux':
            final_return = os_get('ping -c 1 ' + str(ipaddress))
        elif os_type == 'Darwin':
            final_return = os_get('ping -c 1  ' + str(ipaddress))
        else:
            final_return = 'error'
        if final_return is not None:
            if final_return != 'error':
                final_output = parsing_the_bytes_to_sting(final_return)
            else:
                final_output = False
        else:
            final_output = False
    else:
        final_output = False
    return final_output
