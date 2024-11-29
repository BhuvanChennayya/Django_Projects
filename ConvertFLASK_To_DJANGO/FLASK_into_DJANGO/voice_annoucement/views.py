from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,FileResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from Data_Recieving.packages import *
from Data_Recieving.database import *
from Data_Recieving.final_ping import *
from django.core.files.storage import default_storage

# Create your views here.

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



# @voice_wifi.route('/connect_and_configure', methods=['POST'])
@csrf_exempt
def connect_and_configure(request):
    start_time = time.time()  ## start time
    print(f"Process started at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
    ret={"message":"something went wrong with connect and config  api"}
    if request.method == 'POST':
        data = json.loads(request.body)
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
                return JsonResponse({'message': 'Failed to connect to Wi-Fi check if your system supports Wi-Fi connection', "success": False})

            configure_ip(ip_mode, ip_address, gateway, subnet)

            existing_device = voiceannoucement_configurations.find_one({'wifi_name': ssid})

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

                voiceannoucement_configurations.update_one(
                    {'wifi_name': ssid},
                    {'$set': update_data}
                )
            else:
                update_data['wifi_name'] = ssid
                update_data['volume_level'] = '55'
                voiceannoucement_configurations.insert_one(update_data)

            end_time = time.time()  ## end time
            print(f"Process ended at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
            
            duration = end_time - start_time  ## total time taken
            print(f"Total process duration: {duration:.2f} seconds")

            return JsonResponse({'message': 'Connected and configured successfully', "success": True})

        except Exception as e:
            return JsonResponse({'error': str(e), "success": False})

    return JsonResponse(ret)
