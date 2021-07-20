from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, LSTM, concatenate, Activation, Masking
from tensorflow.keras.layers import Conv1D, BatchNormalization, GlobalAveragePooling1D, Permute, Dropout
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam
import tensorflow.keras as keras
import tensorflow as tf
# from sklearn.utils import class_weight

import os
import numpy as np
import time

from utils.utils import save_logs
from utils.utils import calculate_metrics


class ClassifierLstmFcn:
    def __init__(self, output_directory, input_shape, nb_classes, verbose=False, build=True):
        self.output_directory = output_directory
        self.batch_size = 128
        self.epochs = 50
        self.learning_rate = 1e-3
        self.monitor = "loss"
        self.optimization_mode = "auto"
        # self.weight_fn = None
        self.callbacks = list()

        if build:
            self.model = self.build_model(input_shape, nb_classes)
            if verbose:
                self.model.summary()
            self.verbose = verbose
            self.model.save_weights(os.path.join(self.output_directory, 'model_init.hdf5'))
        return

    def build_model(self, input_shape, nb_classes):
        input_layer = Input(shape=input_shape)

        x = Masking()(input_layer)
        x = LSTM(8)(x)
        x = Dropout(0.8)(x)

        y = Permute((2, 1))(input_layer)
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

        output_layer = Dense(nb_classes, activation='softmax')(x)

        model = keras.models.Model(inputs=input_layer, outputs=output_layer)
        model.summary()

        model.compile(loss='categorical_crossentropy', optimizer=keras.optimizers.Adam(lr=self.learning_rate),
                      metrics=['accuracy'])

        reduce_lr = keras.callbacks.ReduceLROnPlateau(monitor=self.monitor, patience=100,
                                                      mode=self.optimization_mode, factor=0.5,
                                                      cooldown=0, min_lr=1e-4, verbose=2)

        file_path = os.path.join(self.output_directory, 'best_model.hdf5')

        model_checkpoint = keras.callbacks.ModelCheckpoint(filepath=file_path, monitor=self.monitor, save_best_only=True,
                                                           save_freq=5, verbose=1, mode=self.optimization_mode)

        if not os.path.exists(file_path):
            model.save(filepath=file_path)

        self.callbacks = [reduce_lr, model_checkpoint]

        return model

    def fit(self, x_train, y_train, x_val, y_val, y_true):
        if not tf.test.is_gpu_available:
            print('error')
            exit()
        # x_val and y_val are only used to monitor the test loss and NOT for training

        # mini_batch_size = int(min(x_train.shape[0] / 10, self.batch_size))

        start_time = time.time()

        hist = self.model.fit(x_train, y_train, batch_size=self.batch_size, epochs=self.epochs,
                              verbose=self.verbose, validation_data=(x_val, y_val), callbacks=self.callbacks)

        duration = time.time() - start_time

        self.model.save(os.path.join(self.output_directory, 'last_model.hdf5'))

        try:
            model = keras.models.load_model(os.path.join(self.output_directory, 'best_model.hdf5'))
        except OSError:
            model = keras.models.load_model()

        y_pred = model.predict(x_val)

        # convert the predicted from binary to integer
        y_pred = np.argmax(y_pred, axis=1)

        save_logs(self.output_directory, hist, y_pred, y_true, duration)

        keras.backend.clear_session()

    def predict(self, x_test, y_true, x_train, y_train, y_test, return_df_metrics=True):
        model_path = os.path.join(self.output_directory, 'best_model.hdf5')
        model = keras.models.load_model(model_path)
        y_pred = model.predict(x_test)
        if return_df_metrics:
            y_pred = np.argmax(y_pred, axis=1)
            df_metrics = calculate_metrics(y_true, y_pred, 0.0)
            return df_metrics
        else:
            return y_pred



    # def predict(self, x_test, y_true, x_train, y_train, y_test, return_df_metrics=True):
    #     optm = Adam(lr=1e-3)
    #     self.model.compile(optimizer=optm, loss='categorical_crossentropy', metrics=['accuracy'])
    #     weight_fn = os.path.join(self.output_directory, "weights.h5")
    #     self.model.load_weights(weight_fn)
    #     # self.model.evaluate(x_test, y_test, batch_size=self.batch_size)
    #     y_pred = self.model.predict(x_test)
    #
    #     if return_df_metrics:
    #         y_pred = np.argmax(y_pred, axis=1)
    #         df_metrics = calculate_metrics(y_true, y_pred, 0.0)
    #         return df_metrics
    #     else:
    #         return y_pred

    # def fit(self, x_train, y_train, x_val, y_val, y_true, compile_model=True):
    #     classes = np.unique(y_train)
    #     le = LabelEncoder()
    #     y_ind = le.fit_transform(y_train.ravel())
    #     recip_freq = len(y_train) / (len(le.classes_) *
    #                                  np.bincount(y_ind).astype(np.float64))
    #
    #     class_weight = recip_freq[le.transform(classes)]
    #     class_weights = {x: y for x, y in zip(classes, class_weight)}
    #
    #     y_train = to_categorical(y_train, len(np.unique(y_train)))
    #     y_val = to_categorical(y_val, len(np.unique(y_val)))
    #
    #     factor = 1. / np.cbrt(2)
    #
    #     weight_fn = os.path.join(self.output_directory, "weights.h5")
    #
    #     model_checkpoint = ModelCheckpoint(weight_fn, verbose=1, mode=self.optimization_mode,
    #                                        monitor=self.monitor, save_best_only=True, save_weights_only=True)
    #     reduce_lr = ReduceLROnPlateau(monitor=self.monitor, patience=100, mode=self.optimization_mode,
    #                                   factor=factor, cooldown=0, min_lr=1e-4, verbose=2)
    #     callback_list = [model_checkpoint, reduce_lr]
    #
    #     optm = Adam(lr=self.learning_rate)
    #
    #     if compile_model:
    #         self.model.compile(optimizer=optm, loss='categorical_crossentropy', metrics=['accuracy'])
    #     start_time = time.time()
    #
    #     hist = self.model.fit(x_train, y_train, batch_size=self.batch_size, epochs=self.epochs, callbacks=callback_list,
    #                           sample_weight=class_weights, verbose=2, validation_data=(x_val, y_val))
    #     duration = time.time() - start_time
    #
    #     try:
    #         model = keras.models.load_model(os.path.join(self.output_directory, 'best_model.hdf5'))
    #     except OSError:
    #         model = keras.models.load_model()
    #
    #     y_pred = model.predict(x_val)
    #
    #     # convert the predicted from binary to integer
    #     y_pred = np.argmax(y_pred, axis=1)
    #
    #     save_logs(self.output_directory, hist, y_pred, y_true, duration)
    #
    #     # keras.backend.clear_session()
