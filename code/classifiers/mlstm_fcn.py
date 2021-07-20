from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, LSTM, concatenate, Activation, Masking
from tensorflow.keras.layers import Conv1D, BatchNormalization, GlobalAveragePooling1D, Permute, Dropout
from utils.utils_lstm import squeeze_excite_block
import tensorflow.keras as keras
import os

from classifiers.lstm_fcn import ClassifierLstmFcn


class ClassifierMlstmFcn(ClassifierLstmFcn):
    def build_model(self, input_shape, nb_classes):
        input_layer = Input(shape=input_shape)

        x = Masking()(input_layer)
        x = LSTM(8)(x)
        x = Dropout(0.8)(x)

        y = Permute((2, 1))(input_layer)
        y = Conv1D(128, 8, padding='same', kernel_initializer='he_uniform')(y)
        y = BatchNormalization()(y)
        y = Activation('relu')(y)
        y = squeeze_excite_block(y)

        y = Conv1D(256, 5, padding='same', kernel_initializer='he_uniform')(y)
        y = BatchNormalization()(y)
        y = Activation('relu')(y)
        y = squeeze_excite_block(y)

        y = Conv1D(128, 3, padding='same', kernel_initializer='he_uniform')(y)
        y = BatchNormalization()(y)
        y = Activation('relu')(y)

        y = GlobalAveragePooling1D()(y)

        x = concatenate([x, y])

        output_layer = Dense(nb_classes, activation='softmax')(x)

        model = keras.models.Model(inputs=input_layer, outputs=output_layer)
        model.summary()

        model.compile(loss='categorical_crossentropy', optimizer=keras.optimizers.Adam(lr=self.learning_rate),
                      metrics=['accuracy'])

        reduce_lr = keras.callbacks.ReduceLROnPlateau(monitor="loss", patience=100,
                                                      mode=self.optimization_mode, factor=0.5,
                                                      cooldown=0, min_lr=1e-4, verbose=2)

        file_path = os.path.join(self.output_directory, 'best_model.hdf5')

        model_checkpoint = keras.callbacks.ModelCheckpoint(filepath=file_path, monitor=self.monitor,
                                                           save_best_only=True,
                                                           save_freq=5, verbose=1, mode=self.optimization_mode)

        if not os.path.exists(file_path):
            model.save(filepath=file_path)

        self.callbacks = [reduce_lr, model_checkpoint]

        return model






