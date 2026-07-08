import sqlite3

# ─── Database Connection ───────────────────────────────────────────────────────

def get_connection():
    # Returns a connection to the SQLite database
    return sqlite3.connect('expense.db')

# ─── Create Tables ─────────────────────────────────────────────────────────────

def create_table():
    # Creates income, expense, and category tables if they don't exist
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        create table if not exists income(
            income_id integer primary key,
            source text not null,
            amount real not null,
            description text not null,
            date datetime default current_timestamp
        )""")
    cursor.execute("""
        create table if not exists expense(
            expense_id integer primary key,
            category_id integer not null,
            amount real not null,
            description text not null,
            date datetime default current_timestamp
        )""")
    cursor.execute("""
        create table if not exists category(
            category_id integer primary key,
            category_name text not null
        )""")
    conn.commit()
    conn.close()
    print("connected to database successfully")

# ─── Income Functions ──────────────────────────────────────────────────────────

def add_income(income_id, source, amount, description):
    # Adds a new income record to the database
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("insert into income (income_id, source, amount, description) values(?,?,?,?)",
                       (income_id, source, amount, description))
        conn.commit()
        print(f"{source} added successfully")
    except sqlite3.Error as e:
        print(f"error while adding income {e}")
    finally:
        conn.close()

def view_income():
    # Displays all income records from the database
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("select * from income")
        results = cursor.fetchall()
        if not results:
            print("no income records found")
            return
        for r in results:
            print(f"Income ID: {r[0]} | Source: {r[1]} | Amount: {r[2]} | Description: {r[3]} | Date: {r[4]}")
    except sqlite3.Error as e:
        print(f"error while fetching data {e}")
    finally:
        conn.close()

def update_income(income_id):
    # Updates an existing income record by income_id
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("select source, amount, description from income where income_id=?", (income_id,))
    result = cursor.fetchone()
    if not result:
        print("no income found with this id")
        conn.close()
        return
    print(f"current info: Source: {result[0]}, Amount: {result[1]}, Description: {result[2]}")
    new_source = input(f"enter new source (or press enter to keep {result[0]}): ")
    new_amount = input(f"enter new amount (or press enter to keep {result[1]}): ")
    new_description = input(f"enter new description (or press enter to keep {result[2]}): ")

    # Keep existing values if user presses enter
    final_source = new_source if new_source.strip() != "" else result[0]
    final_amount = new_amount if new_amount.strip() != "" else result[1]
    final_description = new_description if new_description.strip() != "" else result[2]
    try:
        query = "update income set source=?, amount=?, description=? where income_id=?"
        values = (final_source, final_amount, final_description, income_id)
        cursor.execute(query, values)
        conn.commit()
        print("income info updated successfully")
    except sqlite3.Error as e:
        print(f"error while updating {e}")
    finally:
        conn.close()

def delete_income(income_id):
    # Deletes an income record by income_id
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("select source, amount, description, date from income where income_id=?", (income_id,))
        record = cursor.fetchone()
        if not record:
            print(f"error: no income found with id {income_id}")
            return
        cursor.execute("delete from income where income_id=?", (income_id,))
        conn.commit()
        print("income removed successfully")
    except sqlite3.Error as e:
        print(f"error while deleting income {e}")
    finally:
        conn.close()

# ─── Expense Functions ─────────────────────────────────────────────────────────

def add_expense(expense_id, category_id, amount, description):
    # Adds a new expense record to the database
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("insert into expense (expense_id, category_id, amount, description) values(?,?,?,?)",
                       (expense_id, category_id, amount, description))
        conn.commit()
        print("expense added successfully")
    except sqlite3.Error as e:
        print(f"error while adding expense {e}")
    finally:
        conn.close()

def view_expense():
    # Displays all expense records from the database
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("select * from expense")
        results = cursor.fetchall()
        if not results:
            print("no expense records found")
            return
        for r in results:
            print(f"Expense ID: {r[0]} | Category ID: {r[1]} | Amount: {r[2]} | Description: {r[3]} | Date: {r[4]}")
        print("expense fetched successfully")
    except sqlite3.Error as e:
        print(f"error while fetching data {e}")
    finally:
        conn.close()

def update_expense(expense_id):
    # Updates an existing expense record by expense_id
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("select category_id, amount, description from expense where expense_id=?", (expense_id,))
    result = cursor.fetchone()
    if not result:
        print("no expense found with this id")
        conn.close()
        return
    print(f"current info: Category ID: {result[0]}, Amount: {result[1]}, Description: {result[2]}")
    new_category_id = input(f"enter new category id (or press enter to keep {result[0]}): ")
    new_amount = input(f"enter new amount (or press enter to keep {result[1]}): ")
    new_description = input(f"enter new description (or press enter to keep {result[2]}): ")

    # Keep existing values if user presses enter
    final_category_id = new_category_id if new_category_id.strip() != "" else result[0]
    final_amount = new_amount if new_amount.strip() != "" else result[1]
    final_description = new_description if new_description.strip() != "" else result[2]
    try:
        query = "update expense set category_id=?, amount=?, description=? where expense_id=?"
        values = (final_category_id, final_amount, final_description, expense_id)
        cursor.execute(query, values)
        conn.commit()
        print("expense info updated successfully")
    except sqlite3.Error as e:
        print(f"error while updating expense {e}")
    finally:
        conn.close()

def delete_expense(expense_id):
    # Deletes an expense record by expense_id
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("select category_id, amount, description, date from expense where expense_id=?", (expense_id,))
        result = cursor.fetchone()
        if not result:
            print(f"error: no expense found with id {expense_id}")
            return
        cursor.execute("delete from expense where expense_id=?", (expense_id,))
        conn.commit()
        print("expense removed successfully")
    except sqlite3.Error as e:
        print(f"error while deleting expense {e}")
    finally:
        conn.close()

def balance_alert(threshold=5000):
    # Alerts user if current balance falls below the threshold
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("select sum(amount) from income")
        total_income = cursor.fetchone()[0]
        total_income = total_income if total_income is not None else 0

        cursor.execute("select sum(amount) from expense")
        total_expense = cursor.fetchone()[0]
        total_expense = total_expense if total_expense is not None else 0

        current_balance = total_income - total_expense
        print(f"current balance = {current_balance}")
        if current_balance < threshold:
            print(f"alert! your balance {current_balance} is below threshold {threshold}")
        else:
            print(f"your balance {current_balance} is above threshold {threshold}")
    except sqlite3.Error as e:
        print(f"error while checking balance {e}")
    finally:
        conn.close()

# ─── Category Functions ────────────────────────────────────────────────────────

def add_categories(category_id, category_name):
    # Adds a new category to the database
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("insert into category (category_id, category_name) values (?, ?)", (category_id, category_name))
        conn.commit()
        print("category added successfully")
    except sqlite3.Error as e:
        print(f"error while adding category {e}")
    finally:
        conn.close()

def view_categories():
    # Displays all categories from the database
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("select * from category")
        results = cursor.fetchall()
        if not results:
            print("no categories found")
            return
        for r in results:
            print(f"Category ID: {r[0]} | Category Name: {r[1]}")
        print("categories fetched successfully")
    except sqlite3.Error as e:
        print(f"error while fetching data {e}")
    finally:
        conn.close()

def update_categories(category_id, new_category_name):
    # Updates a category name by category_id
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("update category set category_name=? where category_id=?", (new_category_name, category_id))
        conn.commit()
        if cursor.rowcount > 0:
            print("category updated successfully")
        else:
            print("no category found with this id")
    except sqlite3.Error as e:
        print(f"error while updating category {e}")
    finally:
        conn.close()

def delete_categories(category_id):
    # Deletes a category by category_id
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("delete from category where category_id=?", (category_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print("category deleted successfully")
        else:
            print("no category found with this id")
    except sqlite3.Error as e:
        print(f"error while deleting category {e}")
    finally:
        conn.close()

# ─── Report Functions ──────────────────────────────────────────────────────────

def total_income():
    # Calculates and displays total income
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("select sum(amount) from income")
        res = cursor.fetchone()
        income_res = res[0] if res and res[0] is not None else 0
        print(f"total income = {income_res}")
        return income_res
    except sqlite3.Error as e:
        print(f"error while calculating total income {e}")
        return 0
    finally:
        conn.close()

def total_expense():
    # Calculates and displays total expense
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("select sum(amount) from expense")
        res = cursor.fetchone()
        expense_res = res[0] if res and res[0] is not None else 0
        print(f"total expense = {expense_res}")
        return expense_res
    except sqlite3.Error as e:
        print(f"error while calculating total expense {e}")
        return 0
    finally:
        conn.close()

def remaining_balance():
    # Calculates and displays remaining balance (income - expense)
    balance = total_income() - total_expense()
    print(f"remaining balance = {balance}")
    return balance

def highest_expense_category():
    # Finds and displays the category with the highest total expense
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """select c.category_name, sum(e.amount) as total_expense
                   from expense e join category c on e.category_id = c.category_id
                   group by c.category_name order by total_expense desc limit 1"""
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            print(f"category with highest expense is {result[0]} with expense = {result[1]}")
        else:
            print("no expense found")
    except sqlite3.Error as e:
        print(f"error while finding highest expense category {e}")
    finally:
        conn.close()

def monthly_report():
    # Generates a monthly income vs expense report
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("select strftime('%Y-%m', date) as month, sum(amount) from income group by month order by month desc")
        income_results = cursor.fetchall()
        cursor.execute("select strftime('%Y-%m', date) as month, sum(amount) from expense group by month order by month desc")
        expense_results = cursor.fetchall()
        income_dict = {row[0]: row[1] for row in income_results if row[0] is not None}
        expense_dict = {row[0]: row[1] for row in expense_results if row[0] is not None}
        all_months = sorted(list(set(income_dict.keys()) | set(expense_dict.keys())), reverse=True)
        if not all_months:
            print("no income or expense data found")
            return
        print(f"{'Month':<12} | {'Total Income':<15} | {'Total Expense':<15} | {'Net Balance':<15}")
        print("-" * 60)
        for month in all_months:
            income = income_dict.get(month, 0)
            expense = expense_dict.get(month, 0)
            net_balance = income - expense
            print(f"{month:<12} | {income:<15} | {expense:<15} | {net_balance:<15}")
    except sqlite3.Error as e:
        print(f"error while generating monthly report {e}")
    finally:
        conn.close()

def yearly_report():
    # Generates a yearly income vs expense report
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("select strftime('%Y', date) as year, sum(amount) from income group by year order by year desc")
        income_results = cursor.fetchall()
        cursor.execute("select strftime('%Y', date) as year, sum(amount) from expense group by year order by year desc")
        expense_results = cursor.fetchall()
        income_dict = {row[0]: row[1] for row in income_results if row[0] is not None}
        expense_dict = {row[0]: row[1] for row in expense_results if row[0] is not None}
        all_years = sorted(list(set(income_dict.keys()) | set(expense_dict.keys())), reverse=True)
        if not all_years:
            print("no income or expense data found")
            return
        print(f"{'Year':<12} | {'Total Income':<15} | {'Total Expense':<15} | {'Net Balance':<15}")
        print("-" * 60)
        for year in all_years:
            income = income_dict.get(year, 0)
            expense = expense_dict.get(year, 0)
            net_balance = income - expense
            print(f"{year:<12} | {income:<15} | {expense:<15} | {net_balance:<15}")
    except sqlite3.Error as e:
        print(f"error while generating yearly report {e}")
    finally:
        conn.close()

# ─── Search Functions ──────────────────────────────────────────────────────────

def search_by_date(key):
    # Searches income and expense records by date keyword
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("select * from income where date like ?", ('%' + key + '%',))
        results_income = cursor.fetchall()
        cursor.execute("select * from expense where date like ?", ('%' + key + '%',))
        results_expense = cursor.fetchall()
        if results_income:
            for r in results_income:
                print(f"Income ID: {r[0]} | Source: {r[1]} | Amount: {r[2]} | Description: {r[3]} | Date: {r[4]}")
        else:
            print("no income found with this date")
        if results_expense:
            for r in results_expense:
                print(f"Expense ID: {r[0]} | Category ID: {r[1]} | Amount: {r[2]} | Description: {r[3]} | Date: {r[4]}")
        else:
            print("no expense found with this date")
    except sqlite3.Error as e:
        print(f"error while searching data {e}")
    finally:
        conn.close()

def search_by_category(key):
    # Searches expense records by category name keyword
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""select e.expense_id, c.category_name, e.amount, e.description, e.date
                          from expense e join category c on e.category_id = c.category_id
                          where c.category_name like ?""", ('%' + key + '%',))
        results = cursor.fetchall()
        if results:
            for r in results:
                print(f"Expense ID: {r[0]} | Category Name: {r[1]} | Amount: {r[2]} | Description: {r[3]} | Date: {r[4]}")
        else:
            print("no expense found with this category")
    except sqlite3.Error as e:
        print(f"error while searching data {e}")
    finally:
        conn.close()

def search_by_amount(target_amount):
    # Searches income and expense records by exact amount
    conn = get_connection()
    cursor = conn.cursor()
    try:
        amt = float(target_amount)
        cursor.execute("select * from income where amount=?", (amt,))
        income_res = cursor.fetchall()
        cursor.execute("select * from expense where amount=?", (amt,))
        expense_res = cursor.fetchall()
        if income_res:
            for r in income_res:
                print(f"Income ID: {r[0]} | Source: {r[1]} | Amount: {r[2]} | Description: {r[3]} | Date: {r[4]}")
        else:
            print("no income found with this amount")
        if expense_res:
            for r in expense_res:
                print(f"Expense ID: {r[0]} | Category ID: {r[1]} | Amount: {r[2]} | Description: {r[3]} | Date: {r[4]}")
        else:
            print("no expense found with this amount")
    except sqlite3.Error as e:
        print(f"error while searching data {e}")
    finally:
        conn.close()

# ─── Analytics Functions ───────────────────────────────────────────────────────

def highest_expense_month():
    # Finds the month with the highest total expense
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """select strftime('%Y-%m', date) as month, sum(amount) as total_expense
                   from expense group by month order by total_expense desc limit 1"""
        cursor.execute(query)
        result = cursor.fetchone()
        if result and result[0] is not None:
            print(f"month with highest expense is {result[0]} with expense = {result[1]}")
            return result[0], result[1]
        else:
            print("no expense data found")
            return None, 0
    except sqlite3.Error as e:
        print(f"error while finding highest expense month {e}")
    finally:
        conn.close()

def lowest_expense_month():
    # Finds the month with the lowest total expense
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """select strftime('%Y-%m', date) as month, sum(amount) as total_expense
                   from expense group by month order by total_expense asc limit 1"""
        cursor.execute(query)
        result = cursor.fetchone()
        if result and result[0] is not None:
            print(f"month with lowest expense is {result[0]} with expense = {result[1]}")
            return result[0], result[1]
        else:
            print("no expense data found")
            return None, 0
    except sqlite3.Error as e:
        print(f"error while finding lowest expense month {e}")
    finally:
        conn.close()

def avg_monthly_spend():
    # Calculates and displays the average monthly spending
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """select avg(total_expense) from
                   (select sum(amount) as total_expense from expense
                   group by strftime('%Y-%m', date))"""
        cursor.execute(query)
        result = cursor.fetchone()
        avg = result[0] if result and result[0] is not None else 0
        print(f"average monthly spend = {avg:.2f}")
        return avg
    except sqlite3.Error as e:
        print(f"error while calculating average monthly spend {e}")
    finally:
        conn.close()

# ─── Main Menu ─────────────────────────────────────────────────────────────────

def main_menu():
    while True:
        print("\n1. Income")
        print("2. Expense")
        print("3. Category")
        print("4. Report")
        print("5. Search")
        print("6. Analytics")
        print("7. Exit")
        choice = input("Enter your choice= ")

        # ── Income Menu ──
        if choice == '1':
            while True:
                print("\n1. Add income")
                print("2. View income")
                print("3. Update income")
                print("4. Delete income")
                print("5. Exit")
                sub_choice = input("Enter your choice= ")
                if sub_choice == '1':
                    income_id = input("Enter the income id= ")
                    source = input("Enter the source= ")
                    amount = input("Enter the amount= ")
                    description = input("Enter the description= ")
                    add_income(income_id, source, amount, description)
                elif sub_choice == '2':
                    view_income()
                elif sub_choice == '3':
                    income_id = input("Enter income id to update= ")
                    update_income(income_id)
                elif sub_choice == '4':
                    income_id = input("Enter income id to delete= ")
                    delete_income(income_id)
                elif sub_choice == '5':
                    print("exiting income menu")
                    break
                else:
                    print("invalid choice")

        # ── Expense Menu ──
        elif choice == '2':
            while True:
                print("\n1. Add expense")
                print("2. View expense")
                print("3. Update expense")
                print("4. Delete expense")
                print("5. Balance alert")
                print("6. Exit")
                sub_choice = input("Enter your choice= ")
                if sub_choice == '1':
                    expense_id = input("Enter the expense id= ")
                    category_id = input("Enter the category id= ")
                    amount = input("Enter the amount= ")
                    description = input("Enter the description= ")
                    add_expense(expense_id, category_id, amount, description)
                elif sub_choice == '2':
                    view_expense()
                elif sub_choice == '3':
                    expense_id = input("Enter expense id to update= ")
                    update_expense(expense_id)
                elif sub_choice == '4':
                    expense_id = input("Enter expense id to delete= ")
                    delete_expense(expense_id)
                elif sub_choice == '5':
                    balance_alert()
                elif sub_choice == '6':
                    print("exiting expense menu")
                    break
                else:
                    print("invalid choice")

        # ── Category Menu ──
        elif choice == '3':
            while True:
                print("\n1. Add category")
                print("2. View category")
                print("3. Update category")
                print("4. Delete category")
                print("5. Exit")
                sub_choice = input("Enter your choice= ")
                if sub_choice == '1':
                    category_id = int(input("Enter the category id= "))
                    category_name = input("Enter the category name= ")
                    add_categories(category_id, category_name)
                elif sub_choice == '2':
                    view_categories()
                elif sub_choice == '3':
                    category_id = int(input("Enter category id to update= "))
                    new_category = input("Enter new category name= ")
                    update_categories(category_id, new_category)
                elif sub_choice == '4':
                    category_id = int(input("Enter category id to delete= "))
                    delete_categories(category_id)
                elif sub_choice == '5':
                    print("exiting category menu")
                    break
                else:
                    print("invalid choice")

        # ── Report Menu ──
        elif choice == '4':
            while True:
                print("\n1. Total income")
                print("2. Total expense")
                print("3. Remaining balance")
                print("4. Highest spent category")
                print("5. Monthly report")
                print("6. Yearly report")
                print("7. Exit")
                sub_choice = input("Enter your choice= ")
                if sub_choice == '1':
                    total_income()
                elif sub_choice == '2':
                    total_expense()
                elif sub_choice == '3':
                    remaining_balance()
                elif sub_choice == '4':
                    highest_expense_category()
                elif sub_choice == '5':
                    monthly_report()
                elif sub_choice == '6':
                    yearly_report()
                elif sub_choice == '7':
                    print("exiting report menu")
                    break
                else:
                    print("invalid choice")

        # ── Search Menu ──
        elif choice == '5':
            while True:
                print("\n1. Search by date")
                print("2. Search by category")
                print("3. Search by amount")
                print("4. Exit")
                sub_choice = input("Enter your choice= ")
                if sub_choice == '1':
                    key = input("Enter date to search= ")
                    search_by_date(key)
                elif sub_choice == '2':
                    key = input("Enter category to search= ")
                    search_by_category(key)
                elif sub_choice == '3':
                    search_by_amount(input("Enter amount to search= "))
                elif sub_choice == '4':
                    print("exiting search menu")
                    break
                else:
                    print("invalid choice")

        # ── Analytics Menu ──
        elif choice == '6':
            while True:
                print("\n1. Month with highest expense")
                print("2. Month with lowest expense")
                print("3. Average monthly spend")
                print("4. Exit")
                sub_choice = input("Enter your choice= ")
                if sub_choice == '1':
                    highest_expense_month()
                elif sub_choice == '2':
                    lowest_expense_month()
                elif sub_choice == '3':
                    avg_monthly_spend()
                elif sub_choice == '4':
                    print("exiting analytics menu")
                    break
                else:
                    print("invalid choice")

        elif choice == '7':
            print("exiting program")
            break
        else:
            print("invalid choice")

# ─── Entry Point ───────────────────────────────────────────────────────────────
create_table()
main_menu()
