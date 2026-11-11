import logging
from flask import Flask, render_template, request, redirect, url_for
from db import init_db, get_db_connection

app = Flask(__name__)

init_db()

@app.route("/expense", methods=["GET", "POST"])
@app.route("/expense/<int:expense_id>", methods=["GET", "POST"])
def expense(expense_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        if request.method == "POST":
            action = request.form.get("action")
            title = request.form.get("title")
            amount = float(request.form.get("amount", 0))
            category = request.form.get("category")
            date =  request.form.get("date")

            if action == "delete" and expense_id is not None :
                cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
                conn.commit()
                return redirect(url_for("expense"))
            
            if expense_id is not None:
                cursor.execute(
                    "UPDATE expenses SET title = ?, amount = ?, category = ?, date = ? WHERE id = ?",
                    (title, amount, category, date, expense_id)
                )
                conn.commit()
                return redirect(url_for("expense"))
            else:
                cursor.execute(
                    "INSERT INTO expenses (title, amount, category, date) VALUES (?, ?, ?, ?)",
                    (title, amount, category, date)
                )
                conn.commit()
                return redirect(url_for("expense"))

        expenses = cursor.execute("SELECT * FROM expenses").fetchall()
        edit_expense = None
        if expense_id is not None:
            edit_expense = cursor.execute(
                "SELECT * FROM expenses WHERE id = ?", 
                (expense_id,)
            ).fetchone()

            if edit_expense is None:
                abort(404)
        app.logger.info(f"{expenses} vimal=========")
        total = sum(float(item["amount"]) for item in expenses)
        return render_template("expense.html", expenses=expenses, total=total, edit_expense=edit_expense)
    finally:
        conn.close()

@app.route("/expenseDetails/<int:expense_id>", methods=["GET", "POST"])
def expense_details(expense_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    expense = cursor.execute(
        "SELECT * FROM expenses WHERE id = ?", 
        (expense_id,)
    ).fetchone()

    conn.close()

    app.logger.info(f"{expense_id} {expense}=========")
    return render_template("expenseDetails.html", expense=expense)


if __name__ == "__main__":
    app.run(debug=True)