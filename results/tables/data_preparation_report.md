
# Data Preparation Report

## Project
Prompt Injection Detection Using Fine-Tuned Transformer Models with a Glass-Box Approach with Explainable AI

## Dataset Source
The dataset used in this preparation stage is the prompt-injection dataset stored in the GitHub repository under `data/raw`.

## Label Meaning
- 0 = SAFE
- 1 = INJECTION

## Raw Dataset Size
- Original train dataset: 546 rows
- Original test dataset: 116 rows

## Final Prepared Dataset Size
- Final train dataset: 436 rows
- Validation dataset: 110 rows
- Final test dataset: 116 rows

## Text Preparation Strategy
The original prompt text was preserved. Aggressive text cleaning was not applied.

The following were preserved:
- punctuation
- symbols
- newlines
- repeated spaces
- unusual characters
- command-style prompt-injection terms
- long prompts

## Model Input Column
The final model input column is:

`text_for_model`

## Target Column
The target column is:

`label`

## Validation Split Method
The validation split was created only from the original training dataset using stratified splitting based on the label column.

The official test set was kept untouched and reserved only for final model evaluation.

## Maximum Sequence Length Decision
The maximum sequence length for later transformer tokenization is:

`MAX_LENGTH = 512`

Long prompts were kept. Truncation will be applied during tokenization in the model fine-tuning stage.

## Final Processed Files
The following files were saved:

- data/processed/clean_train.csv
- data/processed/clean_validation.csv
- data/processed/clean_test.csv
- data/processed/clean_train.parquet
- data/processed/clean_validation.parquet
- data/processed/clean_test.parquet

## Summary
Dataset preparation is complete. The processed train, validation, and test files are ready for model fine-tuning.
