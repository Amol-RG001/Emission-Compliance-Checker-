import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from emissions import calculate_emissions, check_compliance
from report import generate_pdf_report

def run_checker():
    try:
        fuel_type = fuel_var.get()
        hours = float(hours_entry.get())
        power = float(power_entry.get())
        emissions = calculate_emissions(fuel_type, hours, power)
        compliance = check_compliance(emissions)

        result_text.set("\n".join(
            f"{p}: {v} g/kWh | {'PASS' if compliance[p] else 'FAIL'}"
            for p, v in emissions.items()
        ))

        if messagebox.askyesno("Save Report", "Do you want to save a PDF report?"):
            filename = filedialog.asksaveasfilename(defaultextension=".pdf")
            if filename:
                #generate_pdf_report(filename, fuel_type, emissions, compliance)
                from emissions import load_datasets
                _, limits = load_datasets()
                generate_pdf_report(filename, fuel_type, power, hours, emissions, limits)
                messagebox.showinfo("Success", "Report saved successfully!")

    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Emission Compliance Checker")
root.geometry("400x300")

fuel_var = tk.StringVar(value="Diesel")
fuel_label = tk.Label(root, text="Fuel Type:")
fuel_label.pack()
fuel_dropdown = ttk.Combobox(root, textvariable=fuel_var, values=["Diesel", "Petrol", "CNG"])
fuel_dropdown.pack()

hours_label = tk.Label(root, text="Operating Hours:")
hours_label.pack()
hours_entry = tk.Entry(root)
hours_entry.pack()

power_label = tk.Label(root, text="Power Output (kW):")
power_label.pack()
power_entry = tk.Entry(root)
power_entry.pack()

ttk.Button(root, text="Check Compliance", command=run_checker).pack(pady=10)
result_text = tk.StringVar()
tk.Label(root, textvariable=result_text, justify="left").pack()

root.mainloop()
