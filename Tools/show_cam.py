"""
Show multiple the cameras and store frames
JCA
"""
import os
from datetime import datetime  
import argparse

import numpy as np
import cv2 as cv

# Number of cameras to display
CAM_NUM = 3
SCALE = 0.5
SAVE_PATH = 'Captures'

parser = argparse.ArgumentParser(
                    prog = 'Camera Show',
                    description = 'Show videos from multiple cameras',
                    epilog = 'Press Q to end recording. Press S to save frames')

parser.add_argument('cam', help='Number of cameras', type=int, default=1)
parser.add_argument('-s', '--scale', help='Scale frames to show', default=SCALE, type=float)


def show_cap(cap, window, scale=1, rect=True, color=(0, 0, 255)):
    """Show video capture in window"""
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        return
    frame = cv.resize(frame, (0, 0), fx=scale, fy=scale)
    # draw square centered on frame
    if rect:
        h, w = frame.shape[:-1]
        # represents the top left corner of rectangle
        halfsize= 10
        start_point = (w//2-halfsize, h//2-halfsize)
        # represents the bottom right corner of rectangle
        end_point = (w//2+halfsize, h//2+halfsize)
        
        thickness = 1
        cv.rectangle(frame, start_point, end_point, color, thickness)

    cv.imshow(window, frame)


def save_im(cap, idx, savepath):
    """Save frame capture"""
    ret, frame = cap.read()
    if ret:
        now = datetime.now()
        timestamp = now.strftime("%d-%b-%Y-%H|%M|%S") + f'_{idx}'
        filepath = os.path.join(savepath, f'{timestamp}.png')
        cv.imwrite(filepath, frame)
        print(f'Saved image from camera {idx}')
    else:
        print("Could't save frame!º")


def main(cam_num, scale):

    print(f'Creating directory: {SAVE_PATH}')
    os.makedirs(SAVE_PATH, exist_ok=True)

    print('Loading cameras...')
    caps = [cv.VideoCapture(i) for i in range(cam_num) if cv.VideoCapture(i).isOpened]
    
    print('Starting')
    while True:
        i=0
        for cap in caps:
            show_cap(cap, f'cam-{i}', scale=scale)
            i+=1

        key = cv.waitKey(1)
        if key == ord('q'):
            break
        if key == ord('s'):
            print('Saving photos')
            i=0
            for cap in caps:
                save_im(cap, i, SAVE_PATH)
                i+=1
            # cv.imwrite('foto.jpg', frame)
    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    args = parser.parse_args()
    main(args.cam, args.scale)


