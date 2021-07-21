# Deep-learning-supervised-topology-detection
Journal: Deep learning supervised topology detection of building energy systems by generated time series of generic grey-box models


## Examples

In the folder `code` the code for using the classifier is included. `main.py` is an example of the use of the code. The code for the classifiers `ALSTM-FCN`, `LSTM-FCN`, `MALSTM-FCN` and `MLSTM-FCN` are taken from paper `IsmailFawaz.2019` and have been adapted accordingly for our use case.  The code for the remaining classifiers is taken from papers `IsmailFawaz.2019` and `Fawaz.11.09.2019` and has also been adapted to our use case accordingly. The `utils` files were also taken from paper `IsmailFawaz.2019` and adapted accordingly.

In folder `data_set` all nine data sets are saved (three cases (case 1-3) with training and testing with real data (real), training and testing with simulated data (sim) and training with simulated data and testing with real data (real_sim). Each record is stored in a `.npy`and `.pkl` file. These can be read with the help of python (packages `numpy` and `pickle`). The pickle files are in the format matching [sktime](https://www.sktime.org/). With the classifiers existing in `sktime`, these data sets can be used. `sktime` has several methods to convert the data sets suitably into other formats.

## Used Paper

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
