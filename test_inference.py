import os
import time
import serverCom
import cv2
from datetime import datetime
import random
import string
import sys
from fingerprint import main as fingerprint

sys.path.append('/Users/changbeankang/Claw_For_Humanity/HOS_II/FastSAM-main/')
import single_segpred


class tools:
    def search_cam(max_ports=10):
        '''only use this as a debugging/
            running this everytime is not recommended.'''
        print('[LOG]: searching cam ports')
        available_ports = []
        for port in range(max_ports):
            camera = cv2.VideoCapture(port)
            if camera.isOpened():
                available_ports.append(port)
                camera.release()
        return available_ports
    
    def current_time():
        '''returns current yyyymmddhhmmss in string'''
        now = datetime.now()
        year_month_time = now.strftime("%Y%m%d%H%M%S")
        
        return str(year_month_time)
    
    



class bucket:
    cam = None
    frame = None
    
    waiting_list = [] # waiting list for detected objects
    

    # times
    function_start_time = None
    google_start_time = None

    google_result_time = {'uplaod time':0.0, 'inference time': 0.0} # drive time, inference time, 


class initialize:
    def init(search_cam, camPort = 0):
        '''initialize the code'''
    # initialize server com
        # initialize servercom plugin
        serverCom.initializer.__init__(
                                        os.getcwd(),
                                       'gen-lang-client-0521940196-1f1db2e46768',
                                       '1mTU6uOBwlx7VCEKP-Y038Ucm8aLXnpeToN1ddxqGCe4',
                                       '1NPciFwLIoW_ysdBg3ObeXRN4QvJBMXBl'
                                       )

        # initialize camera
        if search_cam:
            cam_ports = tools.search_cam() # search cam port
            bucket.cam = cv2.VideoCapture(cam_ports[0]) # use the first cam port in existence.
        else:
            bucket.cam = cv2.VideoCapture(camPort)
        
    # initialize fastsam
        single_segpred.initialize.init()


        print('\ninitialization done\n')

class main:
    def main():
        ''' fastsam -> crop -> upload
            circularnet inference
            retrieve info from gs
           '''
        time.sleep(3)
        r, bucket.frame = bucket.cam.read()
        img_name = f'{fingerprint.generate()}.jpg'
        target = os.path.join(os.getcwd(),'.imgs', img_name)
        cv2.imwrite(target, bucket.frame)
        
        img = cv2.imread(target)

        everything_result = single_segpred.main.inference(target, False, debugging = True)
        
        fastSam = single_segpred.main.annotate(everything_result,True,img, debugging = True)


        print(f'fastsam output is {fastSam}')


        return None


    def cropping():
        None


    def test(): # capture frame -> upload -> inference -> access data
        bucket.function_start_time = time.time() # initiaiting time in sec
        
        # take picture and save it in jpg
        time.sleep(5)
        r, bucket.frame = bucket.cam.read()
        img_name = f'frame_{fingerprint.generate()}.jpg'
        target = os.path.join(os.getcwd(),'.imgs', img_name)
        cv2.imwrite(target, bucket.frame)

        # upload to g drive
        bucket.google_start_time = time.time()
        google_drive_start_time = time.time()
        serverCom.uploader.photo(img_name, img_name)
        google_drive_end_time = time.time()


        print('everything completed')

        # while resolving,
        # keep looking for changes in gspread
        


        

        # bucket.google_result_time.append(google_drive_end_time-google_drive_start_time)
        



        




initialize.init(False)
main.main()