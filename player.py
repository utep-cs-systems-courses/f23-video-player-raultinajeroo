#!/usr/bin/env python3
import cv2, threading, params, videoQueue
from threading import Thread, Lock

params = params.parseParams()
video_file, frame_count, usage = params["video"], int(params['frames']), params["usage"]
if usage:
    params.usage()

def extractFrames(video_file, inVideo, maxFrames):
    vidcap = cv2.VideoCapture(video_file)
    if not vidcap.isOpened():
        print(f"There was an error processing {video_file}")
        return
    
    success, image = vidcap.read()
    count = 0
    while success and count < maxFrames:
        print(f"Extracting frame #{count}: {success}")
        success, jpg = cv2.imencode('.jpg', image)
        if not success:
            print(f"There was an error processing frame {count}")
            break
        inVideo.enque(jpg)
        success, image = vidcap.read()
        count += 1
    vidcap.release()

def convertGrayscale(inVideo, outVideo, maxFrames):
    count = 0
    frame = inVideo.deque()
    while frame is not None and count < maxFrames:
        image = cv2.imdecode(frame, cv2.IMREAD_UNCHANGED)
        g_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print(f"Converting frame #{count}")
        outVideo.enque(g_frame)
        frame = inVideo.deque()
        count += 1

def displayFrames(outVideo):
    delay = 42
    frame = outVideo.deque()
    while frame is not None:
        cv2.imshow('Video', frame)
        if cv2.waitKey(delay) and 0xFF == ord('q'):
            break
        print(f"Displaying frame")
        frame = outVideo.deque()
    cv2.destroyAllWindows()

def videoPlayer():
    inVideo = videoQueue.videoQueue()
    outVideo = videoQueue.videoQueue()

    # Simultaneous thead start
    extract = Thread(target = extractFrames, args = (video_file, inVideo, frame_count))
    convert = Thread(target = convertGrayscale, args = (inVideo, outVideo, frame_count))
    display = Thread(target = displayFrames, args = (outVideo,))

    # Start all threads
    extract.start()
    convert.start()
    display.start()

    # Join when done
    extract.join()
    convert.join()
    display.join()


def main():
    videoPlayer()

if __name__ == "__main__":
    main()