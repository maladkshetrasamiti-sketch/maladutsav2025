# maladutsav2025

## How to Use the `callingListNew.ipynb` Jupyter Notebook

This notebook helps generate calling dashboards and individual calling lists for the Vivah Sahyog Samiti program. Follow these steps to use it:

### 1. Prepare Input Files

- **Create a new folder** inside the `program` directory. The folder name should match the `key` variable you set in the notebook (e.g., `vivahsamiti2`).
- Place the following two CSV files inside your new folder:
	1. `karykarta.csv` — Must contain a column: `Samiti Member Phone Number` and `Samiti Member Name`.
	2. `karykarta_member_assignment.csv` — Must contain columns: `Samiti Member Phone Number`, `Assigned Person`, and `Mobile Number`.
- Make sure your CSV files are properly formatted and saved as UTF-8.

### 2. Configure the Notebook

- Open `callingListNew.ipynb` in Jupyter or VS Code.
- **Edit only the first cell** to set the correct `key` and other configuration variables as per your folder and program details.

### 3. Run the Notebook

- Run all cells in the notebook sequentially.
- The notebook will:
	- Download the latest call log data (if configured).
	- Read your input CSVs.
	- Generate:
		- A dashboard HTML file in the root folder (e.g., `dashboard_vivahsamiti2.html`).
		- Individual calling list HTML files for each Samiti member in the output folder inside your program directory.

### 4. Output

- The dashboard file will be created at the root of the project (e.g., `dashboard_vivahsamiti2.html`).
- Individual calling list HTML files will be created in `program/<key>/output/`.

### 5. Notes

- If you update your input CSVs, re-run the notebook to refresh the outputs.
- Make sure all required columns are present in your CSVs.
- For any issues, check the notebook output for error messages.

### 6. Publish the changes back to github