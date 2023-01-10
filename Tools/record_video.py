"""
Record video from camera

JCA
"""
import os
import argparse
import time

import cv2 as cv


SCALE = 0.3
SAVEPATH = 'Recordings'
FPS = 15

parser = argparse.ArgumentParser(
                    prog = 'Video Record',
                    description = 'Record video from camera',
                    epilog = 'Press C to end recording')

parser.add_argument('filename', help='Name of the file to store video')
parser.add_argument('cam', help='Camera ID number', type=int)
parser.add_argument('-f', '--fps', help='Frames per second of video record', default=FPS)


def main(filename, cam_id, fps):
    print(f'Creating directory: {SAVEPATH}')
    os.makedirs(SAVEPATH, exist_ok=True)
    savepath = os.path.join(SAVEPATH, filename+'.avi')

    cam_id = int(cam_id)
    print(f'Recording video on {savepath} of camera {cam_id}')

    cap = cv.VideoCapture(cam_id)
    # Get frame size to create recorder
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    out = cv.VideoWriter(savepath, cv.VideoWriter_fourcc('M','J','P','G'), fps, (frame_width,frame_height))

    # Check if camera opened successfully
    if (cap.isOpened()== False): 
        print("Error opening video stream or file")
        exit()
    prev_frame_time = 0
    new_frame_time = 0
    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            out.write(frame)

            new_frame_time = time.time()
            real_fps = str(int(1/(new_frame_time-prev_frame_time)))
            prev_frame_time = new_frame_time

            # Scale frame to display
            frame = cv.resize(frame, (0,0), fx=SCALE, fy=SCALE)
            cv.putText(frame, f'FPS: {real_fps}', (7, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (100, 255, 0), 1, cv.LINE_AA)
            cv.imshow('Frame', frame)

            if cv.waitKey(1) & 0xFF == ord('c'):
                break
        
        # Break the loop
        else: 
            break
    
    # When everything done, release the video capture object
    cap.release()
    
    # Closes all the frames
    cv.destroyAllWindows()


if __name__ == '__main__':
    args = parser.parse_args()
    main(args.filename, args.cam, args.fps)