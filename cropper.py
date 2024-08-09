import numpy as np

def converter(input_list):
    '''converts (x,y,x+w,y+h) into (x,y,w,h)'''
    output_list = []
    for (x1, y1, x2, y2) in input_list:
        width = x2 - x1
        height = y2 - y1
        output_list.append((x1, y1, width, height))
    return output_list

def crop(image_size, fastSam, path_to_image):
    '''input image size should be (height,width)'''
    # input image size 
    image_height = image_size[0]  
    image_width = image_size[1]  
    

    # crop height is instance segmentation expected input (512x1024)
    crop_width = 1024  
    crop_height = 512  

    bounding_boxes = []

    for i in range(len(fastSam)):
        bounding_boxes.append(fastSam[i]['plot'])
    
    bounding_boxes = converter(bounding_boxes)

    # List of bounding boxes in the format (x, y, w, h)
    # bounding_boxes = [
    #     (500, 300, 100, 200),  # Example bounding box 1
    #     (1000, 1000, 300, 300),  # Example bounding box 2
    #     (2000, 1500, 400, 400),  # Example bounding box 3
    #     # Add more bounding boxes as needed
    # ]

    def count_boxes_in_crop(crop_x, crop_y, crop_width, crop_height, bounding_boxes):
        count = 0
        for (x, y, w, h) in bounding_boxes:
            if (x + w > crop_x and x < crop_x + crop_width and
                    y + h > crop_y and y < crop_y + crop_height):
                count += 1
        return count

    # Initialize variables to keep track of the best crop
    best_crop_x = 0
    best_crop_y = 0
    max_boxes_in_crop = 0

    # Sliding window approach to find the best crop position
    for crop_x in range(0, image_width - crop_width + 1, 10):  # Step by 10 pixels to reduce computation
        for crop_y in range(0, image_height - crop_height + 1, 10):
            boxes_in_crop = count_boxes_in_crop(crop_x, crop_y, crop_width, crop_height, bounding_boxes)
            if boxes_in_crop > max_boxes_in_crop:
                max_boxes_in_crop = boxes_in_crop
                best_crop_x = crop_x
                best_crop_y = crop_y

    print(f"Best crop position: (x: {best_crop_x}, y: {best_crop_y}) with {max_boxes_in_crop} boxes inside.")

    # Optional: You can now crop the image using the best crop position
    # For example, using OpenCV (cv2) to perform the cropping
    import cv2

    # Load the 4K image
    image = cv2.imread(path_to_image)

    # Crop the image
    cropped_image = image[best_crop_y:best_crop_y + crop_height, best_crop_x:best_crop_x + crop_width]

    # Save or display the cropped image
    cv2.imwrite('./output/cropped_image.jpg', cropped_image)

img_path = '/Users/changbeankang/Claw_For_Humanity/HOS_II/Google-Circularnet-Integration/output/output.jpg'
imgsize = (1080,1920)
fastSam = [{'fingerprint': '5q2as5xm', 'plot': (1590, 203, 1693, 263)}, {'fingerprint': 'alpzazrl', 'plot': (0, 352, 250, 665)}, {'fingerprint': 'xouxjdhv', 'plot': (0, 894, 193, 1080)}, {'fingerprint': 'lqarsks4', 'plot': (483, 832, 550, 888)}, {'fingerprint': '1r7t9whn', 'plot': (693, 409, 742, 443)}, {'fingerprint': 'nda5mk9b', 'plot': (1444, 172, 1919, 666)}]

crop(imgsize,fastSam,img_path)