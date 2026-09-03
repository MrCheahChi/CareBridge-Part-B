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
    patient_id = ""
    department = ""
    appointment_text = ""
    appointment_time = ""

    minimum_date = date.today() + timedelta(days=8)

    if request.method == "POST":
        patient_id = request.form.get(
            "patient_id", ""
        ).strip().upper()

        department = request.form.get(
            "department", ""
        ).strip()

        appointment_text = request.form.get(
            "appointment_date", ""
        ).strip()

        appointment_time = request.form.get(
            "appointment_time", ""
        ).strip()

        valid_patient_id = (
            len(patient_id) == 5
            and patient_id[0] in ("Y", "N")
            and patient_id[1] == "-"
            and patient_id[2:].isdigit()
        )

        available_times = {
            "09:00": "9:00 AM",
            "11:00": "11:00 AM",
            "14:00": "2:00 PM",
            "16:00": "4:00 PM",
        }

        if not valid_patient_id:
            error = "Patient ID must use the format Y-001 or N-001."

        elif department not in ("GP", "Specialist"):
            error = "Please select GP or Specialist."

        elif not appointment_text:
            error = "Please select an appointment date."

        elif appointment_time not in available_times:
            error = "Please select an available appointment time."

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
                    if department == "GP":
                        doctor = "Dr. Daniel Tan"
                        location = "General Outpatient Clinic - Room 5"
                    else:
                        doctor = "Dr. Aisha Rahman"
                        location = "Specialist Centre - Room 8"

                    booking_reference = (
                        f"CB-{appointment_date.strftime('%Y%m%d')}-"
                        f"{patient_id.replace('-', '')}"
                    )

                    booking = {
                        "patient_id": patient_id,
                        "department": department,
                        "date": appointment_date.strftime(
                            "%d/%m/%Y"
                        ),
                        "time": available_times[appointment_time],
                        "doctor": doctor,
                        "location": location,
                        "reference": booking_reference,
                    }

                    return render_template(
                        "appointment_details.html",
                        booking=booking,
                    )

    return render_template(
        "booking.html",
        error=error,
        patient_id=patient_id,
        department=department,
        appointment_text=appointment_text,
        appointment_time=appointment_time,
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


@app.route("/calculate-bill", methods=["GET", "POST"])
def calculate_bill():
    error = None
    bill = None
    patient_id = ""
    patient_type = ""
    tests_text = ""

    if request.method == "POST":
        patient_id = request.form.get("patient_id", "").strip().upper()
        patient_type = request.form.get("patient_type", "").strip()
        tests_text = request.form.get("lab_tests", "").strip()

        valid_patient_id = (
            len(patient_id) == 5
            and patient_id[0] in ("Y", "N")
            and patient_id[1] == "-"
            and patient_id[2:].isdigit()
        )

        if not valid_patient_id:
            error = "Patient ID must use the format Y-001 or N-001."

        elif patient_type not in ("Subsidised", "Private"):
            error = "Please select a valid patient type."

        elif not tests_text.isdigit():
            error = "Number of lab tests must be a whole number."

        elif int(tests_text) < 0 or int(tests_text) > 50:
            error = "Number of lab tests must be between 0 and 50."

        else:
            number_of_tests = int(tests_text)
            consultation_fee = 100.00
            lab_test_fee = number_of_tests * 10.00
            subtotal = consultation_fee + lab_test_fee

            if patient_type == "Subsidised":
                discount = subtotal * 0.30
            else:
                discount = 0.00

            total = subtotal - discount

            bill = {
                "patient_id": patient_id,
                "patient_type": patient_type,
                "number_of_tests": number_of_tests,
                "consultation_fee": consultation_fee,
                "lab_test_fee": lab_test_fee,
                "subtotal": subtotal,
                "discount": discount,
                "total": total,
            }

    return render_template(
        "bill.html",
        error=error,
        bill=bill,
        patient_id=patient_id,
        patient_type=patient_type,
        tests_text=tests_text,
    )


@app.route("/assign-triage-room", methods=["GET", "POST"])
def assign_triage_room():
    error = None
    triage = None
    patient_id = ""
    symptoms = ""
    severity_text = ""

    if request.method == "POST":
        patient_id = request.form.get("patient_id", "").strip().upper()
        symptoms = request.form.get("symptoms", "").strip()
        severity_text = request.form.get("severity", "").strip()

        valid_patient_id = (
            len(patient_id) == 5
            and patient_id[0] in ("Y", "N")
            and patient_id[1] == "-"
            and patient_id[2:].isdigit()
        )

        if not valid_patient_id:
            error = "Patient ID must use the format Y-001 or N-001."

        elif not symptoms:
            error = "Please enter the patient's main symptoms."

        elif len(symptoms) > 250:
            error = "Symptoms must not exceed 250 characters."

        elif not severity_text.isdigit():
            error = "Severity level must be a whole number from 1 to 10."

        elif int(severity_text) < 1 or int(severity_text) > 10:
            error = "Severity level must be between 1 and 10."

        else:
            severity = int(severity_text)

            if severity <= 4:
                room = "Waiting Room"
                category = "Low Priority"
                category_class = "low-priority"
                instruction = "Please wait until your patient ID is called."
            elif severity <= 7:
                room = "Room 1"
                category = "Medium Priority"
                category_class = "medium-priority"
                instruction = "Please proceed to Room 1 for assessment."
            else:
                room = "Room 2"
                category = "High Priority"
                category_class = "high-priority"
                instruction = "Please proceed immediately to Room 2."

            triage = {
                "patient_id": patient_id,
                "symptoms": symptoms,
                "severity": severity,
                "room": room,
                "category": category,
                "category_class": category_class,
                "instruction": instruction,
            }

    return render_template(
        "triage.html",
        error=error,
        triage=triage,
        patient_id=patient_id,
        symptoms=symptoms,
        severity_text=severity_text,
    )

if __name__ == "__main__":
    app.run(debug=True)
