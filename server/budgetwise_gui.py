import tkinter as tk
from tkinter import ttk, messagebox
import requests
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
from tkcalendar import DateEntry

CURRENT_USER_ID = None

root = tk.Tk()
root.title("BudgetWise")
root.geometry("1000x800")
root.configure(bg="black")

style = ttk.Style()
style.theme_use('default')
style.configure("green.Horizontal.TProgressbar", troughcolor="#333333", background="green") # Green bar for within budget
style.configure("red.Horizontal.TProgressbar", troughcolor="#333333", background="red") # Red bar for exceeding budget

# ------------ Frames -------------- #
landing_frame = tk.Frame(root, bg="black")
auth_frame = tk.Frame(root, bg="black")
login_frame = tk.Frame(root, bg="black")
register_frame = tk.Frame(root, bg="black")

for frame in (landing_frame, auth_frame, login_frame, register_frame):
    frame.place(relwidth=1, relheight=1)

def show_frame(frame):
    frame.tkraise()

# ------------ Auth Navigation -------------- #
tk.Label(auth_frame, text="Sign In or Create Account", font=("Arial", 18), bg="black", fg="white").pack(pady=40)

user_action_button = tk.Button(landing_frame, font=("Arial", 10), bg="#222", fg="white")
user_action_button.place(relx=0.93, rely=0.03, anchor="ne")
user_action_button.config(text="Sign In", command=lambda: show_frame(auth_frame))

tk.Button(auth_frame, text="Sign In", command=lambda: show_frame(login_frame), font=("Arial", 12), bg="#333", fg="white").pack(pady=10)
tk.Button(auth_frame, text="Create Account", command=lambda: show_frame(register_frame), font=("Arial", 12), bg="#333", fg="white").pack(pady=10)
tk.Button(auth_frame, text="Back", command=lambda: show_frame(landing_frame), font=("Arial", 10), bg="gray", fg="white").pack(pady=30)

# ------------ Login/Logout Form -------------- #
tk.Label(login_frame, text="Sign In", font=("Arial", 18), bg="black", fg="white").pack(pady=20)
login_username = tk.Entry(login_frame)
login_password = tk.Entry(login_frame, show="*")
tk.Label(login_frame, text="Username", bg="black", fg="white").pack()
login_username.pack()
tk.Label(login_frame, text="Password", bg="black", fg="white").pack()
login_password.pack()

def clear_transactions():
    for widget in tracking_frame.winfo_children():
        if widget != transaction_header_wrapper:
            widget.destroy()

def clear_budgets():
    for widget in goals_frame.winfo_children():
        if widget != budget_header_wrapper:
            widget.destroy()

def clear_chart():
    ax.clear()
    ax.set_facecolor("#121212")
    ax.set_title("Income & Expense Trend", color="white")
    ax.set_ylabel("Amount ($)", color="white")
    ax.tick_params(colors="white")
    fig.patch.set_facecolor("#121212")
    chart_canvas.draw()
            
def logout_user():
    global CURRENT_USER_ID
    CURRENT_USER_ID = None
    user_action_button.config(text="Sign In", command=lambda: show_frame(auth_frame))
    
    # Clear the login fields
    login_username.delete(0, tk.END)
    login_password.delete(0, tk.END)
    
    # Clear old transactions and budgets when user signs out
    clear_transactions()
    clear_budgets()
    clear_chart()
    messagebox.showinfo("Log Out Sucess", "You have been logged out and your data has been cleared.")
 
    show_frame(auth_frame)

def login_user():
    global CURRENT_USER_ID
    data = {
        "username": login_username.get(),
        "password": login_password.get()
    }
    response = requests.post("http://localhost:5000/login", json=data)
    if response.status_code == 200:
        CURRENT_USER_ID = response.json()["user_id"]
        show_frame(landing_frame)
        user_action_button.config(text="Logout", command=logout_user)
        load_transactions_to_graph()
        display_transactions()
        display_budgets()
        messagebox.showinfo("Login Success", "Logged In Successfully!")
    else:
        messagebox.showinfo("401 Login Failure", "Login Failed: Invalid Username/Password")

tk.Button(login_frame, text="Login", command=login_user, bg="#333", fg="white").pack(pady=10)
tk.Button(login_frame, text="Back", command=lambda: show_frame(auth_frame), font=("Arial", 10), bg="gray", fg="white").pack()

# ------------ Register Form -------------- #
tk.Label(register_frame, text="Create Account", font=("Arial", 18), bg="black", fg="white").pack(pady=20)
register_username = tk.Entry(register_frame)
register_password = tk.Entry(register_frame, show="*")
tk.Label(register_frame, text="Username", bg="black", fg="white").pack()
register_username.pack()
tk.Label(register_frame, text="Password", bg="black", fg="white").pack()
register_password.pack()

def register_user():
    data = {
        "username": register_username.get(),
        "password": register_password.get()
    }
    response = requests.post("http://localhost:5000/register", json=data)
    if response.status_code == 201:
        messagebox.showinfo("Registration Success", "You can now sign into your account.")
        show_frame(login_frame)
    elif response.status_code == 409:
        messagebox.showinfo("409 Registration Failure", "Username already exists!")
    else:
        messagebox.showinfo("400 Regsitration Failure", "Missing input fields!")
        

tk.Button(register_frame, text="Register", command=register_user, bg="#333", fg="white").pack(pady=10)
tk.Button(register_frame, text="Back", command=lambda: show_frame(auth_frame), font=("Arial", 10), bg="gray", fg="white").pack()

# ------------ Landing Page Layout -------------- #
tk.Label(landing_frame, text="BudgetWise", font=("Arial", 28, "bold"), fg="white", bg="black").pack(pady=20)

# Scrollable Transaction Frame
transaction_container = tk.Frame(landing_frame, bg="#121212", bd=1, relief="ridge")
transaction_container.place(relx=0.05, rely=0.15, relwidth=0.45, relheight=0.25)

transaction_canvas = tk.Canvas(transaction_container, bg="#121212", highlightthickness=0)
transaction_scrollbar = tk.Scrollbar(transaction_container, orient="vertical", command=transaction_canvas.yview)

tracking_frame = tk.Frame(transaction_canvas, bg="#121212")

tracking_frame.bind(
    "<Configure>",
    lambda e: transaction_canvas.configure(scrollregion=transaction_canvas.bbox("all"))
)

def resize_transaction_frame(event):
    transaction_canvas.itemconfig(transaction_window, width=event.width)

transaction_window = transaction_canvas.create_window((0.5, 0), window=tracking_frame, anchor="n")
transaction_canvas.configure(yscrollcommand=transaction_scrollbar.set)
transaction_canvas.pack(side="left", fill="both", expand=True)
transaction_scrollbar.pack(side="right", fill="y")

# Scrollable Goals Frame
budget_container = tk.Frame(landing_frame, bg="#121212", bd=1, relief="ridge")
budget_container.place(relx=0.525, rely=0.15, relwidth=0.45, relheight=0.25)

budget_canvas = tk.Canvas(budget_container, bg="#121212", highlightthickness=0)
budget_scrollbar = tk.Scrollbar(budget_container, orient="vertical", command=budget_canvas.yview)

goals_frame = tk.Frame(budget_canvas, bg="#121212")

goals_frame.bind(
    "<Configure>",
    lambda e: budget_canvas.configure(scrollregion=budget_canvas.bbox("all"))
)

def resize_budget_frame(event):
    budget_canvas.itemconfig(budget_window, width=event.width)
    
budget_window = budget_canvas.create_window((0.5, 0), window=goals_frame, anchor="n")
budget_canvas.configure(yscrollcommand=budget_scrollbar.set)
budget_canvas.pack(side="left", fill="both", expand=True)
budget_scrollbar.pack(side="right", fill="y")

transaction_canvas.bind("<Configure>", resize_transaction_frame)
budget_canvas.bind("<Configure>", resize_budget_frame)

# Income/Expense Section
transaction_header_wrapper = tk.Frame(tracking_frame, bg="#121212")
transaction_header_wrapper.pack(pady=(5, 0))

income_label = tk.Label(transaction_header_wrapper, text="Income & Expense Tracking", bg="#121212", fg="white", font=("Arial", 12, "bold"))
income_label.pack()

add_transaction_btn = tk.Button(transaction_header_wrapper, text="+ Add Transaction", bg="#222", fg="white")
add_transaction_btn.pack(pady=5)

transaction_form = tk.Frame(transaction_header_wrapper, bg="#121212")
transaction_form.pack_forget()

category_entry = ttk.Combobox(transaction_form, values=[
    "Food", "Transportation", "Housing", "Entertainment", 
    "Utilities", "Healthcare", "Savings", "Other"
], state="readonly", width=18)

amount_entry = tk.Entry(transaction_form, width=20)
date_entry = DateEntry(transaction_form, width=18, background="black", foreground="white", borderwidth=2, date_pattern='yyyy-mm-dd')
type_entry = ttk.Combobox(transaction_form, values=["Income", "Expense"], state="readonly", width=18)
transaction_form.pack_forget() 

category_entry.set("Select Category")
amount_entry.insert(0, "Amount ($)")
type_entry.set("Expense") 

category_entry.pack(pady=1)
amount_entry.pack(pady=1)
date_entry.pack(pady=1)
type_entry.pack(pady=1)

submit_btn = tk.Button(transaction_form, text="Submit", command=lambda: submit_transaction(), bg="#444", fg="white")
submit_btn.pack(pady=5)
transaction_form.pack_forget()

# Budget Section
budget_header_wrapper = tk.Frame(goals_frame, bg="#121212")
budget_header_wrapper.pack(pady=(5, 0))

budget_label = tk.Label(budget_header_wrapper, text="Budget Goals", bg="#121212", fg="white", font=("Arial", 12, "bold"))
budget_label.pack()

add_budget_btn = tk.Button(budget_header_wrapper, text="+ Add Budget", bg="#222", fg="white")
add_budget_btn.pack(pady=5)

budget_form = tk.Frame(budget_header_wrapper, bg="#121212")
budget_form.pack_forget()

budget_cat_entry = ttk.Combobox(budget_form, values=[
    "Food", "Transportation", "Housing", "Entertainment", 
    "Utilities", "Healthcare", "Savings", "Other"
], state="readonly", width=18)

limit_entry = tk.Entry(budget_form, width=20)
budget_start_entry = DateEntry(budget_form, width=18, background="black", foreground="white", borderwidth=2, date_pattern='yyyy-mm-dd')
budget_end_entry = DateEntry(budget_form, width=18, background="black", foreground="white", borderwidth=2, date_pattern='yyyy-mm-dd')

budget_cat_entry.set("Select Category")
limit_entry.insert(0, "Budget Limit ($)")

budget_cat_entry.pack(pady=1)
limit_entry.pack(pady=1)
budget_start_entry.pack(pady=1)
budget_end_entry.pack(pady=1)

tk.Button(budget_form, text="Submit", command=lambda: submit_budget(), bg="#444", fg="white").pack(pady=5)
budget_form.pack_forget()

def toggle_transaction_form():
    if transaction_form.winfo_ismapped():
        transaction_form.pack_forget()
        add_transaction_btn.config(text="+ Add Transaction")
    else:
        transaction_form.pack(pady=5)
        add_transaction_btn.config(text="– Hide Transaction")
        
add_transaction_btn.config(command=toggle_transaction_form)

def toggle_budget_form():
    if budget_form.winfo_ismapped():
        budget_form.pack_forget()
        add_budget_btn.config(text="+ Add Budget")
    else:
        budget_form.pack(pady=5)
        add_budget_btn.config(text="– Hide Budget")
        
add_budget_btn.config(command=toggle_budget_form)

# Chart
chart_frame = tk.Frame(landing_frame, bg="#121212", bd=1, relief="ridge")
chart_frame.place(relx=0.05, rely=0.45, relwidth=0.9, relheight=0.5)
fig = Figure(figsize=(5, 3), dpi=100)
ax = fig.add_subplot(111)
chart_canvas = FigureCanvasTkAgg(fig, master=chart_frame)
chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def load_transactions_to_graph():
    ax.clear()
    if CURRENT_USER_ID is None:
        return
    
    response = requests.get(f"http://localhost:5000/transactions/{CURRENT_USER_ID}")
    if response.status_code == 200:
        data = response.json()
        
        # Group the data by type (Income/Expense) & Date of Transaction
        expense_by_date = defaultdict(float)
        income_by_date = defaultdict(float)

        for item in data:
            date = item["date_created"][:10]
            amount = item["amount"]
            if item["type"] == "Expense":
                expense_by_date[date] += amount
            elif item["type"] == "Income":
                income_by_date[date] += amount
                
        # Sort user-transaction data by date
        sorted_dates = sorted(set(expense_by_date.keys()) | set(income_by_date.keys()))
        expense_values = [expense_by_date.get(d, 0) for d in sorted_dates]
        income_values = [income_by_date.get(d, 0) for d in sorted_dates]

        # Plot both lines (Expense and Income)
        ax.plot(sorted_dates, expense_values, marker="o", color="red", linewidth=2, label="Expenses")
        ax.plot(sorted_dates, income_values, marker="o", color="green", linewidth=2, label="Income")

        # Final chart configuration
        ax.set_facecolor("#121212")
        ax.set_title("Income & Expense Trend", color="white")
        ax.set_ylabel("Amount ($)", color="white")
        ax.tick_params(colors="white")
        ax.legend(facecolor="#121212", edgecolor="white", labelcolor="white")
        fig.patch.set_facecolor("#121212")
        chart_canvas.draw()

def submit_transaction():
    if CURRENT_USER_ID is None:
        messagebox.showerror("Unauthorized", "Please sign in to add a transaction.")
        return

    category = category_entry.get()
    amount_text = amount_entry.get()
    date = date_entry.get()
    type = type_entry.get()

    # Validate amount is a number
    try:
        amount = float(amount_text)
    except ValueError:
        messagebox.showerror("Input Error", "Amount must be a number.")
        return

    if not category or category == "Select Category" or not date or type not in ["Income", "Expense"]:
        messagebox.showerror("Input Error", "Please fill out all fields correctly.")
        return

    data = {
        "user_id": CURRENT_USER_ID,
        "category": category,
        "amount": amount,
        "date_created": date,
        "type": type
    }

    response = requests.post("http://localhost:5000/transactions", json=data)
    if response.status_code == 201:
        load_transactions_to_graph()
        display_transactions()
        display_budgets()
        messagebox.showinfo("Success", "Transaction added!")

        # Clear entries
        category_entry.set("Select Category")
        amount_entry.delete(0, tk.END)
        amount_entry.insert(0, "Amount ($)")
        type_entry.set("Expense")

        transaction_form.pack_forget()
        add_transaction_btn.config(text="+ Add Transaction")

def submit_budget():
    if CURRENT_USER_ID is None:
        messagebox.showerror("Unauthorized", "Please sign in to add a budget goal.")
        return

    category = budget_cat_entry.get()
    limit_text = limit_entry.get()
    start_date = budget_start_entry.get()
    end_date = budget_end_entry.get()

    # Validate category
    if not category or category == "Select Category":
        messagebox.showerror("Input Error", "Please select a valid budget category.")
        return

    # Validate limit is a number
    try:
        limit = float(limit_text)
    except ValueError:
        messagebox.showerror("Input Error", "Limit must be a number.")
        return

    if not start_date or not end_date:
        messagebox.showerror("Input Error", "Please provide valid start and end dates.")
        return

    data = {
        "user_id": CURRENT_USER_ID,
        "category": category,
        "limit_amount": limit,
        "start_date": start_date,
        "end_date": end_date
    }

    response = requests.post("http://localhost:5000/budget", json=data)
    if response.status_code == 201:
        display_budgets()
        messagebox.showinfo("Success", "Budget goal added successfully!")

        # Reset fields
        budget_cat_entry.set("Select Category")
        limit_entry.delete(0, tk.END)
        limit_entry.insert(0, "Limit Amount ($)")
        budget_start_entry.delete(0, tk.END)
        budget_start_entry.insert(0, "Start YYYY-MM-DD")
        budget_end_entry.delete(0, tk.END)
        budget_end_entry.insert(0, "End YYYY-MM-DD")

        budget_form.pack_forget()
        add_budget_btn.config(text="+ Add Budget")
    else:
        messagebox.showerror("Error", "Failed to add budget goal.")


def display_transactions():
    if CURRENT_USER_ID is None:
        return

    # Clear only transaction rows and column headers, keep label and add button
    for widget in tracking_frame.winfo_children():
        if widget != transaction_header_wrapper:
            widget.destroy()
    
    # Ensuring the form always comes right after the button
    transaction_form.pack_forget()

    # Wrapper 
    wrapper = tk.Frame(tracking_frame, bg="#121212")
    wrapper.pack(pady=5)

    # Column headers    
    tk.Label(wrapper, text="Date", width=16, bg="#121212", fg="gray", anchor="center").grid(row=0, column=0, padx=6, pady=2)
    tk.Label(wrapper, text="Category", width=26, bg="#121212", fg="gray", anchor="center").grid(row=0, column=1, padx=6, pady=2)
    tk.Label(wrapper, text="Amount", width=14, bg="#121212", fg="gray", anchor="center").grid(row=0, column=2, padx=6, pady=2)
    tk.Label(wrapper, text="Type", width=13, bg="#121212", fg="gray", anchor="center").grid(row=0, column=3, padx=6, pady=2)

    # Transactions list
    response = requests.get(f"http://localhost:5000/transactions/{CURRENT_USER_ID}")
    if response.status_code != 200:
        messagebox.showinfo("Failure", "Failed to load Transactions!")
        return

    data = response.json()
    for i, txn in enumerate(data, start=1):
        tk.Label(wrapper, text=txn["date_created"][:10], width=16, bg="#121212", fg="white", anchor="center").grid(row=i, column=0, padx=6, pady=1)
        tk.Label(wrapper, text=txn["category"], width=26, bg="#121212", fg="white", anchor="center").grid(row=i, column=1, padx=6, pady=1)
        tk.Label(wrapper, text=f"${txn['amount']:.2f}", width=14, bg="#121212", fg="white", anchor="center").grid(row=i, column=2, padx=6, pady=1)
        tk.Label(wrapper, text=txn["type"], width=13, bg="#121212", fg="white", anchor="center").grid(row=i, column=3, padx=6, pady=1)

        delete_btn = tk.Button(wrapper, text="X", bg="#aa0000", fg="white", font=("Arial", 8), width=3,
                           command=lambda txn_id=txn["id"]: delete_transaction_by_id(txn_id))
        delete_btn.grid(row=i, column=4, padx=6, pady=1)

def display_budgets():
    for widget in goals_frame.winfo_children():
        if widget != budget_header_wrapper:
            widget.destroy()
            
    budget_form.pack_forget()
    
    response = requests.get(f"http://localhost:5000/budgets/{CURRENT_USER_ID}")
    if response.status_code == 200:
        data = response.json()
        
        for budget in data:
            cat = budget["category"]
            limit = budget["limit_amount"]
            spent = 0
            transactions = requests.get(f"http://localhost:5000/transactions/{CURRENT_USER_ID}").json()
            
            for t in transactions:
                if t["category"] == cat and budget["start_date"] <= t["date_created"] <= budget["end_date"]:
                    spent += t["amount"]
            percent = spent / limit if limit else 0

             # Style choice based on budget status
            bar_style = "green.Horizontal.TProgressbar" if spent <= limit else "red.Horizontal.TProgressbar"

            tk.Label(goals_frame, text=f"{cat}: ${spent:.0f} / ${limit:.0f}", bg="#121212", fg="white").pack(anchor="w", padx=20)

            # Create a sub-frame for bar + delete button
            bar_frame = tk.Frame(goals_frame, bg="#121212")
            bar_frame.pack(fill="x", padx=20, pady=(0, 6))

            # Add progress bar 
            ttk.Progressbar(bar_frame, style=bar_style, value=min(percent, 1.0)*100, maximum=100, length=200).pack(side="left", fill="x", expand=True)

            # Add small delete button
            delete_btn = tk.Button(bar_frame, text="X", bg="#aa0000", fg="white", font=("Arial", 8), width=3, height=1,
                       command=lambda bid=budget["id"]: delete_budget_by_id(bid))
            delete_btn.pack(side="left", padx=(8, 0))

            
def delete_transaction_by_id(transaction_id):
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this transaction?")
    if confirm:
        response = requests.delete(f"http://localhost:5000/transaction/{transaction_id}")
        if response.status_code == 200:
            display_transactions()
            load_transactions_to_graph()
            display_budgets()
            messagebox.showinfo("Deleted", "Transaction deleted successfully.")
        else:
            messagebox.showerror("Error", "Failed to delete transaction.")

def delete_budget_by_id(budget_id):
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this budget?")
    if confirm:
        response = requests.delete(f"http://localhost:5000/budget/{budget_id}")
        if response.status_code == 200:
            display_budgets()
            messagebox.showinfo("Deleted", "Budget deleted successfully.")
        else:
            messagebox.showerror("Error", "Failed to delete budget.")


show_frame(landing_frame)
root.mainloop()
