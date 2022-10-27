"""
Script for show multiple the image from multiple cameras
Using OpenCV

JCA
"""
import numpy as np
import cv2 as cv

# Number of cameras to display
CAM_NUM = 3
SCALE = 0.5
SAVE_PATH = 'Captures'


def show_cap(cap, window, scale=1, rect=True, color=(0, 0, 255)):
    """Show video capture in window"""
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv.resize(frame, (0, 0), fx=scale, fy=scale)

    # draw square centered on frame
    if rect:
        h, w = frame.shape[:-1]
        # represents the top left corner of rectangle
        halfsize= 10
        start_point = (w//2-halfsize, h//2-halfsize)
        # represents the bottom right corner of rectangle
        end_point = (w//2+halfsize, h//2+halfsize)
        
        # Line thickness of 2 px
        thickness = 1
        
        # Using cv2.rectangle() method
        # Draw a rectangle with blue line borders of thickness of 2 px
        image = cv.rectangle(frame, start_point, end_point, color, thickness)

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        return
    # Our operations on the frame come here
    # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv.imshow(window, frame)

def save_im(caps):
    """Save frame capture"""



def main():
    print('Loading cameras...')
    caps = [cv.VideoCapture(i) for i in range(CAM_NUM) if cv.VideoCapture(i).isOpened]
    
    print('Starting')
    while True:
        i=0
        for cap in caps:
            show_cap(cap, f'cam-{i}', scale=SCALE)
            i+=1

        key = cv.waitKey(1)
        if key == ord('q'):
            break
        if key == ord('a'):
            print('Saving photos')
            # cv.imwrite('foto.jpg', frame)
    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()