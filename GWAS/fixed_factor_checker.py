import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm
from tkinter import filedialog
import tkinter as tk

def load_files():
    """Open file dialogs to select input files"""
    root = tk.Tk()
    root.withdraw()
    
    print("Select your phenotype file...")
    pheno_file = filedialog.askopenfilename(title="Select phenotype file",
                                           filetypes=[("Text files", "*.txt")])
    
    print("Select your covariates file...")
    covar_file = filedialog.askopenfilename(title="Select covariates file",
                                           filetypes=[("Text files", "*.txt")])
    
    return pheno_file, covar_file

def analyze_fixed_factors(pheno_file, covar_file):
    try:
        # Read data with headers
        print(f"\nReading phenotype data from {pheno_file}...")
        pheno_df = pd.read_csv(pheno_file, sep='\t')
        
        print(f"Reading covariate data from {covar_file}...")
        covar_df = pd.read_csv(covar_file, sep='\t')
        
        # Select the trait to analyze
        trait_columns = pheno_df.columns[2:]  # All columns except FID and IID
        print("\nAvailable traits:", list(trait_columns))
        trait_name = input("Which trait would you like to analyze? ")
        
        if trait_name not in trait_columns:
            raise ValueError(f"Trait {trait_name} not found in phenotype file")
        
        # Extract trait and factors
        trait = pd.to_numeric(pheno_df[trait_name], errors='coerce')
        factor_columns = [col for col in covar_df.columns if col not in ['FID', 'IID', trait_name]]
        factors = covar_df[factor_columns]
        
        # Convert factors to numeric
        for col in factors.columns:
            factors[col] = pd.to_numeric(factors[col], errors='coerce')
        
        # Create output directory
        import os
        if not os.path.exists('factor_analysis'):
            os.makedirs('factor_analysis')

        # 1. Correlation Analysis
        plt.figure(figsize=(12, 10))
        plt.rcParams['figure.dpi'] = 600
        
        # Create correlation matrix
        corr_matrix = factors.corr(method='spearman')
        
        # Plot heatmap
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
        plt.title(f"Correlation Matrix of Fixed Factors for {trait_name}")
        plt.tight_layout()
        plt.savefig('factor_analysis/correlation_matrix.png', dpi=600, bbox_inches='tight')
        plt.close()

        # 2. Factor Importance Analysis
        importance_dict = {}
        
        for col in factors.columns:
            X = factors[col].values.reshape(-1, 1)
            y = trait.values
            
            # Remove NA values
            mask = ~(pd.isna(X).any(axis=1) | pd.isna(y))
            X = X[mask]
            y = y[mask]
            
            X = sm.add_constant(X)
            model = sm.OLS(y, X).fit()
            importance_dict[col] = model.rsquared
        
        # Sort factors by importance
        importance_sorted = dict(sorted(importance_dict.items(), 
                                      key=lambda x: x[1], 
                                      reverse=True))
        
        # Plot factor importance
        plt.figure(figsize=(12, 6))
        plt.bar(importance_sorted.keys(), importance_sorted.values())
        plt.xticks(rotation=45, ha='right')
        plt.title(f"Factor Importance for {trait_name}")
        plt.ylabel("R-squared value")
        plt.tight_layout()
        plt.savefig('factor_analysis/factor_importance.png', dpi=600, bbox_inches='tight')
        plt.close()

        # 3. VIF Analysis
        X = StandardScaler().fit_transform(factors)
        X = sm.add_constant(X)
        
        vif_data = pd.DataFrame()
        vif_data["Factor"] = factors.columns
        vif_data["VIF"] = [variance_inflation_factor(X, i+1) 
                           for i in range(len(factors.columns))]
        
        # Print results and save to report
        with open('factor_analysis/analysis_report.txt', 'w') as f:
            f.write(f"Fixed Factor Analysis Report for {trait_name}\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("1. Factor Importance (R-squared values):\n")
            for factor, importance in importance_sorted.items():
                line = f"{factor}: {importance:.4f}"
                print(line)
                f.write(line + "\n")
            
            f.write("\n2. High Correlations:\n")
            high_corr_pairs = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr = corr_matrix.iloc[i,j]
                    if abs(corr) > 0.7:
                        pair = (corr_matrix.columns[i], 
                               corr_matrix.columns[j], 
                               corr)
                        high_corr_pairs.append(pair)
                        line = f"{pair[0]} - {pair[1]}: {pair[2]:.2f}"
                        print(line)
                        f.write(line + "\n")
            
            f.write("\n3. VIF Analysis:\n")
            print("\nVIF Analysis:")
            print(vif_data)
            f.write(vif_data.to_string())
            
            f.write("\n\nRecommendations for GCTA analysis:\n")
            recommendations = [
                "Consider including factors with R² > 0.05",
                "Consider removing or combining highly correlated factors (correlation > 0.7)",
                "Factors with VIF > 10 may cause multicollinearity issues"
            ]
            
            for i, rec in enumerate(recommendations, 1):
                f.write(f"{i}. {rec}\n")
                print(f"{i}. {rec}")

        print("\nAnalysis completed! Check factor_analysis/ directory for detailed results.")
        
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        print("Please check your input files and try again.")

def variance_inflation_factor(X, i):
    try:
        return np.linalg.inv(np.corrcoef(X.T))[i,i]
    except:
        return np.nan

if __name__ == "__main__":
    print("Let's analyze your fixed factors...")
    pheno_file, covar_file = load_files()
    if pheno_file and covar_file:
        analyze_fixed_factors(pheno_file, covar_file)
    else:
        print("Files not selected. Exiting...")
