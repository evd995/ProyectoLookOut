"""Demo code shows how to estimate human head pose.
Currently, human face is detected by a detector from an OpenCV DNN module.
Then the face box is modified a little to suits the need of landmark
detection. The facial landmark detection is done by a custom Convolutional
Neural Network trained with TensorFlow. After that, head pose is estimated
by solving a PnP problem.
"""
from multiprocessing import Process, Queue

import numpy as np

import cv2
from mark_detector import MarkDetector
from mark_detector import FaceDetector
from os_detector import detect_os
from pose_estimator import PoseEstimator
from stabilizer import Stabilizer


import time

from keras.preprocessing import image
# multiprocessing may not work on Windows and macOS, check OS for safety.
detect_os()

# 3d intersection: https://stackoverflow.com/questions/2549708/intersections-of-3d-polygons-in-python

CNN_INPUT_SIZE = 128

def dump_queue(queue):
    """
    Empties all pending items in a queue and returns them in a list.
    """
    result = []

    for i in iter(queue.get, 'STOP'):
        result.append(i)
    #time.sleep(.1)
    return result


def get_face(detector, img_queue, box_queue):
    """Get face from image queue. This function is used for multiprocessing"""
    while True:
        image = img_queue.get()
        box = detector.extract_cnn_facebox(image)
        box_queue.put(box)

def get_faces(detector, img_queue, box_queue):
    """Get face from image queue. This function is used for multiprocessing"""
    while True:
        image = img_queue.get()
        confidences, faceboxes = detector.get_faceboxes(image, threshold=0.5)
        for box in faceboxes:
            box_queue.put(box)
        box_queue.put('STOP')

def main():
    """MAIN"""
    # Video source from webcam or video file.
    video_src = 0
    cam = cv2.VideoCapture(video_src)
    _, sample_frame = cam.read()

    # Introduce mark_detector to detect landmarks.
    mark_detector = MarkDetector()
    face_detector = FaceDetector()

    # Setup process and queues for multiprocessing.
    img_queue = Queue()
    box_queue = Queue()
    img_queue.put(sample_frame)
    #box_process = Process(target=get_face, args=(mark_detector, img_queue, box_queue,))
    box_process = Process(target=get_faces, args=(face_detector, img_queue, box_queue,))
    box_process.start()

    # Introduce pose estimator to solve pose. Get one frame to setup the
    # estimator according to the image size.
    height, width = sample_frame.shape[:2]
    pose_estimator = PoseEstimator(img_size=(height, width))

    # Introduce scalar stabilizers for pose.
    pose_stabilizers = [Stabilizer(
        state_num=2,
        measure_num=1,
        cov_process=0.1,
        cov_measure=0.1) for _ in range(6)]

    #face expression recognizer initialization
    from keras.models import model_from_json
    model = model_from_json(open("./model/facial_expression_model_structure.json", "r").read())
    model.load_weights('./model/facial_expression_model_weights.h5') #load weights

    #-----------------------------

    emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')

    while True:
        # Read frame, crop it, flip it, suits your needs.
        frame_got, frame = cam.read()
        if frame_got is False:
            break

        # Crop it if frame is larger than expected.
        # frame = frame[0:480, 300:940]

        # If frame comes from webcam, flip it so it looks like a mirror.
        if video_src == 0:
            frame = cv2.flip(frame, 2)

        # Pose estimation by 3 steps:
        # 1. detect face;
        # 2. detect landmarks;
        # 3. estimate pose

        # Feed frame to image queue.
        img_queue.put(frame)

        # Get face from box queue.

        #facebox = box_queue.get()

        faceboxes = dump_queue(box_queue)

        for facebox in faceboxes:
            if min(facebox) < 0:
                continue
            # Detect landmarks from image of 128x128.
            face_img = frame[facebox[1]: facebox[3],
                             facebox[0]: facebox[2]]
            face_img = cv2.resize(face_img, (CNN_INPUT_SIZE, CNN_INPUT_SIZE))
            face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
            marks = mark_detector.detect_marks(face_img)

            # Convert the marks locations from local CNN to global image.
            marks *= (facebox[2] - facebox[0])
            marks[:, 0] += facebox[0]
            marks[:, 1] += facebox[1]

            # Uncomment following line to show raw marks.
            # mark_detector.draw_marks(
            #     frame, marks, color=(0, 255, 0))

            detected_face = frame[facebox[1]: facebox[3],facebox[0]: facebox[2]] #crop detected face
            detected_face = cv2.cvtColor(detected_face, cv2.COLOR_BGR2GRAY) #transform to gray scale
            detected_face = cv2.resize(detected_face, (48, 48)) #resize to 48x48



            # emotion estimation
            img_pixels = image.img_to_array(detected_face)
            img_pixels = np.expand_dims(img_pixels, axis = 0)

            img_pixels /= 255 #pixels are in scale of [0, 255]. normalize all pixels in scale of [0, 1]

            predictions = model.predict(img_pixels) #store probabilities of 7 expressions

            #find max indexed array 0: angry, 1:disgust, 2:fear, 3:happy, 4:sad, 5:surprise, 6:neutral
            max_index = np.argmax(predictions[0])

            emotion = emotions[max_index]

            #write emotion text above rectangle

            #V_FONT_HERSHEY_SIMPLEX normal size sans-serif font
            #CV_FONT_HERSHEY_PLAIN small size sans-serif font
            #CV_FONT_HERSHEY_DUPLEX normal size sans-serif font (more complex than CV_FONT_HERSHEY_SIMPLEX )
            #CV_FONT_HERSHEY_COMPLEX normal size serif font
            #CV_FONT_HERSHEY_TRIPLEX normal size serif font (more complex than CV_FONT_HERSHEY_COMPLEX )
            #CV_FONT_HERSHEY_COMPLEX_SMALL smaller version of CV_FONT_HERSHEY_COMPLEX
            #CV_FONT_HERSHEY_SCRIPT_SIMPLEX hand-writing style font
            #CV_FONT_HERSHEY_SCRIPT_COMPLEX more complex variant of CV_FONT_HERSHEY_SCRIPT_SIMPLEX

            image_text = ""
            for index in range(len(emotions)):
                if predictions[0][index]>0.3:
                    image_text += "{0} : {1} %\n".format(emotions[index], int(predictions[0][index]*100))

            space = 0
            for text in image_text.strip().split("\n"):
                cv2.putText(
                img = frame,
                text= text,
                org =(int(facebox[0]), int(facebox[1])-space),
                fontFace = cv2.FONT_HERSHEY_PLAIN,
                fontScale = 0.8,
                color   =  (255,255,255),
                thickness = 1
                )
                space += int(0.25*48)



            # Try pose estimation with 68 points.
            pose = pose_estimator.solve_pose_by_68_points(marks)

            # Stabilize the pose.
            #stabile_pose = []
            #pose_np = np.array(pose).flatten()
            #for value, ps_stb in zip(pose_np, pose_stabilizers):
            #    ps_stb.update([value])
            #    stabile_pose.append(ps_stb.state[0])
            #stabile_pose = np.reshape(stabile_pose, (-1, 3))

            # Uncomment following line to draw pose annotaion on frame.
            pose_estimator.draw_annotation_box(
                 frame, pose[0], pose[1], color=(255, 128, 128))

            # Uncomment following line to draw stabile pose annotaion on frame.
            #pose_estimator.draw_annotation_box(
            #    frame, stabile_pose[0], stabile_pose[1], color=(128, 255, 128))


        # Show preview.
        cv2.imshow("Preview", frame)
        if cv2.waitKey(10) == 27:
            break

    # Clean up the multiprocessing process.
    box_process.terminate()
    box_process.join()


if __name__ == '__main__':
    main()
