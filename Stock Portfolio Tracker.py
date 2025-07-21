import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

# --- CONSTANTS ---
STOCK_PRICES = {
    "AAPL": 180,
    "TSLA": 250,
    "GOOGL": 2700,
    "MSFT": 310,
    "AMZN": 3300
}

portfolio = {}


# --- CORE LOGIC FUNCTIONS ---

def calculate_total():
    """Calculate and return total portfolio value."""
    return sum(qty * STOCK_PRICES[stock] for stock, qty in portfolio.items())


def update_display():
    """Update the text area and total label."""
    textbox.config(state='normal')
    textbox.delete(1.0, tk.END)

    lines = [
        f"{'Stock':<10} {'Qty':<10} {'Price':<10} {'Value':<10}",
        "-" * 45
    ]

    for stock, qty in portfolio.items():
        price = STOCK_PRICES[stock]
        value = qty * price
        lines.append(f"{stock:<10} {qty:<10.2f} {price:<10.2f} {value:<10.2f}")

    textbox.insert(tk.END, "\n".join(lines))
    textbox.config(state='disabled')

    total = calculate_total()
    total_var.set(f"💰 Total Investment: ${total:.2f}")


def add_stock():
    """Add a stock and update."""
    stock = stock_var.get().upper()
    qty_str = qty_var.get()

    if stock not in STOCK_PRICES:
        messagebox.showerror("Invalid Stock", f"Stock '{stock}' not in price list.")
        return

    try:
        qty = float(qty_str)
        if qty <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Quantity", "Quantity must be a positive number.")
        return

    portfolio[stock] = portfolio.get(stock, 0) + qty
    stock_var.set("")
    qty_var.set("")
    update_display()


def save_portfolio():
    """Save portfolio to CSV."""
    if not portfolio:
        messagebox.showwarning("Empty", "Portfolio is empty!")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return

    try:
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Stock", "Quantity", "Price", "Value"])
            for stock, qty in portfolio.items():
                price = STOCK_PRICES[stock]
                value = qty * price
                writer.writerow([stock, f"{qty:.2f}", f"{price:.2f}", f"{value:.2f}"])
            writer.writerow([])
            writer.writerow(["Total Investment", "", "", f"{calculate_total():.2f}"])
        messagebox.showinfo("Saved", f"Portfolio saved to:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def load_portfolio():
    """Load portfolio from CSV."""
    global portfolio
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return

    try:
        portfolio.clear()
        with open(file_path, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            for row in reader:
                if not row or row[0] == "Total Investment":
                    break
                stock, qty_str = row[0], row[1]
                if stock in STOCK_PRICES:
                    portfolio[stock] = float(qty_str)
        update_display()
        messagebox.showinfo("Loaded", f"Portfolio loaded from:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def clear_portfolio():
    """Clear portfolio."""
    if messagebox.askyesno("Confirm", "Are you sure you want to clear your portfolio?"):
        portfolio.clear()
        update_display()


# --- GUI SETUP ---

root = tk.Tk()
root.title("📈 Stock Portfolio Tracker")
root.geometry("700x550")
root.resizable(False, False)

frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

# Input fields
ttk.Label(frame, text="Stock Symbol:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
stock_var = tk.StringVar()
stock_entry = ttk.Entry(frame, textvariable=stock_var, width=15)
stock_entry.grid(row=0, column=1, sticky=tk.W, padx=5)

ttk.Label(frame, text="Quantity:").grid(row=0, column=2, sticky=tk.W, padx=5)
qty_var = tk.StringVar()
qty_entry = ttk.Entry(frame, textvariable=qty_var, width=10)
qty_entry.grid(row=0, column=3, sticky=tk.W, padx=5)

add_btn = ttk.Button(frame, text="➕ Add Stock", command=add_stock)
add_btn.grid(row=0, column=4, padx=10)

# Textbox for portfolio display
textbox = tk.Text(frame, height=20, width=80, bg="#f8f8f8", fg="black", state='disabled', font=("Courier", 10))
textbox.grid(row=1, column=0, columnspan=5, pady=10)

# Total Investment label
total_var = tk.StringVar(value="💰 Total Investment: $0.00")
total_label = ttk.Label(frame, textvariable=total_var, font=("Arial", 12, "bold"), foreground="green")
total_label.grid(row=2, column=0, columnspan=5, pady=5)

# Buttons
save_btn = ttk.Button(frame, text="💾 Save Portfolio", command=save_portfolio)
save_btn.grid(row=3, column=0, pady=10)

load_btn = ttk.Button(frame, text="📂 Load Portfolio", command=load_portfolio)
load_btn.grid(row=3, column=1, pady=10)

clear_btn = ttk.Button(frame, text="🧹 Clear Portfolio", command=clear_portfolio)
clear_btn.grid(row=3, column=2, pady=10)

quit_btn = ttk.Button(frame, text="🚪 Quit", command=root.destroy)
quit_btn.grid(row=3, column=4, pady=10)

root.mainloop()
