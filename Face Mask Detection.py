# -*- coding: utf-8 -*-
"""Copy of convolutional_neural_network.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1895qvHm9Ot-wLuexvzngY7kF9CrdH4Ip

# Convolutional Neural Network

### Importing the libraries
"""

import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator
tf.__version__

"""## Part 1 - Data Preprocessing

### Preprocessing the Training set
"""

training_datagen=ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)
training_set=training_datagen.flow_from_directory(
    'dataset/training_set',
    target_size=(64,64),
    batch_size=32,
    class_mode='binary'
)

"""### Preprocessing the Test set"""

test_datagen=ImageDataGenerator(rescale=1./255)
test_set=test_datagen.flow_from_directory(
    'dataset/test_set',
    target_size=(64,64),
    batch_size=32,
    class_mode='binary'
)

"""## Part 2 - Building the CNN

### Initialising the CNN
"""

cnn=tf.keras.models.Sequential()

"""### Step 1 - Convolution"""

cnn.add(tf.keras.layers.Conv2D(filters=32,kernel_size=3,activation='relu',input_shape=[64,64,3]))

"""### Step 2 - Pooling"""

cnn.add(tf.keras.layers.MaxPool2D(pool_size=2,strides=2))

"""### Adding a second convolutional layer"""

cnn.add(tf.keras.layers.Conv2D(filters=32,kernel_size=3,activation='relu'))
cnn.add(tf.keras.layers.MaxPool2D(pool_size=2,strides=2))

"""### Step 3 - Flattening"""

cnn.add(tf.keras.layers.Flatten())

"""### Step 4 - Full Connection"""

cnn.add(tf.keras.layers.Dense(units=128,activation='relu'))

"""### Step 5 - Output Layer"""

cnn.add(tf.keras.layers.Dense(units=1,activation='sigmoid'))

"""## Part 3 - Training the CNN

### Compiling the CNN
"""

cnn.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])

"""### Training the CNN on the Training set and evaluating it on the Test set"""

cnn.fit(x=training_set,validation_data=test_set,epochs=25)

"""## Part 4 - Making a single prediction"""
'''
import numpy as np
from keras.preprocessing import image
test_image=image.load_img('dataset/single_prediction/augmented_image_281.jpg',target_size=(64,64))
test_image=image.img_to_array(test_image)
test_image=np.expand_dims(test_image,axis=0)
result=cnn.predict(test_image)
training_set.class_indices
if (result[0][0]==1):
  prediction='without mask'
else:
  prediction='with mask' '''
import numpy as np
from keras.preprocessing import image
import cv2
classifier=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
source=cv2.VideoCapture(0)
while(True):

    ret,img=source.read()
    faces=classifier.detectMultiScale(img,scaleFactor=1.5,minNeighbors=5)
    for (x,y,w,h) in faces:
        #region of interest of frames
        roi_color=img[y:y+h,x:x+w]
        duplicate="imagecurrent.jpg"
        cv2.imwrite(duplicate,roi_color)
        #capturing face in a rectangle 
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        test_image=image.load_img(duplicate,target_size=(64,64))
        test_image=image.img_to_array(test_image)
        test_image=np.expand_dims(test_image,axis=0)
        result=cnn.predict(test_image)
        training_set.class_indices
        if (result[0][0]==1):
            prediction='without mask'
        else:
            prediction='with mask'
        font=cv2.FONT_HERSHEY_SIMPLEX
        name=prediction
        if prediction=="with mask":
            color=(255,0,0)
        if prediction=="without mask":
            color=(0,0,255)
        stroke=2
        cv2.putText(img,name,(x,y),font,1,color,stroke,cv2.LINE_AA)
     
    '''cv2.rectangle(img,(x,y),(x+w,y+h),color_dict[label],2)
    cv2.rectangle(img,(x,y-40),(x+w,y),color_dict[label],-1)
    cv2.putText(img, labels_dict[label], (x, y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)'''
        
        
    cv2.imshow('LIVE',img)
    key=cv2.waitKey(1)
    
    if(key==27):
        break
source.release()     
cv2.destroyAllWindows()
    