import pandas as pd
from collections import defaultdict

def nested_dict_to_df(nested_dict):
    """
    Convert a nested dictionary to a pandas DataFrame.
    - Top-level keys become rows
    - Nested keys become columns
    - Further nested dictionaries are flattened with dot notation
    - Equivalent keys in different nested structures are handled correctly
    """
    # Function to flatten nested dictionaries
    def flatten_dict(d, parent_key=''):
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}.{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten_dict(v, new_key).items())
            else:
                items.append((new_key, v))
        return dict(items)
    
    # Process each top-level entry
    rows = {}
    for key, value in nested_dict.items():
        if isinstance(value, dict):
            rows[key] = flatten_dict(value)
        else:
            rows[key] = {'value': value}
    
    # Create DataFrame
    return pd.DataFrame.from_dict(rows, orient='index')

# Example nested dictionary with equivalent keys at different levels
example_dict = {
    'person1': {
        'name': 'John',
        'details': {
            'age': 30,
            'type': 'employee'
        },
        'contact': {
            'email': 'john@example.com',
            'type': 'personal'  # Note: 'type' appears in both details and contact
        }
    },
    'person2': {
        'name': 'Sarah',
        'details': {
            'age': 28,
            'type': 'contractor'
        },
        'contact': {
            'email': 'sarah@example.com',
            'type': 'work'  # Note: 'type' appears in both details and contact
        }
    },
    'person3': {
        'name': 'Mike',
        'details': {
            'age': 35
        },
        'type': 'unknown'  # Note: 'type' at a different level
    }
}

# Convert to DataFrame
df = nested_dict_to_df(example_dict)
print("\nDataFrame with equivalent keys in different structures:")
print(df)

# Let's verify we can access these columns separately
print("\nAccessing specific columns:")
if 'details.type' in df.columns and 'contact.type' in df.columns:
    print(f"details.type column: {df['details.type'].tolist()}")
    print(f"contact.type column: {df['contact.type'].tolist()}")
if 'type' in df.columns:
    print(f"top-level type column: {df['type'].tolist()}")
