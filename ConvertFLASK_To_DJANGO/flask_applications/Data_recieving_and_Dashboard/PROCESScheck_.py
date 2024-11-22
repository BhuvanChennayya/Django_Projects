import subprocess

def checkProcessRunning(processName):
    ret = {'message': 'Something went wrong with checking process running', 'success': False}
    process_data = []

    if isinstance(processName, list):
        if processName:
            for name in processName:
                try:
                    subprocess.check_output(['pgrep', name.lower()])
                    process_data.append({'process_name': name.lower(), 'process_status': True})
                except subprocess.CalledProcessError:
                    process_data.append({'process_name': name.lower(), 'process_status': False})
        else:
            print('Warning: Process list is empty')
    elif processName is not None:
        try:
            subprocess.check_output(['pgrep', processName.lower()])
            process_data.append({'process_name': processName.lower(), 'process_status': True})
        except subprocess.CalledProcessError:
            process_data.append({'process_name': processName.lower(), 'process_status': False})

    if process_data:
        ret = {'message': process_data, 'success': True}
    else:
        ret = {'message': 'Processes are not working', 'success': False}

    return ret

# Example usage:

result = checkProcessRunning(['docketrun-app', 'python3', 'node', 'dup', 'esi-monitor','smrec','hydra-app','phaseone-app','fire_smoke_app'])
print(result)