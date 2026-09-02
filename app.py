from datetime import date, timedelta

from flask import Flask, render_template, request


app = Flask(__name__)


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


if __name__ == "__main__":
    app.run(debug=True)