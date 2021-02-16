from tensorflow.keras import datasets
import tensorflow as tf
from threading import Thread, Lock
import keras
from keras import models
from keras.preprocessing import image

def import_model(folder_path):
    # Load model
    tf_model = keras.models.load_model(folder_path)
    model = ParkindModel(tf_model)
    return model


def tweak_gpu():
    """Tweaks the GPU for dynamic memory growth

    Function tweaks the the tensorflow library to use dynamic memory allocation in GPU computing
    operations. Tested only with CUDA.

    """
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            # Currently, memory growth needs to be the same across GPUs
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            logical_gpus = tf.config.experimental.list_logical_devices('GPU')
            print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
        except RuntimeError as e:
            # Memory growth must be set before GPUs have been initialized
            print(e)


def get_model(img_shape, model_name):
    """Gets a model by the model name

    Function sets up a base model (without the classifier) that corresponds to the given name. It 
    also sets it up with imagenet values.

    """

    base_model = models.Sequential()
    base_model.add(tf.keras.layers.experimental.preprocessing.Resizing(75, 75))
    # resized_img_shape = (75, 75, 3)

    if model_name == 'MobileNetV2':
        base_model = tf.keras.Sequential([base_model,
            tf.keras.applications.MobileNetV2(input_shape=img_shape, include_top=False, 
            weights='imagenet')])
    elif model_name == 'InceptionResNetV2':
        base_model = tf.keras.Sequential([base_model,
            tf.keras.applications.InceptionResNetV2(input_shape=img_shape, include_top=False, 
            weights='imagenet')])
    elif model_name == 'InceptionV3':
        base_model = tf.keras.Sequential([base_model, 
            tf.keras.applications.InceptionV3(input_shape=img_shape, include_top=False, 
            weights='imagenet')])
    else:
        return None
    # base_model.trainable = False
    return base_model


def apply_classifier(base_model, class_count):
    """Creates the classifier and applies it to the base model"""

    global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
    prediction_layer = keras.layers.Dense(class_count, activation='relu')
    model = tf.keras.Sequential([
        base_model, global_average_layer,
        prediction_layer
    ])
    return model


class ParkindModel:
    """Container for Parkind ready binary detection tensorflow model"""
    
    def __init__(self, tf_model=None):
        self.mtx = Lock()
        self.mtx.acquire()
        self.Tf_model = tf_model
        self.mtx.release()

    def Detect(self, f_name):
        self.mtx.acquire()
        # TODO: Implement, remember about a mutex in this class
        img = image.load_img(path=f_name)
        img = image.img_to_array(img)
        img_class = model.predict_classes(test_img)
        print(img_class[0])
        self.mtx.release()

