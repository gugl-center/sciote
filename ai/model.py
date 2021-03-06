from tensorflow.python.keras import Input, Model
from tensorflow.python.keras.layers import Dropout, Dense, Concatenate

from config import BLOCKS


def _last_layer_params(classes_len):
    """Calculates layer parameters based on classes set length

    :param classes_len: the amount of classes
    :return: the number of units and activation function
    """
    if classes_len == 2:
        activation = 'sigmoid'
        units = 1
    else:
        activation = 'softmax'
        units = classes_len

    return units, activation


def build_model(input_shape, dropout_rate, units, activation):
    metrics_num, words_num = input_shape

    inputs = [Input((metrics_num, )), Input((words_num, ))]

    metrics_tensor = inputs[0]
    metrics_tensor = Dropout(rate=dropout_rate)(metrics_tensor)
    metrics_tensor = Dense(units=50, activation='relu')(metrics_tensor)
    metrics_tensor = Dropout(rate=dropout_rate)(metrics_tensor)
    metrics_tensor = Dense(units=50, activation=activation)(metrics_tensor)

    words_tensor = inputs[1]
    words_tensor = Dense(50)(words_tensor)
    for _ in range(BLOCKS):
        words_tensor = Dropout(rate=dropout_rate)(words_tensor)
        words_tensor = Dense(300)(words_tensor)
        words_tensor = Dense(200)(words_tensor)

    words_tensor = Dropout(rate=dropout_rate)(words_tensor)
    words_tensor = Dense(units=50, activation=activation)(words_tensor)

    output_tensor = Concatenate()([words_tensor, metrics_tensor])
    output_tensor = Dropout(rate=dropout_rate)(output_tensor)
    output_tensor = Dense(units=25, activation='relu')(output_tensor)
    output_tensor = Dropout(rate=dropout_rate)(output_tensor)
    output_tensor = Dense(units=units, activation=activation)(output_tensor)

    model = Model(inputs=inputs, outputs=[output_tensor])

    return model
