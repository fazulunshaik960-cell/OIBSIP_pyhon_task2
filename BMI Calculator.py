import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt


# ---------------- DATABASE ----------------

try:
    conn = sqlite3.connect("bmi_records.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bmi_history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        weight REAL,
        height REAL,
        bmi REAL,
        category TEXT,
        date TEXT
    )
    """)

    conn.commit()

except Exception as e:
    print("Database Error:", e)



# ---------------- BMI CALCULATION ----------------

def calculate_bmi():

    try:

        name = name_entry.get()

        weight = float(weight_entry.get())

        height = float(height_entry.get())


        if name == "":
            messagebox.showerror(
                "Error",
                "Enter user name"
            )
            return


        if weight <= 0 or height <= 0:

            messagebox.showerror(
                "Error",
                "Weight and height must be positive"
            )

            return



        bmi = weight / (height ** 2)

        bmi = round(bmi,2)



        if bmi < 18.5:

            category = "Underweight"
            color = "blue"


        elif bmi < 24.9:

            category = "Normal"
            color = "green"


        elif bmi < 29.9:

            category = "Overweight"
            color = "orange"


        else:

            category = "Obese"
            color = "red"



        result_label.config(
            text=f"BMI: {bmi}\nCategory: {category}",
            fg=color
        )


        # Save Record

        cursor.execute(
        """
        INSERT INTO bmi_history
        (name,weight,height,bmi,category,date)
        VALUES(?,?,?,?,?,?)
        """,
        (
            name,
            weight,
            height,
            bmi,
            category,
            datetime.now().strftime("%Y-%m-%d")
        ))

        conn.commit()


    except ValueError:

        messagebox.showerror(
            "Invalid Input",
            "Enter numbers only"
        )


    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )



# ---------------- GRAPH ----------------

def show_graph():

    name = name_entry.get()


    try:

        cursor.execute(
            "SELECT date,bmi FROM bmi_history WHERE name=?",
            (name,)
        )

        records = cursor.fetchall()


        if not records:

            messagebox.showinfo(
                "No Data",
                "No BMI history found"
            )

            return



        dates = []

        values = []


        for row in records:

            dates.append(row[0])

            values.append(row[1])



        plt.figure(figsize=(7,4))

        plt.plot(
            dates,
            values,
            marker="o"
        )

        plt.xlabel("Date")

        plt.ylabel("BMI")

        plt.title(
            name + " BMI Trend"
        )

        plt.xticks(rotation=45)

        plt.tight_layout()

        plt.show()



    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )



# ---------------- GUI ----------------


window = tk.Tk()

window.title("BMI Calculator")

window.geometry("400x450")



tk.Label(
    window,
    text="BMI Calculator",
    font=("Arial",20)
).pack(pady=10)



tk.Label(window,text="User Name").pack()

name_entry=tk.Entry(window)

name_entry.pack()



tk.Label(window,text="Weight (kg)").pack()

weight_entry=tk.Entry(window)

weight_entry.pack()



tk.Label(window,text="Height (m)").pack()

height_entry=tk.Entry(window)

height_entry.pack()



tk.Button(
    window,
    text="Calculate BMI",
    command=calculate_bmi
).pack(pady=15)



result_label=tk.Label(
    window,
    text="BMI Result",
    font=("Arial",14)
)

result_label.pack()



tk.Button(
    window,
    text="Show BMI History Graph",
    command=show_graph
).pack(pady=15)



window.mainloop()