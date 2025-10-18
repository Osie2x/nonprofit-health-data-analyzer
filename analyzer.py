import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_immunization_data(file_path='immunization_coverage.csv'):
    try:
        df = pd.read_csv(file_path)
        print("--- Starting Global Health Data Analysis ---")
        print(f"Initial dataset loaded with {df.shape[0]} rows and {df.shape[1]} columns.\n")

        print("Cleaning and preparing the data...")
        df_dtp = df[df['Vaccine'] == 'DTP3'].copy()

        cols_to_drop = ['WHO_REGION', 'ISO_CODE', 'DATA_SOURCE']
        df_dtp.drop(columns=cols_to_drop, inplace=True)

        initial_rows = df_dtp.shape[0]
        df_dtp.dropna(subset=['COVERAGE'], inplace=True)
        rows_dropped = initial_rows - df_dtp.shape[0]
        print(f"- Focused on DTP3 vaccine and dropped {rows_dropped} rows with no coverage data.")
        print(f"Prepared dataset has {df_dtp.shape[0]} records.\n")

        print("--- Performing Analysis ---")

        avg_coverage_by_country = df_dtp.groupby('COUNTRY')['COVERAGE'].mean().sort_values(ascending=True)
        lowest_coverage_countries = avg_coverage_by_country.head(10)

        print("Top 10 Countries with the Lowest Average DTP3 Immunization Coverage:")
        print(lowest_coverage_countries)
        print("\nInsight: A nonprofit could use this list to identify countries that may require the most urgent aid or programmatic support for vaccination campaigns.\n")

        countries_to_plot = lowest_coverage_countries.index[:3].tolist()
        df_trend = df_dtp[df_dtp['COUNTRY'].isin(countries_to_plot)]

        print(f"Analyzing coverage trend over time for: {', '.join(countries_to_plot)}")

        plt.style.use('seaborn-v0_8-whitegrid')
        fig, ax = plt.subplots(figsize=(12, 7))

        sns.lineplot(data=df_trend, x='YEAR', y='COVERAGE', hue='COUNTRY', marker='o', ax=ax)

        ax.set_title(f'DTP3 Immunization Coverage Trends in High-Need Countries', fontsize=16, weight='bold')
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel('Coverage (%)', fontsize=12)
        ax.legend(title='Country')
        ax.set_ylim(0, 100)
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)

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
    analyze_immunization_data()
