# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 14:52:11 2019

@author: fst-vev
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels


def y_2d_to_1d(y_2d):
    y_1d = np.zeros((y_2d.shape[0], 1), dtype=np.uint8)
    for i in range(y_2d.shape[0]):
        label = np.argmax(y_2d[i])
        y_1d[i] = label
    return y_1d


def y_argmax_2d(y):
    y_report = np.zeros((y.shape[0], y.shape[1]), dtype=np.uint8)
    for i in range(y_report.shape[0]):
        label = np.argmax(y[i])
        y_report[i][label] = 1
    return y_report


def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'
        
    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    # Only use the labels that appear in the data
    classes = classes[unique_labels(y_true, y_pred)]
    
    """uncoment if print not as plot"""
    if normalize:
        cm = (cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]) *100
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center", size='large',
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    fig.savefig('cm.png', dpi=300, bbox_inches="tight")
    return ax, cm
