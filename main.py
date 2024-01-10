import pygame, sys, cv2, numpy, tkinter, tkinter.filedialog
from button import Button

pygame.init()

# Initialize the program's window
WINDOW = pygame.display.set_mode((1280, 750))
pygame.display.set_caption("Car Color Detector")

# Initialize the background images
BG = pygame.image.load("assets/background.png")
BG2 = pygame.image.load("assets/background2.jpg")

# Function for getting the font and adjusting font size
def get_font(size): 
    return pygame.font.Font("assets/font.ttf", size)

# Function for opening a file manager window
def prompt_file():
    FILE_NAME = tkinter.filedialog.askopenfilename(initialdir="./assets/videos")
    return FILE_NAME

# Function to start the program
def start():
    while True:
        pygame.event.get()

        # Set background image
        WINDOW.blit(BG2, (0, 0))
        # Get mouse position
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        # Draw a rectangle
        # Second argument = color's RGB value
        # Third argument = (x-axis, y-axis, width, height)
        pygame.draw.rect(WINDOW, (0,0,0), (240,100,800,550))

        # Setup buttons
        PLAY_VID_BUTTON = Button(BG_IMAGE=pygame.image.load("assets/options.png"), POSITION=(645, 300), 
                            BUTTON_TEXT="PLAY A VIDEO", FONT=get_font(25), BASE_COLOR="#ffaa1f", HOVER_COLOR="#ff561e")
        OPEN_CAM_BUTTON = Button(BG_IMAGE=pygame.image.load("assets/options.png"), POSITION=(645, 450), 
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
                    play_video()
                if OPEN_CAM_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    open_webcam()

        # Update the window
        pygame.display.update()

# Function for playing a video file
def play_video():
    # Get the video file name
    FILE_NAME = prompt_file()

    # Open cam for video capturing
    VIDEO = cv2.VideoCapture(FILE_NAME)
    FPS = VIDEO.get(cv2.CAP_PROP_FPS)
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
        # Limit the FPS in the application loop
        CLOCK.tick(FPS)
        
        # Draw a rectangle
        # Second argument = color's RGB value
        # Third argument = (x-axis, y-axis, width, height)
        pygame.draw.rect(WINDOW, (0,0,0), (240,100,800,610))

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

        # Handle video frames
        SUCCESS, VIDEO_FRAME = VIDEO.read()
        if SUCCESS:
            # Resize the frame
            VIDEO_FRAME = cv2.resize(VIDEO_FRAME, (800, 550))
            # Convert frame to pygame's Surface object
            VIDEO_SURF = pygame.image.frombuffer(VIDEO_FRAME.tobytes(), VIDEO_FRAME.shape[1::-1], "BGR")
            # Render frame in the window
            WINDOW.blit(VIDEO_SURF, (240, 40))
            # Update the window
            pygame.display.update()

            # Add event handler
            for EVENT in pygame.event.get():
                if EVENT.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        else:
            # When vid is finished, go back to start()
            start()

# Function for opening the webcam
def open_webcam():

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
        # Limit the FPS in the application loop
        CLOCK.tick(FPS)

        # Draw a rectangle
        # Second argument = color's RGB value
        # Third argument = (x-axis, y-axis, width, height)
        pygame.draw.rect(WINDOW, (0,0,0), (240,100,800,610))

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

        # Handle video frames
        SUCCESS, VIDEO_FRAME = WEBCAM.read()
        # Resize the frame
        VIDEO_FRAME = cv2.resize(VIDEO_FRAME, (800, 550))
        # Convert from BGR to RGB format
        FRAME_IN_RGB = cv2.cvtColor(VIDEO_FRAME, cv2.COLOR_BGR2RGB)
        # Rotate the frame
        ROTATE_FRAME = numpy.rot90(FRAME_IN_RGB)
        # Convert frame to pygame's Surface object
        FRAME_TO_SURFACE_OBJECT = pygame.surfarray.make_surface(ROTATE_FRAME).convert()
        # Render frame in the window
        WINDOW.blit(FRAME_TO_SURFACE_OBJECT, (240, 40))
        # Update the window
        pygame.display.update()

        # Add event handler
        for EVENT in pygame.event.get():
            if EVENT.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def main_menu():
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
        START_BUTTON = Button(BG_IMAGE=pygame.image.load("assets/options.png"), POSITION=(640, 450), 
                            BUTTON_TEXT="START", FONT=get_font(75), BASE_COLOR="#ffaa1f", HOVER_COLOR="#ff561e")
        QUIT_BUTTON = Button(BG_IMAGE=pygame.image.load("assets/options.png"), POSITION=(640, 600), 
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