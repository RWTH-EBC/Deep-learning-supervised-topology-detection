from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, concatenate, Activation, Masking
from tensorflow.keras.layers import Conv1D, BatchNormalization, GlobalAveragePooling1D, Permute, Dropout
# from utils.utils_lstm import squeeze_excite_block

from classifiers.lstm_fcn import ClassifierLstmFcn
from utils.layer_utils import AttentionLSTM


class ClassifierAlstmFcn(ClassifierLstmFcn):
    def build_model(self, input_shape, nb_classes):
        ip = Input(shape=input_shape)

        x = Masking()(ip)
        x = AttentionLSTM(64)(x)
        x = Dropout(0.8)(x)

        y = Permute((2, 1))(ip)
        y = Conv1D(128, 8, padding='same', kernel_initializer='he_uniform')(y)
        y = BatchNormalization()(y)
        y = Activation('relu')(y)

        y = Conv1D(256, 5, padding='same', kernel_initializer='he_uniform')(y)
        y = BatchNormalization()(y)
        y = Activation('relu')(y)

        y = Conv1D(128, 3, padding='same', kernel_initializer='he_uniform')(y)
        y = BatchNormalization()(y)
        y = Activation('relu')(y)

        y = GlobalAveragePooling1D()(y)

        x = concatenate([x, y])

        out = Dense(nb_classes, activation='softmax')(x)

        model = Model(ip, out)
        model.summary()

        return model
