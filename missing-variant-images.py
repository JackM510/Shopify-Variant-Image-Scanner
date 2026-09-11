import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

def run():
    # --- Select CSV ---
    path = filedialog.askopenfilename(title="Select CSV", filetypes=[("CSV Files", "*.csv")])
    if not path:
        return

    # --- Read CSV and normalise cols ---
    file = pd.read_csv('file.csv')
    file.columns = [c.strip().lower() for c in file.columns]

    # --- Confirm target cols exist ---
    if 'handle' not in file.columns:
        raise ValueError("CSV is missing 'Handle' column")
    if 'option1 name' not in file.columns:
        raise ValueError("CSV is missing 'Option1 Name' column")
    if 'variant image' not in file.columns:
        raise ValueError("CSV is missing 'Variant Image' column")
    if 'variant sku' not in file.columns:
            raise ValueError("CSV is missing 'Variant SKU' column")
    if 'status' not in file.columns:
        raise ValueError("CSV is missing 'Status' column")

    # --- Group each row by product handle
    grouped = file.groupby('handle')
    # --- Sort by active products
    sort_active = grouped['status'].first().str.lower().isin(['active'])
    active_handles = sort_active[sort_active].index
    active_products = file[file['handle'].isin(active_handles)]
    # --- Sort by colour products
    sort_colour = grouped['option1 name'].first().str.lower().isin(['color', 'colour'])
    colour_handles = sort_colour[sort_colour].index
    colour_products = active_products[active_products['handle'].isin(colour_handles)]

    # --- Sort by cols without variant image and remove blank sku cols ---
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
    # --- Drop duplicate handles (show 1 product)
    unique_handles = missing_images['handle'].drop_duplicates()

    # --- Save File ---
    save_path = filedialog.asksaveasfilename(
        title="Save Output CSV",
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")]
    )

    if save_path:
        unique_handles.to_csv(save_path, index=False)
        messagebox.showinfo("Done", f"Exported {len(unique_handles)} handles.")


root = tk.Tk()
root.title("Missing Image Checker")

btn = tk.Button(root, text="Select CSV", command=run, width=30)
btn.pack(padx=20, pady=20)

root.mainloop()