import pandas as pd
import numpy as np

def clean_and_preprocess_csv(file_path, output_path):
    try:
        # Loading the CSV file
        df = pd.read_csv(file_path)
        
        # Display basic info
        print("Initial DataFrame Info:")
        print(df.info())
        
        # Display initial few rows
        print("\nInitial DataFrame Head:")
        print(df.head())

        # Remove duplicate rows
        df = df.drop_duplicates()
        print(f"\nRemoved duplicates. New shape: {df.shape}")

        # Handle missing values and filling missing values with the median for numerical columns
        for column in df.select_dtypes(include=[np.number]).columns:
            if df[column].isnull().any():
                median_value = df[column].median()
                df[column].fillna(median_value, inplace=True)
        
        # Fill missing values with a placeholder "Unknown" for categorical columns
        for column in df.select_dtypes(include=[object]).columns:
            if df[column].isnull().any():
                df[column].fillna('Unknown', inplace=True)

        # Convert Data types if necessary
        date_columns = [col for col in df.columns if 'date' in col.lower()]
        for date_column in date_columns:
            df[date_column] = pd.to_datetime(df[date_column], errors='coerce')

        # Normalize
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        if not numerical_cols.empty:
            for col in numerical_cols:
                min_val = df[col].min()
                max_val = df[col].max()
                if min_val != max_val:  # Prevent division by zero
                    df[col] = (df[col] - min_val) / (max_val - min_val)
                else:
                    df[col] = 0

        # Save the cleaned Data to new CSV file
        df.to_csv(output_path, index=False)
        print(f"\nCleaned DataFrame saved to {output_path}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Change the path for cleaning and saving
input_csv_path = r"C:\User\Training_Dataset.csv"
output_csv_path = r"C:\User\Clean_Dataset.csv"
clean_and_preprocess_csv(input_csv_path, output_csv_path)
