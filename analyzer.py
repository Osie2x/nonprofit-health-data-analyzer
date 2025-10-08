# Nonprofit Health Data Analyzer
# This script analyzes a dataset on global immunization coverage to identify trends
# and areas of need. It's a practical example of how data analysis can be used to
# support the mission of non-profits in the global health sector, aligning with
# the work of organizations Digital Aid Seattle partners with.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_immunization_data(file_path='immunization_coverage.csv'):
    """
    Loads, cleans, and analyzes global immunization data to find trends
    that could inform nonprofit strategy.

    Args:
        file_path (str): The path to the immunization coverage CSV file.

    Returns:
        None: The function prints analysis and saves a plot.
    """
    try:
        # Load the dataset
        df = pd.read_csv(file_path)
        print("--- Starting Global Health Data Analysis ---")
        print(f"Initial dataset loaded with {df.shape[0]} rows and {df.shape[1]} columns.\n")

        # --- 1. Data Cleaning and Preparation ---
        print("Cleaning and preparing the data...")
        # For this analysis, we'll focus on a key vaccine: DTP3 (Diphtheria, Tetanus, Pertussis)
        # It's a good indicator of a health system's strength.
        df_dtp = df[df['Vaccine'] == 'DTP3'].copy()

        # Drop columns that are not needed for this specific analysis
        cols_to_drop = ['WHO_REGION', 'ISO_CODE', 'DATA_SOURCE']
        df_dtp.drop(columns=cols_to_drop, inplace=True)

        # Handle missing coverage data by removing those rows
        initial_rows = df_dtp.shape[0]
        df_dtp.dropna(subset=['COVERAGE'], inplace=True)
        rows_dropped = initial_rows - df_dtp.shape[0]
        print(f"- Focused on DTP3 vaccine and dropped {rows_dropped} rows with no coverage data.")
        print(f"Prepared dataset has {df_dtp.shape[0]} records.\n")


        # --- 2. Exploratory Data Analysis (EDA) ---
        print("--- Performing Analysis ---")

        # Find the 10 countries with the lowest average immunization coverage over the years
        avg_coverage_by_country = df_dtp.groupby('COUNTRY')['COVERAGE'].mean().sort_values(ascending=True)
        lowest_coverage_countries = avg_coverage_by_country.head(10)

        print("Top 10 Countries with the Lowest Average DTP3 Immunization Coverage:")
        print(lowest_coverage_countries)
        print("\nInsight: A nonprofit could use this list to identify countries that may require the most urgent aid or programmatic support for vaccination campaigns.\n")

        # Analyze the trend of DTP3 coverage over time for a few of these low-coverage countries
        # Let's pick three from the list for a focused analysis.
        countries_to_plot = lowest_coverage_countries.index[:3].tolist()
        df_trend = df_dtp[df_dtp['COUNTRY'].isin(countries_to_plot)]

        print(f"Analyzing coverage trend over time for: {', '.join(countries_to_plot)}")

        # --- 3. Data Visualization ---
        # Create a plot to visualize the trend, which is a powerful tool for reports and presentations.
        plt.style.use('seaborn-v0_8-whitegrid')
        fig, ax = plt.subplots(figsize=(12, 7))

        sns.lineplot(data=df_trend, x='YEAR', y='COVERAGE', hue='COUNTRY', marker='o', ax=ax)

        ax.set_title(f'DTP3 Immunization Coverage Trends in High-Need Countries', fontsize=16, weight='bold')
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel('Coverage (%)', fontsize=12)
        ax.legend(title='Country')
        ax.set_ylim(0, 100) # Coverage is a percentage
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)

        # Save the plot to a file
        output_plot_path = 'immunization_coverage_trends.png'
        plt.savefig(output_plot_path)

        print(f"\n--- Analysis Complete ---")
        print(f"A visualization has been saved to '{output_plot_path}'.")
        print("This plot clearly shows the volatility and challenges in maintaining immunization coverage, a key insight for any health-focused NGO.")


    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        print("Please download the 'immunization_coverage.csv' dataset and place it in the same directory.")
        return None

if __name__ == '__main__':
    # This block runs when the script is executed directly.
    # Assumes the dataset is in the same directory.
    analyze_immunization_data()