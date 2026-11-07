import pandas as pd 
import numpy as np
import tensorflow as tf
from keras.applications import MobileNetV2
from keras.applications.mobilenet_v2 import preprocess_input

class Embedder:
    def __init__(self):
        self.model=MobileNetV2(weights='imagenet',
                          include_top=False,
                          pooling='avg')
        self.model.trainable=False,

        print("Embedder in action!!")

    def embedd(self,path):

        image=tf.io.read_file(path)
        tf.debugging.assert_positive(
            tf.strings.length(image),
            message="The image file is empty"
        )
        image=tf.image.decode_jpeg(image,channels=3)
        image=tf.image.resize(image,(224,224))

        image=preprocess_input(image)

        image=tf.expand_dims(image,axis=0)

        embedding=self.model.predict(image)
        
        return embedding.astype('float32')
