# RASEL: Dairy vs Draft Cattle Classifier

This repository contains a trained ensemble model, **RASEL** (Robust Animal SNP Ensemble Learner), which classifies cattle populations into Dairy or Draft categories based on SNP genotype data.

## Model Overview

**RASEL** uses an ensemble approach combining:

* Random Forest
* Gradient Boosting
* XGBoost
* Logistic Regression

The model was trained on SNP genotypes from various cattle breeds with known dairy/draft classification. It can be used to classify other cattle populations using the same SNP set.

## Repository Structure

```
├── model/
│   ├── rasel_ensemble_model.joblib          # Trained RASEL ensemble model
│   ├── feature_names.txt                    # SNP names used by the model
│   ├── breed_classes.txt                    # Classification categories (e.g., DR, ML)
│   ├── example_classify.py                  # Example script to use RASEL
│   └── README.md                            # Usage instructions
├── scripts/
│   ├── train_model.py                       # Script used to train RASEL
│   └── evaluate_model.py                    # Script to evaluate RASEL
└── README.md                                # This file
```

## Installation

To use **RASEL**, install the required packages:

```bash
pip install pandas numpy scikit-learn xgboost joblib
```

## Usage

### Quick Start

1. Clone the repository:

```bash
git clone https://github.com/your-username/rasel-cattle-classifier.git
cd rasel-cattle-classifier
```

2. Run the example script on your SNP genotype data:

```bash
python model/example_classify.py --input your_data.csv --output predictions.csv
```

### Input Data Format

Input CSV should have:

* Column `Individuals` with sample or breed IDs
* Remaining columns as SNP genotype data (coded as 0, 1, 2)
* SNP columns must match those in `model/feature_names.txt`

Example structure:

```
Individuals,BovineHD0100034532,BovineHD4100000740,BovineHD0200004201,...
Sample1,0,1,2,...
Sample2,1,1,0,...
```

### Output

The script outputs:

* Original sample IDs
* Predicted classification (`DR` for Draft, `ML` for Dairy)

## Citation

If you use this model in your research, please cite:

**Kanaka KK, Ganguly I, Singh S, et al. (2025). *RASEL: An ensemble model for selection of core SNPs and its application for identification and classification of cattle breeds.* Preprint at Research Square. [https://doi.org/10.21203/rs.3.rs-6048799/v1](https://doi.org/10.21203/rs.3.rs-6048799/v1)**

## Contact

For support or inquiries, contact: **[Kanaka KK](mail to:kkokay07@gmail.com)**


