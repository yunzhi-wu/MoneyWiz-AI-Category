import csv


def find_same_category_descriptions(csv_file_path):
    category_descriptions = {}

    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            category = row["Category"]
            description = row["Description"]

            if category in category_descriptions:
                # Check if the description is not already in the list for that category
                if description not in category_descriptions[category]:
                    category_descriptions[category].append(description)
            else:
                category_descriptions[category] = [description]

    return category_descriptions


# Example usage:
csv_file_path = 'C:\\Others\\Wiz3\\report_all.csv'
result = find_same_category_descriptions(csv_file_path)

# Print the result
for category, descriptions in result.items():
    if len(descriptions) > 1:
        print(f'Category: {category}, Descriptions: {", ".join(descriptions)}')
    # Remove
