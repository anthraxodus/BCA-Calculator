import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def calculate_bca_standard_curve(exp_name):
    # Step 1: Read the standards and unknown files
    standards = pd.read_csv('standards.csv', index_col=0, header=None)
    unknowns = pd.read_csv('unknowns.csv', index_col=0)

    # Step 2: Average the standards replicates
    standards['Standard Averaged Absorbance'] = standards.mean(axis=1)

    # Step 3: Plot the curve
    experiment_name = exp_name
    x = np.array(standards.index)
    y = np.array(standards['Standard Averaged Absorbance'])
    curve_fit = np.polyfit(x, y, 3)
    equation = f"{curve_fit[0]:.4f}x^3 + {curve_fit[1]:.4f}x^2 + {curve_fit[2]:.4f}x + {curve_fit[3]:.4f}"
    r_squared = round(1 - (sum((y - np.polyval(curve_fit, x))**2) / ((len(y)-1) * np.var(y, ddof=1))), 4)

    fig, ax = plt.subplots()
    ax.plot(x, y, 'bo', label='Standards')
    ax.plot(x, np.polyval(curve_fit, x), 'k-', label='Trendline')
    ax.plot(x, np.polyval(curve_fit, x), 'r--', label='Curve fit')
    ax.legend(loc='lower right')
    ax.text(0, max(y), f'Equation: {equation}\nR squared: {r_squared}', fontsize=10, verticalalignment='top')
    if r_squared < 0.9:
        ax.text(max(x)*0.7, max(y)*0.9, f'R squared < 0.9', fontsize=10, color='orange', verticalalignment='top')
    if r_squared < 0.8:
        ax.text(max(x)*0.7, max(y)*0.8, f'R squared < 0.8', fontsize=10, color='red', verticalalignment='top')
    ax.set_xlabel('Standard (μg/mL)')
    ax.set_ylabel('Averaged Absorbance')
    ax.set_title(experiment_name)

    # Remove grid lines and set border around the plot
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(2)

    # Step 4: Save the plot
    if not os.path.exists(experiment_name):
        os.mkdir(experiment_name)
    plt.savefig(os.path.join(experiment_name, f'{experiment_name}_Standard_Curve.png'), dpi=300)

    # Return the curve_fit coefficients and equation
    return curve_fit, equation


def get_curve_coefficients():
    standards = pd.read_csv('standards.csv', index_col=0)
    x = np.array(standards.index)
    y = np.array(standards.mean(axis=1))
    curve_fit = np.polyfit(x, y, 3)

    curve_fit = curve_fit.round(4)

    # print(curve_fit)

    return list(curve_fit)

coefs = get_curve_coefficients()


def calculate_concentration(coefficients, absorbance):
    # Calculate concentration using the equation from the BCA standard curve
    a, b, c, d = coefficients
    # Solve for y (concentration) based on the provided curve equation
    roots = np.roots([a, b, c, d - absorbance])
    real_roots = [root.real for root in roots if root.imag == 0]
    
    if not real_roots:
        raise ValueError("No real roots found. Check the curve equation.")
    
    concentration = max(real_roots, key=abs)  # Select the root with highest magnitude
    
    return concentration

def calculate_sample_concentration(coefficients, sample_averages, blank_average):
    # Step 1: Ask user for dilution factor
    dilution_factor = input("Is there a dilution factor applied? (yes or no): ")

    # Step 2: Calculate sample concentrations using BCA equation, excluding the blank
    concentrations = {}
    for sample, average in sample_averages.items():

        # print(sample, average)
        if sample != "Blank":
            corrected_average = average - blank_average

            # print(corrected_average)
            
            concentration = calculate_concentration(coefficients, corrected_average)
            concentrations[sample] = concentration
    
    # Step 3: Multiply the concentrations by the dilution factor if applicable
    if dilution_factor.lower() == "yes":
        factor = float(input("Please enter the dilution factor: "))
        for sample in concentrations:
            concentrations[sample] *= factor
    else:
        factor = 1
    
    return concentrations, factor

def bca_standard_curve_values():
    # Step 1: Read the standards and unknown files
    standards = pd.read_csv('standards.csv', index_col=0)
    unknowns = pd.read_csv('unknowns.csv', index_col=0)

    # Step 2: Average the standards replicates
    standards['Standard Averaged Absorbance'] = standards.mean(axis=1)
    unknowns['Unknown Averaged Absorbance']    = unknowns.mean(axis=1)

    ##################################################################


    x = np.array(standards.index)
    y = np.array(standards['Standard Averaged Absorbance'])


    x = np.array(standards.index)
    y = np.array(standards.mean(axis=1))
    curve_fit = np.polyfit(x, y, 3)

    curve_fit = curve_fit.round(4)

    # print(curve_fit)

    # Step 3: Obain the curve
    curve_fit = np.polyfit(x, y, 3)
    equation = f"{curve_fit[0]:.4f}x^3 + {curve_fit[1]:.4f}x^2 + {curve_fit[2]:.4f}x + {curve_fit[3]:.4f}"
    r_squared = round(1 - (sum((y - np.polyval(curve_fit, x))**2) / ((len(y)-1) * np.var(y, ddof=1))), 4)

    # print(r_squared)

    curve_fit = curve_fit.round(4)

    # print(curve_fit)

    unknowns['R Squared'] = str(r_squared)
    unknowns['Used Equation']  = equation

    standards = standards.round(3)
    unknowns = unknowns.round(3)


    final = pd.concat([standards, unknowns])


    return final



def main():

    exp_name = input("Enter the experiment name: ")

    # Step 1: Calculate BCA standard curve
    calculate_bca_standard_curve(exp_name)

    # Step 2: Get BCA curve coefficients
    curve_coefficients = get_curve_coefficients()

    # Step 3: Read unknown samples
    unknown_samples = pd.read_csv('unknowns.csv', index_col=0)

    # Step 4: Average unknown replicates
    unknown_averages = unknown_samples.mean(axis=1)

    # Step 5: Get blank average
    blank_average = unknown_samples.loc['Blank'].mean()

    # Step 6: Calculate sample concentrations
    sample_concentrations, dilution_fac = calculate_sample_concentration(curve_coefficients, unknown_averages, blank_average)

    # Step 7: Print sample concentrations
    # print("Sample Concentrations:")

    # Creating lists for the second plot 
    samples_list = []
    abs_list     = []
    conc_list    = []

    for sample, concentration in sample_concentrations.items():
        # print(f"{sample}: {concentration:.4f} μg/μL")
        samples_list.append(sample)
        conc_list.append(concentration)
    for absorbance in unknown_averages:
        abs_list.append(absorbance - blank_average)
    
    # print(abs_list)

    # Removing the last element of the list, because is always the Blank.

    abs_list.pop(-1), abs_list
    # print(dilution_fac)

    conc_result = pd.DataFrame.from_dict(sample_concentrations, orient='index')

    conc_result = conc_result.round(3)

    conc_result.rename(columns = {0:f'Dilution Factor Corrected Concentration μg/ μL (x{dilution_fac})' }, inplace = True)

    # print(conc_result)

    # Step 1: Read the standards and unknown files
    standards = pd.read_csv('standards.csv', index_col=0, header=None)
    unknowns = pd.read_csv('unknowns.csv', index_col=0)

    

    # Step 2: Average the standards replicates
    standards['Standard Averaged Absorbance'] = standards.mean(axis=1)
    unknowns['Unknown Averaged Absorbance']   = unknowns.mean(axis=1)
    unknowns['Unknown Averaged Absorbance Minus Blank']   = unknowns.mean(axis=1) - blank_average


    x = np.array(standards.index)
    y = np.array(standards['Standard Averaged Absorbance'])


    x = np.array(standards.index)
    y = np.array(standards.mean(axis=1))
    curve_fit = np.polyfit(x, y, 3)

    curve_fit = curve_fit.round(4)

    # print(curve_fit)

    # Step 3: Obain the curve
    curve_fit = np.polyfit(x, y, 3)
    equation = f"{curve_fit[0]:.4f}x^3 + {curve_fit[1]:.4f}x^2 + {curve_fit[2]:.4f}x + {curve_fit[3]:.4f}"
    r_squared = round(1 - (sum((y - np.polyval(curve_fit, x))**2) / ((len(y)-1) * np.var(y, ddof=1))), 4)

    # print(r_squared)

    curve_fit = curve_fit.round(4)

    # print(curve_fit)

    unknowns['R Squared'] = str(r_squared)
    unknowns['Used Equation']  = equation

    standards = standards.round(3)
    
    unknowns = unknowns.round(3)

    final = pd.concat([standards, unknowns])


    conc_result['Calculated Concentration μg/ μL'] = conc_result[f'Dilution Factor Corrected Concentration μg/ μL (x{dilution_fac})'] / dilution_fac 
    
 
    # conc_result = conc_result.round(3)

    conc_result = conc_result.reindex(columns=['Calculated Concentration μg/ μL', f'Dilution Factor Corrected Concentration μg/ μL (x{dilution_fac})'])

    # Necessary concentration for...

    conc_result['Necessary to 5 μg (μl)']  = 5  / conc_result[f'Dilution Factor Corrected Concentration μg/ μL (x{dilution_fac})'] 
    conc_result['Necessary to 10 μg (μl)'] = 10 / conc_result[f'Dilution Factor Corrected Concentration μg/ μL (x{dilution_fac})'] 
    conc_result['Necessary to 15 μg (μl)'] = 15 / conc_result[f'Dilution Factor Corrected Concentration μg/ μL (x{dilution_fac})'] 
    conc_result['Necessary to 20 μg (μl)'] = 20 / conc_result[f'Dilution Factor Corrected Concentration μg/ μL (x{dilution_fac})'] 
    conc_result['Necessary to 25 μg (μl)'] = 25 / conc_result[f'Dilution Factor Corrected Concentration μg/ μL (x{dilution_fac})'] 
    conc_result['Necessary to 30 μg (μl)'] = 30 / conc_result[f'Dilution Factor Corrected Concentration μg/ μL (x{dilution_fac})'] 
    conc_result['Necessary to 35 μg (μl)'] = 35 / conc_result[f'Dilution Factor Corrected Concentration μg/ μL (x{dilution_fac})'] 
    conc_result['Necessary to 40 μg (μl)'] = 40 / conc_result[f'Dilution Factor Corrected Concentration μg/ μL (x{dilution_fac})'] 
    conc_result['Necessary to 45 μg (μl)'] = 45 / conc_result[f'Dilution Factor Corrected Concentration μg/ μL (x{dilution_fac})'] 
    conc_result['Necessary to 50 μg (μl)'] = 50 / conc_result[f'Dilution Factor Corrected Concentration μg/ μL (x{dilution_fac})'] 
    # Generation the final .csv file

    # Generate the final table
    conc_dict = { }

    for sample, row in unknowns.iterrows():
        if (sample != 'Blank'):
            conc_dict[sample] = unknowns.loc[sample].tolist() + conc_result.loc[sample].tolist()
        else:
            conc_dict[sample] = unknowns.loc[sample].tolist()

    cols = unknowns.columns.tolist() + conc_result.columns.tolist()

    conc_result = pd.DataFrame.from_dict(conc_dict, orient='index', columns=cols)
    conc_result = conc_result.round(3)

    final = pd.concat([standards, conc_result])

    # Saving Final Results

    final.to_csv(f'{exp_name}/{exp_name}_Obtained_Concentrations.csv')

    # print(final)

    #####################################################################################

    name = samples_list
    absorbance = abs_list


    concentration = conc_list

    # print(name)
    # print(absorbance)
    # print(concentration)

    # Step 2: Average the standards replicates
    standards['Standard Averaged Absorbance'] = standards.mean(axis=1)
    experiment_name = f"{exp_name} Plotted Obtained Concentrations"
    # Step 3: Plot the curve
    # experiment_name = input("Enter the experiment name: ")

    fig, ax = plt.subplots()
    ax.plot(x, y, 'bo', label='Standards')
    ax.plot(x, np.polyval(curve_fit, x), 'k-', label='Trendline')
    ax.plot(x, np.polyval(curve_fit, x), 'r--', label='Curve fit')
    # ax.plot(concentration, absorbance,  'x', label='Unknown Samples', color='red')

    #print(concentration)

    # Dividing the result by the silution factor again just for the plot

    concentration = [x/dilution_fac for x in concentration]

    #print(concentration)

    # Plot data and display names
    plt.plot(concentration, absorbance, 'x', label='Unknown Samples', color='red')
    # for i, name in enumerate(name):
    #     plt.text(concentration[i], absorbance[i], '  ' + name, fontsize=7)
    
    ax.legend(loc='lower right')
    ax.text(0, max(y), f'Equation: {equation}\nR squared: {r_squared}', fontsize=10, verticalalignment='top')
    if r_squared < 0.9:
        ax.text(max(x)*0.7, max(y)*0.9, f'R squared < 0.9', fontsize=10, color='orange', verticalalignment='top')
    if r_squared < 0.8:
        ax.text(max(x)*0.7, max(y)*0.8, f'R squared < 0.8', fontsize=10, color='red', verticalalignment='top')
    ax.set_xlabel('Standard (μg/ mL)')
    ax.set_ylabel('Averaged Absorbance')
    ax.set_title(experiment_name)


    # Remove grid lines and set border around the plot
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(2)
    
    experiment_name = exp_name

    # Step 4: Save the plot
    if not os.path.exists(experiment_name):
        os.mkdir(experiment_name)
    plt.savefig(os.path.join(experiment_name, f'{experiment_name}_Obtained_Concentrations.png'), dpi=300)
    # plt.show()

    #Moving input files to the experiment folder

    std = 'standards.csv'
    std_destination = f'{experiment_name}/standards.csv'

    os.rename(std, std_destination)

    ukn = 'unknowns.csv'
    ukn_destination = f'{experiment_name}/unknowns.csv'

    os.rename(ukn, ukn_destination)

if __name__ == '__main__':
    main()