import subprocess

#-------------------------------------------------------------------------------
def is_device_available(device_name):
    '''
    This function checks if the specified SDR device is available.
    '''

    if device_name=='cosine':
        return True

    elif device_name=='hackrf':
        command = ["lsusb -v | grep -o 'HackRF' | sort -u"]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()
        # the output is not in proper UTF-8 format for some reason. So, we ignore the parts that are not convertible to Unicode. Then we remove the newline charactor in that string as well.
        stdout = stdout.decode('utf-8', 'ignore').strip('\n')
        if stdout=="HackRF":
	        return True   
        else:
            return False

    elif device_name=='rtlsdr':
        command = ["lsusb -v | grep -o 'RTL2838' | sort -u"]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()
        # the output is not in proper UTF-8 format for some reason. So, we ignore the parts that are not convertible to Unicode. Then we remove the newline charactor in that string as well.
        stdout = stdout.decode('utf-8', 'ignore').strip('\n')
        if stdout=="RTL2838":
	        return True   
        else:
            return False
    else:
        return False