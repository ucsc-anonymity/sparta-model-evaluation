# performance

Code to get performance numbers for different model types.

## Contents
- data, directory for enron and seattle datasets
    - enron, email metadata from enron corpus
        - clean.csv, datasets cleaned of incorrect, missing values, email
          contents
        - raw.csv, the raw datasets
        - users.csv, emails corresponding to the user indices
    - seattle, email metadata from seattle city government.
        - clean.csv, datasets cleaned of incorrect, missing values, email
          contents
        - raw.csv, the raw datasets
        - senders_processed.csv, clean dataset processed so that for each
          sender we have their messages grouped and who received them
        - users.csv, emails corresponding to the user indices
- data_clean
    - clean.py, cleans the datasets and processes them into a usable form
- src, main logic used in experiment.py
