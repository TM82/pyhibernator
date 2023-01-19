# pyhibernator

Corresponding paper: https://doi.org/10.1016/j.joi.2023.101378

#### Introduction

This is the pyhibernator toolkit developed for extracting slow-cited papers in science from bibliometric data. This toolkit covers 11 major slow-cited papers extraction methods.

### Requirements

#### Slow-cited paper extraction
Python 3.8, pandas, numpy

#### Analysis
powerlaw 1.4.4(https://pypi.org/project/powerlaw/)

### Usage

#### Import Module

```
git clone git@github.com:TM82/pyhibernator.git
pip install .
```
or
```
pip install git+ssh://git@github.com/TM82/pyhibernator.git
```

Then, you can use
```
import pyhibernator

pyhibernator.Naive.extract(
    c = [0,0,1,0,0,2,1,...,20,18],
    s = 5,
    cs = 2,
    ca = 100
)
-> True
```

For more detail usage, see notebooks/1_ExtractHibernator.ipynb

### Analysis

#### Prepare Dataset

Use Scopus API(https://dev.elsevier.com/) or buld dataset from Elsevier to obtain raw dataset

The following columns are required to extract all the hibernators.

```
c_history: list[int]
- Required in any methods
- Citation history from publication to 2020 using reference data for each publication
- ex) [0,1,0,2,1,0,5,2,3,10,15,13,22]

subjs: list[str]
- Required in "DNIC" and "Quartile"
- All Science Journal Classification Codes for published journal
- ex) ['CHEM','MATH','PHYS']

year: int
- Required in "DNIC" and "Quartile"
- Publication year
- ex) 2008
```

#### Main Analysis

- 1_ExtractHibernator.ipynb
    - Extract slow-cited papers for 11 methods
    - 10 times montecarlo simulations

- 2_Analysis.ipynb
    - Compare bibliometric features of hibernators extracted in 1_ExtractHibernator.ipynb


#### Citation

> Miura, T., Asatani, K. & Sakata, I. (2023). Revisiting the uniformity and inconsistency of slow-cited papers in science. Journal of Informetrics, 17(1), 101378. https://doi.org/10.1016/j.joi.2023.101378


## License
MIT

```
Contact: Takahiro Miura, miura@ipr-ctr.t.u-tokyo.ac.jp
```
