# from flask import Flask, request, jsonify,Blueprint
# import subprocess
# import platform
# import requests
# import ipaddress
# from pywifi import PyWiFi, const, Profile
# import time

from Data_recieving_and_Dashboard.packages import *
voice_wifi= Blueprint('voice_wifi', __name__)



def connect_to_wifi(ssid, password):
    wifi = PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    time.sleep(2)
    scan_results = iface.scan_results()

    iface.remove_all_network_profiles()
    profile = Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password
    iface.add_network_profile(profile)

    iface.connect(profile)
    max_retries = 10
    connected = False

    for i in range(max_retries):
        time.sleep(1)
        iface.scan()
        scan_results = iface.scan_results()
        connected = any(network.ssid == ssid for network in scan_results)
        if connected:
            break

    return connected

def configure_ip(ip_mode, ip_address, gateway, subnet):
    network = ipaddress.IPv4Network(f'{ip_address}/{subnet}', strict=False)
    ip = ipaddress.IPv4Address(ip_address)
    gw = ipaddress.IPv4Address(gateway)

    if ip == network.network_address or ip == network.broadcast_address:
        raise ValueError('Invalid IP address: Cannot be network or broadcast address')
    
    if gw not in network:
        raise ValueError('Invalid gateway: Must be within the same subnet as the IP address')
    
    base_url = 'http://192.168.4.1/lansetting'
    if ip_mode.lower() == 'static':
        static_mode = 1
    elif ip_mode.upper() == 'DHCP':
        static_mode = 0
    else:
        return jsonify({"message": "Invalid IP mode","success":False}), 400

    params = {
        'static': static_mode,
        'ip': ip_address,
        'gateway': gateway,
        'subnet': subnet,
        'save': 1
    }
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        raise Exception('Failed to update IP configuration')

    ping_response = subprocess.run(['ping', '-n', '2', '-w', '1000', ip_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if ping_response.returncode != 0:
        raise Exception('IP configuration updated, but device is not reachable via ping')

    return True



@voice_wifi.route('/connect_and_configure', methods=['POST'])
def connect_and_configure():
    start_time = time.time()  ## start time
    print(f"Process started at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")

    data = request.json
    ssid = data.get('ssid')
    password = data.get('password')
    ip_mode = data.get('ip_mode')
    ip_address = data.get('ip_address')
    gateway = data.get('gateway')
    subnet = data.get('subnet')

    try:
        if platform.system() == "Windows":
            connected = connect_to_wifi(ssid, password)
        elif platform.system() == "Linux":
            command = ['nmcli', 'd', 'wifi', 'connect', ssid, 'password', password]
            result = subprocess.run(command)
            connected = (result.returncode == 0)

        if not connected:
            return jsonify({'message': 'Failed to connect to Wi-Fi check if your system supports Wi-Fi connection', "success": False})

        configure_ip(ip_mode, ip_address, gateway, subnet)

        existing_device = mongo.db.voiceannoucement_configurations.find_one({'wifi_name': ssid})

        update_data = {
            'ip_address': ip_address,
            'status': True,
            'ip_mode': ip_mode,
            'timestamp': datetime.utcnow().strftime('%Y%m%d'),
            'gateway': gateway,
            'subnet': subnet
        }

        if existing_device:
            if 'volume_level' not in existing_device:
                update_data['volume_level'] = '55'

            mongo.db.voiceannoucement_configurations.update_one(
                {'wifi_name': ssid},
                {'$set': update_data}
            )
        else:
            update_data['wifi_name'] = ssid
            update_data['volume_level'] = '55'
            mongo.db.voiceannoucement_configurations.insert_one(update_data)

        end_time = time.time()  ## end time
        print(f"Process ended at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
        
        duration = end_time - start_time  ## total time taken
        print(f"Total process duration: {duration:.2f} seconds")

        return jsonify({'message': 'Connected and configured successfully', "success": True})

    except Exception as e:
        return jsonify({'error': str(e), "success": False})



@voice_wifi.route('/add_data', methods=['POST'])
def add_data():
    data = request.json
    ssid = data.get('ssid')  
    ip_mode = data.get('ip_mode')
    ip_address = data.get('ip_address')
    gateway = data.get('gateway')
    subnet = data.get('subnet')
    
    
    # if not all([ssid, ip_mode, ip_address, gateway, subnet]):
    #     return jsonify({'error': 'SSID, IP mode, IP address, gateway, and subnet are required and cannot be empty', "success": False}), 400

    try:
        existing_device = mongo.db.voiceannoucement_configurations.find_one({'wifi_name': ssid})

        update_data = {
            'ip_address': ip_address,
            'status': True,
            'ip_mode': ip_mode,
            'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'gateway': gateway,
            'subnet': subnet
        }

        if existing_device:
            if 'volume_level' not in existing_device:
                update_data['volume_level'] = '55'

            mongo.db.voiceannoucement_configurations.update_one(
                {'wifi_name': ssid},
                {'$set': update_data}
            )
        else:
            update_data['wifi_name'] = ssid
            update_data['volume_level'] = '55'
            mongo.db.voiceannoucement_configurations.insert_one(update_data)

        return jsonify({'message': 'Data saved successfully', "success": True})

    except Exception as e:
        return jsonify({'error': str(e), "success": False})



@voice_wifi.route('/configured_devices', methods=['GET'])
def configured_devices():
    try:
        devices = list(mongo.db.voiceannoucement_configurations.find(
            {'status': True}, 
            {'_id': 0, 'status': 0}  
        ))

        if len(devices) ==0:
            return jsonify({'message': 'there are no any configured voice announcement devices.', "success": False})

        return jsonify({'configured_devices': devices, "success": True})

    except Exception as e:
        return jsonify({'error': str(e), "success": False})
    

@voice_wifi.route('/removed_devices', methods=['GET'])
def deleted_devices():
    try:
        devices = list(mongo.db.voiceannoucement_configurations.find(
            {'status': 'deleted'},  
            {'_id': 0, 'status': 0} 
        ))
        if len(devices) ==0:
            return jsonify({'message': 'there are no any deleted voice announcement devices.', "success": False})

        return jsonify({'deleted_devices': devices, "success": True})

    except Exception as e:
        return jsonify({'error': str(e), "success": False})
    


@voice_wifi.route('/set_ip_config', methods=['POST'])
def set_ip_config():
    data = request.json
    
    ssid = data.get('ssid')  
    ip_mode = data.get('ip_mode')
    ip_address_1 = data.get('old_ip')  
    ip_address_2 = data.get('new_ip')  
    gateway = data.get('gateway')
    subnet = data.get('subnet')

    
    # if ssid is None or ip_mode is None or gateway is None or subnet is None or ip_address_1 is None:
    #     return jsonify({'error': 'SSID, IP mode, gateway, subnet, and old IP are required', "success": False}), 400
    
    try:
        if ip_address_2:
            network = ipaddress.IPv4Network(f'{ip_address_2}/{subnet}', strict=False)
            ip = ipaddress.IPv4Address(ip_address_2)
            
            if ip == network.network_address or ip == network.broadcast_address:
                return jsonify({'error': 'Invalid IP address: Cannot be network or broadcast address', "success": False}), 400
    except ValueError as e:
        return jsonify({'error': str(e), "success": False}), 400
    
    try:
        if ip_address_2:
            ip_to_use = ip_address_2
        else:
            existing_device = mongo.db.voiceannoucement_configurations.find_one({'wifi_name': ssid})
            if existing_device:
                ip_to_use = existing_device.get('ip_address', ip_address_1) 
        base_url = f'http://{ip_address_1}/lansetting'

        
        if ip_mode.lower() == 'static':
            static_mode = 1
        elif ip_mode.upper() == 'DHCP':
            static_mode = 0
        else:
            return jsonify({"message": "Invalid IP mode", "success": False}), 400
            
        params = {
            'static': static_mode,
            'ip': ip_to_use,
            'gateway': gateway,
            'subnet': subnet,
            'save': 1
        }

        response = requests.get(base_url, params=params,timeout=5)
        if response.status_code != 200:
            return jsonify({'error': 'Failed to update IP configuration', 'details': response.text, "success": False}), 500
        
        existing_device = mongo.db.voiceannoucement_configurations.find_one({'wifi_name': ssid})

        update_data = {
            'ip_address': ip_to_use,
            'status': True,
            'ip_mode': ip_mode,
            'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'gateway': gateway,
            'subnet': subnet
        }

        if existing_device:
          
            if 'volume_level' not in existing_device:
                update_data['volume_level'] = '55'

            mongo.db.voiceannoucement_configurations.update_one(
                {'wifi_name': ssid},
                {'$set': update_data}
            )
        else:
            update_data['wifi_name'] = ssid
            update_data['volume_level'] = '55'
            mongo.db.voiceannoucement_configurations.insert_one(update_data)

       
        if platform.system() == "Windows":
            ping_response = subprocess.run(['ping', '-n', '4', ip_to_use], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        elif platform.system() == "Linux":
            ping_response = subprocess.run(['ping', '-c', '4', ip_to_use], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)

        if ping_response.returncode == 0:
            return jsonify({'message': 'IP configuration updated successfully and device is reachable', "success": True})
        else:
            return jsonify({'message': 'IP configuration updated, but device is not reachable via ping', "success": False}), 500
    
    except requests.exceptions.ConnectTimeout:
        return jsonify({'error': 'Connection timed out. device is not reachble, can not set the ip.', "success": False}), 504

    except Exception as e:
        return jsonify({'error': str(e), "success": False}), 500





# @voice_wifi.route('/list_wifi', methods=['GET'])
# def list_wifi():
#     try:
#         if platform.system() == 'Windows':
#             wifi = PyWiFi()
#             interfaces = wifi.interfaces()
            
#             if not interfaces:
#                 return jsonify({'error': 'your system is not WIFI based so cannot list the available wifi', "success": False}), 500

#             iface = interfaces[0]
#             iface.scan()
#             time.sleep(3)
#             scan_results = iface.scan_results()

#             esp_networks_set = {network.ssid for network in scan_results if network.ssid.startswith("ESP")}
#             esp_networks = list(esp_networks_set)
            
#             if not esp_networks:
#                 return jsonify({'message': 'No ESP Wi-Fi networks available', "success": False}), 404

#             return jsonify({'Available_WIFI': esp_networks, "success": True})

#         elif platform.system() == 'Linux':
#             command_device_check = subprocess.run(['nmcli', '-t', '-f', 'DEVICE,TYPE', 'device'], capture_output=True, text=True)
#             if command_device_check.returncode != 0:
#                 return jsonify({'message': 'Failed to check for network devices', "success": False}), 500
#             devices = command_device_check.stdout.strip().split('\n')
#             wifi_devices = [dev for dev in devices if 'wifi' in dev.lower()]
            
#             if not wifi_devices:
#                 return jsonify({'error': 'your system is not WIFI based so cannot list the available wifi', "success": False}), 500

#             command_scan = subprocess.run(['nmcli', '-t', '-f', 'SSID', 'dev', 'wifi'], capture_output=True, text=True)

#             if command_scan.returncode != 0:
#                 return jsonify({'error': 'Failed to scan for Wi-Fi networks', "success": False}), 404

#             wifi_networks = command_scan.stdout.strip().split('\n')

#             esp_networks = [ssid for ssid in wifi_networks if ssid.startswith("ESP")]
            
#             if not esp_networks:
#                 return jsonify({'message': 'No ESP Wi-Fi networks available', "success": False}), 404

#             return jsonify({'Available_WIFI': esp_networks, "success": True})

#         else:
#             return jsonify({'error': 'Unsupported platform. Only Windows and Linux (Ubuntu) are supported.', "success": False}), 400

#     except Exception as e:
#         return jsonify({'error': 'An error occurred: {}'.format(str(e)), "success": False}), 500
    

@voice_wifi.route('/list_wifi', methods=['GET'])
def list_wifi():
    try:
        if platform.system() == 'Windows':
            wifi = PyWiFi()
            interfaces = wifi.interfaces()
            
            if not interfaces:
                return jsonify({'error': 'your system is not WIFI based so cannot list the available wifi', "success": False}), 500

            iface = interfaces[0]
            iface.scan()
            time.sleep(3)
            scan_results = iface.scan_results()

            esp_networks_set = {network.ssid for network in scan_results if network.ssid.startswith("ESP")}
            esp_networks = list(esp_networks_set)
            
            if not esp_networks:
                return jsonify({'message': 'No ESP Wi-Fi networks available', "success": False}), 200

            return jsonify({'Available_WIFI': esp_networks, "success": True})

        elif platform.system() == 'Linux':
            command_device_check = subprocess.run(['nmcli', '-t', '-f', 'DEVICE,TYPE', 'device'], capture_output=True, text=True)
            if command_device_check.returncode != 0:
                return jsonify({'message': 'Failed to check for network devices', "success": False}), 500
            devices = command_device_check.stdout.strip().split('\n')
            wifi_devices = [dev for dev in devices if 'wifi' in dev.lower()]
            
            if not wifi_devices:
                return jsonify({'error': 'your system is not WIFI based so cannot list the available wifi', "success": False}), 500

            command_scan = subprocess.run(['nmcli', '-t', '-f', 'SSID', 'dev', 'wifi'], capture_output=True, text=True)

            if command_scan.returncode != 0:
                return jsonify({'error': 'Failed to scan for Wi-Fi networks', "success": False}), 404

            wifi_networks = command_scan.stdout.strip().split('\n')

            esp_networks = [ssid for ssid in wifi_networks if ssid.startswith("ESP")]
            
            if not esp_networks:
                return jsonify({'message': 'No ESP Wi-Fi networks available', "success": False}), 200

            return jsonify({'Available_WIFI': esp_networks, "success": True})

        else:
            return jsonify({'error': 'Unsupported platform. Only Windows and Linux (Ubuntu) are supported.', "success": False}), 400

    except Exception as e:
        return jsonify({'error': 'An error occurred: {}'.format(str(e)), "success": False}), 500
                                                                
# @voice_wifi.route('/list_file',methods=['POST'])
# def list_file():
#     data = request.json
#     ip_address = data.get('ip_address')
#     if ip_address is None:
#         return jsonify({'error': 'IP address is required',"success":False}), 400
#     try:
#         url=f'http://{ip_address}/filelist'
#         response = requests.get(url)
#         filelist = response.json()
#         return jsonify({'File_list':filelist, "success": True})
#     except Exception as e:
#         return jsonify({'error': str(e),"success":False}), 500



@voice_wifi.route('/list_file', methods=['POST'])
def list_file():
    data = request.json
    ip_address = data.get('ip_address')
    
    # if ip_address is None:
    #     return jsonify({'error': 'IP address is required', "success": False}), 400
    
    try:
        url = f'http://{ip_address}/filelist'
        response = requests.get(url, timeout=5)
        filelist = response.json()
        
        return jsonify({'File_list': filelist, "success": True})
    
    except requests.exceptions.ConnectTimeout:
        return jsonify({'error': 'Connection timed out. device may not be reachable so cannot list the file.Check the device working status', "success": False}), 504
    
    except requests.exceptions.HTTPError as http_err:
        return jsonify({'error': f"HTTP error occurred: {http_err}", "success": False}), response.status_code
    
    
    except Exception as e:
        return jsonify({'error': str(e), "success": False}), 500
    


@voice_wifi.route('/info_ip',methods=['POST'])
def info_ip():
    data = request.json
    ip_address=data.get('ip_address')
    if ip_address is None:
        return jsonify({'error': 'IP address is required',"success":False}), 400
        
    try:
        url=f'http://{ip_address}/ipinfo'
        response = requests.get(url, timeout=5)
        ip_info = response.json()
        return jsonify(ip_info)
       
    except Exception as e:
        return jsonify({'error': str(e),"success":False}), 500
        


@voice_wifi.route('/level_volume', methods=['POST'])
def level_volume():
    data = request.json
    ip_address = data.get('ip_address')
    volume_level = data.get('volume_level')


    try:
        base_url = f'http://{ip_address}/vol'
        params = {'level': volume_level}
        response = requests.get(base_url, params=params,timeout=5)

        if response.status_code == 200:
            result = mongo.db.voiceannoucement_configurations.update_one(
                {'ip_address': ip_address},
                {'$set': {'volume_level': volume_level}}
            )

            if result.matched_count > 0:
                return jsonify({"message": f"Volume successfully set to {volume_level}%", "success": True})
            
    
    except requests.exceptions.ConnectTimeout:
        return jsonify({'error': 'Connection timed out. device is not reachable can not set volume.Check the device working status', "success": False}), 504

    except Exception as e:
        return jsonify({'error': str(e), "success": False}), 500
    


 

current_dir = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(current_dir)
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')


@voice_wifi.route('/load_file', methods=['POST'])
def upload_file():
    ip_address = request.form.get('ip_address')
    if ip_address is None:
        return jsonify({'error': 'IP address is required', "success": False})

    try:
        if 'file' not in request.files or request.files['file'].filename == '':
            return jsonify({'error': 'No file selected for upload', "success": False})

        file = request.files['file']
        if file.mimetype != 'audio/mpeg':
            return jsonify({'error': 'Please upload only MP3 files', "success": False})

        ip_folder = os.path.join(UPLOAD_FOLDER, ip_address)
        if not os.path.exists(ip_folder):
            os.makedirs(ip_folder)  
     
        file_path = os.path.join(ip_folder, file.filename)
        file.save(file_path)
         

        files = {'file': (file.filename, file.stream, file.mimetype)}
        url = f'http://{ip_address}/upload'
        response = requests.post(url, files=files)

        if response.status_code == 200:
            return jsonify({"message": "File uploaded and stored successfully", "success": True})
            
        else:
            return jsonify({"error": "Failed to upload the file", "success": False}), response.status_code
    
    except requests.exceptions.ConnectTimeout:
        return jsonify({'error': 'Connection timed out. The server is down can not upload the file.Check the device working status', "success": False}), 504

    except Exception as e:
        return jsonify({'error': str(e), "success": False})
    



@voice_wifi.route('/download_file', methods=['GET'])
def download_file():
    ip_address = request.args.get('ip_address')
    filename = request.args.get('filename')
    
    if not ip_address:
        return jsonify({"error": "IP address is required", "success": False})
    if not filename:
        return jsonify({"error": "Filename is required", "success": False})

    ip_folder = os.path.join(UPLOAD_FOLDER, ip_address)
    file_path = os.path.join(ip_folder, filename)

    if not os.path.exists(ip_folder):
        return jsonify({"error": f"No folder found for IP address {ip_address}", "success": False}) ,404
    if not os.path.exists(file_path):
        return jsonify({"error": f"File {filename} not found for IP address {ip_address}", "success": False}),404

    try:
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e), "success": False})
    

@voice_wifi.route('/del_file',methods=['POST'])
def delete_file():
    data = request.json
    ip_address=data.get('ip_address')
    file_name = data.get('file_name')
    if file_name is None:
        return jsonify({'message':'select the file',"success":False})
          
    if ip_address is None  :
        return jsonify({'error': 'IP address is required',"success":False}), 400
    try:
        base_url=f'http://{ip_address}/filedel'
        param = {
            'filename':file_name
        }

        response = requests.get(base_url,params=param)
        if response.status_code==200:
            return jsonify({"message":f"succesfully deleted the file {file_name}","success":True})
        else:
            return jsonify({"error":"There is some problem while deleting the file or the particular file doesnot exists","success":False})
        
    except requests.exceptions.ConnectTimeout:
        return jsonify({'error': 'Connection timed out. The server is down can not delete file.Check the device working status', "success": False}), 504   
    
    except Exception as e:
        return jsonify({'error': str(e),"success":False}), 500
        



# @voice_wifi.route('/rename_file',methods=['post'])
# def rename_file():
#     data = request.json
#     ip_address=data.get('ip_address')
#     file_A = data.get('file_A')
#     file_B = data.get('file_B') 
#     if ip_address is None  :
#         return jsonify({'error': 'IP address is required',"success":False}), 400
        
#     if file_A is None or file_B is None:
#         return jsonify({'message':'both fields are required',"success":False})
    
#     if file_A == file_B:
#         return jsonify({'message': 'File names cannot be the same. Try with different names.', "success": False}), 400
       

#     try:
#         base_url=f'http://{ip_address}/rename'
#         param ={
#             'fa':file_A,
#             'fb':file_B
#         } 
#         response = requests.get(base_url,params=param)
#         if response.status_code == 200:
#             return jsonify({"message": f"Successfully renamed the file {file_A} to {file_B}", "success": True})
#         elif response.status_code == 404:
#             return jsonify({"error": f"File {file_A} does not exist on the server", "success": False}), 404
#         elif response.status_code == 500:
#             return jsonify({"error": f"Internal server error on the remote server", "success": False}), 500
#         else:
#             return jsonify({"error": f"Unexpected error: {response.text}", "success": False}), response.status_code   

            

    # except Exception as e:
    #     return jsonify({'error': str(e),"success":False}), 500


@voice_wifi.route('/play',methods=['POST'])
def play():
    data = request.json
    ip_address=data.get('ip_address')
    file_name = data.get('file_name')
    loop = data.get('loop')
    try:
        base_url= f'http://{ip_address}/play'
        param={
            "filename":file_name,
            "loop":loop
        }
        response = requests.get(base_url,params=param)
        if response.status_code == 200:
            if loop is None:
                return jsonify({"message":f"playing {file_name}","success":True})
               
            loop = int(loop)
            if loop < 0:
                return jsonify({"message":"invalid literal for loop","success":False})
            else:
                return jsonify({"message":f"playing {file_name} in {loop} loops","success":True})
        else:
            return jsonify({"message":"unable to play the sound or the request mp3 doesnot exist","success":False})
        
    except requests.exceptions.ConnectTimeout:
        return jsonify({'error': 'Connection timed out. The server is down can not play the audio. Check the device working status', "success": False}), 504
    
    except Exception as e:
        return jsonify ({"error":str(e),"success":False})
        


@voice_wifi.route('/stop',methods = ['POST'])
def stop():
    data = request.json
    ip_address=data.get('ip_address')
    try:
        base_url=f'http://{ip_address}/stop'
        response = requests.get(base_url)
        if response.status_code == 200:
            return jsonify ({"message":"stopped playing sound","success":False})
        else:
            return jsonify ({"error":"unable to stop the sound","success":False})
    
    except requests.exceptions.ConnectTimeout:
        return jsonify({'error': 'Connection timed out. The server is down can not stop the audio.Check the device working status', "success": False}), 504

    except Exception as e:
        return jsonify ({"error":str(e),"success":False})
    




@voice_wifi.route('/delete_device', methods=['POST'])
def delete_device():
    data = request.json
    
    ssid = data.get('ssid')  
    
    # if ssid is None or ssid.strip() == "":
    #     return jsonify({'error': 'SSID is required to delete a device', "success": False}), 400
    
    try:
        existing_device = mongo.db.voiceannoucement_configurations.find_one({'wifi_name': ssid})
        
        if existing_device:
            mongo.db.voiceannoucement_configurations.update_one(
                {'wifi_name': ssid},
                {'$set': {'status': 'deleted'}}  
            )
            return jsonify({'message': f'Device with SSID {ssid} marked as deleted successfully', "success": True}), 200
        else:
            return jsonify({'error': f'Device with SSID {ssid} not found', "success": False}), 404

    except Exception as e:
        return jsonify({'error': str(e), "success": False})




languages = ["English", "Hindi"]
@voice_wifi.route("/languages",methods=['GET'])
def get_languages():
    try:
        if not languages:
            return jsonify({"detail": "Languages not found.",'success': False}), 404
        return jsonify({"languages": languages,'success': True}), 200
    except Exception as e:
        return jsonify({"detail": "Unable to fetch the languages. Please try again later.",'success': False})


violations = ["Crowd_Count", "Personal_Protective_Equipment", "Danger_Zone","No_Parking","Protection_Zone","Traffic_Jam","Fire","Smoke","Dust","PPE_Helmet","Vest","Crash_Helmet","Parking","wheel_Count","Fire_Smoke_Dust","Fire_Smoke"]
@voice_wifi.route("/violations",methods=['GET'])
def get_violations():
    try:
        if not violations:
            return jsonify({"detail": "Violations not found.",'success': False}),404
        return jsonify({"violations": violations,'success': True}), 200
    except Exception as e:
        return jsonify({"detail": "Unable to fetch the violations. Please try again later.",'success': False}),
    





@voice_wifi.route('/filter_file_mp3', methods=['POST'])
def get_files():
    try:
        data = request.json
        languages = data.get('languages', [])  
        violation = data.get('violation')

        device_ip = data.get('device_ip')
        
        if 'languages' in data and 'violation' in data:
            if  not languages or not violation  or not device_ip:
                return jsonify({'success': False, 'message': 'Missing required parameters'})
            url = f'http://{device_ip}/filelist'

            response = requests.get(url)
            
            if response.status_code != 200:
                return jsonify({'success': False, 'message': 'Failed to fetch file list from the device'})

            file_list = response.json()  

            filtered_files = []
            for file in file_list:
                if file['type'] == 'file':
                    for language in languages:
                        expected_file_name = f'{language}-{violation}.mp3'
                        if file['name'] == expected_file_name:
                            filtered_files.append(file['name'])

            
            if filtered_files:
                return jsonify({'success': True, 'files': filtered_files}), 200
            else:
                return jsonify({'success': True, 'message': 'No matching files found', 'files': []}), 200
        
        elif 'languages' in data and not 'violation' in data:
            if not languages or not device_ip:
                return jsonify({'success': False, 'message': 'Missing required parameters'})
            
            url = f'http://{device_ip}/filelist'
            response = requests.get(url)
            
            if response.status_code != 200:
                return jsonify({'success': False, 'message': 'Failed to fetch file list from the device'})

            
            file_list = response.json()
        
            
            filtered_files = []
            for file in file_list:
                if file['type'] == 'file' :
                    for language in languages:
                        if file['name'].startswith(f'{language}-'):
                            filtered_files.append(file['name'])
            
            if filtered_files:
                return jsonify({'success': True, 'files': filtered_files}), 200
            else:
                return jsonify({'success': True, 'message': 'No matching files found', 'files': []}), 200
            
        elif 'violation' in data and 'languages' not in data:
            if not violation or not device_ip:
                return jsonify({'success': False, 'message': 'Missing parameter'})

            url = f'http://{device_ip}/filelist'
            response = requests.get(url)
            if response.status_code != 200:
                return jsonify({'success': False, 'message': 'Failed to fetch file list from the device'})
            file_list = response.json()
            filtered_files = []
            for file in file_list:
                if file['type'] == 'file' and file['name'].endswith(f'-{violation}.mp3'):
                    filtered_files.append(file['name'])

            return jsonify({'success': True, 'files': filtered_files if filtered_files else []}), 200


    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    


@voice_wifi.route('/filter_language_wise', methods=['POST'])
def get_the_files():
    try:
        data = request.json
        language = data.get('language')
        device_ip = data.get('device_ip')

        if not language or not device_ip:
            return jsonify({'success': False, 'message': 'Missing required parameters'})
        
        url = f'http://{device_ip}/filelist'
        response = requests.get(url)
        
        if response.status_code != 200:
            return jsonify({'success': False, 'message': 'Failed to fetch file list from the device'})

        
        file_list = response.json()
        
        filtered_files = []
        for file in file_list:
            if file['type'] == 'file' and file['name'].startswith(f'{language}-'):
                filtered_files.append(file['name'])
        
        if filtered_files:
            return jsonify({'success': True, 'files': filtered_files}), 200
        else:
            return jsonify({'success': True, 'message': 'No matching files found', 'files': []}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    



####ping API####

@voice_wifi.route('/ping_ip', methods=['POST'])
def ping_ip():
    data = request.json

    ip_address = data.get('ip_address')
    if ip_address is None:
        return jsonify({'error': 'IP address is required', "success": False}), 400

    try:
        if platform.system() == "Windows":
            ping_command = ['ping', '-n', '4', ip_address]  
        elif platform.system() == "Linux":
            ping_command = ['ping', '-c', '4', ip_address]  
        else:
            return jsonify({'error': 'Unsupported platform', "success": False}), 500

       
        ping_response = subprocess.run(
            ping_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,  
            timeout=10
        )

      
        if "Destination host unreachable" in ping_response.stdout:
            return jsonify({'error': f'{ip_address} is not reachable: Destination host unreachable', "success": False}), 

       
        if ping_response.returncode == 0:
            return jsonify({'message': f'{ip_address} is reachable', "success": True})

        
        return jsonify({'error': f'{ip_address} is not reachable as it is not in the same network range', "success": False}), 

    except subprocess.TimeoutExpired:
        return jsonify({'error': f'{ip_address} device is not working, please check if it is in network range ', "success": False}), 500

    except Exception as e:
        return jsonify({'error': str(e), "success": False}), 500
































    