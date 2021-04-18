import numpy as np
from keras.models import load_model
from keras.preprocessing import image
import cv2
my_model = load_model('FaceMask_model.h5')

c = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while c.isOpened():
    _, img = c.read()
    face = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=4)
    for (x, y, w, h) in face:
        face_img = img[y:y + h, x:x + w]
        cv2.imwrite('temporary.jpg', face_img)
        test_image = image.load_img('temporary.jpg', target_size=(150, 150, 3))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        pred = my_model.predict_classes(test_image)[0][0]
        if pred == 1:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
            cv2.putText(img, 'NO MASK!!', ((x + w) // 2, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        else:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.putText(img, 'MASK', ((x + w) // 2, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)


    cv2.imshow('img', img)

    if cv2.waitKey(1) == ord('q'):
        break

c.release()
cv2.destroyAllWindows()