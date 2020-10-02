def device_info(device, username, password):

    import requests
    import json
    from requests.auth import HTTPBasicAuth
    
    device_list = [device]  
    
    for device in device_list:

        api_response = requests.get("https://api.cognosos.net/device/findByDeviceID?device_id=" + str(device), auth=HTTPBasicAuth(username, password))
        # api_response2 = requests.get("https://api.cognosos.net/node/activeNodeStatus?device_id=" + str(device), auth=HTTPBasicAuth(username, password))
        if api_response.status_code == 200:
            # print("********")
            # print(device_num)
            api_contents = json.loads(api_response.text)
            status = api_contents['status']
            try:
                customer = api_contents['customer']['name']
            except:
                customer = "?"
            try:
                application = api_contents['application_code']
            except:
                application = "?"
            try:
                gps_time = api_contents['gps_time']
            except:
                gps_time = "?"
            try:
                gps_adj = api_contents['gps_adjustment']
            except:
                gps_adj = "?"
            try:
                is_quiet = api_contents['isQuiet']
            except:
                is_quiet = "?"
            try:
                last_mess = api_contents['last_message_date']
            except:
                last_mess = '?'
        
        message = "Device: " + str(device) + " | Status: " + str(status) + " | Customer: " + str(customer) + " | Application: " + str(application) + " | GPS Time: " + str(gps_time) 

        #return message   
        return [device, status, customer, application, gps_time] 

        # for attr, value in api_contents.items():
                # print(attr,"--",value)
        # else:
            # print("API Error: ")
            # print("API Response: {0}, API Response Content: {1}".format(
                    # api_response, api_response.content))
    workbook.close()
