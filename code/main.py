from utils.utils import create_directory
from utils.utils_paper import read_all_datasets, fit_classifier, create_classifier
from utils.utils_paper import DATASET_NAMES
import os
import numpy as np
import sys
import sklearn
import utils
from utils.constants import CLASSIFIERS
from utils.constants import ITERATIONS
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(threadName)s %(message)s",
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
)


if __name__ == "__main__":
    ############################################### main

    # change this directory for your machine

    # root_dir = r"D:\Sciebo\Programmierung\GIT\_Publications\supervised-topology-detection-by-generalized-models\MA_Llopis_Time_Series\npy"

    classifiers = CLASSIFIERS
    # classifiers = ["mlstm-fcn"]
    # classifiers = ["encoder"]
    # classifiers = ["mlp", "resnet", "mlstm-fcn"]
    # classifiers = ["mlstm-fcn-low"]

    dataset_names = DATASET_NAMES
    # dataset_names = ["case_4_real_sim", "case_5_real_sim", "case_6_real_sim"]
    # dataset_names = ["case_2_real", "case_2_real_sim"]
    # dataset_names = ["case_5_sim"]

    # monitor = "accuracy"

    dataset_real = ["case_1_real", "case_2_real", "case_3_real"]
    classifier_exception = ["mlp", "tlenet", "mcnn", "twiesn", "mcdcnn"]
    # classifier_exception = []

    classifiers = [x for x in classifiers if x not in classifier_exception]
    datasets_dict = read_all_datasets(os.path.join(os.getcwd(), "npy"), dataset_names)

    for classifier_name in classifiers:
        logger.info(r"classifier_name: {}".format(classifier_name))

        for dataset_name in dataset_names:
            logger.info(r"dataset_name: {}".format(dataset_name))
            # monitor = "accuracy" if dataset_name in dataset_real else "loss"
            for iter1 in range(ITERATIONS):
                logger.info(r"iter: {}".format(iter1))
                trr = ""
                if iter1 != 0:
                    trr = "_itr_" + str(iter1)
                output_directory = os.path.join(
                    os.getcwd(), "npy", "results2", classifier_name, dataset_name + trr
                )
                logger.info(output_directory)
                create_directory(output_directory)
                fit_classifier(
                    datasets_dict, dataset_name, output_directory, classifier_name
                )
                logger.info(r"DONE")
