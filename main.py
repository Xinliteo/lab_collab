import tkinter as tk
from tkinter import messagebox
import clips

# Create CLIPS environment
env = clips.Environment()

# Add rules (minimum 2 rules)
env.build("""
(defrule covid-high-risk
    (symptom fever)
    (symptom cough)
    =>
    (assert (diagnosis "High possibility of Covid-19")))
""")

env.build("""
(defrule covid-low-risk
    (symptom none)
    =>
    (assert (diagnosis "Low risk of Covid-19")))
""")

def run_diagnosis(symptoms):
    env.reset()

    # Insert symptoms into CLIPS
    for s in symptoms:
        env.assert_string(f"(symptom {s})")

    env.run()

    # Extract diagnosis
    for fact in env.facts():
        if fact.template.name == "diagnosis":
            return fact.slots["slot1"]

    return "No diagnosis found."

# Tkinter UI
def submit():
    symptoms = []

    if fever_var.get() == 1:
        symptoms.append("fever")

    if cough_var.get() == 1:
        symptoms.append("cough")

    if not symptoms:
        symptoms.append("none")

    result = run_diagnosis(symptoms)
    messagebox.showinfo("Diagnosis Result", result)

# Window
root = tk.Tk()
root.title("Covid-19 Expert System")
root.geometry("350x250")

title = tk.Label(root, text="Covid-19 Diagnosis System", font=("Arial", 14))
title.pack(pady=10)

fever_var = tk.IntVar()
cough_var = tk.IntVar()

tk.Checkbutton(root, text="Fever", variable=fever_var).pack()
tk.Checkbutton(root, text="Cough", variable=cough_var).pack()

tk.Button(root, text="Check Diagnosis", command=submit).pack(pady=20)

root.mainloop()