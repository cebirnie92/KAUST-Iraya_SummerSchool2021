<img src="figures/logo.jpg">

Welcome to KAUST and Iraya's virtual summer school on Utilising unstructured data in geoscience. Over three days, we will give 
you an introduction to what is Natural Language Processing, how the geoscience industry is leveraging it, and the new
avenues that are up for exploration. 

In this repository we have shared our codes for the tutorials as well as guidance on setting this up on your 
workstation. The lectures which accompany the tutorials will be available as video recordings in the near future.

Getting started on your machine
-------------------------------

To create the environment which has all the necessary python packages pre-installed, in your terminal in this folder 
directory run:

`conda env create -f environment.yml`

This creates a conda environment named "mlg_summer_school". Before we begin you will need to activate this environment.
To do so, in your terminal run the command:

`conda activate mlg_summer_school`


Prerequisites
-------------
All participants are expected to have a basic knowledge of python. 

Material
--------

| Day   | Tutorial (Github) | Tutorial (Colab) | Videos |
|-----------|------------------|------------------|------------------|
| 1: Introduction to NLP | [Link](notebooks/day1_word_embeddings.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cebirnie92/KAUST-Iraya_SummerSchool2021/blob/main/notebooks/day1_word_embeddings.ipynb)  | - | 
| 2: Active Learning | - | - | - | 
| 3: Attention and Transformers | - | -  | - | 


Limitations on Use of Test Data
--------------------------------

The sample test data used for this experiment is extracted from ED2K, an initiative between Iraya Energies and European Association of Geoscientists and Engineer (EAGE) to process the EarthDoc database, using the latest in machine learning techniques to read the earth better.

The API access will be available until 17th June 2021 and is available for academic use only. Thank you in advance for deletion of downloaded dataset after the completion of the class. For the utilization of data beyond the duration of this Summer School or use of bigger ED2K dataset, pls send an email request to info@irayaenergies.com.


About us
--------
This virtual school has been organised in collaboration between King Abdullah University of Science and Technology 
(KAUST) and Iraya Energies.
