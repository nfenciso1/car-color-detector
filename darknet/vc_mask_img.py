import darknet
import cv2
import numpy as np
from scipy import ndimage
from sklearn.metrics import mean_squared_error
import webcolors

# Adapted from Sir Val's
# test_darknet_on_video_stream_opencv.py

#open a video capture object --> webcam in your laptop start at "0" ... Laptop builtin cam is 0 by default
vid = cv2.VideoCapture(0)
vid_width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
vid_height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
vid_fps = vid.get(cv2.CAP_PROP_FPS)

print("Video size = ", vid_width, " x ", vid_height, " ")
print("Video FPS = ", vid_fps, " ")
vid.release() #close the stream, will open again when reading

def find_closest_color(color):
    hex = "#{:02x}{:02x}{:02x}".format(color[0],color[1],color[2])

    try:
        nm = webcolors.hex_to_name(hex, spec='css3')
    except ValueError as v_error:
        print("{}".format(v_error))
        rms_lst = []
        for img_clr, img_hex in webcolors.CSS3_NAMES_TO_HEX.items():
            cur_clr = webcolors.hex_to_rgb(img_hex)
            rmse = np.sqrt(mean_squared_error(color, cur_clr))
            rms_lst.append(rmse)

        closest_color = rms_lst.index(min(rms_lst))

        nm = list(webcolors.CSS3_NAMES_TO_HEX.items())[closest_color][0]
    return nm

# darknet helper function to run detection on image


def darknet_helper(img, width, height, network, class_names):
    darknet_image = darknet.make_image(width, height, 3)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(img_rgb, (width, height),
                             interpolation=cv2.INTER_LINEAR)
    # get image ratios to convert bounding boxes to proper size
    img_height, img_width, _ = img.shape
    width_ratio = img_width / width
    height_ratio = img_height / height
    #    run model on darknet style image to get detections
    darknet.copy_image_from_bytes(darknet_image, img_resized.tobytes())
    detections = darknet.detect_image(network, class_names, darknet_image)
    darknet.free_image(darknet_image)
    return detections, width_ratio, height_ratio

lower_black = np.array([0, 0, 0]) 
upper_black = np.array([180, 255, 110]) 

lower_white = np.array([0,0,190])
upper_white = np.array([180,50,255])

lower_gray = np.array([0,25,0])
upper_gray = np.array([180,70,255])

def process_darknet():
    network, class_names, class_colors = darknet.load_network("cfg\\yolov4.cfg", "cfg\\coco.data","yolov4.weights")
    width = darknet.network_width(network)
    height = darknet.network_height(network)

    return network, class_names, width, height

def process_img(frame, network, class_names, width, height, thres_values):
    lower_black = thres_values[0][0]
    upper_black = thres_values[0][1]
    percent_black = thres_values[0][2]

    lower_white = thres_values[1][0]
    upper_white = thres_values[1][1]
    percent_white = thres_values[1][2]

    lower_gray = thres_values[2][0]
    upper_gray = thres_values[2][1]
    percent_gray = thres_values[2][2]

    try:
        img = frame
        vehicles = []
        vehicles_color = []

        detections, width_ratio, height_ratio = darknet_helper(img, width, height, network, class_names)

        #mask = cv2.inRange(img, Lower_hsv, Upper_hsv) 
        #cv2.imshow("mask", mask)
        
        for label, confidence, bbox in detections:
            if float(confidence) > 50 and label in ["car"]:
                left, top, right, bottom = darknet.bbox2points(bbox)
                left, top, right, bottom = int(left * width_ratio), int(top * height_ratio), int(right * width_ratio), int(
                    bottom * height_ratio)

                vehicles.append(img[int(top):int(bottom), int(left):int(right)])

        #print(len(vehicles))
        for i in range(len(vehicles)):
            #print()
            hsv_img = cv2.cvtColor(vehicles[i], cv2.COLOR_BGR2HSV)


            mask = cv2.inRange(hsv_img, lower_black, upper_black)

            white = np.sum(mask == 255)
            total = np.sum(mask >- 1)

            if white/total*100 >= percent_black:
                color = "Black"
            else:
                mask2 = cv2.inRange(hsv_img, lower_white, upper_white)
                white2 = np.sum(mask2 == 255)

                if white2/total*100 >= percent_white:
                    color = "White"
                else:
                    mask3 = cv2.inRange(hsv_img, lower_gray, upper_gray)
                    white3 = np.sum(mask3 == 255)

                    if white3/total*100 >= percent_gray:
                        color = "Gray"
                    else:
                        color = "Other"
            vehicles_color.append(color)

            #print(i, white, total, (white/total)*100)

        counter0 = 0
        for label, confidence, bbox in detections:
            if float(confidence) > 50 and label in ["car"]:
                left, top, right, bottom = darknet.bbox2points(bbox)
                left, top, right, bottom = int(left * width_ratio), int(top * height_ratio), int(right * width_ratio), int(
                    bottom * height_ratio)

                cv2.rectangle(img, (left,top), (right, bottom), (0,0,0), 2)
                cv2.putText(img, "{} {} - {}".format(counter0,label[0], vehicles_color[counter0]), # vehicles_color[counter0]
                        (left, top - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0,0,0), 2)
                # class_colors[label]
                counter0+=1
        return img, vehicles_color
    
    except:
        return "error", "Problem occurred for current frame"

if __name__ == "__main__":
    #inside the darknet folder is the cfg folder which contains the basic yolov4.cfg and coco.data--> you must download the yolov4.weights from the github separately
    #and place it inside darknet folder for this code snippet to work
    
    network, class_names, class_colors = darknet.load_network("cfg\\yolov4.cfg", "cfg\\coco.data","yolov4.weights")
    width = darknet.network_width(network)
    height = darknet.network_height(network)

    vid = cv2.VideoCapture("inputs\\cars_motorcycles.mp4") 

    while (True):
        ret, frame = vid.read() #get a frame

        try:   
            #img = cv2.imread("vehicles4.jpg")
            img = process_img(frame)
                    
            cv2.imshow("YOLO Output", img)
            #cv2.waitKey(0)
            if cv2.waitKey(5) == ord('q'):
                break
        except:
            print("Problem occurred for current frame")
            pass
    vid.release()
    cv2.destroyAllWindows()