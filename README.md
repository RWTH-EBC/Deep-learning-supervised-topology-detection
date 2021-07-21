# Deep-learning-supervised-topology-detection

Journal: Deep learning supervised topology detection of building energy systems by generated time series of generic grey-box models

## Contact

If you have any questions about the code, please feel free to contact fstinner@eonerc.rwth-aachen.de.

## Examples

In the folder `code` the code for using the classifier is included. `main.py` is an example of the use of the code. The code for the classifiers `ALSTM-FCN`, `LSTM-FCN`, `MALSTM-FCN` and `MLSTM-FCN` are taken from paper `IsmailFawaz.2019` and have been adapted accordingly for our use case.  The code for the remaining classifiers is taken from papers `IsmailFawaz.2019` and `Fawaz.11.09.2019` and has also been adapted to our use case accordingly. The `utils` files were also taken from paper `IsmailFawaz.2019` and adapted accordingly.

In folder `data_set` all nine data sets are saved (three cases (case 1-3) with training and testing with real data (real), training and testing with simulated data (sim) and training with simulated data and testing with real data (real_sim). Each record is stored in a `.npy`and `.pkl` file. These can be read with the help of python (packages `numpy` and `pickle`). The pickle files are in the format matching [sktime](https://www.sktime.org/). With the classifiers existing in `sktime`, these data sets can be used. `sktime` has several methods to convert the data sets suitably into other formats. The datasets are divided into `X_train`, `X_test`, `y_train` and `y_test`. These can be used directly with any algorithm.

The code for generating generic data from simulation models is under revision for better usage but is included in folder `code_simulation` with small examples.

## Used paper for deep learning

```bibtex
@article{IsmailFawaz.2019,
 author = {{Ismail Fawaz}, Hassan and Forestier, Germain and Weber, Jonathan and Idoumghar, Lhassane and Muller, Pierre-Alain},
 abstract = {Data Mining and Knowledge Discovery, https://doi.org/10.1007/s10618-019-00619-1},
 year = {2019},
 title = {Deep learning for time series classification: a review},
 pages = {917--963},
 volume = {33},
 number = {4},
 journal = {Data Mining and Knowledge Discovery}}
```

```bibtex
@booklet{Karim.2018b,
 author = {Karim, Fazle and Majumdar, Somshubra and Darabi, Houshang and Harford, Samuel},
 year = {2018},
 title = {Multivariate LSTM-FCNs for Time Series Classification}}
```

```bibtex
@booklet{Fawaz.11.09.2019,
 author = {{Ismail Fawaz}, Hassan and Lucas, Benjamin and Forestier, Germain and Pelletier, Charlotte and Schmidt, Daniel F. and Weber, Jonathan and Webb, Geoffrey I. and Idoumghar, Lhassane and Muller, Pierre-Alain and Petitjean, Fran{\c{c}}ois},
 year = {2019},
 title = {InceptionTime: Finding AlexNet for Time Series Classification}}
```

## Used paper for simulation

```bibtex
@incollection{Muller.2016,
 author = {M{\"u}ller, Dirk and Lauster, Moritz and Constantin, Ana and Fuchs, Marcus and Remmen, Peter},
 title = {AixLib - An Open-Source Modelica Library within the IEA-EBC Annex 60 Framework},
 urldate = {21.08.2018},
 pages = {3--9},
 booktitle = {BauSim 2016},
 year = {September 2016}}
```

```bibtex
@inproceedings{Stinner.2019c,
 author = {Stinner, Florian and Yang, Yingying and Schreiber, Thomas and Bode, Gerrit and Baranski, Marc and M{\"u}ller, Dirk},
 title = {Generating Generic Data Sets for Machine Learning Applications in Building Services Using Standardized Time Series Data},
 publisher = {{International Association for Automation and Robotics in Construction (IAARC)}},
 series = {Proceedings of the International Symposium on Automation and Robotics in Construction (IAARC)},
 editor = {Al-Hussein, Mohamed},
 booktitle = {Proceedings of the 36th International Symposium on Automation and Robotics in Construction (ISARC)},
 year = {2019}}
```
