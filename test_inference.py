import os
import time
import serverCom
import cv2
from datetime import datetime
import random
import string

class tools:
    def search_cam(max_ports=10):
        '''u can always use this as a debugging'''
        available_ports = []
        for port in range(max_ports):
            camera = cv2.VideoCapture(port)
            if camera.isOpened():
                available_ports.append(port)
                camera.release()
        return available_ports
    
    def current_time():
        now = datetime.now()
        year_month_time = now.strftime("%Y%m%d%H%M%S")
        
        return year_month_time
    
    def fingerprint():
        characters = string.ascii_lowercase + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(8))
        return random_string



class bucket:
    cam = None

    frame = None

    # times
    function_start_time = None
    google_start_time = None

    google_result_time = {'uplaod time':0.0, 'inference time': 0.0} # drive time, inference time, 


class initialize:
    def init():
        # initialize servercom plugin   
        print('intiializing communication')     
        serverCom.initializer.__init__(
                                        os.getcwd(),
                                       'gen-lang-client-0521940196-1f1db2e46768',
                                       '1mTU6uOBwlx7VCEKP-Y038Ucm8aLXnpeToN1ddxqGCe4',
                                       '1NPciFwLIoW_ysdBg3ObeXRN4QvJBMXBl'
                                       )
        print('connection established!')

        # initialize camera
        print('initiating camera')
        print('searching for available camera ports')
        cam_ports = tools.search_cam()
        cam_ports = cam_ports[0]
        print(f'using {cam_ports} as a camera port')
        bucket.cam = cv2.VideoCapture(cam_ports)
        print('camera captured')

        print('\ninitialization complete\n')



class main:
    def check_changes():
        None

    def test(): # capture frame -> upload -> inference
        bucket.function_start_time = time.time() # initiaiting time in sec
        
        # take picture and save it in jpg
        r, bucket.frame = bucket.cam.read()
        img_name = f'frame_{tools.fingerprint()}.jpg'
        cv2.imwrite(img_name, bucket.frame)

        # upload to g drive
        bucket.google_start_time = time.time()
        google_drive_start_time = time.time()
        serverCom.uploader.photo(img_name, img_name)
        google_drive_end_time = time.time()

        # while resolving,
        # keep looking for changes in gspread
        


        

        bucket.google_result_time.append(google_drive_end_time-google_drive_start_time)
        



        





print(tools.fingerprint())