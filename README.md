Prompt Injection Detection Using Fine-Tuned Transformer Models: A Glass-Box Approach with Explainable AI
The project focuses on building a machine learning-based prompt injection detection system for Large Language Model (LLM) applications. The system is designed to classify input prompts as either SAFE or INJECTION using transformer-based text classification models.
The main objective is to develop an accurate and interpretable binary text classifier that can detect prompt injection attempts and provide explainable outputs using SHAP-based token-level explanations.

Project Aim
The aim of this project is to build an explainable prompt injection detection system by fine-tuning transformer-based language models and evaluating their performance on a labelled prompt injection dataset.
The system is intended to support safer LLM-integrated applications by identifying potentially malicious prompts before they are processed by an LLM.

Research Objectives
The main objectives of this project are:
To prepare and analyse a labelled prompt injection dataset for binary text classification.
To fine-tune transformer-based models for SAFE/INJECTION classification.
To compare the performance of selected transformer models using standard classification metrics.
To apply SHAP explainability to identify important tokens influencing model predictions.
To evaluate both predictive performance and explanation quality.
To develop a simple prototype interface for prompt injection detection.

Classification Task
This project uses a binary classification approach.
Label
Class Name
Meaning
0
SAFE
Normal or benign prompt
1
INJECTION
Prompt injection or malicious instruction


Dataset
The project uses a prompt injection dataset in Parquet format.
Current raw dataset files are stored in:
data/raw/

Expected files:
train-00000-of-00001-9564e8b05b4757ab.parquet
test-00000-of-00001-701d16158af87368.parquet

Initial dataset summary:
Split
Rows
Columns
Train
546
text, label
Test
116
text, label
Total
662
text, label


Models
The project is planned to use and compare transformer-based models, including:
DistilBERT
RoBERTa
SecBERT / cybersecurity-domain BERT variant
These models will be fine-tuned for binary text classification.

Evaluation Metrics
The classification models will be evaluated using:
Accuracy
Precision
Recall
F1-score
Confusion matrix
AUC-ROC, where applicable
For prompt injection detection, recall is especially important because false negatives may allow malicious prompts to pass through the system. Precision is also important because too many false positives may incorrectly block safe user prompts.

Explainable AI
The project uses SHAP for explainability.
The explainability stage aims to show which words or tokens contributed most to the model prediction. This supports the glass-box aim of the project by making the detector’s decision more interpretable.
token-level importance scores
SHAP-highlighted prompt examples
explanation comparison between SAFE and INJECTION predictions
sufficiency and comprehensiveness-based explanation quality analysis

Repository Structure
PromptInjectionDetectionSystem/
│
├── data/
│   ├── raw/
│   │   └── original dataset files
│   └── processed/
│       └── cleaned and prepared dataset files
│
├── docs/
│   └── project documentation and methodology notes
│
├── models/
│   └── saved model information or checkpoint notes
│
├── notebooks/
│   ├── 00_environment_check.ipynb
│   └── 01_dataset_preparation.ipynb
│
├── results/
│   ├── figures/
│   │   └── graphs and visualisations
│   └── tables/
│       └── dataset summaries and evaluation tables
│
├── screenshots/
│   └── project screenshots and evidence
│
├── src/
│   └── reusable Python scripts
│
├── webapp/
│   └── prototype web application files
│
├── requirements.txt
├── .gitignore
└── README.md


Environment Setup
This project is developed using Python.
Recommended environment:
Python 3.10+
Google Colab or local Python environment
GPU support recommended for transformer fine-tuning
Install required libraries using:
pip install -r requirements.txt

Main Python libraries:
pandas
numpy
pyarrow
openpyxl
matplotlib
seaborn
scikit-learn
datasets
transformers
torch
evaluate
accelerate
shap
tqdm


Current Project Stage
Current stage:
Data Analysis and Dataset Preparation

Completed or planned tasks in this stage:
project folder structure created
raw dataset folder prepared
dataset files added
dataset loading notebook prepared
data quality checks planned
class distribution analysis planned
text length analysis planned
cleaned dataset preparation planned

Planned Workflow
1. Load raw dataset
2. Inspect dataset structure
3. Verify labels
4. Check missing values
5. Check duplicate records
6. Analyse class distribution
7. Analyse text length
8. Clean and standardise text
9. Create train, validation, and test splits
10. Save processed dataset
11. Fine-tune transformer models
12. Evaluate model performance
13. Apply SHAP explainability
14. Build prototype detection interface


Project Output
The final system is expected to provide:
prompt classification result: SAFE or INJECTION
confidence score
model evaluation results
explanation of important tokens using SHAP
simple web-based prototype for demonstration

Academic Context
This repository is part of an MSc Cyber Security dissertation project. The work focuses on prompt injection detection, transformer-based NLP classification, and explainable AI for safer LLM-integrated systems.

Author
Al-Amin
MSc Cyber Security Student
GitHub: Al-Amin95

