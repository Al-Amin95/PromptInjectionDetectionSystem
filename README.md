# Prompt Injection Detection Using Fine-Tuned Transformer Models with a Glass-Box Approach with Explainable AI

A machine learning-based prompt injection detection system for Large Language Model (LLM) applications. The system is designed to classify input prompts as either **SAFE** or **INJECTION** using transformer-based text classification models.

The main objective is to develop an accurate and interpretable binary text classifier that can detect prompt injection attempts and provide explainable outputs using SHAP-based token-level explanations.

---

## Aim

The aim of this project is to build an explainable prompt injection detection system by fine-tuning transformer-based language models and evaluating their performance on a labelled prompt injection dataset.

The system is intended to support safer LLM-integrated applications by identifying potentially malicious prompts before they are processed by an LLM.

---

## Objectives

* Prepare and analyse a labelled prompt injection dataset for binary text classification.
* Fine-tune transformer-based models for **SAFE/INJECTION** classification.
* Compare the performance of selected transformer models using standard classification metrics.
* Apply SHAP explainability to identify important tokens influencing model predictions.
* Evaluate both predictive performance and explanation quality.
* Develop a simple prototype interface for prompt injection detection.

---

## Classification Task

This project uses a binary classification approach.

| Label | Class Name | Meaning                                   |
| ----- | ---------- | ----------------------------------------- |
| `0`   | SAFE       | Normal or benign prompt                   |
| `1`   | INJECTION  | Prompt injection or malicious instruction |

---

## Dataset

The project uses a prompt injection dataset in Parquet format.

Current raw dataset files are stored in:

```text
data/raw/
```

Expected files:

```text
train-00000-of-00001-9564e8b05b4757ab.parquet
test-00000-of-00001-701d16158af87368.parquet
```

Initial dataset summary:

| Split | Rows | Columns     |
| ----- | ---: | ----------- |
| Train |  546 | text, label |
| Test  |  116 | text, label |
| Total |  662 | text, label |

---

## Models

The project is planned to use and compare transformer-based models, including:

* **DistilBERT**
* **RoBERTa**
* **SecBERT / cybersecurity-domain BERT variant**

These models will be fine-tuned for binary text classification.

---

## Evaluation Metrics

The classification models will be evaluated using:

* Accuracy
* Precision
* Recall
* F1-score
* Confusion matrix
* AUC-ROC, where applicable

For prompt injection detection, **recall** is especially important because false negatives may allow malicious prompts to pass through the system. **Precision** is also important because too many false positives may incorrectly block safe user prompts.

---

## Explainable AI

The project uses **SHAP** for explainability.

The explainability stage aims to show which words or tokens contributed most to the model prediction. This supports the glass-box aim of the project by making the detector’s decision more interpretable.

Planned explanation outputs include:

* Token-level importance scores
* SHAP-highlighted prompt examples
* Explanation comparison between SAFE and INJECTION predictions
* Sufficiency and comprehensiveness-based explanation quality analysis

---

## Project Structure

```text
PromptInjectionDetectionSystem/
│
├── data/
│   ├── raw/                 # Original dataset files
│   └── processed/           # Cleaned and prepared dataset files
│
├── docs/                    # Project documentation and methodology notes
│
├── models/                  # Saved model information or checkpoint notes
│
├── notebooks/
│   ├── 00_environment_check.ipynb
│   └── 01_dataset_preparation.ipynb
│
├── results/
│   ├── figures/             # Graphs and visualisations
│   └── tables/              # Dataset summaries and evaluation tables
│
├── screenshots/             # Project screenshots and evidence
│
├── src/                     # Reusable Python scripts
│
├── webapp/                  # Prototype web application files
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Environment Setup

This project is developed using Python.

Recommended environment:

* Python 3.10+
* Google Colab or local Python environment
* GPU support recommended for transformer fine-tuning

Install required libraries using:

```bash
pip install -r requirements.txt
```

Main Python libraries:

```text
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
```

---

## Current Project Stage

Current stage:

```text
Data Analysis and Dataset Preparation
```

Completed or planned tasks in this stage:

* [x] Project folder structure created
* [x] Raw dataset folder prepared
* [ ] Dataset files added
* [x] Dataset loading notebook prepared
* [ ] Data quality checks completed
* [ ] Class distribution analysis completed
* [ ] Text length analysis completed
* [ ] Cleaned dataset prepared

---

## Planned Workflow

```text
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
```

---

## Project Output

The final system is expected to provide:

* Prompt classification result: **SAFE** or **INJECTION**
* Confidence score
* Model evaluation results
* Explanation of important tokens using SHAP
* Simple web-based prototype for demonstration

---

## Academic Context

This repository is part of an MSc Cyber Security dissertation project. The work focuses on prompt injection detection, transformer-based NLP classification, and explainable AI for safer LLM-integrated systems.

---

## Author

**Al-Amin**
MSc Cyber Security Student
GitHub: [Al-Amin95](https://github.com/Al-Amin95)

---

## Note

This repository is part of an academic dissertation project. Results are reported only after experiments are completed and verified.
