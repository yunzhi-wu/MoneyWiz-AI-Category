import os
import pandas as pd
import joblib


def get_engine(filename):
    engine = None
    if filename.endswith('.xlsx'):
        engine = 'openpyxl'
    elif filename.endswith('.xls'):
        engine = 'xlrd'
    return engine


def determine_skip_rows(excel_file_path, max_rows_to_check=150):
    # Read the first few rows of the Excel file
    sample_df = pd.read_excel(excel_file_path, engine='openpyxl', nrows=20, header=None)

    for i, row in enumerate(sample_df.iterrows()):
        # print(f"determine_skip_rows(): \n {row}")
        for value in row[1].items():
            # value has a type of tuple, e.g., ('Unnamed: 8', nan)
            if isinstance(value[1], str) and \
                    ('Transaktionsdatum' in value[1] or
                     'Transaction' in value[1] or
                     'Description' in value[1] or
                     'Amount' in value[1] or
                     'Text' in value[1]):
                print(f"Found the header at row {i} by matching key word: {value[1]}")
                return i

    # If no specific condition is met, return 0 to skip no rows
    return 0


def find_description_column_name(columns):
    target_texts = ['Text', 'Inköpsställe', 'Description']
    for text in target_texts:
        if text in columns:
            return text
    return None


def find_amount_column_name(columns):
    target_texts = ['Belopp', 'Amount']
    for text in target_texts:
        if text in columns:
            return text
    return None


def loaded_classifier_vectorizer(model_filename="C:\\Others\\Wiz3\\trained_model.joblib", \
                                 pkl_filename="C:\\Others\\Wiz3\\vectorizer.pkl"):
    return joblib.load(model_filename), joblib.load(pkl_filename)


# Function to remove spaces between thousands
def remove_thousand_separator(value):
    return value.replace(' ', '')


def convert_excel_to_csv(folder_path):
    classifier, vectorizer = loaded_classifier_vectorizer()

    # Iterate through files in the folder
    for filename in os.listdir(folder_path):
        print(filename)
        engine = get_engine(filename)
        if engine:
            # Construct full file paths
            excel_file_path = os.path.join(folder_path, filename)

            skip_rows = determine_skip_rows(excel_file_path)
            print(f"skip_rows: {skip_rows}")

            # Read Excel file into a DataFrame
            df = pd.read_excel(excel_file_path, engine=engine, skiprows=skip_rows)
            # print(df)

            csv_file_path = os.path.join(folder_path, os.path.splitext(filename)[0] + '.csv')

            # Write DataFrame to CSV
            df.to_csv(csv_file_path, index=False, encoding='utf-8', mode='w')
            print(f"Converted {excel_file_path} to {csv_file_path}")

            descript_key = find_description_column_name(df.columns)
            if not descript_key:
                print(f'No descript_key found')
                continue
            my_df = df[descript_key]
            my_df = my_df.fillna('')
            my_df = my_df.astype(str)
            # print(my_df)

            value_key = find_amount_column_name(df.columns)
            if not value_key:
                print(f'No value_key found')
                continue

            df[value_key] = df[value_key].astype(str)
            df[value_key] = df[value_key].apply(remove_thousand_separator)

            # Transform the new string into the same feature representation
            new_string_feature = vectorizer.transform(my_df)

            # Make predictions using the loaded model
            predicted_category = classifier.predict(new_string_feature)

            # print(f'{predicted_category}')

            df['Category'] = predicted_category

            # Save the new csv file which has the 'Category' column
            csv_file_path2 = os.path.join(folder_path, os.path.splitext(filename)[0] + '2.csv')
            df.to_csv(csv_file_path2, index=False, encoding='utf-8', mode='w')
            print(f"Converted {excel_file_path} to {csv_file_path2}")
            print('-------------------------------------------------')


# Specify the folder containing Excel files
folder_path = 'C:\\Others\\Wiz3\\tmp'

# Call the function to convert Excel files to CSV
convert_excel_to_csv(folder_path)
