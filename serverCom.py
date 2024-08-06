import gspread
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import time

class bucket:
  creds = None
  gc = None
  sh = None
  worksheet = None


class initializer:
    SCOPES = ['https://www.googleapis.com/auth/drive'] # final

    PATH_SERVICE_ACCOUNT_FILE = None
    PATH_CAPTURED_IMAGES = None
    ID_PARENT_FOLDER = None


    def __init__(DEFAULT_PATH, account_id, destination_parent_id):
        '''example is
        (default_base_folder, "cfh-hawkeye-xxxxxx", "xxxxxx (end of the addy)")'''
        initializer.PATH_SERVICE_ACCOUNT_FILE = os.path.join(DEFAULT_PATH, 'data', f'{account_id}.json')
        initializer.PATH_CAPTURED_IMAGES = os.path.join(DEFAULT_PATH, 'capturedImages')
        initializer.ID_PARENT_FOLDER = destination_parent_id

        # define creds and authenticate
        bucket.creds = initializer.authenticate()
        bucket.gc = gspread.authorize(bucket.creds)
        bucket.sh = bucket.gc.open('DetectedOutput') # open_by_key is an alternative fo rhtis
        bucket.worksheet = bucket.gc.open('DetectedOutput').sheet1


    def authenticate():
        creds = service_account.Credentials.from_service_account_file(initializer.PATH_SERVICE_ACCOUNT_FILE, scopes = initializer.SCOPES)
        return creds


class tools:
  def current_time():
    now = datetime.now()
    year_month_time = now.strftime("%Y%m%d%H%M%S")
    return year_month_time

class uploader:
    def photo(image_name, upload_name):
        '''make sure to include format of the file as well i.e.) .png '''
        if initializer.PATH_CAPTURED_IMAGES == None or initializer.PATH_SERVICE_ACCOUNT_FILE == None or bucket.creds == None:
            print("initialize first!")
            print(f"[LOG] : {initializer.PATH_CAPTURED_IMAGES}")
            print(f"[LOG] : {initializer.PATH_SERVICE_ACCOUNT_FILE}")
            print(f"[LOG] : {bucket.creds}")
            
            exit()
        
        service = build('drive', 'v3', credentials=bucket.creds)

        file_metadata = {
            'name':f"{upload_name}",
            'parents': [initializer.ID_PARENT_FOLDER]
        }

        file_path = os.path.join(initializer.PATH_CAPTURED_IMAGES, f'{image_name}')

        file = service.files().create(
            body=file_metadata,
            media_body=file_path
        ).execute()

        print('uploaded!')

class editor:
  endDateStr = "endDate"
  endTokenStr = "endToken"
  endDataStr = "endData"

  def mainInitiator(token):
    ''' stage one - main brain needs to upload pictures and upload token name to the spreadsheet
    outline
      1. find dateCell, tokenCell, and dataCell 
      2. if they match, input current session time and token into the cell
      3. push one cells below'''
    worksheet = bucket.worksheet
    cell_session_time = tools.current_time()
    print(f"current cell time is {cell_session_time}")

    # find date cell, token cell and data cell
    dateCell = worksheet.find(editor.endDateStr)
    tokenCell = worksheet.find(editor.endTokenStr)
    dataCell = worksheet.find(editor.endDataStr)

    # enter token cell
    if dateCell.col == 1 and tokenCell.col == 2 and dataCell.col ==3:
      print('datecell, tokenCell, dataCell is correctly oriented')
      worksheet.update_cell(dataCell.row, dataCell.col, f"uninferenced_{token}")
      worksheet.update_cell(tokenCell.row, tokenCell.col, f"{token}")
      worksheet.update_cell(dateCell.row, dateCell.col, f"{cell_session_time}")


    # enter new token and push cells to one cell bottom.
    worksheet.update_cell(dateCell.row + 1, dateCell.col, editor.endDateStr)
    worksheet.update_cell(tokenCell.row +1, tokenCell.col, editor.endTokenStr)
    worksheet.update_cell(dataCell.row + 1, dataCell.col, editor.endDataStr)

    

  
  def colab_edit(infOut, token):
    '''for google colab
      stage two - google colab needs to inference pictures and upload data on spreadsheet
      outline
        1. match token from title 
        2. put inferenced data into the spreadsheet'''
    worksheet = bucket.worksheet
    uninferencedCell = worksheet.find(f"uninferenced_{token}")
    print(f"Found uninferenced data at R{uninferencedCell.row}C{uninferencedCell.col}")
    worksheet.update_cell(uninferencedCell.row, uninferencedCell.col, f"{infOut}")
    print('progress done')

  def accessor(token):
    '''stage three - main brain needs to have access to the inferenced data
    returns string output value '''
    worksheet = bucket.worksheet
    processedTokenCell = worksheet.find(f"{token}")
    processedDataCell = worksheet.cell(processedTokenCell.row, processedTokenCell.col + 1)
    outputValue = processedDataCell.value
    print(f'token number:{token}')
    print(f'output value is {outputValue}')
    return outputValue
    
    

# example token 016b59179
# example inferenced value is "{'error': 'invalid_grant', 'error_description': 'Invalid JWT Signature.'}"


initializer.__init__('/Users/changbeankang/Claw_For_Humanity/HOS_II/Plugins/', 'cfh-hawkeye-c23853ec0580', '1OlbAmA_yr76eaoT217e3nyAdT9X7ZkBh')
time.sleep(3)
editor.mainInitiator("016b59179")
time.sleep(3)
editor.colab_edit("{'error': 'invalid_grant', 'error_description': 'Invalid JWT Signature.'}", "016b59179")
time.sleep(3)
editor.accessor("016b59179")