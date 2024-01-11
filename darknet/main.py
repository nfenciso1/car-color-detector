import pygame, sys, cv2, numpy, tkinter, tkinter.filedialog
from button import Button
from vc_mask_img import process_img         # --------- darknet ------------
from vc_mask_img import process_darknet         # --------- darknet ------------
import numpy as np
import pygame_gui

pygame.init()

# Initialize the program's window
WINDOW = pygame.display.set_mode((1280, 750))
pygame.display.set_caption("Car Color Detector")

# Initialize the background images
BG = pygame.image.load("../assets/background.png")
BG2 = pygame.image.load("../assets/background2.jpg")

# Function for getting the font and adjusting font size
def get_font(size): 
    return pygame.font.Font("../assets/font.ttf", size)

# Function for opening a file manager window
def prompt_file():
    top = tkinter.Tk()
    top.withdraw()
    FILE_NAME = tkinter.filedialog.askopenfilename(initialdir="./assets/videos", parent = top)
    top.destroy()

    if FILE_NAME[-3:] == "mp4":
        return FILE_NAME, "video"
    else:
        return FILE_NAME, "image"

def process_inputs(black_inputs, white_inputs, gray_inputs):
    # defaults
    lower_black = np.array([0, 0, 0]) 
    upper_black = np.array([180, 255, 110]) 
    percent_black = 45
    lower_white = np.array([0,0,190])
    upper_white = np.array([180,50,255])
    percent_white = 30
    lower_gray = np.array([0,25,0])
    upper_gray = np.array([180,70,255])
    percent_gray = 40

    black = [lower_black, upper_black, percent_black]
    white = [lower_white, upper_white, percent_white]
    gray = [lower_gray, upper_gray, percent_gray]
    thres_values = [black, white, gray]
    input_values = [black_inputs, white_inputs, gray_inputs]


    for i in range(0,3):
        if not (input_values[i][0] == ""):
            val = input_values[i][0].split(" ")
            lower_thres = np.array([int(val[0]), int(val[1]), int(val[2])])
            thres_values[i][0] = lower_thres

        if not (input_values[i][1] == ""):
            val = input_values[i][1].split(" ")
            upper_thres = np.array([int(val[0]), int(val[1]), int(val[2])])
            thres_values[i][1] = upper_thres

        if not (input_values[i][2] == ""):
            thres_values[i][2] = int(input_values[i][2])

    return thres_values
        

# Function to start the program
def start():
    # --- for input text ---
    manager = pygame_gui.UIManager((1280, 750))
    ub = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((920, 240), (110, 30)), manager=manager,
                                                object_id='#upper-b')
    lb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((1062, 240), (110, 30)), manager=manager,
                                                object_id='#lower-b')
    pb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((1204, 240), (40, 30)), manager=manager,
                                                object_id='#percent-b')
    uw = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((920, 300), (110, 30)), manager=manager,
                                                object_id='#upper-w')
    lw = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((1062, 300), (110, 30)), manager=manager,
                                                object_id='#lower-w')
    pw = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((1204, 300), (40, 30)), manager=manager,
                                                object_id='#percent-w')
    ug = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((920, 360), (110, 30)), manager=manager,
                                                object_id='#upper-g')
    lg = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((1062, 360), (110, 30)), manager=manager,
                                                object_id='#lower-g')
    pg = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((1204, 360), (40, 30)), manager=manager,
                                                object_id='#percent-g')
    


    clock = pygame.time.Clock()
    UI_REFRESH_RATE = clock.tick(60)/1000
    while True:
        pygame.event.get()

        # Set background image
        WINDOW.blit(BG2, (0, 0))
        # Get mouse position
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        # Draw a rectangle
        # Second argument = color's RGB value
        # Third argument = (x-axis, y-axis, width, height)
        pygame.draw.rect(WINDOW, (0,0,0), (100,100,800,550))

        BLACK_TEXT = get_font(10).render("black threshold:",True, "White")
        BLACK_REC = BLACK_TEXT.get_rect(center=(1000, 230))
        WHITE_TEXT = get_font(10).render("white threshold:",True, "White")
        WHITE_REC = BLACK_TEXT.get_rect(center=(1000, 290))
        GRAY_TEXT = get_font(10).render("gray threshold:",True, "White")
        GRAY_REC = BLACK_TEXT.get_rect(center=(1000, 350))
        WINDOW.blit(BLACK_TEXT, BLACK_REC)
        WINDOW.blit(WHITE_TEXT, WHITE_REC)
        WINDOW.blit(GRAY_TEXT, GRAY_REC)


        # Setup buttons
        PLAY_VID_BUTTON = Button(BG_IMAGE=pygame.image.load("../assets/options.png"), POSITION=(500, 300), 
                            BUTTON_TEXT="OPEN MEDIA FILE", FONT=get_font(25), BASE_COLOR="#ffaa1f", HOVER_COLOR="#ff561e")
        OPEN_CAM_BUTTON = Button(BG_IMAGE=pygame.image.load("../assets/options.png"), POSITION=(500, 450), 
                            BUTTON_TEXT="OPEN THE WEBCAM", FONT=get_font(25), BASE_COLOR="#ffaa1f", HOVER_COLOR="#ff561e")
        for BUTTON in [PLAY_VID_BUTTON, OPEN_CAM_BUTTON]:
            BUTTON.changeColor(PLAY_MOUSE_POS)
            BUTTON.update(WINDOW)

        # Add event handlers
        for EVENT in pygame.event.get():
            if EVENT.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if EVENT.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_VID_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    black_inputs = [ub.get_text(), lb.get_text(), pb.get_text()]
                    white_inputs = [uw.get_text(), lw.get_text(), pw.get_text()]
                    gray_inputs = [ug.get_text(), lg.get_text(), pg.get_text()]
                    thres_values = process_inputs(black_inputs, white_inputs, gray_inputs)

                    play_video(thres_values)
                if OPEN_CAM_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    black_inputs = [ub.get_text(), lb.get_text(), pb.get_text()]
                    white_inputs = [uw.get_text(), lw.get_text(), pw.get_text()]
                    gray_inputs = [ug.get_text(), lg.get_text(), pg.get_text()]
                    thres_values = process_inputs(black_inputs, white_inputs, gray_inputs)

                    open_webcam(thres_values)

            manager.process_events(EVENT)

        manager.update(UI_REFRESH_RATE)

        manager.draw_ui(WINDOW)

        # Update the window
        pygame.display.update()

PREV_FRAME = np.ones((550, 800, 3), dtype=np.uint8) * 255
PREV_COLORS = []
network = 0
class_names = 0
width = 0
height = 0


# Function for playing a video file
def play_video(thres_values):
    global PREV_FRAME, PREV_COLORS
    global network, class_names, width, height

    # Get the video file name
    FILE_NAME, type = prompt_file()

    if type == "video":
        # Open cam for video capturing
        VIDEO = cv2.VideoCapture(FILE_NAME)
        FPS = VIDEO.get(cv2.CAP_PROP_FPS)
    else:
        FRAME = cv2.imread(FILE_NAME)
        FPS = 30.0
    
    CLOCK = pygame.time.Clock()

    # Setup the car color counters
    BLACK_COUNT = 0
    WHITE_COUNT = 0
    GRAY_COUNT = 0
    OTHERS_COUNT = 0
    BLUE_COUNT = 0
    RED_COUNT = 0

    

    while True:
        pygame.event.get()
        # Get mouse position
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        # Limit the FPS in the application loop
        CLOCK.tick(FPS)
        
        # Draw a rectangle
        # Second argument = color's RGB value
        # Third argument = (x-axis, y-axis, width, height)
        pygame.draw.rect(WINDOW, (0,0,0), (240,100,800,610))
        vehicles_color = []

        # Setup back button
        BACK_BUTTON = Button(BG_IMAGE=pygame.image.load("../assets/back_button_bg.png"), POSITION=(150, 90), 
                            BUTTON_TEXT="BACK", FONT=get_font(25), BASE_COLOR="#ffaa1f", HOVER_COLOR="#ff561e")
        BACK_BUTTON.changeColor(PLAY_MOUSE_POS)
        BACK_BUTTON.update(WINDOW)

        if type == "video":
            # Handle video frames
            SUCCESS, VIDEO_FRAME = VIDEO.read()
        else:
            VIDEO_FRAME = FRAME
            SUCCESS = True

        if SUCCESS:
            # Resize the frame
            VIDEO_FRAME = cv2.resize(VIDEO_FRAME, (800, 550))
            # Convert frame to pygame's Surface object

            outp, vehicles_color = process_img(VIDEO_FRAME, network, class_names, width, height, thres_values)  # --------- darknet ------------
            
            if isinstance(outp, str):
                outp = PREV_FRAME
                vehicles_color = PREV_COLORS
            else:
                PREV_FRAME = outp
                PREV_COLORS = vehicles_color

            VIDEO_SURF = pygame.image.frombuffer(outp.tobytes(), outp.shape[1::-1], "BGR")
            # VIDEO_SURF = pygame.image.frombuffer(VIDEO_FRAME.tobytes(), VIDEO_FRAME.shape[1::-1], "BGR")
            
            # Add event handler
            for EVENT in pygame.event.get():
                if EVENT.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if EVENT.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_BUTTON.checkForInput(PLAY_MOUSE_POS):
                        start()

            BLACK_COUNT = vehicles_color.count("Black")
            WHITE_COUNT = vehicles_color.count("White")
            GRAY_COUNT = vehicles_color.count("Gray")
            OTHERS_COUNT = vehicles_color.count("Other")
            BLUE_COUNT = vehicles_color.count("Blue")
            RED_COUNT = vehicles_color.count("Red")

            # Setup the car color counters' texts
            BLACK_TEXT = get_font(20).render("BLACK: " + str(BLACK_COUNT), True, "White")
            BLACK_REC = BLACK_TEXT.get_rect(center=(340, 625))
            
            WHITE_TEXT = get_font(20).render("WHITE: " + str(WHITE_COUNT), True, "White")
            WHITE_REC = WHITE_TEXT.get_rect(center=(340, 675))

            GRAY_TEXT = get_font(20).render("GRAY: " + str(GRAY_COUNT), True, "White")
            GRAY_REC = GRAY_TEXT.get_rect(center=(640, 625))
            
            OTHERS_TEXT = get_font(20).render("OTHERS: " + str(OTHERS_COUNT), True, "White")
            OTHERS_REC = OTHERS_TEXT.get_rect(center=(640, 675))

            RED_TEXT = get_font(20).render("RED: " + str(RED_COUNT), True, "White")
            RED_REC = RED_TEXT.get_rect(center=(940, 625))

            BLUE_TEXT = get_font(20).render("BLUE: " + str(BLUE_COUNT), True, "White")
            BLUE_REC = BLUE_TEXT.get_rect(center=(940, 675))

            # Render the car color counters to window
            WINDOW.blit(BLACK_TEXT, BLACK_REC)
            WINDOW.blit(WHITE_TEXT, WHITE_REC)
            WINDOW.blit(GRAY_TEXT, GRAY_REC)
            WINDOW.blit(BLUE_TEXT, BLUE_REC)
            WINDOW.blit(RED_TEXT, RED_REC)
            WINDOW.blit(OTHERS_TEXT, OTHERS_REC)

            # Render frame in the window
            WINDOW.blit(VIDEO_SURF, (240, 40))
            # Update the window
            pygame.display.update()

        else:
            # When vid is finished, go back to start()
            start()
        
# Function for opening the webcam
def open_webcam(thres_values):
    global PREV_FRAME, PREV_COLORS
    global network, class_names, width, height

    # Create an empty surface
    empty_surface = pygame.Surface((100, 100))  # Replace (100, 100) with your desired dimensions
    empty_surface.fill((255, 255, 255))
    PREV_FRAME = empty_surface


    # Open the webcam
    WEBCAM = cv2.VideoCapture(0)
    FPS = WEBCAM.get(cv2.CAP_PROP_FPS)
    CLOCK = pygame.time.Clock()

    # Setup the car color counters
    BLACK_COUNT = 0
    WHITE_COUNT = 0
    GRAY_COUNT = 0
    OTHERS_COUNT = 0
    BLUE_COUNT = 0
    RED_COUNT = 0

    while True:
        pygame.event.get()
        # Get mouse position
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        # Limit the FPS in the application loop
        CLOCK.tick(FPS)

        # Draw a rectangle
        # Second argument = color's RGB value
        # Third argument = (x-axis, y-axis, width, height)
        pygame.draw.rect(WINDOW, (0,0,0), (240,100,800,610))

        # Setup back button
        BACK_BUTTON = Button(BG_IMAGE=pygame.image.load("../assets/back_button_bg.png"), POSITION=(150, 90), 
                            BUTTON_TEXT="BACK", FONT=get_font(25), BASE_COLOR="#ffaa1f", HOVER_COLOR="#ff561e")
        BACK_BUTTON.changeColor(PLAY_MOUSE_POS)
        BACK_BUTTON.update(WINDOW)


        # Handle video frames
        SUCCESS, VIDEO_FRAME = WEBCAM.read()

        outp, vehicles_color = process_img(VIDEO_FRAME, network, class_names, width, height, thres_values)    # --------- darknet ------------
        if isinstance(outp, str):
            outp = PREV_FRAME
            vehicles_color = PREV_COLORS
        else:
            PREV_FRAME = outp
            PREV_COLORS = vehicles_color

        # Resize the frame
        VIDEO_FRAME = cv2.resize(outp, (800, 550))
        # Convert from BGR to RGB format
        FRAME_IN_RGB = cv2.cvtColor(VIDEO_FRAME, cv2.COLOR_BGR2RGB)
        # Rotate the frame
        ROTATE_FRAME = numpy.rot90(FRAME_IN_RGB)
        # Convert frame to pygame's Surface object
        FRAME_TO_SURFACE_OBJECT = pygame.surfarray.make_surface(ROTATE_FRAME).convert()
        
        BLACK_COUNT = vehicles_color.count("Black")
        WHITE_COUNT = vehicles_color.count("White")
        GRAY_COUNT = vehicles_color.count("Gray")
        OTHERS_COUNT = vehicles_color.count("Other")
        BLUE_COUNT = vehicles_color.count("Blue")
        RED_COUNT = vehicles_color.count("Red")
        # Setup the car color counters' texts
        BLACK_TEXT = get_font(20).render("BLACK: " + str(BLACK_COUNT), True, "White")
        BLACK_REC = BLACK_TEXT.get_rect(center=(340, 625))
        
        WHITE_TEXT = get_font(20).render("WHITE: " + str(WHITE_COUNT), True, "White")
        WHITE_REC = WHITE_TEXT.get_rect(center=(340, 675))

        GRAY_TEXT = get_font(20).render("GRAY: " + str(GRAY_COUNT), True, "White")
        GRAY_REC = GRAY_TEXT.get_rect(center=(640, 625))
        
        OTHERS_TEXT = get_font(20).render("OTHERS: " + str(OTHERS_COUNT), True, "White")
        OTHERS_REC = OTHERS_TEXT.get_rect(center=(640, 675))

        RED_TEXT = get_font(20).render("RED: " + str(RED_COUNT), True, "White")
        RED_REC = RED_TEXT.get_rect(center=(940, 625))

        BLUE_TEXT = get_font(20).render("BLUE: " + str(BLUE_COUNT), True, "White")
        BLUE_REC = BLUE_TEXT.get_rect(center=(940, 675))

        # Render the car color counters to window
        WINDOW.blit(BLACK_TEXT, BLACK_REC)
        WINDOW.blit(WHITE_TEXT, WHITE_REC)
        WINDOW.blit(GRAY_TEXT, GRAY_REC)
        WINDOW.blit(BLUE_TEXT, BLUE_REC)
        WINDOW.blit(RED_TEXT, RED_REC)
        WINDOW.blit(OTHERS_TEXT, OTHERS_REC)

        # Render frame in the window
        WINDOW.blit(FRAME_TO_SURFACE_OBJECT, (240, 40))
        # Update the window
        pygame.display.update()

        # Add event handler
        for EVENT in pygame.event.get():
            if EVENT.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if EVENT.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    start()

def main_menu():
    global network, class_names, width, height

    network, class_names, width, height = process_darknet()         # --------- darknet ------------
    while True:
        # Set background image
        WINDOW.blit(BG, (0, 0))
        # Get mouse position
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Setup program's title texts
        UPPER_TEXT = get_font(80).render("CAR COLOR", True, "White")
        UPPER_RECT = UPPER_TEXT.get_rect(center=(640, 135))

        LOWER_TEXT = get_font(80).render("DETECTOR", True, "White")
        LOWER_RECT = LOWER_TEXT.get_rect(center=(640, 275))

        # Setup buttons
        START_BUTTON = Button(BG_IMAGE=pygame.image.load("../assets/options.png"), POSITION=(640, 450), 
                            BUTTON_TEXT="START", FONT=get_font(75), BASE_COLOR="#ffaa1f", HOVER_COLOR="#ff561e")
        QUIT_BUTTON = Button(BG_IMAGE=pygame.image.load("../assets/options.png"), POSITION=(640, 600), 
                            BUTTON_TEXT="QUIT", FONT=get_font(75), BASE_COLOR="#ffaa1f", HOVER_COLOR="#ff561e")
        for BUTTON in [START_BUTTON, QUIT_BUTTON]:
            BUTTON.changeColor(MENU_MOUSE_POS)
            BUTTON.update(WINDOW)

        # Render title texts to window
        WINDOW.blit(UPPER_TEXT, UPPER_RECT)
        WINDOW.blit(LOWER_TEXT, LOWER_RECT)
        
        # Add event handlers
        for EVENT in pygame.event.get():
            if EVENT.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if EVENT.type == pygame.MOUSEBUTTONDOWN:
                if START_BUTTON.checkForInput(MENU_MOUSE_POS):
                    start()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        # Update the window
        pygame.display.update()

main_menu()