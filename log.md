# Project Log

## [2026-04-25T15:50:19+02:00] Data Generation Update
- **Attempted**: Overwrite `generate_data.py` to create 2,000 rows with specific columns (`Genre_Pop`, `Is_Holiday`, `Marketing_Spend`, `Viewership`) and defined true causal effects (+5M for marketing, +12M for holiday). Ran the script to generate `netflix_data.csv`.
- **Output**: 
  ```
  Successfully generated netflix_data.csv with 2,000 rows.
  ```
- **Learned/Changed**: The new dataset was successfully generated with the precise structure required for the next phase.

## [2026-04-25T16:46:34+02:00] Workflow Update & Git Push
- **Attempted**: Acknowledge the complete strict workflow (including `git push origin main`) and push the previous commit.
- **Output**: Workflow adopted.
- **Learned/Changed**: All future steps will end with writing to log.md, git add ., git commit, and git push.

## [2026-04-25T16:47:37+02:00] Phase 2 Execution & Debugging
- **Attempted**: Created `generate_data.py` with specific causal rules (confounder: holiday bias, marketing dependency) to generate 2,000 biased Netflix samples. Executed the script.
- **Output**:
  ```
  UnicodeEncodeError on Windows due to checkmark emoji in print statement.
  Removed emoji and reran successfully:
  Success: 'netflix_data.csv' created with 2000 rows.
  ```
- **Learned/Changed**: The dataset generated successfully embodies the intended hidden bias (where holiday season heavily influences marketing spend and viewership). Fixed a minor Windows terminal encoding error by removing a Unicode checkmark emoji from the print statement.

## [2026-04-25T17:03:50+02:00] Phase 3: Causal Analysis
- **Attempted**: Created and executed `causal_analysis.py` to calculate the Naive correlation effect and the Causal ATE using DoWhy.
- **Output**:
  ```
  NAIVE LIFT (Correlation): 11.07 Million Hours
  CAUSAL ATE (True Impact): 5.42 Million Hours
  ```
- **Learned/Changed**: The causal analysis successfully removed the confounding bias. The Naive Lift was highly inflated (11.07) because it grouped the holiday effect in with marketing spend. By conditioning on the confounders, the Causal ATE dropped to 5.42, which is remarkably close to our known "True" generated effect of 5.0.
