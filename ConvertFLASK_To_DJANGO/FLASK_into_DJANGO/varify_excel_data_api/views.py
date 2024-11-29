from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,FileResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from Data_Recieving.packages import *
from Data_Recieving.database import *
from Data_Recieving.final_ping import *
from django.core.files.storage import default_storage

# Create your views here.
#Get currenttime with seconds
current_timestamp = datetime.now()                      
 

"""Draw boarder Fun"""
def set_border(ws, cell_range, brd):
    # thin = Side(border_style="thin", color="000000")
    thin = Side(border_style=brd, color="000000")
    for row in ws[cell_range]:
        for cell in row:
            cell.border = Border(top=thin, left=thin, right=thin, bottom=thin)

def set_border1(ws, cell_range):
    rows = ws[cell_range]
    for row in rows:
        # print("")
        if row == rows[0][0] or row == rows[0][-1] or row == rows[-1][0] or row == rows[-1][-1]:
            pass
        else:
            row[0].border = Border(left=Side(style='medium'))
            row[-1].border = Border(right=Side(style='medium'))
            
            for c in rows[0]:
                # print("*********************************", type(c))
                c.border = Border(top=Side(style='medium'))

            for c in rows[-1]:
                c.border = Border(bottom=Side(style='medium'))
                # c.border = Border(top=Side(style='thick'))
    rows[0][0].border = Border(left=Side(style='medium'), top=Side(style='medium'))
    rows[0][-1].border = Border(right=Side(style='medium'), top=Side(style='medium'))
    rows[-1][0].border = Border(left=Side(style='medium'), bottom=Side(style='medium'))
    rows[-1][-1].border = Border(right=Side(style='medium'), bottom=Side(style='medium'))



def update_status(data, sh):
    for i in data: 
        print()
        sh.append(i)

def get_letter_index(index):
    get_letter = openpyxl.utils.cell.get_column_letter(index)
    return get_letter


"""Update new_column value to the 'old_key tuple' and also update new_column number to the 'new_key tuple'"""
def replace_key(data, old_key, sh):
    new_key = []
    for k in range(1, len(old_key)+3):
        new_key.append(k)
    for index in new_key:
        letter = get_letter_index(index)
        sh.column_dimensions[letter].width = 30
    ls_key = zip(old_key, new_key)
    for ls_k in list(ls_key):
        data[ls_k[1]] = data[ls_k[0]]
        del data[ls_k[0]]    
    return data

#fun to replace dict keys as index num
def get_require_data_ls(list_row, sh):
    require_data = []
    for row_val in list_row:
        listing_keys = list(row_val.keys())[1:]
        row_val = replace_key(row_val, listing_keys, sh)
        first_key = next(iter(row_val))
        first_value = row_val.pop(first_key)
        require_data.append(row_val)
    return require_data, listing_keys


def get_cell(max_columns_ex, sh):
    cell_bold = sh[max_columns_ex]
    convert_type = str(cell_bold[-1])
    test = convert_type.split('.')
    ret = test[1][:-1]
    return ret


def colour_indication(sh, keys_list):
    max_rows_ex = sh.max_row
    max_columns_ex = sh.max_column
    #Updating the colour_code with status
    sh.cell(row = 2, column = max_columns_ex + 2).fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF",fill_type = "solid")
    sh.cell(row = 3, column = max_columns_ex + 2).fill = PatternFill(start_color="FDB777", end_color="FDB777",fill_type = "solid")
    sh.cell(row = 4, column = max_columns_ex + 2).fill = PatternFill(start_color="c2e9fb", end_color="c2e9fb",fill_type = "solid")
    sh.cell(row = 5, column = max_columns_ex + 2).fill = PatternFill(start_color="66ff99", end_color="66ff99",fill_type = "solid")
    sh.cell(row = 6, column = max_columns_ex + 2).fill = PatternFill(start_color="F07470", end_color="F07470",fill_type = "solid")
    sh.cell(row = 2, column = max_columns_ex + 3, value = "Both RTSP and IP working", ) #FFFFFF
    letter = get_letter_index(max_columns_ex + 3)
    to_bold = letter + '2'
    cell_bold = sh[to_bold]
    cell_bold.font = Font(bold=True)
    sh.cell(row = 3, column = max_columns_ex + 3, value = "Both RTSP and IP not working") #FDB777
    letter = get_letter_index(max_columns_ex + 3)
    to_bold = letter + '3'
    cell_bold = sh[to_bold]
    cell_bold.font = Font(bold=True)
    # cell_bold.font = Font(bold=True)
    sh.cell(row = 4, column = max_columns_ex + 3, value = "RTSP not working and IP  working") #c2e9fb
    # cell_bold = sh["I4"]
    letter = get_letter_index(max_columns_ex + 3)
    to_bold = letter + '4'
    cell_bold = sh[to_bold]
    cell_bold.font = Font(bold=True)
    # cell_bold.font = Font(bold=True)
    sh.cell(row = 5, column = max_columns_ex + 3, value = "Ip is not working and RTSP is working") #66ff99
    # cell_bold = sh["I5"]
    letter = get_letter_index(max_columns_ex + 3)
    to_bold = letter + '5'
    cell_bold = sh[to_bold]
    cell_bold.font = Font(bold=True)
    # cell_bold.font = Font(bold=True)
    sh.cell(row = 6, column = max_columns_ex + 3, value = "Both RTSP and IP not given") #F07470
    # cell_bold = sh["I6"]
    letter = get_letter_index(max_columns_ex + 3)
    to_bold = letter + '6'
    cell_bold = sh[to_bold]
    cell_bold.font = Font(bold=True)    
    # cell_bold.font = Font(bold=True)
    # cell_bold.font = Font(bold=True)
    fun_res = get_cell(max_columns_ex, sh)
    cell_val = sh.cell(2, max_columns_ex + 2)
    test = str(cell_val).split('.')
    ret = test[1][:-1]
    fun_res_1 = get_cell(max_columns_ex -5, sh)
    clm_num = 'A'+ str(2)
    row_n = sh.max_row
    get_clm_range = sh.max_column
    clr_indication_brd = get_letter_index(get_clm_range-1) + '2' + ':' + get_letter_index(get_clm_range) + '6'
    set_border1(sh, clr_indication_brd)    
    row_num = get_letter_index(get_clm_range -3) + str(row_n)
    range_num = clm_num + ':' + row_num
    set_border(sh, range_num, "thin")
    sh.column_dimensions['I'].width = 36
    for rows in sh.iter_rows(min_row=1, max_row = 1, min_col=1, max_col = len(keys_list)-1):
        count = 0
        for cell in rows:
            cell.value = keys_list[count]
            count = count + 1
            cell.font = Font(bold=True, size=16, color = "700070")
            cell.alignment = Alignment(horizontal='center', vertical='center')
    return True


#Fun to write the excel sheet
def write_excel(cam_status_file):
    wb = openpyxl.Workbook()
    sh = wb.active
    #Get latest data
    trial = camera_excel_details.find_one({},sort=[( '_id', pymongo.DESCENDING )])
    row_list = list(excel_cameras.find({"token": trial["token"]}))
    if len(row_list) != 0:
        #Fun to get the list of column headers and replace data dict key as index.
        require_data, list_keys = get_require_data_ls(row_list, sh)

        #Fun to get ip and rtsp column name
        verify_the_keys = verify_key_exist_or_not(list_keys)
        
        if len(verify_the_keys) != 0:
            if len(verify_the_keys[0]) != 0 and len(verify_the_keys[1]) != 0:
                camera_ip_key = verify_the_keys[0][0]
                rtsp_key = verify_the_keys[1][0]

            elif len(verify_the_keys[0]) != 0 and len(verify_the_keys[1]) == 0:
                camera_ip_key = verify_the_keys[0][0]
                rtsp_key = None

            elif len(verify_the_keys[0]) == 0 and len(verify_the_keys[1]) != 0:
                camera_ip_key = None
                rtsp_key = verify_the_keys[1][0]

            else:
                camera_ip_key = None
                rtsp_key = None

            #If both CAMERA IP and RTSP in the list
            # if "CAMERA IP" in list_keys and "rtsp" in list_keys:
            if camera_ip_key in list_keys and rtsp_key in list_keys:
                for data_1 in require_data:
                    # remove the last key using .pop() method[Removing token from the data.]
                    last_key = list(data_1)[-1]
                    removed_tuple = data_1.pop(last_key)
                    sh.insert_rows(1)

                    #Both "rtsp and ip" Working 
                    if ("ip_working") in data_1.values() and "rtsp_working" in data_1.values():
                        for col, value in data_1.items():
                            sh.cell(row=2, column=col, value=value)
                            sh.cell(row=2, column=col).fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF",fill_type = "solid")
                            sh.cell(row=2, column=col).alignment = Alignment(horizontal='center', vertical='center')

                    #Both "rtsp and ip" not working
                    elif ("ip_not_working") in data_1.values() and "rtsp_not_working" in data_1.values():
                        for col, value in data_1.items():
                            sh.cell(row=2, column=col, value=value)
                            sh.cell(row=2, column=col).fill = PatternFill(start_color="FDB777", end_color="FDB777",fill_type = "solid")
                            sh.cell(row=2, column=col).alignment = Alignment(horizontal='center', vertical='center')

                    #rtsp is "connected" and ip is "offline"
                    elif ("ip_working") in data_1.values() and "rtsp_not_working" in data_1.values():
                        for col, value in data_1.items():
                            sh.cell(row=2, column=col, value=value)
                            sh.cell(row=2, column=col).fill = PatternFill(start_color="c2e9fb", end_color="c2e9fb",fill_type = "solid")
                            sh.cell(row=2, column=col).alignment = Alignment(horizontal='center', vertical='center')

                    #rtsp is not "connected" and ip is "online"
                    elif ("ip_not_working") in data_1.values() and "rtsp_working" in data_1.values():
                        for col, value in data_1.items():
                            sh.cell(row=2, column=col, value=value)
                            sh.cell(row=2, column=col).fill = PatternFill(start_color="66ff99", end_color="66ff99",fill_type = "solid")
                            sh.cell(row=2, column=col).alignment = Alignment(horizontal='center', vertical='center')


                    #Both rtsp and ip not given
                    elif "ip_address_not_given" in data_1.values() and "rtsp_not_given" in data_1.values():
                        for col, value in data_1.items():
                            sh.cell(row=2, column=col, value=value)
                            sh.cell(row=2, column=col).fill = PatternFill(start_color="F07470", end_color="F07470",fill_type = "solid")
                            sh.cell(row=2, column=col).alignment = Alignment(horizontal='center', vertical='center')

                    #If rtsp is not working and ip is not given
                    elif "ip_address_not_given" in data_1.values() and "rtsp_not_working" in data_1.values():
                        for col, value in data_1.items():
                            sh.cell(row=2, column=col, value=value)
                            sh.cell(row=2, column=col).fill = PatternFill(start_color="FDB777", end_color="FDB777",fill_type = "solid")
                            sh.cell(row=2, column=col).alignment = Alignment(horizontal='center', vertical='center')

                    #If rtsp is working and ip is not given
                    elif "ip_address_not_given" in data_1.values() and "rtsp_working" in data_1.values():
                        for col, value in data_1.items():
                            sh.cell(row=2, column=col, value=value)
                            sh.cell(row=2, column=col).fill = PatternFill(start_color="66ff99", end_color="66ff99",fill_type = "solid")
                            sh.cell(row=2, column=col).alignment = Alignment(horizontal='center', vertical='center')

                    #If ip is not working and rtsp is not given
                    elif "ip_not_working" in data_1.values() and "rtsp_not_given" in data_1.values():
                        for col, value in data_1.items():
                            sh.cell(row=2, column=col, value=value)
                            sh.cell(row=2, column=col).fill = PatternFill(start_color="FDB777", end_color="FDB777",fill_type = "solid")
                            sh.cell(row=2, column=col).alignment = Alignment(horizontal='center', vertical='center')

                    #rtsp is not given and ip is working
                    elif "ip_working" in data_1.values() and "rtsp_not_given" in data_1.values():
                        for col, value in data_1.items():
                            sh.cell(row=2, column=col, value=value)
                            sh.cell(row=2, column=col).fill = PatternFill(start_color="c2e9fb", end_color="c2e9fb",fill_type = "solid")
                            sh.cell(row=2, column=col).alignment = Alignment(horizontal='center', vertical='center')

                res = {"message": "Successfully created the camera_status excel.", "success": True}


            elif camera_ip_key in list_keys and rtsp_key not in list_keys:
                for data_1 in require_data:
                    # remove the last key using .pop() method
                    last_key = list(data_1)[-1]
                    removed_tuple = data_1.pop(last_key)
                    sh.insert_rows(1)

                    #Both "rtsp and ip" not working
                    if "ip_not_working" in list(data_1.values()) and "rtsp_not_working" in list(data_1.values()):
                        for col, value in data_1.items():
                            sh.cell(row=2, column=col, value=value)
                            sh.cell(row=2, column=col).fill = PatternFill(start_color="FDB777", end_color="FDB777", fill_type = "solid")
                            sh.cell(row=2, column=col).alignment = Alignment(horizontal='center', vertical='center')


                    #Ip is working but rtsp is not working
                    elif ("ip_working") in data_1.values() and "rtsp_not_working" in data_1.values():
                        for col, value in data_1.items():
                            sh.cell(row=2, column=col, value=value)
                            sh.cell(row=2, column=col).fill = PatternFill(start_color="c2e9fb", end_color="c2e9fb",fill_type = "solid")
                            sh.cell(row=2, column=col).alignment = Alignment(horizontal='center', vertical='center')

                res = {"message": "Successfully created the camera_status excel.", "success": True}


            elif rtsp_key in list_keys and camera_ip_key not in list_keys:
                for data_1 in require_data:
                    # remove the last key from dict using .pop() method
                    last_key = list(data_1)[-1]
                    removed_tuple = data_1.pop(last_key)
                    sh.insert_rows(1)
                    
                    #Both rtsp and ip not working
                    if "rtsp_not_working" in list(data_1.values()) and "ip_address_not_given" in list(data_1.values()):
                        for col, value in data_1.items():
                            sh.cell(row=2, column=col, value=value)
                            sh.cell(row=2, column=col).fill = PatternFill(start_color="FDB777", end_color="FDB777", fill_type = "solid")
                            sh.cell(row=2, column=col).alignment = Alignment(horizontal='center', vertical='center')

                    #rtsp is online and ip is "offline"
                    elif ("rtsp_working") in data_1.values() and "ip_address_not_given" in data_1.values():
                        for col, value in data_1.items():
                            sh.cell(row=2, column=col, value=value)
                            sh.cell(row=2, column=col).fill = PatternFill(start_color="66ff99", end_color="66ff99",fill_type = "solid")
                            sh.cell(row=2, column=col).alignment = Alignment(horizontal='center', vertical='center')

                res = {"message": "Successfully created the camera_status excel.", "success": True}
                

            elif "CAMERA_IP" not in list_keys and "rtsp" not in list_keys:
                res = {"message": "requier camera details not there.", "success": False}

            
            colour_indication(sh, list_keys)
            camera_status_filename = os.getcwd()+'/'+'camera_status_excel_sheets/'+cam_status_file    
            if not os.path.exists('camera_status_excel_sheets'):
                os.makedirs('camera_status_excel_sheets')

            wb.save(camera_status_filename)

        else:
            res = {"message":"no data"}

    else:
        res = {"message":"Given token excel is not existed, please upload the excel sheet."}

    return res

"""To read the excel sheet data with returning all the data of excel sheet and the column headers."""
def get_excel_sheet_data(filename):
    # load excel with its path
    wrkbk = openpyxl.load_workbook(filename)
    sh = wrkbk.active

    # iterate through excel and display data
    ls = []
    all_data = []
    for i in range(1, sh.max_row+1):
        for j in range(1, sh.max_column+1):

            cell_obj = sh.cell(row=i, column=j)
            all_data.append(cell_obj.value)

            if i==1:
                ls.append(cell_obj.value)

    return all_data, ls


"""This fun to get the all row datas with column headers in the dictionary format."""
def dict_data_excel(all_data, ls, filename):
    all_dict = []
    i = 0
    val_dict = {}

    wrkbk = openpyxl.load_workbook(filename)
    sh = wrkbk.active

    ttl_columns = sh.max_column
    
    for val in all_data[ttl_columns:]:
        val_dict.update({ls[i]: val})
        i = i + 1
        if i == ttl_columns:
            i = 0
            all_dict.append(val_dict)
            val_dict = {}

    return all_dict

def get_ip_rtsp(verify_the_keys):
    rtsp_ls = []
    ip_ls = []
    ret = []
    for kk in verify_the_keys:
        if 'ip' in kk:
            camera_ip_key_1 = kk
            ip_ls.append(camera_ip_key_1)

        if 'IP' in kk:
            camera_ip_key_1 = kk
            ip_ls.append(camera_ip_key_1)
        
        if 'rtsp' in kk:
            rtsp_key_1 = kk
            rtsp_ls.append(rtsp_key_1)
            
    return ip_ls, rtsp_ls


def verify_key_exist_or_not(list_keys):
    empty_ls = []
    print("LISTING KEYS:", list_keys)
    if len(list_keys) != 0:
        for akey in list_keys:
            # print("ioooo ==== ", akey)
            # if 'ip' == akey or 'rtsp' in akey:
            #     empty_ls.append(akey)

            if 'cameraip' in akey or 'rtsp' in akey:
                empty_ls.append(akey)

            elif 'CAMERAIP' in akey or 'RTSP' in akey:
                empty_ls.append(akey)

            # elif 'IP' == akey or 'rtsp' in akey:
            #     empty_ls.append(akey)

            else:
                print("NOT THERE", empty_ls)

        fun_response = get_ip_rtsp(empty_ls)

    else:
        fun_response = {"message":"Given excel sheet does not existed the 'ip' and 'rtsp'.", "success": False}

    print("function response -----------------8888 ", fun_response)
    return fun_response


"""Update excel sheet data to the database"""
def data_upload(all_json_data, list_parameters, unique_str):
    ret = {"Something went wrong"}
    list_parameters_ls = []
    for c, clm_par in enumerate(list_parameters):
        print("PARA:", clm_par, c)
        print("type ====", type(clm_par))
        print("kkkkk====",clm_par.lower() )
        # newLOwercase = clm_par.lower()
        if type(clm_par) == str:
            # clm_par.lower()
            # list_parameters_ls.append(clm_par)
            list_parameters_ls.append(clm_par.lower())
        else:
            list_parameters_ls.append(clm_par)
        # list_parameters_ls.append(newLOwercase)
        # list_parameters[c].str.lower()
    print()
    print("LIST OF PARAMETERS:", list_parameters_ls)
    if 'cameraip' in list_parameters_ls or 'rtsp' in list_parameters_ls or "CAMERAIP" in list_parameters_ls  or "RTSP" in list_parameters_ls:
        verify_the_keys = verify_key_exist_or_not(list_parameters_ls)
        print("VERIFY KEYS FUN RESP", verify_the_keys)

        if len(verify_the_keys) != 0:
            if len(verify_the_keys[0]) != 0 and len(verify_the_keys[1]) != 0:
                camera_ip_key = verify_the_keys[0][0]
                rtsp_key = verify_the_keys[1][0]

            elif len(verify_the_keys[0]) != 0 and len(verify_the_keys[1]) == 0:
                camera_ip_key = verify_the_keys[0][0]
                rtsp_key = None

            elif len(verify_the_keys[0]) == 0 and len(verify_the_keys[1]) != 0:
                camera_ip_key = None
                rtsp_key = verify_the_keys[1][0]

            else:
                camera_ip_key = None
                rtsp_key = None


            for cam_data in all_json_data:
                #only CAMERA IP is avilable in the excel sheet.
                # if "CAMERA IP" in list_parameters and "rtsp" not in list_parameters:
                if camera_ip_key in list_parameters_ls and rtsp_key not in list_parameters_ls:
                    #CAM_IP is not none.
                    if cam_data[camera_ip_key] != None:
                        res = ping_test(cam_data[camera_ip_key])
                        cam_data.update({"ip_status": res, "rtsp_status":"rtsp_not_given", "token": unique_str})
                        # insert_cam_ip_data = excel_cameras.find_one({camera_ip_key: cam_data[camera_ip_key], "ip_status": res})
                        insert_cam_ip_data = excel_cameras.find({camera_ip_key: cam_data[camera_ip_key], "ip_status": res, "token": unique_str})

                        if len(list(insert_cam_ip_data)) == 0:
                            excel_cameras.insert_one(cam_data)
                            ret = {"message": "Successfully updated the excel sheet.", "success": True}

                        # else:
                        #     ret = {"message":"Given excel already existed.", "success":False}


                        

                #only RTSP is avilable in the excel sheet.
                elif rtsp_key in list_parameters_ls and camera_ip_key not in list_parameters_ls:
                    #RTSP is not None.
                    if cam_data[rtsp_key] != None:
                        res_rtsp = CHECKRTSPWORKINGORNOT(cam_data[rtsp_key])                            #verifying the RTSP is working or not.

                        cam_data.update({"ip_status": "ip_address_not_given", "rtsp_status": res_rtsp, "token": unique_str})
                        insert_rtsp_data = excel_cameras.find_one({rtsp_key: cam_data[rtsp_key], "rtsp_status": res_rtsp, "token": unique_str})
                        if insert_rtsp_data == None:
                            excel_cameras.insert_one(cam_data)
                            
                            ret = {"message": "Successfully updated the excel sheet.", "success": True}


                # Both CAMERA IP and RTSP are in the excel sheet.
                elif camera_ip_key in list_parameters_ls and rtsp_key in list_parameters_ls:
                    #Both RTSP and CAMERAIP are not empty.
                    if cam_data[rtsp_key] != None and cam_data[camera_ip_key] != None:
                        res = ping_test(cam_data[camera_ip_key])
                        rtsp = cam_data[rtsp_key]
                        res_rtsp = CHECKRTSPWORKINGORNOT(rtsp)
                        cam_data.update({"ip_status": res, "rtsp_status": res_rtsp, "token": unique_str})
                        insert_data = excel_cameras.find_one({camera_ip_key: cam_data[camera_ip_key], "ip_status": res, "rtsp_status":res_rtsp, "token": unique_str})
                        if insert_data == None:
                            excel_cameras.insert_one(cam_data)
                            
                    #Both RTSP and Cam_ip not given
                    elif cam_data[rtsp_key] == None and cam_data[camera_ip_key] == None:
                        cam_data.update({"ip_status": "ip_address_not_given", "rtsp_status": "rtsp_not_given", "token": unique_str})
                        insert_data = excel_cameras.find_one({camera_ip_key: cam_data[camera_ip_key], "ip_status": "ip_address_not_given"})
                        if insert_data == None:
                            excel_cameras.insert_one(cam_data)

                    #RTSP is empty and Cam_ip had given      
                    elif cam_data[rtsp_key] == None and cam_data[camera_ip_key] != None:
                        res = ping_test(cam_data[camera_ip_key])
                        cam_data.update({"ip_status": res, "rtsp_status": "rtsp_not_given", "token": unique_str})
                        insert_data = excel_cameras.find_one({camera_ip_key: cam_data[camera_ip_key], "ip_status": res, "token": unique_str})
                        if insert_data == None:
                            excel_cameras.insert_one(cam_data)

                    # """Cam_ip is empty and RTSP had given."""        
                    elif cam_data[rtsp_key] != None and cam_data[camera_ip_key] == None:
                        res_rtsp = CHECKRTSPWORKINGORNOT(rtsp)
                        cam_data.update({"ip_status": "ip_address_not_given", "rtsp_status": res_rtsp, "token": unique_str})
                        insert_data = excel_cameras.find_one({camera_ip_key: cam_data[camera_ip_key], "rtsp_status": res_rtsp, "token": unique_str})
                        if insert_data == None:
                            excel_cameras.insert_one(cam_data)

                    ret = {"message": "Successfully updated the excel sheet.", "success": True}

                elif camera_ip_key not in list_parameters and rtsp_key not in list_parameters:
                    ret = {"message": "Camera IP and RTSP not there in the given excel sheet.", "success": False}
    else:
        ret = {"message":"Given excel sheet does not existed the 'ip' and 'rtsp'.", "success": False}

    return ret


# @check_camera.route('/upload_cameras_excel', methods = ['POST'])
@csrf_exempt
def upload_cameras_excel(request):
    ret={'message':'something went wrong with upload cameras excel','success':False}
    if request.method == "POST":
        try:
            file = request.FILES['excel_file']
            filename = file.name
            res = CHECKEXCELFILEEXTENTION(filename)

            if res == True:
                """SAVEING GIVEN FILE WITH CREATING NEW FOLDER"""
                filename_db = os.getcwd()+'/'+'camera_detail_excel_sheets/'+filename
                if not os.path.exists('camera_detail_excel_sheets'):
                    os.makedirs('camera_detail_excel_sheets')   

                with default_storage.open(f'{filename_db}', 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                print("**********************************************************************************")
                #Fun to generate a token.
                token = GENERATEALPHANUMERICKEYFOREXCELTEST50()
                
                #Verifying the inserting data is exist or not in the db.
                verify_data = camera_excel_details.find_one({"requested_time": current_timestamp, "token": token})
                if verify_data == None:                                             
                    #If not data not exist insert to the db.
                    camera_excel_details.insert_one({"requested_time":current_timestamp, "token": token}) 
            
                #Fun to get the excelsheet column headers and all rows data.
                all_data = get_excel_sheet_data(filename_db)
                print("all data__________--------",all_data)

                #Fun to get all excel sheet data in the dictionary format.
                all_dictionary_data = dict_data_excel(all_data[0], all_data[1], filename_db)

                print("***************** test *****************", all_data[1])
                #Fun to update excelsheet data to the database.
                ret = data_upload(all_dictionary_data, all_data[1],token)
                
            else:
                ret = {"message": "Please give the excelsheet file.", "success": False}
        except ( 
            pymongo.errors.AutoReconnect,            pymongo.errors.BulkWriteError,             pymongo.errors.PyMongoError, 
            pymongo.errors.ProtocolError,             pymongo.errors.CollectionInvalid ,             pymongo.errors.ConfigurationError,
            pymongo.errors.ConnectionFailure,             pymongo.errors.CursorNotFound,             pymongo.errors.DocumentTooLarge,
            pymongo.errors.DuplicateKeyError,             pymongo.errors.EncryptionError,             pymongo.errors.ExecutionTimeout,
            pymongo.errors.InvalidName,             pymongo.errors.InvalidOperation,             pymongo.errors.InvalidURI,
            pymongo.errors.NetworkTimeout,             pymongo.errors.NotPrimaryError,             pymongo.errors.OperationFailure,
            pymongo.errors.ProtocolError,             pymongo.errors.PyMongoError,             pymongo.errors.ServerSelectionTimeoutError,
            pymongo.errors.WTimeoutError,                           pymongo.errors.WriteConcernError,
            pymongo.errors.WriteError) as error1:
            print("print(,)", str(error1))
            ret['message' ] = '  something error --------------has occured in  apis ' + str(error1)
            if restart_mongodb_r_service():
                print("mongodb restarted")
            else:
                if forcerestart_mongodb_r_service():
                    print("mongodb service force restarted-")
                else:
                    print("mongodb service is not yet started.")
        except Exception as error:
            ret['message']='something error ************has occured ' +str(error)

    return JsonResponse(ret)



# @check_camera.route('/get_camera_status_excel', methods = ['GET'])
@csrf_exempt
def get_camera_status_excel(request):
    res={'message':'something went wrong with get_camera_status_excel api','success':False}
    if request.method == "GET":
        cam_status_filename = "camera_status_excel_sheet" + "_" +replace_spl_char_time_to(str(current_timestamp)) + ".xlsx"
        res = write_excel(cam_status_filename)
    return JsonResponse(res)

# @check_camera.route('/download_camera_status_sheet', methods=['GET'])
@csrf_exempt
def excel_result(request):
    res={'message':'something went wrong with download_camera_status_sheet api','success':False}
    if request.method == "GET":
        try:
            list_of_files = glob.glob(os.getcwd() + '/camera_status_excel_sheets/' +'/*')
            # print('list of elements from the folder---- ',list_of_files)
            latest_file = max(list_of_files, key=os.path.getctime)
            path, filename = os.path.split(latest_file)
            if filename:
                main_path = os.path.abspath(path)
                file_path = os.path.join(main_path, filename)
        
                if os.path.exists(file_path):
                        # Open the file in binary mode and return it as an attachment
                    with open(file_path, 'rb') as file:
                        return FileResponse(file, as_attachment=True, filename=filename)
                else:
                      return JsonResponse({'success': False, 'message': 'File is not found.'})
               
            else:
                return JsonResponse({'success': False, 'message': 'File is not found.'})
        except (NameError, RuntimeError, FileNotFoundError, AssertionError,
                AttributeError, EOFError, FloatingPointError, TypeError,
                GeneratorExit, IndexError, KeyError, KeyboardInterrupt, MemoryError,
                NotImplementedError, OSError, OverflowError, ReferenceError,
                StopIteration, SyntaxError, IndentationError, TabError, SystemError,
                SystemExit, TypeError, UnboundLocalError, UnicodeError,
                UnicodeEncodeError, UnicodeDecodeError, UnicodeTranslateError,
                ValueError, ZeroDivisionError, ConnectionError, KeyboardInterrupt,
                BaseException, ValueError) as e:
            
            return JsonResponse({'success': False, 'message': str(e)})
        
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})