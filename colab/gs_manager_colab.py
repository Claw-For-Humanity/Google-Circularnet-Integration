from google.colab import auth
from oauth2client.client import GoogleCredentials
import gspread
from google.auth import default
from datetime import datetime
import string
import random

class bucket:
    creds = None
    gc = None
    spreadsheet = None
    worksheet = None

class tools:
    def fingerprint():
        characters = string.ascii_lowercase + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(8))
        return random_string

class initialize:
    def init(fileName, sheetName):
        auth.authenticate_user()
        bucket.creds, _ = default()
        _ = None # for security
        gc = gspread.authorize(bucket.creds)
        bucket.spreadsheet = gc.open(f'{str(fileName)}')
        bucket.worksheet = bucket.spreadsheet.worksheet(f'{str(sheetName)}')
        bucket.gc = None
        bucket.creds = None


class main:
    def gs_edit(worksheet, fingerprint, data):
        endDateStr = "endDate"
        endFingerprintStr = "endFingerprint"
        endDataStr = "endData"

        cell_session_time = datetime.now().strftime("%Y%m%d%H%M%S")
        print(f"current cell time is {cell_session_time}")

        dateCell = worksheet.find(endDateStr)
        fingerprintCell = worksheet.find(endFingerprintStr)
        dataCell = worksheet.find(endDataStr)

        if dateCell.col == 1 and fingerprintCell.col == 2 and dataCell.col ==3:
            print('datecell, tokenCell, dataCell is correctly oriented')
            if data == None:
                data = "None"
            worksheet.update_cell(dataCell.row, dataCell.col, f"{data}") # data
            worksheet.update_cell(fingerprintCell.row, fingerprintCell.col, f"{fingerprint}") # tocken
            worksheet.update_cell(dateCell.row, dateCell.col, f"{cell_session_time}") # date

        worksheet.update_cell(dateCell.row + 1, dateCell.col, endDateStr)
        worksheet.update_cell(fingerprintCell.row +1, fingerprintCell.col, endFingerprintStr)
        worksheet.update_cell(dataCell.row + 1, dataCell.col, endDataStr)


    def data_manager(data):
        k = data['num_detections'][0]

        output_dicts = []

        for i in range(k):
            output_dict = {
                'detection_class': data['detection_classes'][i],
                'detection_score': data['detection_scores'][0][i],
                'detection_box': data['detection_boxes'][0][i],
                'detection_class_name': data['detection_classes_names'][i]
            }
            output_dicts.append(output_dict)

        return output_dicts, k

    