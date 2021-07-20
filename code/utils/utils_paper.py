import numpy as np
import sklearn
import os
from scipy.signal import savgol_filter
from scipy.signal import butter
from scipy.signal import wiener
from scipy.signal import medfilt

DATASET_NAMES = ["case_1_real", "case_1_real_sim", "case_1_sim",
                 "case_2_real", "case_2_real_sim", "case_2_sim",
                 "case_3_real", "case_3_real_sim", "case_3_sim"]

EPOCHS = 500
BATCH_SIZE = 16
MIN_ACT = 0.015


def read_all_datasets(root_dir, dataset_names):
    datasets_dict = {}
    # dataset_names_to_sort = []

    for dataset_name in dataset_names:
        root_dir_dataset = os.path.join(root_dir, dataset_name)
        # root_dir_dataset = r"{}/{}/".format(root_dir, dataset_name)

        x_train = np.load(os.path.join(root_dir_dataset, 'X_train.npy'))
        y_train = np.load(os.path.join(root_dir_dataset, 'y_train.npy'))
        x_train, y_train = preprocessing(x_train, y_train)
        x_train = filter_all(x_train, filter_="savgol", window_length=11, polyorder=2,
                             nan_to_num=0.0)

        x_test = np.load(os.path.join(root_dir_dataset, 'X_test.npy'))
        y_test = np.load(os.path.join(root_dir_dataset, 'y_test.npy'))
        x_test, y_test = preprocessing(x_test, y_test)
        x_test = filter_all(x_test, filter_="savgol", window_length=11, polyorder=2,
                            nan_to_num=0.0)

        datasets_dict[dataset_name] = (x_train.copy(), y_train.copy(), x_test.copy(), y_test.copy())
    return datasets_dict


def fit_classifier(datasets_dict, dataset_name, output_directory, classifier_name, fit=True):
    x_train = datasets_dict[dataset_name][0]
    y_train = datasets_dict[dataset_name][1]
    x_test = datasets_dict[dataset_name][2]
    y_test = datasets_dict[dataset_name][3]

    nb_classes = len(np.unique(np.concatenate((y_train, y_test), axis=0)))

    # transform the labels from integers to one hot vectors
    enc = sklearn.preprocessing.OneHotEncoder(categories='auto')
    enc.fit(np.concatenate((y_train, y_test), axis=0).reshape(-1, 1))
    y_train = enc.transform(y_train.reshape(-1, 1)).toarray()
    y_test = enc.transform(y_test.reshape(-1, 1)).toarray()

    # save orignal y because later we will use binary
    y_true = np.argmax(y_test, axis=1)

    if len(x_train.shape) == 2:  # if univariate
        # add a dimension to make it multivariate with one dimension
        x_train = x_train.reshape((x_train.shape[0], x_train.shape[1], 1))
        x_test = x_test.reshape((x_test.shape[0], x_test.shape[1], 1))

    input_shape = x_train.shape[1:]
    classifier = create_classifier(classifier_name, input_shape, nb_classes, output_directory)
    if fit:
        classifier.fit(x_train, y_train, x_test, y_test, y_true)


def calculate_activity(x, window=11, threshold=0.01):
    act = list()
    x = np.nan_to_num(x=x, nan=0.0)
    for dim in range(0, x.shape[0]):
        der1 = savgol_filter(x[dim, :], window_length=window, polyorder=2, deriv=1)
        der2 = savgol_filter(x[dim, :], window_length=window, polyorder=2, deriv=2)
        act.append((abs(der1) > threshold).sum() + (abs(der2) > threshold).sum())
    return act


def preprocessing(x_total, y_total, min_act=MIN_ACT):
    mask = np.ones(len(x_total), dtype=bool)
    for x, y, i in zip(x_total, y_total, range(len(x_total))):
        x = np.nan_to_num(x=x, nan=0.0)
        act = min(calculate_activity(x))
        if act < min_act:
            mask[[i]] = False
    x_total = x_total[mask]
    y_total = y_total[mask]
    return x_total, y_total


def filter_x(x, filter_="savgol", nan_to_num=None, **kwargs):
    for dim in range(0, x.shape[0]):
        if nan_to_num is not None:
            x[dim, :] = np.nan_to_num(x=x[dim, :], nan=nan_to_num)
        if filter_ == "savgol":
            x[dim, :] = savgol_filter(x[dim, :], **kwargs)
        elif filter_ == "med":
            x[dim, :] = medfilt(x[dim, :], **kwargs)
        elif filter_ == "wiener":
            x[dim, :] = wiener(x[dim, :], **kwargs)
        else:
            raise TypeError("{} is not a valid filter".format(filter_))
    return x


def filter_all(x_total, filter_="savgol", **kwargs):
    for dim in range(0, x_total.shape[0]):
        x_total[dim, :, :] = filter_x(x_total[dim, :, :], filter_=filter_, **kwargs)
    return x_total


def create_classifier(classifier_name, input_shape, nb_classes, output_directory, verbose=False):
    if classifier_name == 'fcn':
        from classifiers import fcn
        return fcn.Classifier_FCN(output_directory, input_shape, nb_classes, verbose)
    elif classifier_name == 'mlp':
        from classifiers import mlp
        return mlp.Classifier_MLP(output_directory, input_shape, nb_classes, verbose)
    elif classifier_name == 'resnet':
        from classifiers import resnet
        return resnet.Classifier_RESNET(output_directory, input_shape, nb_classes, verbose)
    elif classifier_name == 'mcnn':
        from classifiers import mcnn
        return mcnn.Classifier_MCNN(output_directory, verbose)
    elif classifier_name == 'tlenet':
        from classifiers import tlenet
        return tlenet.Classifier_TLENET(output_directory, verbose)
    elif classifier_name == 'twiesn':
        from classifiers import twiesn
        return twiesn.Classifier_TWIESN(output_directory, verbose)
    elif classifier_name == 'encoder':
        from classifiers import encoder
        return encoder.Classifier_ENCODER(output_directory, input_shape, nb_classes, verbose)
    elif classifier_name == 'mcdcnn':
        from classifiers import mcdcnn
        return mcdcnn.Classifier_MCDCNN(output_directory, input_shape, nb_classes, verbose)
    elif classifier_name == 'cnn':  # Time-CNN
        from classifiers import cnn
        return cnn.Classifier_CNN(output_directory, input_shape, nb_classes, verbose)
    elif classifier_name == 'inception':
        from classifiers import inception
        return inception.Classifier_INCEPTION(output_directory, input_shape, nb_classes, verbose)
    elif classifier_name == "mlstm-fcn":
        from classifiers import mlstm_fcn
        return mlstm_fcn.ClassifierMlstmFcn(output_directory, input_shape, nb_classes, verbose)
    elif classifier_name == "malstm-fcn":
        from classifiers import malstm_fcn
        return malstm_fcn.ClassifierMalstmFcn(output_directory, input_shape, nb_classes, verbose)
    elif classifier_name == "lstm-fcn":
        from classifiers import lstm_fcn
        return lstm_fcn.ClassifierLstmFcn(output_directory, input_shape, nb_classes, verbose)
    elif classifier_name == "alstm-fcn":
        from classifiers import alstm_fcn
        return alstm_fcn.ClassifierAlstmFcn(output_directory, input_shape, nb_classes, verbose)
    elif classifier_name == "mlstm-fcn-low":
        from classifiers import mlstm_fcn_low
        return mlstm_fcn_low.ClassifierMlstmFcnLow(output_directory, input_shape, nb_classes, verbose)
    elif classifier_name == "mlstm-fcn2":
        from classifiers import mlstm_fcn_low
        return mlstm_fcn_low.ClassifierMlstmFcnLow(output_directory, input_shape, nb_classes, verbose)
    elif classifier_name == 'tsfresh_rfc':
        from classifiers import tsfresh_rfc
        return tsfresh_rfc.TsfreshRfc(output_directory, input_shape, nb_classes, verbose)