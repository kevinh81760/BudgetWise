import tkinter as tk
from tkinter import ttk
import requests
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

CURRENT_USER_ID = None

root = tk.Tk()
root.title("BudgetWise")
root.geometry("1000x800")
root.configure(bg="black")

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
tk.Button(auth_frame, text="Sign In", command=lambda: show_frame(login_frame), font=("Arial", 12), bg="#333", fg="white").pack(pady=10)
tk.Button(auth_frame, text="Create Account", command=lambda: show_frame(register_frame), font=("Arial", 12), bg="#333", fg="white").pack(pady=10)
tk.Button(auth_frame, text="Back", command=lambda: show_frame(landing_frame), font=("Arial", 10), bg="gray", fg="white").pack(pady=30)

# ------------ Login Form -------------- #
tk.Label(login_frame, text="Sign In", font=("Arial", 18), bg="black", fg="white").pack(pady=20)
login_username = tk.Entry(login_frame)
login_password = tk.Entry(login_frame, show="*")
tk.Label(login_frame, text="Username", bg="black", fg="white").pack()
login_username.pack()
tk.Label(login_frame, text="Password", bg="black", fg="white").pack()
login_password.pack()

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
        print("Logged in successfully!")
        load_transactions_to_graph()
        display_transactions()
        display_budgets()
    else:
        print("Login failed:", response.text)

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
        print("Account created! Now you can login.")
        show_frame(login_frame)
    else:
        print("Registration failed:", response.text)

tk.Button(register_frame, text="Register", command=register_user, bg="#333", fg="white").pack(pady=10)
tk.Button(register_frame, text="Back", command=lambda: show_frame(auth_frame), font=("Arial", 10), bg="gray", fg="white").pack()

# ------------ Landing Page Layout -------------- #
tk.Label(landing_frame, text="BudgetWise", font=("Arial", 28, "bold"), fg="white", bg="black").pack(pady=20)
tk.Button(landing_frame, text="Sign In", command=lambda: show_frame(auth_frame), font=("Arial", 10), bg="#222", fg="white").place(relx=0.93, rely=0.03, anchor="ne")

# Scrollable Tracking Frame
transaction_container = tk.Frame(landing_frame, bg="#121212", bd=1, relief="ridge")
transaction_container.place(relx=0.05, rely=0.15, relwidth=0.45, relheight=0.25)

transaction_canvas = tk.Canvas(transaction_container, bg="#121212", highlightthickness=0)
transaction_scrollbar = tk.Scrollbar(transaction_container, orient="vertical", command=transaction_canvas.yview)

tracking_frame = tk.Frame(transaction_canvas, bg="#121212")

tracking_frame.bind(
    "<Configure>",
    lambda e: transaction_canvas.configure(scrollregion=transaction_canvas.bbox("all"))
)
transaction_canvas.create_window((0, 0), window=tracking_frame, anchor="nw")
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
budget_canvas.create_window((0, 0), window=goals_frame, anchor="nw")
budget_canvas.configure(yscrollcommand=budget_scrollbar.set)
budget_canvas.pack(side="left", fill="both", expand=True)
budget_scrollbar.pack(side="right", fill="y")

# Income/Expense Section
income_label = tk.Label(tracking_frame, text="Income & Expense Tracking", bg="#121212", fg="white", font=("Arial", 12, "bold"))
income_label.pack(pady=(5,0))

add_transaction_btn = tk.Button(tracking_frame, text="+ Add Transaction", bg="#222", fg="white")
add_transaction_btn.pack(pady=5)

transaction_form = tk.Frame(tracking_frame, bg="#121212")
category_entry = tk.Entry(transaction_form, width=20)
amount_entry = tk.Entry(transaction_form, width=20)
date_entry = tk.Entry(transaction_form, width=20)
category_entry.insert(0, "Category")
amount_entry.insert(0, "Amount")
date_entry.insert(0, "YYYY-MM-DD")
category_entry.pack(pady=1)
amount_entry.pack(pady=1)
date_entry.pack(pady=1)
submit_btn = tk.Button(transaction_form, text="Submit", command=lambda: submit_transaction(), bg="#444", fg="white")
submit_btn.pack(pady=5)
transaction_form.pack_forget()

# Budget Section
budget_label = tk.Label(goals_frame, text="Budget Goals", bg="#121212", fg="white", font=("Arial", 12, "bold"))
budget_label.pack(pady=(5,0))

add_budget_btn = tk.Button(goals_frame, text="+ Add Budget", bg="#222", fg="white")
add_budget_btn.pack(pady=5)

budget_form = tk.Frame(goals_frame, bg="#121212")
budget_cat_entry = tk.Entry(budget_form, width=20)
limit_entry = tk.Entry(budget_form, width=20)
budget_start_entry = tk.Entry(budget_form, width=20)
budget_end_entry = tk.Entry(budget_form, width=20)
budget_cat_entry.insert(0, "Category")
limit_entry.insert(0, "Limit")
budget_start_entry.insert(0, "Start YYYY-MM-DD")
budget_end_entry.insert(0, "End YYYY-MM-DD")
budget_cat_entry.pack(pady=1)
limit_entry.pack(pady=1)
budget_start_entry.pack(pady=1)
budget_end_entry.pack(pady=1)
tk.Button(budget_form, text="Submit", command=lambda: submit_budget(), bg="#444", fg="white").pack(pady=5)
budget_form.pack_forget()

add_transaction_btn.config(command=lambda: transaction_form.pack())
add_budget_btn.config(command=lambda: budget_form.pack())

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
        dates = [item["date_created"][:10] for item in data]
        amounts = [item["amount"] for item in data]
        ax.plot(dates, amounts, marker="o", color="white", linewidth=2)
        ax.set_facecolor("#121212")
        ax.set_title("Spending Trend", color="white")
        ax.set_ylabel("Amount ($)", color="white")
        ax.tick_params(colors="white")
        fig.patch.set_facecolor("#121212")
        chart_canvas.draw()

def submit_transaction():
    if CURRENT_USER_ID is None:
        return
    data = {
        "user_id": CURRENT_USER_ID,
        "category": category_entry.get(),
        "amount": float(amount_entry.get()),
        "date_created": date_entry.get()
    }
    response = requests.post("http://localhost:5000/transactions", json=data)
    if response.status_code == 201:
        print("Transaction added!")
        load_transactions_to_graph()
        display_transactions()

def submit_budget():
    if CURRENT_USER_ID is None:
        return
    data = {
        "user_id": CURRENT_USER_ID,
        "category": budget_cat_entry.get(),
        "limit_amount": float(limit_entry.get()),
        "start_date": budget_start_entry.get(),
        "end_date": budget_end_entry.get()
    }
    response = requests.post("http://localhost:5000/budget", json=data)
    if response.status_code == 201:
        print("Budget goal added!")
        display_budgets()

def display_transactions():
    if CURRENT_USER_ID is None:
        return

    # Clear only transaction rows and column headers, keep label and add button
    for widget in tracking_frame.winfo_children():
        if widget not in [income_label, add_transaction_btn, transaction_form]:
            widget.destroy()

    # Column headers
    header_frame = tk.Frame(tracking_frame, bg="#121212")
    header_frame.pack(fill="x", pady=(5, 2))
    tk.Label(header_frame, text="Date", width=15, bg="#121212", fg="gray", anchor="w").grid(row=0, column=0)
    tk.Label(header_frame, text="Description", width=25, bg="#121212", fg="gray", anchor="w").grid(row=0, column=1)
    tk.Label(header_frame, text="Amount", width=15, bg="#121212", fg="gray", anchor="w").grid(row=0, column=2)

    # Transactions list
    response = requests.get(f"http://localhost:5000/transactions/{CURRENT_USER_ID}")
    if response.status_code != 200:
        print("Failed to load transactions:", response.text)
        return

    data = response.json()
    for i, txn in enumerate(data):
        row = tk.Frame(tracking_frame, bg="#121212")
        row.pack(fill="x", pady=1)
        tk.Label(row, text=txn["date_created"][:10], width=15, bg="#121212", fg="white", anchor="w").grid(row=0, column=0)
        tk.Label(row, text=txn["category"], width=25, bg="#121212", fg="white", anchor="w").grid(row=0, column=1)
        tk.Label(row, text=f"${txn['amount']:.2f}", width=15, bg="#121212", fg="white", anchor="w").grid(row=0, column=2)

def display_budgets():
    for widget in goals_frame.pack_slaves():
        if isinstance(widget, tk.Label) and widget.cget("text") not in ["Budget Goals"]:
            widget.destroy()
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
            percent = min(1.0, spent / limit) if limit else 0
            tk.Label(goals_frame, text=f"{cat}: ${spent:.0f} / ${limit:.0f}", bg="#121212", fg="white").pack()
            ttk.Progressbar(goals_frame, value=percent*100, maximum=100).pack(fill="x", padx=20, pady=2)

show_frame(landing_frame)
root.mainloop()
