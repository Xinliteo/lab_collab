import tkinter as tk
from tkinter import messagebox
import clips

env = clips.Environment()

# Template for diagnosis
env.build("""
(deftemplate diagnosis
    (slot result)
)
""")

# Rule 1: High risk (fever AND cough)
env.build("""
(defrule covid-high-risk
    (symptom fever)
    (symptom cough)
    =>
    (assert (diagnosis (result "High risk: Fever + Cough detected. High possibility of Covid-19.")))
)
""")

# Rule 2: Medium risk (fever only)
env.build("""
(defrule covid-medium-risk
    (symptom fever)
    (not (symptom cough))
    =>
    (assert (diagnosis (result "Medium risk: Fever detected. Possible infection.")))
)
""")

# Rule 3: Mild risk (cough only)
env.build("""
(defrule covid-mild-risk
    (symptom cough)
    (not (symptom fever))
    =>
    (assert (diagnosis (result "Mild risk: Cough detected. Mild respiratory symptoms.")))
)
""")

# Rule 4: Low risk (no symptoms)
env.build("""
(defrule covid-low-risk
    (symptom none)
    =>
    (assert (diagnosis (result "Low risk: No symptoms detected.")))
)
""")

def run_diagnosis(symptoms):
    env.reset()

    for s in symptoms:
        env.assert_string(f"(symptom {s})")

    env.run()

    # Read diagnosis fact
    for fact in env.facts():
        if fact.template.name == "diagnosis":
            return fact["result"]

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

root = tk.Tk()
root.title("Covid-19 Expert System")
root.geometry("350x250")

tk.Label(root, text="Covid-19 Diagnosis System", font=("Arial", 14)).pack(pady=10)

fever_var = tk.IntVar()
cough_var = tk.IntVar()

tk.Checkbutton(root, text="Fever", variable=fever_var).pack()
tk.Checkbutton(root, text="Cough", variable=cough_var).pack()

tk.Button(root, text="Check Diagnosis", command=submit).pack(pady=20)

root.mainloop()