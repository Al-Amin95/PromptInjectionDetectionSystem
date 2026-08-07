# Prompt Injection Detection Using Fine-Tuned Transformer Models with a Glass-Box Approach with Explainable AI

A machine learning-based prompt injection detection system for Large Language Model (LLM) applications. The system classifies input prompts as either SAFE or INJECTION using transformer-based text classification models, and provides explainable outputs using SHAP-based token-level explanations.

## Author & Supervisor

- **Author:** Md. Al Amin
- **Supervisor:** Mohammad Abdullah Awais

## Aim

To build an explainable prompt injection detection system by fine-tuning transformer-based language models and evaluating their performance on a labelled prompt injection dataset, supporting safer LLM-integrated applications by identifying malicious prompts before they reach an LLM.

## Objectives

- Prepare and analyse a labelled prompt injection dataset for binary text classification.
- Fine-tune transformer-based models for SAFE/INJECTION classification.
- Compare the performance of selected transformer models using standard classification metrics.
- Apply SHAP explainability to identify important tokens influencing model predictions.
- Evaluate both predictive performance and explanation quality.
- Develop a simple prototype interface for prompt injection detection.

## Classification Task

Binary classification with two classes:

| Label | Class Name | Meaning |
|-------|------------|---------|
| 0 | SAFE | Normal or benign prompt |
| 1 | INJECTION | Prompt injection or malicious instruction |

## Dataset

Combined from three publicly available sources:

- deepset/prompt-injections — https://huggingface.co/datasets/deepset/prompt-injections/tree/main/data
- neuralchemy/Prompt-injection-dataset — https://huggingface.co/datasets/neuralchemy/Prompt-injection-dataset
- S-Labs/prompt-injection-dataset — https://huggingface.co/datasets/S-Labs/prompt-injection-dataset

Raw and processed (cleaned/combined) versions used in this project are available in the `datasets/` folder of this repository.

## Technologies Used

Python, Flask, HuggingFace Transformers, PyTorch, SHAP, Pandas, NumPy, HTML/CSS/JavaScript, Jupyter Notebook, Git and Git LFS, GitHub.

## Getting Started

### Option 1: Clone with Git LFS (recommended)

The trained model file (model.safetensors, ~255MB) is stored using Git LFS. Downloading a plain ZIP from GitHub will not include the actual model file, only a small pointer file — so cloning is required.

1. Install Git LFS if not already installed: https://git-lfs.github.com
2. Clone the repository:

```bash
git lfs install
git clone https://github.com/Al-Amin95/PromptInjectionDetectionSystem.git
```

Git LFS will automatically download the real model files during clone.

### Option 2: Downloaded as ZIP

If the repository was downloaded as a ZIP instead of cloned, the `webapp/models/model.safetensors` file will be broken or empty (Git LFS files are not included in ZIP downloads). To fix this:

1. Download these 4 files from Google Drive: config.json, model.safetensors, tokenizer_config.json, tokenizer.json
   https://drive.google.com/drive/u/0/folders/1Q4Yuq7c-kTWN5O8V81oQNLWS6UI2qPem
2. Replace these 4 files inside `webapp/models/` with the downloaded ones (do not touch `app_config.json` — it downloads correctly with the ZIP and does not need replacing).

### Running the Web App

Navigate into the webapp folder:

```bash
cd webapp
```

Create and activate a virtual environment:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies and run the app:

```bash
pip install -r requirements.txt
python app.py
```

Open the browser link shown in the terminal to use the prompt injection detection interface.

## Project Documents

Full project report, poster, and supporting images/screenshots are shared via Google Drive:

https://drive.google.com/drive/u/0/folders/1nh1DLrc4ZCj0WEOpY3nWANDUCrcIXyaD
