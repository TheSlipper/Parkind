from tensorflow.keras import datasets
import tensorflow as tf
from threading import Thread, Lock
import keras
from keras import models

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
    
    def __init__(self, tf_model=None, history=None):
        self.mutex = Lock()
        self.mutex.acquire()
        self.Tf_model = tf_model
        self.History = history
        self.mutex.release()

    def Train_net(self, dataset):
        """Trains a neural network with the given dataset and returns history of training"""
        self.mutex.acquire()

        model.compile(optimizer=tf.keras.optimizers.RMSprop(lr=base_learning_rate),
            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])
    
        self.history = model.fit(dataset.Train_data, dataset.Train_labels, epochs=dataset.Epochs, 
            validation_data=(dataset.Test_data, dataset.Test_labels))
        self.mutex.release()

    def Detect(self, img):
        self.mutex.acquire()
        # TODO: Implement, remember about a mutex in this class
        
        self.mutex.release()

    def Save(self, path):
        pass

    def Load(self, path):
        pass


class Dataset:
    """Contains a set of information used for """
    def __init__(self, train_data, train_labels, test_data, test_labels, epochs):
        self.Train_data = train_data
        self.Train_labels = train_labels
        self.Test_data = test_data
        self.Test_labels = test_labels
        self.Epochs = epochs
