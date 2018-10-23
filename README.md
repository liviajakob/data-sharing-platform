# Data Sharing Platform for a Research Group

This is a dissertation project. For more information see in my portfolio: [http://www.livia.geo-blog.com/msc-thesis.html](http://www.livia.geo-blog.com/msc-thesis.html)



# Installation guide

Tested with Python version 3.6.4

Using a virtual environment for python (e.g. virtualenv) is recommended.

### Clone the repository

```git init```

```git clone https://github.com/liviajakob/data-sharing-platform```


### Change to folder

```cd data-sharing-platform/data-sharing```


### Install dependencies

```pip3 install -r requirements.txt --user```

You might have to follow [this](https://pypi.org/project/GDAL/) (https://pypi.org/project/GDAL/) installation guide to install GDAL.

### Generate configuration file

- Run ```python write_config.py```

**Optional**

- Open ```write_config.py``` file in current folder and change database configuration, data input path, data output path or other settings, run it as described above
- When using Oracle make the changes in ```data-display/models.py``` suggested in the comments


### Ingest Data 

The software comes with two example data files in ```data-sharing/data/input/```

**Example for file Greenland_1000DEM.tif located in data input folder**

```python add_dataset.py dem.tif dem 2017-06-26```


**Add another layer to the dataset with id 1:**


```python add_layer.py 1 rate.tif rate 2017-06-27```

### For help type:

```
python add_dataset.py --help
python add_layer.py --help
```


### Run web application:

```
python app.py
```

Access on ```localhost:5000```

### Run web API:

```
python api.py
```

Access on ```localhost:5002```


