# Data Sharing Platform for a Research Group

This is a dissertation project.

For more information see in my portfolio: [http://www.livia.geo-blog.com/msc-thesis.html](http://www.livia.geo-blog.com/msc-thesis.html)



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

### Change configuration file

- Open ```write_config.py``` file in current folder and change (1) database configuration, (2) data input path and (3) data output path
- Run ```python write_config.py```
- When using Oracle make the changes in ```data-display/models.py``` suggested in the comments


### Ingest Data 

**Example for file Greenland_1000DEM.tif located in data input folder**

```python add_dataset.py Greenland_1000_DEM.tif dem 2017-06-26```


**Add another layer to the dataset with id 1:**


```python add_layer.py 1 Greenland_1000_rate.tif rate 2017-06-27```

### For help type:

```
python add_dataset.py --help
python add_layer.py --help
```


### Run Webapplication:

```
python app.py
```

Access on ```localhost:5000```

### Run web API:

```
python api.py
```

Access on ```localhost:5002```


