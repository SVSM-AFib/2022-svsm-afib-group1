# Identifying Atrial Fibrillation with Stepping Windows

## Project Description

This repository contains the code and resources for group 1's atrial fibrillation (AFib) research from Summer Ventures in Science and Mathematics 2022 at UNC Wilmington. The project focuses on the analysis of physiological data, specifically ECG or RR interval data, to develop and evaluate machine learning models for the detection or classification of atrial fibrillation. It includes various Jupyter notebooks for data extraction, feature engineering, model training, and performance evaluation.

## Features

- **Data Extraction**: Notebooks for extracting relevant features from raw physiological data, including different windowing and stepping strategies.
- **Feature Engineering**: Scripts to create various features, such as statistical measures (mean, variance, standard deviation, IQR, etc.), and transition proportions from RR intervals.
- **Machine Learning Models**: Implementation and testing of various classification models, including tree-based classifiers (Decision Trees, Random Forests, Boosting) and other non-tree classifiers.
- **Model Tuning and Evaluation**: Notebooks dedicated to hyperparameter tuning and comprehensive evaluation of model performance using techniques like cross-validation and permutation importance.
- **Visualization**: Scripts for generating plots to visualize data characteristics, feature distributions, and model performance.

## Installation

This project is written in Python and requires a virtual environment. The project exclusively uses `uv` for dependency management. After cloning the repository, run the following command to install the dependencies and set up the environment:

    ```bash
    uv sync
    ```

## Usage

Most of the project's functionality is demonstrated within the Jupyter notebooks. Development work is best done within the notebooks feature of an IDE like VS Code. Open the `.ipynb` files located in `extraction_experiment.ipynb`, `rr_int_extraction.ipynb`, `models/`, `testing/`, etc., and run the cells.

## Project Structure

-   `extraction_experiment.ipynb`, `gpu_extraction.ipynb`, `rr_int_extraction.ipynb`: Notebooks for data extraction processes.
-   `mit-bih-raw/`: Contains raw MIT-BIH Arrhythmia Database files.
-   `model_testing.ipynb`: General notebook for model testing.
-   `models/`: Contains various subdirectories for different classification models and feature selection techniques.
    -   `cov_classifiers.ipynb`, `iqr_classifiers.ipynb`, `mad_classifiers.ipynb`, `range_classifiers.ipynb`, `rmean_var_classifiers.ipynb`, `rmssd_classifiers.ipynb`, `rr_var_classifiers.ipynb`, `std_classifiers.ipynb`, `transition_proportions_classifiers.ipynb`: Specific classifier implementations based on different features.
    -   `feature_selection/`: Notebooks related to feature selection (e.g., `rfecv.ipynb`).
    -   `jshs/`: Contains notebooks and plots related to specific model testing or analysis.
    -   `perm_importance/`: Notebooks for permutation importance analysis (e.g., `catboost.ipynb`).
    -   `subsets/`: Contains notebooks exploring different model subsets (e.g., `bagging.ipynb`, `boosting_1.ipynb`, `decision_tree.ipynb`, `random_forest.ipynb`).
    -   `tuned/`: Notebooks for tuned models (e.g., `decision_tree.ipynb`).
-   `plots/`: Directory for various plots generated during the research, organized by checkpoints, final results, and weekly progress.
-   `testing/`: Contains notebooks for various testing purposes, including different data extraction and feature extraction methodologies.
-   `SVSM_Research_Project.pdf`: The associated research paper for this project.

## Further Information

For more detailed information regarding the methodologies, experiments, and results of this project, please refer to the artifacts in the `docs/` directory.