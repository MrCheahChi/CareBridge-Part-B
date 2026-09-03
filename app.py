from datetime import date, timedelta

from flask import Flask, render_template, request


app = Flask(__name__)

patient_numbers = {
    "Y": 0,
    "N": 0
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/book-appointment", methods=["GET", "POST"])
def book_appointment():
    error = None
    booking = None
    department = ""
    appointment_text = ""

    minimum_date = date.today() + timedelta(days=8)

    if request.method == "POST":
        department = request.form.get(
            "department", ""
        ).strip()

        appointment_text = request.form.get(
            "appointment_date", ""
        ).strip()

        if department not in ("GP", "Specialist"):
            error = "Please select GP or Specialist."

        elif not appointment_text:
            error = "Please select an appointment date."

        else:
            try:
                appointment_date = date.fromisoformat(
                    appointment_text
                )
            except ValueError:
                error = "Please enter a valid appointment date."
            else:
                earliest_allowed = (
                    date.today() + timedelta(days=7)
                )

                if appointment_date <= earliest_allowed:
                    error = (
                        "The appointment must be more than "
                        "seven days from today."
                    )
                else:
                    booking = {
                        "department": department,
                        "date": appointment_date.strftime(
                            "%d/%m/%Y"
                        ),
                    }

                    department = ""
                    appointment_text = ""

    return render_template(
        "booking.html",
        error=error,
        booking=booking,
        department=department,
        appointment_text=appointment_text,
        minimum_date=minimum_date.isoformat(),
    )

@app.route("/register-patient", methods=["GET", "POST"])
def register_patient():
    error = None
    name = ""
    age_text = ""
    priority = ""

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age_text = request.form.get("age", "").strip()
        priority = request.form.get("priority", "").strip()

        if not name:
            error = "Patient name cannot be blank."

        elif not all(
            character.isalpha() or character in " -'."
            for character in name
        ):
            error = (
                "Patient name can only contain letters, spaces, "
                "hyphens, apostrophes, and periods."
            )

        elif not any(character.isalpha() for character in name):
            error = "Patient name must contain at least one letter."

        elif not age_text.isdigit():
            error = "Age must be a whole number."

        elif int(age_text) < 1 or int(age_text) > 120:
            error = "Age must be between 1 and 120."

        elif priority not in ("Y", "N"):
            error = "Please select whether the patient is urgent."

        else:
            patient_numbers[priority] += 1
            patient_id = f"{priority}-{patient_numbers[priority]:03d}"

            if priority == "Y":
                priority_text = "Urgent"
                department = "Emergency Department"
                location = "Emergency Wing - Room 2"
                doctor = "Dr. Sarah Lim"
            else:
                priority_text = "Non-Urgent"
                department = "General Outpatient Clinic"
                location = "Outpatient Wing - Room 5"
                doctor = "Dr. Daniel Tan"

            patient = {
                "name": name,
                "age": int(age_text),
                "priority": priority_text,
                "id": patient_id,
                "department": department,
                "location": location,
                "doctor": doctor,
            }

            return render_template(
                "patient_details.html",
                patient=patient,
            )

    return render_template(
        "register.html",
        error=error,
        name=name,
        age_text=age_text,
        priority=priority,
    )

if __name__ == "__main__":
    app.run(debug=True)
