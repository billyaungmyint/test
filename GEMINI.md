# GEMINI.md for Python Machine Learning Project

## Project Overview

This project is a collection of Python scripts that demonstrate basic machine learning concepts. It includes implementations of linear regression and a comparison of clustering algorithms (K-means vs. DBSCAN). The scripts use common data science libraries to perform calculations and generate plots to visualize the results.

### Key Technologies
- **Language:** Python
- **Core Libraries:**
    - `scikit-learn`: For machine learning algorithms.
    - `numpy`: For numerical operations.
    - `matplotlib`: For generating plots.
- **Testing:** `unittest` framework.

## Running the Scripts

It is recommended to use a Python virtual environment.

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Execute a Script:**
    Each main script can be run directly from the command line.

    *   **Linear Regression:**
        ```bash
        python linear_regression.py
        ```
        This will print the model's slope, intercept, a prediction, and the R-squared value. It will also save a plot named `regression_plot.png`.

    *   **Clustering Comparison:**
        ```bash
        python clustering_comparison.py
        ```
        This will print evaluation metrics for K-means and DBSCAN clustering and save a comparison plot named `clustering_comparison_plot.png`.

## Testing

The project uses Python's built-in `unittest` framework for testing.

*   **Running Tests:**
    To run all tests, execute the following command from the project's root directory:
    ```bash
    python -m unittest discover
    ```

*   **Test Structure:**
    - Tests are located in files named `test_*.py`.
    - Each test file corresponds to a specific script (e.g., `test_linear_regression.py` tests `linear_regression.py`).
    - The tests verify the correctness of the machine learning models' outputs and ensure that plot files are generated.

## Development Conventions

*   **File Structure:** Core logic is contained in individual Python scripts. Corresponding test files are located in the root directory.
*   **Code Style:** The code follows standard Python conventions.
*   **Output:** Scripts that generate visualizations save them as `.png` files in the root directory.
