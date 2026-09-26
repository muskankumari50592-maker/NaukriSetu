import sqlite3

DATABASE = "naukrisetu.db"


def create_database():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # JOBS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            organization TEXT NOT NULL,
            qualification TEXT,
            vacancies INTEGER,
            last_date TEXT,
            job_type TEXT,
            location TEXT,
            description TEXT,
            apply_link TEXT,
            status TEXT DEFAULT 'Active'
        )
    """)

    # RESULTS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            organization TEXT NOT NULL,
            result_date TEXT,
            category TEXT,
            result_link TEXT,
            status TEXT DEFAULT 'Declared'
        )
    """)

    # ADMIT CARDS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admit_cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            organization TEXT NOT NULL,
            release_date TEXT,
            exam_date TEXT,
            category TEXT,
            admit_card_link TEXT,
            status TEXT DEFAULT 'Released'
        )
    """)

    # ANSWER KEYS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS answer_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            organization TEXT NOT NULL,
            release_date TEXT,
            category TEXT,
            answer_key_link TEXT,
            status TEXT DEFAULT 'Released'
        )
    """)

    # SYLLABUS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS syllabus (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            organization TEXT NOT NULL,
            category TEXT,
            qualification TEXT,
            syllabus_date TEXT,
            syllabus_link TEXT,
            status TEXT DEFAULT 'Available'
        )
    """)

    # ADMISSIONS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            organization TEXT NOT NULL,
            category TEXT,
            qualification TEXT,
            last_date TEXT,
            admission_link TEXT,
            status TEXT DEFAULT 'Open'
        )
    """)

    # SCHOLARSHIPS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scholarships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            organization TEXT NOT NULL,
            category TEXT,
            eligibility TEXT,
            last_date TEXT,
            scholarship_link TEXT,
            status TEXT DEFAULT 'Open'
        )
    """)

    # GOVERNMENT SCHEMES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schemes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            department TEXT NOT NULL,
            category TEXT,
            eligibility TEXT,
            benefits TEXT,
            last_date TEXT,
            scheme_link TEXT,
            status TEXT DEFAULT 'Active'
        )
    """)

    # EXAM CALENDAR
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exam_calendar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exam_name TEXT NOT NULL,
            organization TEXT NOT NULL,
            category TEXT,
            application_start TEXT,
            application_last_date TEXT,
            exam_date TEXT,
            exam_link TEXT,
            status TEXT DEFAULT 'Upcoming'
        )
    """)

    # CAREER GUIDANCE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS careers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            career_name TEXT NOT NULL,
            category TEXT,
            qualification TEXT,
            skills TEXT,
            description TEXT,
            resources TEXT,
            status TEXT DEFAULT 'Available'
        )
    """)

    # DEMO CAREER DATA
    cursor.execute("SELECT COUNT(*) FROM careers")

    if cursor.fetchone()[0] == 0:

        sample_careers = [

            (
                "Software Developer",
                "Technology",
                "B.Tech / BCA / B.Sc Computer Science",
                "Programming, Data Structures, Git, Problem Solving",
                "Design, develop and maintain software applications.",
                "Learn programming, build projects and practice coding.",
                "Available"
            ),

            (
                "Data Analyst",
                "Data & Analytics",
                "Graduate / B.Tech / B.Sc",
                "Python, SQL, Excel, Statistics, Data Visualization",
                "Analyze data and create useful insights for organizations.",
                "Learn SQL, Python and data visualization tools.",
                "Available"
            ),

            (
                "Government Services",
                "Government Jobs",
                "Graduation / Post Graduation depending on examination",
                "General Awareness, Reasoning, Quantitative Aptitude, Communication",
                "Career opportunities available through various government examinations.",
                "Follow official notifications and prepare according to the examination syllabus.",
                "Available"
            ),

            (
                "Web Developer",
                "Technology",
                "B.Tech / BCA / B.Sc Computer Science",
                "HTML, CSS, JavaScript, Python, Git",
                "Build and maintain websites and web applications.",
                "Create frontend projects and learn backend technologies.",
                "Available"
            ),

            (
                "Cyber Security Professional",
                "Cyber Security",
                "B.Tech / BCA / B.Sc / Relevant Certification",
                "Networking, Linux, Security Fundamentals, Problem Solving",
                "Work on protecting computer systems, networks and applications.",
                "Study networking and security fundamentals through practical projects.",
                "Available"
            ),

            (
                "UI/UX Designer",
                "Design",
                "Any Graduate / Design-related qualification",
                "Figma, UI Design, UX Research, Prototyping",
                "Design user-friendly interfaces and digital experiences.",
                "Build a design portfolio and practice interface design.",
                "Available"
            )

        ]

        cursor.executemany("""
            INSERT INTO careers
            (
                career_name,
                category,
                qualification,
                skills,
                description,
                resources,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, sample_careers)

    connection.commit()
    connection.close()

    print("NaukriSetu database created successfully.")


if __name__ == "__main__":
    create_database()