# 💸 BudgetWise

## 💻 Contributors

- **Kevin Ha** – Backend architecture, ORM modeling, API routes, wireframes
- **Brendan Dishion** – GUI development, user experience, frontend integration, some backend routing/modeling

---

**BudgetWise** is a personal budgeting desktop application built with **Tkinter** and powered by a **Flask** backend. It helps users track income, manage expenses, and visualize spending trends in real time through an intuitive interface.

---

## 📌 Features

- **User Authentication** – Register and log in securely.
- **Budget Dashboard** – Track budgets, expenses, and remaining balance.
- **Transaction Management** – Add, edit, and view transaction history.
- **Category Tracking** – Organize expenses by category (e.g., Food, Bills, etc.).
- **Visual Analytics** – Real-time charts and progress bars with Matplotlib.
- **Data Persistence** – SQLAlchemy-based ORM models for efficient storage.

---

## 📦 Dependencies

- Flask
- Flask-RESTful
- SQLAlchemy
- Tkinter (built-in for Python)
- Matplotlib

*All dependencies are included in `requirements.txt`*

---

## 🛠️ Technologies Used

- **Frontend:** Python `Tkinter`, `Matplotlib`
- **Backend:** `Flask`, `Flask-RESTful`, `SQLAlchemy`
- **Database:** SQLite
- **Project Structure:** Modularized with clear separation of GUI, routes, and models

---

## 📁 Project (File Overview) Structure

```
BudgetWise/
├── server/
│   ├── run.py                 # Flask app entry point
│   ├── budgetwise_gui.py      # Main Tkinter GUI interface
│   ├── config.py              # App configuration settings
│   ├── database.py            # DB connection setup
│   ├── requirements.txt       # Python dependencies
│   ├── models/                # SQLAlchemy ORM models
│   │   ├── user.py
│   │   ├── transaction.py
│   │   └── budget.py
│   └── app/
│       └── routes/            # Flask route handlers
│           ├── auth_routes.py
│           ├── budget_routes.py
│           └── transaction_routes.py
├── budgetwise.db
└── README.md
```

---

## 🚀 Setup and Execution Instructions

1. Clone the Repository
```bash
git clone https://github.com/kevinh81760/BudgetWise.git
cd BudgetWise
```

2. Switch to the Correct Branch  
If you're not on the working branch, switch to `frontend-updates`:
```bash
git checkout frontend-updates
```

3. Set Up a Virtual Environment

On Windows:
```bash
python -m venv BudgetWiseVenv
BudgetWiseVenv\Scripts\activate
```

On macOS/Linux:
```bash
python3 -m venv BudgetWiseVenv
source BudgetWiseVenv/bin/activate
```

4. Install Dependencies  
Run this from the project root:
```bash
pip install -r server/requirements.txt
```

5. Run the Flask Backend  
From the project root:
```bash
python -m server.run
```

6. Run the GUI (in a separate terminal)  
Open a new terminal window, navigate to the project root, and activate your virtual environment again:

On Windows:
```bash
BudgetWiseVenv\Scripts\activate
python server/budgetwise_gui.py
```

On macOS/Linux:
```bash
source BudgetWiseVenv/bin/activate
python server/budgetwise_gui.py
```

### 💡 Recommended Setup Tool

We recommend using **[Visual Studio Code](https://code.visualstudio.com/)** to run BudgetWise. It makes it easier to:

- Open the project folder
- Use the built-in terminal for activating the virtual environment and running scripts
- Keep both backend and GUI windows accessible in one place

No advanced setup is required — just open the folder and follow the steps in the terminal.

USE THE GUI in Fullscreen for full data view (App is designed to be ran on FullScreen Desktop)

---

## 🐞 Known Bugs or Limitations

- No major bugs currently known.
- Currently does not support exporting data to CSV or PDF.
- GUI is optimized for desktop — may require adjustments for scaling on smaller screens.

---

## 📌 Future Improvements

- Add user profile management  
- Export reports as CSV or PDF  
- Multi-platform packaging (using PyInstaller)