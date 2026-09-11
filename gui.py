import tkinter as tk
from tkinter import filedialog, messagebox
from core import missing_image_handles

def get_images():
    # Select CSV
    path = filedialog.askopenfilename(title="Select CSV", filetypes=[("CSV Files", "*.csv")])
    if not path:
        return

    # Run core logic
    try:
        unique_handles = missing_image_handles(path)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

    # Save formatted CSV
    save_path = filedialog.asksaveasfilename(
        title="Save Output CSV",
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")]
    )
    if save_path:
        unique_handles.to_csv(save_path, index=False)
        messagebox.showinfo("Done", f"Exported {len(unique_handles)} handles.")

def start_gui():
    root = tk.Tk()
    root.iconbitmap("favicon.ico")
    root.title("Missing Images")
    root.geometry("250x60")
    root.resizable(False, False)
    root.configure(bg="#E6E6E6")
    frame = tk.Frame(root)
    frame.pack(padx=20, pady=20)
    btn = tk.Button(
        frame, 
        fg="#ffffff", 
        bg="#7AB55C", 
        activeforeground="#ffffff",
        activebackground="#88C26A",
        text="Select CSV", 
        command=get_images, 
        width="20", 
        borderwidth=0, 
        highlightthickness=0
    )
    btn.pack()
    root.mainloop()