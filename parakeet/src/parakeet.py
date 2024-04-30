import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import base64

def create_parquet_with_hidden_flag():
    # Expanded data with 25 bird species, their lifespans, and countries of origin
    data = {
        'Bird Species': [
            'African Grey Parrot', 'Bald Eagle', 'Canary', 'Peregrine Falcon', 'Albatross',
            'Budgerigar', 'Cockatiel', 'Flamingo', 'Golden Eagle', 'Harpy Eagle',
            'Indian Peafowl', 'Jabiru', 'Kiwi', 'Lyrebird', 'Macaw',
            'Nightjar', 'Ostrich', 'Pelican', 'Quetzal', 'Robin',
            'Sparrow', 'Toucan', 'Umbrella Bird', 'Vulture', 'Woodpecker'
        ],
        'Lifespan (Years)': [
            50, 20, 10, 15, 60,
            5, 10, 30, 30, 35,
            20, 36, 8, 30, 50,
            12, 40, 15, 20, 2,
            3, 20, 16, 25, 11
        ],
        'Country of Origin': [
            'Central Africa', 'North America', 'Canary Islands', 'Worldwide', 'Southern Ocean',
            'Australia', 'Australia', 'Africa', 'North America', 'Central America',
            'South Asia', 'Central America', 'New Zealand', 'Australia', 'South America',
            'Worldwide', 'Africa', 'Worldwide', 'Central America', 'Europe',
            'Worldwide', 'Central America', 'South America', 'Worldwide', 'Worldwide'
        ]
    }

    # Create a DataFrame
    df = pd.DataFrame(data)

    table = pa.Table.from_pandas(df)

    # Define custom metadata
    metadata = {'creator': 'ictf{MyParakeetPoopedOnMyParquet}'}

    # Add custom metadata to the table's schema
    new_schema = table.schema.with_metadata(metadata)
    table = table.replace_schema_metadata(new_schema.metadata)
    
    # Write the table to a Parquet file with compression
    pq.write_table(table, 'parakeet.parquet', compression='snappy')

if __name__ == "__main__":
    create_parquet_with_hidden_flag()
    print("Parquet file with hidden flag created.")
