from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "naukrisetu.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# =========================
# HOME
# =========================

@app.route("/")
def home():

    connection = get_db_connection()

    jobs = connection.execute(
        "SELECT * FROM jobs ORDER BY id DESC LIMIT 6"
    ).fetchall()

    connection.close()

    return render_template(
        "index.html",
        jobs=jobs
    )


# =========================
# JOBS
# =========================

@app.route("/jobs")
def jobs():

    connection = get_db_connection()

    search = request.args.get("search", "").strip()
    job_type = request.args.get("job_type", "").strip()
    location = request.args.get("location", "").strip()
    qualification = request.args.get("qualification", "").strip()

    query = "SELECT * FROM jobs WHERE 1=1"
    params = []

    if search:

        query += """
            AND (
                title LIKE ?
                OR organization LIKE ?
                OR qualification LIKE ?
                OR location LIKE ?
            )
        """

        value = "%" + search + "%"

        params.extend([
            value,
            value,
            value,
            value
        ])

    if job_type:

        query += " AND job_type LIKE ?"
        params.append("%" + job_type + "%")

    if location:

        query += " AND location LIKE ?"
        params.append("%" + location + "%")

    if qualification:

        query += " AND qualification LIKE ?"
        params.append("%" + qualification + "%")

    query += " ORDER BY id DESC"

    jobs_data = connection.execute(
        query,
        params
    ).fetchall()

    connection.close()

    return render_template(
        "jobs.html",
        jobs=jobs_data,
        search=search,
        job_type=job_type,
        location=location,
        qualification=qualification
    )


# =========================
# JOB DETAILS
# =========================

@app.route("/job/<int:job_id>")
def job_details(job_id):

    connection = get_db_connection()

    job = connection.execute(
        "SELECT * FROM jobs WHERE id = ?",
        (job_id,)
    ).fetchone()

    connection.close()

    if job is None:
        return "Job not found", 404

    return render_template(
        "job_details.html",
        job=job
    )


# =========================
# ADD JOB
# =========================

@app.route("/add-job", methods=["GET", "POST"])
def add_job():

    if request.method == "POST":

        title = request.form.get("title")
        organization = request.form.get("organization")
        qualification = request.form.get("qualification")
        vacancies = request.form.get("vacancies")
        last_date = request.form.get("last_date")
        job_type = request.form.get("job_type")
        location = request.form.get("location")
        description = request.form.get("description")
        apply_link = request.form.get("apply_link")

        connection = get_db_connection()

        connection.execute(
            """
            INSERT INTO jobs
            (
                title,
                organization,
                qualification,
                vacancies,
                last_date,
                job_type,
                location,
                description,
                apply_link
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                title,
                organization,
                qualification,
                vacancies,
                last_date,
                job_type,
                location,
                description,
                apply_link
            )
        )

        connection.commit()
        connection.close()

        return redirect(url_for("jobs"))

    return render_template("add_job.html")


# =========================
# RESULTS
# =========================

@app.route("/results")
def results():

    connection = get_db_connection()

    results_data = connection.execute(
        "SELECT * FROM results ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template(
        "results.html",
        results=results_data
    )


# =========================
# ADMIT CARD
# =========================

@app.route("/admit-card")
def admit_card():

    connection = get_db_connection()

    data = connection.execute(
        "SELECT * FROM admit_cards ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template(
        "admit_card.html",
        admit_cards=data
    )


# =========================
# ANSWER KEY
# =========================

@app.route("/answer-key")
def answer_key():

    connection = get_db_connection()

    data = connection.execute(
        "SELECT * FROM answer_keys ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template(
        "answer_key.html",
        answer_keys=data
    )


# =========================
# SYLLABUS
# =========================

@app.route("/syllabus")
def syllabus():

    connection = get_db_connection()

    data = connection.execute(
        "SELECT * FROM syllabus ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template(
        "syllabus.html",
        syllabus=data
    )


# =========================
# ADMISSION
# =========================

@app.route("/admission")
def admission():

    connection = get_db_connection()

    data = connection.execute(
        "SELECT * FROM admissions ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template(
        "admission.html",
        admissions=data
    )


# =========================
# SCHOLARSHIP
# =========================

@app.route("/scholarship")
def scholarship():

    connection = get_db_connection()

    data = connection.execute(
        "SELECT * FROM scholarships ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template(
        "scholarship.html",
        scholarships=data
    )


# =========================
# GOVERNMENT SCHEMES
# =========================

@app.route("/schemes")
def schemes():

    connection = get_db_connection()

    data = connection.execute(
        "SELECT * FROM schemes ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template(
        "schemes.html",
        schemes=data
    )


# =========================
# EXAM CALENDAR
# =========================

@app.route("/exam-calendar")
def exam_calendar():

    connection = get_db_connection()

    data = connection.execute(
        "SELECT * FROM exam_calendar ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template(
        "exam_calendar.html",
        exams=data
    )


# =========================
# CAREER
# =========================

@app.route("/career")
def career():

    connection = get_db_connection()

    data = connection.execute(
        "SELECT * FROM careers ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template(
        "career.html",
        careers=data
    )


# =========================
# GLOBAL SEARCH
# =========================

@app.route("/search")
def search():

    connection = get_db_connection()

    query = request.args.get("q", "").strip()

    results = []

    if query:

        value = "%" + query + "%"

        # =========================
        # JOBS
        # =========================

        jobs_data = connection.execute(
            """
            SELECT id, title, organization
            FROM jobs
            WHERE title LIKE ?
            OR organization LIKE ?
            OR qualification LIKE ?
            OR location LIKE ?
            ORDER BY id DESC
            """,
            (
                value,
                value,
                value,
                value
            )
        ).fetchall()

        for item in jobs_data:

            results.append({
                "type": "Job",
                "title": item["title"],
                "organization": item["organization"],
                "link": "/job/" + str(item["id"])
            })


        # =========================
        # RESULTS
        # =========================

        result_data = connection.execute(
            """
            SELECT title, organization, category
            FROM results
            WHERE title LIKE ?
            OR organization LIKE ?
            OR category LIKE ?
            ORDER BY id DESC
            """,
            (
                value,
                value,
                value
            )
        ).fetchall()

        for item in result_data:

            results.append({
                "type": "Result",
                "title": item["title"],
                "organization": item["organization"],
                "category": item["category"],
                "link": url_for("results")
            })


        # =========================
        # ADMIT CARDS
        # =========================

        admit_data = connection.execute(
            """
            SELECT title, organization, category
            FROM admit_cards
            WHERE title LIKE ?
            OR organization LIKE ?
            OR category LIKE ?
            ORDER BY id DESC
            """,
            (
                value,
                value,
                value
            )
        ).fetchall()

        for item in admit_data:

            results.append({
                "type": "Admit Card",
                "title": item["title"],
                "organization": item["organization"],
                "category": item["category"],
                "link": url_for("admit_card")
            })


        # =========================
        # ANSWER KEYS
        # =========================

        answer_data = connection.execute(
            """
            SELECT title, organization, category
            FROM answer_keys
            WHERE title LIKE ?
            OR organization LIKE ?
            OR category LIKE ?
            ORDER BY id DESC
            """,
            (
                value,
                value,
                value
            )
        ).fetchall()

        for item in answer_data:

            results.append({
                "type": "Answer Key",
                "title": item["title"],
                "organization": item["organization"],
                "category": item["category"],
                "link": url_for("answer_key")
            })


        # =========================
        # SYLLABUS
        # =========================

        syllabus_data = connection.execute(
            """
            SELECT title, organization, category
            FROM syllabus
            WHERE title LIKE ?
            OR organization LIKE ?
            OR category LIKE ?
            OR qualification LIKE ?
            ORDER BY id DESC
            """,
            (
                value,
                value,
                value,
                value
            )
        ).fetchall()

        for item in syllabus_data:

            results.append({
                "type": "Syllabus",
                "title": item["title"],
                "organization": item["organization"],
                "category": item["category"],
                "link": url_for("syllabus")
            })


        # =========================
        # ADMISSIONS
        # =========================

        admission_data = connection.execute(
            """
            SELECT title, organization, category
            FROM admissions
            WHERE title LIKE ?
            OR organization LIKE ?
            OR category LIKE ?
            OR qualification LIKE ?
            ORDER BY id DESC
            """,
            (
                value,
                value,
                value,
                value
            )
        ).fetchall()

        for item in admission_data:

            results.append({
                "type": "Admission",
                "title": item["title"],
                "organization": item["organization"],
                "category": item["category"],
                "link": url_for("admission")
            })


        # =========================
        # SCHOLARSHIPS
        # =========================

        scholarship_data = connection.execute(
            """
            SELECT title, organization, category
            FROM scholarships
            WHERE title LIKE ?
            OR organization LIKE ?
            OR category LIKE ?
            OR eligibility LIKE ?
            ORDER BY id DESC
            """,
            (
                value,
                value,
                value,
                value
            )
        ).fetchall()

        for item in scholarship_data:

            results.append({
                "type": "Scholarship",
                "title": item["title"],
                "organization": item["organization"],
                "category": item["category"],
                "link": url_for("scholarship")
            })


        # =========================
        # GOVERNMENT SCHEMES
        # =========================

        scheme_data = connection.execute(
            """
            SELECT title, department, category
            FROM schemes
            WHERE title LIKE ?
            OR department LIKE ?
            OR category LIKE ?
            OR eligibility LIKE ?
            OR benefits LIKE ?
            ORDER BY id DESC
            """,
            (
                value,
                value,
                value,
                value,
                value
            )
        ).fetchall()

        for item in scheme_data:

            results.append({
                "type": "Government Scheme",
                "title": item["title"],
                "organization": item["department"],
                "category": item["category"],
                "link": url_for("schemes")
            })


        # =========================
        # EXAM CALENDAR
        # =========================

        exam_data = connection.execute(
            """
            SELECT exam_name, organization, category
            FROM exam_calendar
            WHERE exam_name LIKE ?
            OR organization LIKE ?
            OR category LIKE ?
            ORDER BY id DESC
            """,
            (
                value,
                value,
                value
            )
        ).fetchall()

        for item in exam_data:

            results.append({
                "type": "Exam Calendar",
                "title": item["exam_name"],
                "organization": item["organization"],
                "category": item["category"],
                "link": url_for("exam_calendar")
            })


    connection.close()

    return render_template(
        "search.html",
        query=query,
        results=results
    )


# =========================
# ORGANIZATION SEARCH
# =========================

@app.route("/organization")
def organization():

    connection = get_db_connection()

    organization_name = request.args.get(
        "name",
        ""
    ).strip()

    jobs_data = []
    results_data = []

    if organization_name:

        value = "%" + organization_name + "%"

        jobs_data = connection.execute(
            """
            SELECT * FROM jobs
            WHERE organization LIKE ?
            ORDER BY id DESC
            """,
            (value,)
        ).fetchall()

        results_data = connection.execute(
            """
            SELECT * FROM results
            WHERE organization LIKE ?
            ORDER BY id DESC
            """,
            (value,)
        ).fetchall()

    connection.close()

    return render_template(
        "organization.html",
        organization_name=organization_name,
        jobs=jobs_data,
        results=results_data
    )


# =========================
# STATE-WISE SEARCH
# =========================

@app.route("/state")
def state_search():

    connection = get_db_connection()

    state_name = request.args.get(
        "state",
        ""
    ).strip()

    jobs_data = []

    if state_name:

        value = "%" + state_name + "%"

        jobs_data = connection.execute(
            """
            SELECT * FROM jobs
            WHERE location LIKE ?
            ORDER BY id DESC
            """,
            (value,)
        ).fetchall()

    connection.close()

    return render_template(
        "state.html",
        state_name=state_name,
        jobs=jobs_data
    )


# =========================
# FAVICON
# =========================

@app.route("/favicon.ico")
def favicon():

    return redirect(
        url_for(
            "static",
            filename="naukri-setu-logo.jpeg"
        )
    )


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":
    app.run(debug=True)