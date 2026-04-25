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

## [2026-04-25T17:12:04+02:00] Phase 4: Robustness Tests
- **Attempted**: Updated `causal_analysis.py` to run three DoWhy refutation tests: Placebo Treatment, Random Common Cause, and Data Subset. Executed the script.
- **Output**: The script successfully completed all refutations without error.
- **Learned/Changed**: The model passed all tests, validating our causal ATE:
  1. **Placebo Treatment**: Effect dropped to near zero, indicating no hidden spurious associations were misidentified as causal.
  2. **Random Common Cause**: Effect remained stable, indicating the model is robust against independent unobserved confounders.
  3. **Data Subset**: Effect remained stable (e.g., 5.43) with a high p-value (0.98), indicating the estimate is not overly sensitive to specific data points.

## [2026-04-25T17:16:31+02:00] Phase 5: Visualization & Reporting
- **Attempted**: Created and executed `visualize_results.py` to generate Plotly visualizations (Scatter Plot showing the confounding context and a Bar Chart comparing Naive vs. Causal estimates). Saved outputs to `causal_report.html`.
- **Output**: The script ran successfully and generated the combined HTML report containing both plots.
- **Learned/Changed**: The visualization clearly reveals the confounding gap. The scatter plot effectively shows how 'Holiday' releases are shifted upwards, making marketing look better than it is. The bar chart accurately contrasts the inflated Naive Lift (11.07M) with the true Causal ATE (5.42M).

## [2026-04-25T17:52:09+02:00] Phase 6: Project Complete
- **Attempted**: Created a high-quality `README.md` explaining the confounding bias challenge, detailing the Naive (11.07M) vs Causal (5.42M) results, and documenting the tech stack and run instructions.
- **Output**: README.md successfully created.
- **Learned/Changed**: The project is completely wrapped up. The repository now contains the full end-to-end causal inference study, and the Master Protocol has been strictly followed from start to finish.

## [2026-04-25T18:14:20+02:00] Season 2 - Phase 7: Heterogeneous Treatment Effect
- **Attempted**: Modified `generate_data.py` to replace the static true marketing effect (5M) with a Heterogeneous Treatment Effect (HTE). Marketing now provides a base effect of 2M, plus an interaction term adding up to 10M for movies with 0 popularity (`10 * (1 - genre_pop/100) * marketing_spend`). Regenerated `netflix_data.csv`.
- **Output**: The script successfully overwrote the dataset with 2000 rows.
- **Learned/Changed**: The underlying dataset now features effect modification. Marketing is no longer uniformly beneficial; its ROI is heavily dependent on the baseline popularity of the genre.

## [2026-04-25T18:26:08+02:00] Season 2 - Phase 8: CATE Analysis
- **Attempted**: Created and executed `cate_analysis.py` to calculate Conditional Average Treatment Effects (CATE) using an X-Learner meta-learner. (Utilized a standard Scikit-Learn fallback implementation as PyPI timed out installing causalml).
- **Output**: 
  ```
  AVERAGE LIFT FOR NICHE CONTENT (<25 Pop): 10.95M Hours
  AVERAGE LIFT FOR BLOCKBUSTERS (>75 Pop): 3.75M Hours
  ```
- **Learned/Changed**: The X-Learner successfully uncovered the heterogeneous treatment effects. It accurately identified that marketing generates significantly more lift for "Niche" content (~10.95M hours) compared to "Blockbuster" content (~3.75M hours).
