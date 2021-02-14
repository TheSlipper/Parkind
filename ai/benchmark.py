import argparse
import time
from tensorflow.keras import datasets
import tensorflow as tf
import keras
from keras import models
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib
import numpy as np
import gc


class GraphData:
    def __init__(self, model_name, comp_time, train_time, avg_eval_time, acc, acc_history):
        self.model_name = model_name
        self.compilation_time = comp_time
        self.training_time = train_time
        self.average_evaluation_time = avg_eval_time
        self.accuracy = acc
        self.accuracy_history = acc_history


# Tweaks the GPU for dynamic memory growth
def tweak_gpu():
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


# Loads the binary dataset and returns a tuple of train data and validation data
def load_binary_dataset(data_dir, batch_size):
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir, validation_split=0.2, subset="training",
        seed=123, image_size=(75, 75),
        batch_size=batch_size)
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir, validation_split=0.2, subset="validation",
        seed=123, image_size=(75, 75),
        batch_size=batch_size)
    train_labels = train_ds.class_names
    val_labels = val_ds.class_names

    # Scale the RGB values to 0-1.0 range
    normalization_layer = tf.keras.layers.experimental.preprocessing.Rescaling(1. / 255)
    train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
    val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y))

    return (train_ds, train_labels), (val_ds, val_labels)


# Creates a mobilenet v2 base model
def get_model(img_shape, model_name):
    base_model = models.Sequential()
    base_model.add(tf.keras.layers.experimental.preprocessing.Resizing(75, 75))
    resized_img_shape = (75, 75, 3)

    if model_name == 'MobileNetV2':
        base_model = tf.keras.Sequential([base_model, tf.keras.applications.MobileNetV2(input_shape=resized_img_shape,
                                                                                        include_top=False,
                                                                                        weights='imagenet')])
    elif model_name == 'InceptionResNetV2':
        base_model = tf.keras.Sequential(
            [base_model, tf.keras.applications.InceptionResNetV2(input_shape=resized_img_shape,
                                                                 include_top=False,
                                                                 weights='imagenet')])
    elif model_name == 'InceptionV3':
        base_model = tf.keras.Sequential([base_model, tf.keras.applications.InceptionV3(input_shape=resized_img_shape,
                                                                                        include_top=False,
                                                                                        weights='imagenet')])
    else:
        return None
    # base_model.trainable = False
    return base_model


# Creates the classifier and applies it to the base model
def apply_classifier(base_model, class_count):
    global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
    prediction_layer = keras.layers.Dense(class_count, activation='relu')
    model = tf.keras.Sequential([
        base_model, global_average_layer,
        prediction_layer
    ])
    return model


# Generate a single bar plot with the given labels and values
def generate_bar_plot(vals, labels, header='Training time', y_axis_label='Training time (s)',
                      title='Comparison of training time', path='graph.png'):
    colors = ['blue', 'green', 'red']
    width = 0.35
    fig, ax = plt.subplots()
    bars = ax.bar(labels, vals, width, label=header)
    ax.set_ylabel(y_axis_label)
    ax.set_title(title)
    # ax.set_xticks()
    j = 0
    for i, v in enumerate(vals):
        ax.text(v + 3, i + .25, str(v), color=colors[j], fontweight='bold')
        bars[j].set_color(colors[j])
        j += 1
    plt.savefig(path)


# Generate grouped bar plot with two pieces of data
def generate_double_bars_plot(vals_left, vals_right, labels, y_axis_label='Training time (s)',
                              title='Comparison of training time', path='graph.png'):
    width = 0.35
    x = np.arange(len(vals_left))
    plt.bar(x, vals_left, width=width, color='royalblue', zorder=2)
    plt.bar(x + width, vals_right, width=width, color='indianred', zorder=2)
    plt.title(title)
    plt.ylabel(y_axis_label)
    plt.xticks(x + width/2, labels)

    plt.savefig(path)


# Generate a graph of the given values
def generate_graph(vals, labels, path='graph.png', x_label='Epoch', y_label='Accuracy (%)',
                   graph_title='Accuracy over time'):
    colors = ['blue', 'green', 'red']
    fig, ax = plt.subplots()
    i = 0
    for arr in vals:
        plt.plot(arr, label=labels[i], color=colors[i])
        i += 1
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.grid()
    plt.savefig(path)


# Generates a csv file with the information on training
def generate_csv(data_arr, path):
    content = 'Model Name,Compilation Time,Training Time,Average Evaluation Time,Average Accuracy\n'
    i = 0

    for model in data_arr:
        content += model.model_name + ',' + str(model.compilation_time) + ',' + str(model.training_time) + ',' + \
                   str(model.average_evaluation_time) + ',' + str(model.accuracy) + '\n'
        i += 1

    with open(path, "w") as file:
        file.write(content)


# Generate all the plots with the benchmarking data after training for one scenario
def generate_plots(data_arr, path_prefix='', tex=False):
    vals = []
    labels = []
    extension = '.png'
    if tex:
        matplotlib.use("pgf")
        plt.rcParams.update({
            "pgf.texsystem": "pdflatex",
            'font.family': 'serif',
            'text.usetex': True,
            'pgf.rcfonts': False,
        })
        extension = '.pgf'

    # Compilation time
    for i in range(0, len(data_arr)):
        labels.append(data_arr[i].model_name)
        vals.append(data_arr[i].compilation_time)
    generate_bar_plot(vals, labels, 'Compilation time', 'Compilation time (s)', 'Comparison of '
        'compilation time', path_prefix + 'compilation_time' + extension)

    # Training time
    for i in range(0, len(data_arr)):
        vals[i] = data_arr[i].training_time
    generate_bar_plot(vals, labels, path=path_prefix + 'training_time' + extension)

    # Avg eval time
    for i in range(0, len(data_arr)):
        vals[i] = data_arr[i].average_evaluation_time
    generate_bar_plot(vals, labels, 'Average evaluation time', 'Evaluation time (s)', 'Comparison of evaluation time',
                      path_prefix + 'avg_evaluation_time' + extension)

    # Accuracy
    for i in range(0, len(data_arr)):
        vals[i] = data_arr[i].accuracy
    generate_bar_plot(vals, labels, 'Accuracy of evaluation', 'Success rate (%)', 'Comparison of evaluation accuracy',
                      path_prefix + 'accuracy' + extension)

    # History of accuracy
    for i in range(0, len(data_arr)):
        vals[i] = data_arr[i].accuracy_history
    generate_graph(vals, labels, path_prefix + 'accuracy_overtime' + extension)

    # Generate CSV
    generate_csv(data_arr, path_prefix + 'data.csv')


# Generate all the plots with the benchmarking data after training for one scenario
def generate_plots_both_scenarios(binary_arr, multi_arr, path_prefix='', tex=False):
    vals_left = []
    vals_right = []
    labels = []
    extension = '.png'
    if tex:
        matplotlib.use("pgf")
        plt.rcParams.update({
            "pgf.texsystem": "pdflatex",
            'font.family': 'serif',
            'text.usetex': True,
            'pgf.rcfonts': False,
        })
        extension = '.pgf'

    # Compilation time
    for i in range(len(binary_arr)):
        labels.append(binary_arr[i].model_name)
        vals_left.append(binary_arr[i].compilation_time)
        vals_right.append(multi_arr[i].compilation_time)
    generate_double_bars_plot(vals_left, vals_right, labels, 'Compilation time (s)', 'Comparison of compilation time',
                              path_prefix + 'compilation_time' + extension)

    # Avg eval time
    for i in range(len(binary_arr)):
        vals_left.append(binary_arr[i].average_evaluation_time)
        vals_right.append(multi_arr[i].average_evaluation_time)
    generate_double_bars_plot(vals_left, vals_right, labels, 'Evaluation time (s)', 'Comparison of evaluation time',
                              path_prefix + 'avg_evaluation_time' + extension)

    # Avg accuracy
    for i in range(len(binary_arr)):
        vals_left.append(binary_arr[i].accuracy)
        vals_right.append(multi_arr[i].accuracy)
    generate_double_bars_plot(vals_left, vals_right, labels, 'Success rate (%)', 'Comparison of evaluation accuracy',
                              path_prefix + 'accuracy' + extension)

    # Training times
    for i in range(len(binary_arr)):  # binary
        vals_left[i] = binary_arr[i].training_time
    for i in range(len(multi_arr)):  # multi
        vals_right[i] = multi_arr[i].training_time
    generate_bar_plot(vals_left, labels, path=path_prefix + 'binary_training_time' + extension)
    generate_bar_plot(vals_right, labels, path=path_prefix + 'multi_training_time' + extension)

    # History of accuracy
    for i in range(0, len(binary_arr)):  # binary
        vals_left[i] = binary_arr[i].accuracy_history
    for i in range(0, len(binary_arr)):  # multi
        vals_right[i] = multi_arr[i].accuracy_history
    generate_graph(vals_left, labels, path_prefix + 'binary_accuracy_overtime' + extension)
    generate_graph(vals_right, labels, path_prefix + 'multi_accuracy_overtime' + extension)

    # Generate CSVs
    generate_csv(binary_arr, path_prefix + 'binary_data.csv')
    generate_csv(multi_arr, path_prefix + 'multi_data.csv')


# Benchmarks
def benchmark_models(model_dict, binary, epochs, base_learning_rate, train_ds, train_labels, test_ds, test_labels, model_path=''):
    model_stats = []
    for key, val in model_dict.items():
        model_dict[key] = apply_classifier(model_dict[key], len(train_labels))
        start = time.time()
        model_dict[key].compile(optimizer=tf.keras.optimizers.RMSprop(lr=base_learning_rate),
                                loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                                metrics=['accuracy'])
        compilation_time = time.time() - start
        if not binary:
            start = time.time()
            history = model_dict[key].fit(train_ds, train_labels, epochs=epochs, validation_data=(test_ds, test_labels))
            training_time = time.time() - start
            start = time.time()
            test_loss, test_acc = model_dict[key].evaluate(test_ds, test_labels, verbose=2)
            avg_evaluation_time = (time.time() - start) / len(test_ds)
        else:
            start = time.time()
            history = model_dict[key].fit(train_ds, epochs=epochs, validation_data=test_ds)
            training_time = time.time() - start
            start = time.time()
            test_loss, test_acc = model_dict[key].evaluate(test_ds, verbose=2)
            avg_evaluation_time = (time.time() - start) / len(test_ds)
        acc_history = history.history['accuracy']
        model_stats.append(GraphData(key, compilation_time, training_time, avg_evaluation_time, test_acc, acc_history))
        if model_path != '':
            model_dict[key].save(model_path+"/"+key)
    return model_stats


# Defines the workflow of training and benchmarking when working with only one dataset
def single_dataset_scenario(binary, epochs, binary_path, output_path, tex, model_output):
    # Load the dataset
    if not binary:
        (train_ds, train_labels), (test_ds, test_labels) = datasets.cifar10.load_data()
    else:
        (train_ds, train_labels), (test_ds, test_labels) = load_binary_dataset(binary_path, 128)

    # Compile, train and evaluate and save the data to the data dictionary
    img_size = (75, 75, 3)
    local_models = {'MobileNetV2': get_model(img_size, 'MobileNetV2'),
                    'InceptionV3': get_model(img_size, 'InceptionV3'),
                    'InceptionResNetV2': get_model(img_size, 'InceptionResNetV2')}
    base_learning_rate = 0.0001
    model_stats = benchmark_models(local_models, binary, epochs, base_learning_rate, train_ds, train_labels, test_ds,
                                   test_labels, model_output)
    generate_plots(model_stats, output_path, tex)


# Defines the workflow of training and benchmarking when working with both datasets
def both_datasets_scenario(epochs, binary_path, output_path, tex):
    # Load the binary classification dataset
    (binary_train_ds, binary_train_labels), (binary_test_ds, binary_test_labels) = load_binary_dataset(binary_path, 128)

    # Prepare resize layers and feature extractors
    img_size = (75, 75, 3)
    binary_models = {'MobileNetV2': get_model(img_size, 'MobileNetV2'),
                    'InceptionV3': get_model(img_size, 'InceptionV3'),
                    'InceptionResNetV2': get_model(img_size, 'InceptionResNetV2')}
    base_learning_rate = 0.0001

    # Benchmark binary classification model and then free memory of the dataset
    binary_model_stats = benchmark_models(binary_models, True, epochs, base_learning_rate, binary_train_ds,
                                          binary_train_labels, binary_test_ds, binary_test_labels)
    binary_train_ds, binary_train_labels, binary_test_ds, binary_test_labels = None, None, None, None
    binary_models = None
    print("Finished training binary classification models")
    gc.collect()

    # Prepare the multi-label classification models, dataset and benchmark them and then free the memory of the dataset
    multi_models = {'MobileNetV2': get_model(img_size, 'MobileNetV2'),
                    'InceptionV3': get_model(img_size, 'InceptionV3'),
                    'InceptionResNetV2': get_model(img_size, 'InceptionResNetV2')}
    (cifar_train_ds, cifar_train_labels), (cifar_test_ds, cifar_test_labels) = datasets.cifar10.load_data()
    multi_model_stats = benchmark_models(multi_models, False, epochs, base_learning_rate, cifar_train_ds,
                                         cifar_train_labels, cifar_test_ds, cifar_test_labels)
    cifar_train_ds, cifar_train_labels, cifar_test_ds, cifar_test_labels = None, None, None, None
    multi_models = None
    print("Finished training multi-label classification models")
    gc.collect()
    generate_plots_both_scenarios(binary_model_stats, multi_model_stats, output_path, tex)


# Main
def main():
    # Set up arguments
    parser = argparse.ArgumentParser(description='Trains, compiles and benchmarks a neural network '
        'model with either a binary- or multi-class dataset and saves the benchmarking data')

    parser.add_argument('--binary-path', dest='binary_path', default='parking_dataset/',
        help='path to the folder with the binary classification dataset')

    parser.add_argument('--output-path', dest='output_path', default='',
        help='path to the folder to which all the graphs and data will be exported')

    parser.add_argument('--export-path', dest='model_export_path', default='',
        help='defines the output path of the received model. If not provided will not export it.')

    parser.add_argument('--epochs', dest='epochs', default="20", help='number of training epochs '
        '(default: 20)')

    parser.add_argument('--binary', '-b', action='store_true', help='If set to true then trains and'
        ' benchmarks binary models')

    parser.add_argument('--all', '-a', action='store_true', help='If the flag is set then benchmarks'
        ' both datasets')

    parser.add_argument('--tex', '-t', action='store_true', help='If the flag is set then the script'
        ' will export to .pgf')

    parser.add_argument('--dynamic-growth', '-d', action='store_true', help='If the flag is set then'
        ' the script will enable dynamic GDDR memory allocation (Fixes crashes on some GPUs. Do not'
        ' use with CPU training)')

    # Load command line data
    args = parser.parse_args()

    # CUDA Tweaks
    if args.dynamic_growth:
        tweak_gpu()

    # Training scenarios
    if not args.all:
        single_dataset_scenario(bool(args.binary), int(args.epochs), args.binary_path, args.output_path,
                                args.tex, args.model_export_path)
    else:
        both_datasets_scenario(int(args.epochs), args.binary_path, args.output_path, args.tex)


if __name__ == "__main__":
    main()
