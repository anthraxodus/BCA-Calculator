# BCA-Calculator
This is a simple script that automatically calculates Bicinchoninic Acid Assay (BCA).
## Description
I developed this calculator to help me throughout my PhD. Once I very often perform this assay, and there is no such code out there. This calculator comes with a Phython script and a Windows .EXE file, in the case you`re not familiar with any programing languages. You may use, edit and distribute the way you want to. Being credited somehow would be great, but it is not a must. 
## Tutorial

### 1. Installing the BCA Calculator:

- If you pretend to use the Python script, simply download and follow the next steps. For Windows users that desire to use the .EXE file, download the source code and add the **BCA_Calculator.EXE** file.

### 2.Preparing to use the calculator.

- Generate a file for the standards (**standards.csv**) and for the unknowns (**unknowns.csv**), containing the corresponding absorbance values as the following example tables. *N* replicates are allowed for both cases.

#### **standards.csv**

|   |   |   |   |
|---|---|---|---|
| 2 | 1 | 1 | 1 |
| 1.5 | 0.8 | 0.8 | 0.8 |
| 1 | 0.6 | 0.6 | 0.6 |
| 0.75 | 0.49 | 0.49 | 0.49 |
| 0.5 | 0.36 | 0.36 | 0.36 |
| 0.25 | 0.24 | 0.24 | 0.24 |
| 0.125 | 0.17 | 0.17 | 0.17 |
| 0.025 | 0.1 | 0.1 | 0.1 |

#### The very first column takes the standard curve concentrations values and the following *n* absorbance replicates. No headers allowed.

#### **unknowns.csv**


| Unknown            | Replicate 1 | Replicate 2 | Replicate 3 |
|--------------------|-------------|-------------|-------------|
| 2ug/ul_Sample      | 1           | 1           | 1           |
| 1.5ug/ul_Sample    | 0.8         | 0.8         | 0.8         |
| 1ug/ul_Sample      | 0.6         | 0.6         | 0.6         |
| 0.75ug/ul_Sample   | 0.49        | 0.49        | 0.49        |
| 0.5ug/ul_Sample    | 0.36        | 0.36        | 0.36        |
| 0.25ug/ul_Sample   | 0.24        | 0.24        | 0.24        |
| 0.125ug/ul_Sample  | 0.17        | 0.17        | 0.17        |
| 0.025ug/ul_Sample  | 0.1         | 0.1         | 0.1         |
| Blank              | 0           | 0           | 0           |

#### The very first column takes the given sample names. The following ones takes values and the following *n* absorbance replicates. Headers must be added such as exemplified. For both files, be aware that sometimes Excell and similar programs alters the files (changes dots and insrts commas, for instance), causing the code to fail.

- Add both files to the project main folder.

### 3. Executing the script/ .EXE:

- After preparing your files, you may run the Python script called '**BCA_Calculator**' or the .EXE file also called '**BCA_Calculator**'. In both cases the script will ask the user few questions.
  - Experiment Name:
  - Is there a dilution factor applied? (yes or no):
  - Please enter a dilution factor (int or float):
- If everything goes well, your input archives will be moved to an new folder/ directory with the given experiment name and figures and output files will also be available.

### 4. How the script works:

**Steps and Explanation:**

1. **Step 1 - Read Data:**
   - The script reads two CSV files, `standards.csv` and `unknowns.csv`, containing absorbance measurements from standard protein samples and unknown samples, respectively.

2. **Step 2 - Average Standards:**
   - It calculates the average absorbance for the standard samples, creating a representative curve.

3. **Step 3 - Plot Standard Curve:**
   - Using the averaged standard absorbance values, the script fits a polynomial curve (3rd degree) to the data.
   - The equation of the curve is calculated and displayed in the format:
     ```
     Concentration (μg/μL) = a * Absorbance^3 + b * Absorbance^2 + c * Absorbance + d
     ```

4. **Step 4 - Calculate Concentrations:**
   - It calculates the concentrations of unknown samples based on their absorbance values and the generated standard curve using the formula mentioned in step 3.
   - Users can specify a dilution factor if applicable.

5. **Step 5 - Generate Outputs:**
   - The script generates several outputs:
     - A plot titled `<experiment_name>_Obtained_Concentrations.png` showing the BCA standard curve and the calculated concentrations of unknown samples.
     - A CSV file named `<experiment_name>_Obtained_Concentrations.csv` containing the following columns:
       - Sample names
       - Average absorbance values for unknown samples
       - Dilution factor corrected concentrations
       - Calculated concentrations using the formula
       - The amount of sample required to achieve specific concentrations (e.g., 5 μg, 10 μg, 15 μg) based on the standard curve.
     - The script also moves the input files (`standards.csv` and `unknowns.csv`) into a folder named after the experiment.

---

**Expected Outputs:**

1. A plot titled `<experiment_name>_Obtained_Concentrations.png` showing the BCA standard curve and the calculated concentrations of unknown samples.

2. A CSV file named `<experiment_name>_Obtained_Concentrations.csv` containing the following columns:
   - Sample names
   - Average absorbance values for unknown samples
   - Dilution factor corrected concentrations
   - Calculated concentrations using the formula mentioned in step 3
   - The amount of sample required to achieve specific concentrations (e.g., 5 μg, 10 μg, 15 μg) based on the standard curve.

3. The input files `standards.csv` and `unknowns.csv` moved into a folder named `<experiment_name>` for organization.
