import pandas as pd

def missing_image_handles(path):
    # Read CSV and normalise cols
    file = pd.read_csv(path)
    file.columns = [c.strip().lower() for c in file.columns]

    # Confirm target cols exist
    required = ['handle', 'option1 name', 'variant image', 'variant sku', 'status']
    for col in required:
        if col not in file.columns:
            raise ValueError(f"CSV is missing '{col}' column")

    # Group rows by product handle
    grouped = file.groupby('handle')
    # Sort by active products
    sort_active = grouped['status'].first().str.lower().isin(['active'])
    active_handles = sort_active[sort_active].index
    active_products = file[file['handle'].isin(active_handles)]
    # Sort by colour products
    sort_colour = grouped['option1 name'].first().str.lower().isin(['color', 'colour'])
    colour_handles = sort_colour[sort_colour].index
    colour_products = active_products[active_products['handle'].isin(colour_handles)]

    # Sort by cols without variant image and remove blank skus
    missing_images = colour_products[
        (
            (colour_products['variant image'].isna()) |
            (colour_products['variant image'].astype(str).str.strip() == '')
        )
        &
        (
            (colour_products['variant sku'].notna()) &
            (colour_products['variant sku'].astype(str).str.strip() != '')
        )
    ]
    # Remove duplicate handles
    return missing_images['handle'].drop_duplicates()