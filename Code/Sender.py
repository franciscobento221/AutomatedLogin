
import cv2

import face_recognition

import os

import socket
 
def load_known_faces(folder_path):

    known_faces = {}

    # Loop through all the files in the folder

    for filename in os.listdir(folder_path):

        if filename.endswith('.jpg') or filename.endswith('.png'):

            # Load the image file

            image_path = os.path.join(folder_path, filename)

            image = face_recognition.load_image_file(image_path)

            # Encode the image

            face_encoding = face_recognition.face_encodings(image)[0]

            # Extract the name of the person from the filename

            name = os.path.splitext(filename)[0]

            # Add to the known_faces dictionary

            known_faces[name] = face_encoding

    return known_faces
 
def get_face_text(name):

    text_folder = "/home/ubuntu/Desktop/ESS/pass"

    text_file_path = os.path.join(text_folder, f"{name}.txt")

    with open(text_file_path, 'r') as file:

        face_text = file.read().strip()

    return face_text
 
def label_faces(frame, face_locations, known_faces, sender_socket):

    for top, right, bottom, left in face_locations:

        # Crop the detected face from the frame

        face_image = frame[top:bottom, left:right]
 
        # Resize the face image to a fixed size for better face recognition

        face_image = cv2.resize(face_image, (150, 150))
 
        # Encode the cropped and resized face image

        face_encoding = face_recognition.face_encodings(face_image)
 
        if len(face_encoding) > 0:

            # Compare the face encoding with the known face encodings

            matches = face_recognition.compare_faces(list(known_faces.values()), face_encoding[0])

            # Label the face with the name if recognized

            label = "Unknown"

            for name, match in zip(known_faces.keys(), matches):

                if match:

                    label = name

                    face_text = get_face_text(name)

                    try:

                        sender_socket.send(face_text.encode())

                    except BrokenPipeError:

                        print("Connection broken. Reconnecting...")

                        sender_socket.close()

                        sender_socket.connect((receiver_ip, receiver_port))

                        sender_socket.send(face_text.encode())

                    break
 
            # Draw a box around the face

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
 
            # Draw a label with the name below the face

            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)

            font = cv2.FONT_HERSHEY_DUPLEX

            cv2.putText(frame, label, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
 
    return frame
 
def main():

    # Specify the path to the folder containing known face images

    folder_path = "/home/ubuntu/Desktop/ESS/fotos"

    # Load known faces

    known_faces = load_known_faces(folder_path)
 
    # Open the webcam

    video_capture = cv2.VideoCapture(0)
 
    # Create a socket object

    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Receiver IP and Port

    receiver_ip = '192.168.88.252'

    receiver_port = 12345

    # Connect to the receiver

    sender_socket.connect((receiver_ip, receiver_port))
 
    while True:

        # Capture each frame from the webcam

        ret, frame = video_capture.read()
 
        # Convert the frame from BGR to RGB

        rgb_frame = frame[:, :, ::-1]
 
        # Find all the faces in the current frame

        face_locations = face_recognition.face_locations(rgb_frame)
 
        # Label the faces

        labeled_frame = label_faces(frame, face_locations, known_faces, sender_socket)
 
        # Display the resulting image

        cv2.imshow('Video', labeled_frame)
 
        # Break the loop if 'q' is pressed

        if cv2.waitKey(1) & 0xFF == ord('q'):

            break
 
    # Release the webcam and close OpenCV windows

    video_capture.release()

    cv2.destroyAllWindows()
 
if __name__ == "__main__":

    main()
