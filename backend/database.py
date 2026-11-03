import sqlite3


DATABASE = "studentstay.db"


def get_db():

    db = sqlite3.connect(DATABASE)

    db.row_factory = sqlite3.Row

    db.execute("PRAGMA foreign_keys = ON")

    return db


def init_db():

    db = get_db()

    try:

        # ==========================================================
        # USERS
        # ==========================================================

        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """)


        # ==========================================================
        # ACCOMMODATIONS
        # ==========================================================

        db.execute("""
            CREATE TABLE IF NOT EXISTS accommodations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                provider_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                address TEXT NOT NULL,
                city TEXT,
                latitude REAL,
                longitude REAL,
                monthly_rent REAL NOT NULL,
                deposit REAL DEFAULT 0,
                room_type TEXT NOT NULL,
                furnished INTEGER DEFAULT 0,
                available_from TEXT NOT NULL,
                available_until TEXT,
                commute_minutes INTEGER,
                status TEXT DEFAULT 'AVAILABLE',

                FOREIGN KEY(provider_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE
            )
        """)


        # ==========================================================
        # STUDENT PROFILES
        # ==========================================================

        db.execute("""
            CREATE TABLE IF NOT EXISTS student_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                university TEXT,
                arrival_date TEXT,
                required_until TEXT,
                max_rent REAL,
                max_upfront_budget REAL,
                room_type TEXT,
                furnished INTEGER DEFAULT 0,
                max_commute_minutes INTEGER,

                FOREIGN KEY(user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE
            )
        """)


        # ==========================================================
        # SAVED ACCOMMODATIONS
        # ==========================================================

        db.execute("""
            CREATE TABLE IF NOT EXISTS saved_accommodations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                accommodation_id INTEGER NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,

                UNIQUE(user_id, accommodation_id),

                FOREIGN KEY(user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE,

                FOREIGN KEY(accommodation_id)
                    REFERENCES accommodations(id)
                    ON DELETE CASCADE
            )
        """)


        # ==========================================================
        # APPLICATIONS
        # ==========================================================

        db.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                accommodation_id INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'PENDING',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,

                UNIQUE(student_id, accommodation_id),

                FOREIGN KEY(student_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE,

                FOREIGN KEY(accommodation_id)
                    REFERENCES accommodations(id)
                    ON DELETE CASCADE
            )
        """)


        # ==========================================================
        # ARRIVAL TASKS
        # ==========================================================

        db.execute("""
            CREATE TABLE IF NOT EXISTS arrival_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                task_name TEXT NOT NULL,
                description TEXT,
                completed INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,

                UNIQUE(user_id, task_name),

                FOREIGN KEY(user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE
            )
        """)


        # ==========================================================
        # EXISTING ACCOMMODATION DATABASE MIGRATION
        # ==========================================================

        columns = db.execute(
            "PRAGMA table_info(accommodations)"
        ).fetchall()

        column_names = [
            column["name"]
            for column in columns
        ]

        if "commute_minutes" not in column_names:

            db.execute("""
                ALTER TABLE accommodations
                ADD COLUMN commute_minutes INTEGER
            """)


        # ==========================================================
        # UNIVERSITIES
        # ==========================================================

        db.execute("""
            CREATE TABLE IF NOT EXISTS universities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                city TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL
            )
        """)


        # ----------------------------------------------------------
        # Remove duplicate universities created by earlier versions.
        # Keep the oldest record for each name/city combination.
        # ----------------------------------------------------------

        db.execute("""
            DELETE FROM universities
            WHERE id NOT IN (
                SELECT MIN(id)
                FROM universities
                GROUP BY name, city
            )
        """)


        # ----------------------------------------------------------
        # Prevent duplicates in the future.
        # ----------------------------------------------------------

        db.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS
            idx_university_name_city
            ON universities(name, city)
        """)


        # ==========================================================
        # REALISTIC UNIVERSITY DATA
        # ==========================================================
        #
        # Curated StudentStay MVP dataset:
        # approximately 40 institutions across major German
        # student and housing markets.
        #
        # Coordinates are used as university-location anchors.
        #
        # ==========================================================

        universities = [

            # ------------------------------------------------------
            # Aachen
            # ------------------------------------------------------

            (
                "RWTH Aachen University",
                "Aachen",
                50.7770,
                6.0770
            ),

            (
                "FH Aachen",
                "Aachen",
                50.7753,
                6.0839
            ),


            # ------------------------------------------------------
            # Berlin
            # ------------------------------------------------------

            (
                "Freie Universität Berlin",
                "Berlin",
                52.4530,
                13.2900
            ),

            (
                "Humboldt-Universität zu Berlin",
                "Berlin",
                52.5170,
                13.3930
            ),

            (
                "Technische Universität Berlin",
                "Berlin",
                52.5125,
                13.3269
            ),

            (
                "Hochschule für Technik und Wirtschaft Berlin",
                "Berlin",
                52.4560,
                13.5250
            ),


            # ------------------------------------------------------
            # Bonn
            # ------------------------------------------------------

            (
                "University of Bonn",
                "Bonn",
                50.7339,
                7.1020
            ),


            # ------------------------------------------------------
            # Bremen
            # ------------------------------------------------------

            (
                "University of Bremen",
                "Bremen",
                53.1067,
                8.8520
            ),

            (
                "Bremen University of Applied Sciences",
                "Bremen",
                53.0720,
                8.8070
            ),


            # ------------------------------------------------------
            # Cologne
            # ------------------------------------------------------

            (
                "University of Cologne",
                "Cologne",
                50.9280,
                6.9280
            ),

            (
                "TH Köln",
                "Cologne",
                50.9390,
                6.9560
            ),


            # ------------------------------------------------------
            # Darmstadt
            # ------------------------------------------------------

            (
                "TU Darmstadt",
                "Darmstadt",
                49.8730,
                8.6550
            ),

            (
                "Hochschule Darmstadt",
                "Darmstadt",
                49.8720,
                8.6500
            ),


            # ------------------------------------------------------
            # Dresden
            # ------------------------------------------------------

            (
                "TU Dresden",
                "Dresden",
                51.0280,
                13.7280
            ),

            (
                "HTW Dresden",
                "Dresden",
                51.0400,
                13.7310
            ),


            # ------------------------------------------------------
            # Düsseldorf
            # ------------------------------------------------------

            (
                "Heinrich Heine University Düsseldorf",
                "Düsseldorf",
                51.1890,
                6.7950
            ),

            (
                "Hochschule Düsseldorf",
                "Düsseldorf",
                51.2410,
                6.7350
            ),


            # ------------------------------------------------------
            # Frankfurt
            # ------------------------------------------------------

            (
                "Goethe University Frankfurt",
                "Frankfurt",
                50.1270,
                8.6670
            ),

            (
                "Frankfurt University of Applied Sciences",
                "Frankfurt",
                50.1320,
                8.6960
            ),


            # ------------------------------------------------------
            # Freiburg
            # ------------------------------------------------------

            (
                "University of Freiburg",
                "Freiburg",
                48.0000,
                7.8420
            ),


            # ------------------------------------------------------
            # Hamburg
            # ------------------------------------------------------

            (
                "Universität Hamburg",
                "Hamburg",
                53.5669,
                9.9840
            ),

            (
                "HAW Hamburg",
                "Hamburg",
                53.5570,
                10.0220
            ),

            (
                "TU Hamburg",
                "Hamburg",
                53.4610,
                9.9690
            ),


            # ------------------------------------------------------
            # Hannover
            # ------------------------------------------------------

            (
                "Leibniz University Hannover",
                "Hannover",
                52.3820,
                9.7170
            ),

            (
                "Hochschule Hannover",
                "Hannover",
                52.3720,
                9.7390
            ),


            # ------------------------------------------------------
            # Heidelberg
            # ------------------------------------------------------

            (
                "Heidelberg University",
                "Heidelberg",
                49.4108,
                8.7060
            ),


            # ------------------------------------------------------
            # Karlsruhe
            # ------------------------------------------------------

            (
                "Karlsruhe Institute of Technology",
                "Karlsruhe",
                49.0090,
                8.4130
            ),

            (
                "Hochschule Karlsruhe",
                "Karlsruhe",
                49.0150,
                8.3940
            ),


            # ------------------------------------------------------
            # Kiel
            # ------------------------------------------------------

            (
                "Kiel University",
                "Kiel",
                54.3420,
                10.1220
            ),


            # ------------------------------------------------------
            # Leipzig
            # ------------------------------------------------------

            (
                "Leipzig University",
                "Leipzig",
                51.3390,
                12.3730
            ),

            (
                "HTWK Leipzig",
                "Leipzig",
                51.3180,
                12.3300
            ),


            # ------------------------------------------------------
            # Mannheim
            # ------------------------------------------------------

            (
                "University of Mannheim",
                "Mannheim",
                49.4830,
                8.4620
            ),

            (
                "Mannheim University of Applied Sciences",
                "Mannheim",
                49.4800,
                8.4950
            ),


            # ------------------------------------------------------
            # Munich
            # ------------------------------------------------------

            (
                "Ludwig-Maximilians-Universität München",
                "Munich",
                48.1508,
                11.5802
            ),

            (
                "Technische Universität München",
                "Munich",
                48.1497,
                11.5673
            ),

            (
                "Munich University of Applied Sciences",
                "Munich",
                48.1530,
                11.5500
            ),


            # ------------------------------------------------------
            # Münster
            # ------------------------------------------------------

            (
                "University of Münster",
                "Münster",
                51.9630,
                7.6200
            ),


            # ------------------------------------------------------
            # Nuremberg
            # ------------------------------------------------------

            (
                "FAU Erlangen-Nürnberg",
                "Nuremberg",
                49.4520,
                11.0820
            ),

            (
                "Technische Hochschule Nürnberg",
                "Nuremberg",
                49.4480,
                11.0790
            ),


            # ------------------------------------------------------
            # Stuttgart
            # ------------------------------------------------------

            (
                "University of Stuttgart",
                "Stuttgart",
                48.7480,
                9.1060
            ),

            (
                "Hochschule Stuttgart",
                "Stuttgart",
                48.7750,
                9.1770
            ),


            # ------------------------------------------------------
            # Wedel
            # ------------------------------------------------------

            (
                "FH Wedel",
                "Wedel",
                53.5833,
                9.7167
            )

        ]


        # ==========================================================
        # INSERT UNIVERSITIES
        # ==========================================================

        for university in universities:

            db.execute(
                """
                INSERT OR IGNORE INTO universities
                (
                    name,
                    city,
                    latitude,
                    longitude
                )
                VALUES (?, ?, ?, ?)
                """,
                university
            )



        # ==========================================================
        # SAMPLE ACCOMMODATION DATA
        # ==========================================================
        # Small controlled dataset for demonstrating the main
        # StudentStay filter combinations.
        #
        # Each city includes representative combinations of:
        # private/shared + furnished/unfurnished.
        # Existing listings are preserved.
        # ==========================================================

        provider = db.execute(
            "SELECT id FROM users WHERE role = 'provider' ORDER BY id LIMIT 1"
        ).fetchone()

        # Create a development provider automatically when the database
        # is fresh, so the sample accommodation data can always be seeded.
        if not provider:
            from auth import hash_password

            password_hash = hash_password("password123")

            cursor = db.execute(
                """
                INSERT INTO users (name, email, password_hash, role)
                VALUES (?, ?, ?, ?)
                """,
                (
                    "Test Provider",
                    "provider@test.com",
                    password_hash,
                    "provider"
                )
            )

            provider_id = cursor.lastrowid
        else:
            provider_id = provider["id"]

        accommodations = [
                # ------------------------------------------------------
                # Berlin
                # ------------------------------------------------------
                (
                    "Berlin Private Furnished Room",
                    "Furnished private student room in Berlin.",
                    "Berlin",
                    620, 1200, "PRIVATE", 1,
                    "2026-09-15", "2027-03-31", 30
                ),
                (
                    "Berlin Private Unfurnished Room",
                    "Private student room with basic unfurnished setup.",
                    "Berlin",
                    680, 1300, "PRIVATE", 0,
                    "2026-10-01", "2027-03-31", 35
                ),
                (
                    "Berlin Shared Furnished Room",
                    "Furnished room in a shared student apartment.",
                    "Berlin",
                    480, 900, "SHARED", 1,
                    "2026-09-20", "2027-03-31", 25
                ),
                (
                    "Berlin Shared Unfurnished Room",
                    "Affordable unfurnished room in a shared apartment.",
                    "Berlin",
                    420, 800, "SHARED", 0,
                    "2026-10-15", "2027-03-31", 40
                ),

                # ------------------------------------------------------
                # Hamburg
                # ------------------------------------------------------
                (
                    "Hamburg Private Furnished Room",
                    "Furnished private student room in Hamburg.",
                    "Hamburg",
                    590, 1100, "PRIVATE", 1,
                    "2026-09-15", "2027-03-31", 25
                ),
                (
                    "Hamburg Private Unfurnished Room",
                    "Private unfurnished room near Hamburg universities.",
                    "Hamburg",
                    560, 1000, "PRIVATE", 0,
                    "2026-10-01", "2027-03-31", 35
                ),
                (
                    "Hamburg Shared Furnished Room",
                    "Furnished room in a shared student flat.",
                    "Hamburg",
                    470, 850, "SHARED", 1,
                    "2026-09-20", "2027-03-31", 20
                ),
                (
                    "Hamburg Shared Unfurnished Room",
                    "Lower-cost unfurnished shared room.",
                    "Hamburg",
                    400, 750, "SHARED", 0,
                    "2026-10-15", "2027-03-31", 40
                ),

                # ------------------------------------------------------
                # Munich
                # ------------------------------------------------------
                (
                    "Munich Private Furnished Room",
                    "Furnished private student room in Munich.",
                    "Munich",
                    760, 1400, "PRIVATE", 1,
                    "2026-09-15", "2027-03-31", 25
                ),
                (
                    "Munich Private Unfurnished Room",
                    "Private unfurnished student room.",
                    "Munich",
                    700, 1300, "PRIVATE", 0,
                    "2026-10-01", "2027-03-31", 35
                ),
                (
                    "Munich Shared Furnished Room",
                    "Furnished room in a shared apartment.",
                    "Munich",
                    590, 1000, "SHARED", 1,
                    "2026-09-20", "2027-03-31", 30
                ),
                (
                    "Munich Shared Unfurnished Room",
                    "Unfurnished shared student room.",
                    "Munich",
                    520, 900, "SHARED", 0,
                    "2026-10-15", "2027-03-31", 40
                ),

                # ------------------------------------------------------
                # Cologne
                # ------------------------------------------------------
                (
                    "Cologne Private Furnished Room",
                    "Furnished private room for a student in Cologne.",
                    "Cologne",
                    600, 1100, "PRIVATE", 1,
                    "2026-09-15", "2027-03-31", 25
                ),
                (
                    "Cologne Private Unfurnished Room",
                    "Private unfurnished student room.",
                    "Cologne",
                    550, 1000, "PRIVATE", 0,
                    "2026-10-01", "2027-03-31", 35
                ),
                (
                    "Cologne Shared Furnished Room",
                    "Furnished room in a shared student flat.",
                    "Cologne",
                    450, 800, "SHARED", 1,
                    "2026-09-20", "2027-03-31", 20
                ),
                (
                    "Cologne Shared Unfurnished Room",
                    "Affordable unfurnished shared room.",
                    "Cologne",
                    390, 700, "SHARED", 0,
                    "2026-10-15", "2027-03-31", 40
                ),

                # ------------------------------------------------------
                # Aachen
                # ------------------------------------------------------
                (
                    "Aachen Private Furnished Room",
                    "Furnished private student room in Aachen.",
                    "Aachen",
                    520, 950, "PRIVATE", 1,
                    "2026-09-15", "2027-03-31", 20
                ),
                (
                    "Aachen Private Unfurnished Room",
                    "Private unfurnished room for students.",
                    "Aachen",
                    470, 850, "PRIVATE", 0,
                    "2026-10-01", "2027-03-31", 30
                ),
                (
                    "Aachen Shared Furnished Room",
                    "Furnished room in a shared student apartment.",
                    "Aachen",
                    390, 700, "SHARED", 1,
                    "2026-09-20", "2027-03-31", 15
                ),
                (
                    "Aachen Shared Unfurnished Room",
                    "Affordable unfurnished shared room.",
                    "Aachen",
                    340, 600, "SHARED", 0,
                    "2026-10-15", "2027-03-31", 35
                ),

                # ------------------------------------------------------
                # Frankfurt
                # ------------------------------------------------------
                (
                    "Frankfurt Private Furnished Room",
                    "Furnished private student room in Frankfurt.",
                    "Frankfurt",
                    650, 1200, "PRIVATE", 1,
                    "2026-09-15", "2027-03-31", 25
                ),
                (
                    "Frankfurt Private Unfurnished Room",
                    "Private unfurnished student room.",
                    "Frankfurt",
                    610, 1100, "PRIVATE", 0,
                    "2026-10-01", "2027-03-31", 35
                ),
                (
                    "Frankfurt Shared Furnished Room",
                    "Furnished room in a shared apartment.",
                    "Frankfurt",
                    500, 900, "SHARED", 1,
                    "2026-09-20", "2027-03-31", 20
                ),
                (
                    "Frankfurt Shared Unfurnished Room",
                    "Lower-cost unfurnished shared room.",
                    "Frankfurt",
                    440, 800, "SHARED", 0,
                    "2026-10-15", "2027-03-31", 40
                ),

                # ------------------------------------------------------
                # Stuttgart
                # ------------------------------------------------------
                (
                    "Stuttgart Private Furnished Room",
                    "Furnished private student room in Stuttgart.",
                    "Stuttgart",
                    650, 1200, "PRIVATE", 1,
                    "2026-09-15", "2027-03-31", 25
                ),
                (
                    "Stuttgart Private Unfurnished Room",
                    "Private unfurnished student room.",
                    "Stuttgart",
                    600, 1100, "PRIVATE", 0,
                    "2026-10-01", "2027-03-31", 35
                ),
                (
                    "Stuttgart Shared Furnished Room",
                    "Furnished room in a shared student flat.",
                    "Stuttgart",
                    490, 850, "SHARED", 1,
                    "2026-09-20", "2027-03-31", 20
                ),
                (
                    "Stuttgart Shared Unfurnished Room",
                    "Affordable unfurnished shared room.",
                    "Stuttgart",
                    430, 750, "SHARED", 0,
                    "2026-10-15", "2027-03-31", 40
                ),

                # ------------------------------------------------------
                # Wedel
                # ------------------------------------------------------
                (
                    "Wedel Private Furnished Room",
                    "Furnished private student room in Wedel.",
                    "Wedel",
                    520, 950, "PRIVATE", 1,
                    "2026-09-15", "2027-03-31", 15
                ),
                (
                    "Wedel Private Unfurnished Room",
                    "Private unfurnished student room.",
                    "Wedel",
                    470, 850, "PRIVATE", 0,
                    "2026-10-01", "2027-03-31", 20
                ),
                (
                    "Wedel Shared Furnished Room",
                    "Furnished room in a shared student apartment.",
                    "Wedel",
                    390, 700, "SHARED", 1,
                    "2026-09-20", "2027-03-31", 10
                ),
                (
                    "Wedel Shared Unfurnished Room",
                    "Affordable unfurnished shared room.",
                    "Wedel",
                    340, 600, "SHARED", 0,
                    "2026-10-15", "2027-03-31", 25
                )
            ]

        for (
            title, description, city, rent, deposit,
            room_type, furnished, available_from,
            available_until, commute_minutes
        ) in accommodations:

            exists = db.execute(
                "SELECT id FROM accommodations WHERE title = ?",
                (title,)
            ).fetchone()

            if not exists:
                db.execute(
                    """
                    INSERT INTO accommodations (
                        provider_id, title, description, address,
                        city, latitude, longitude, monthly_rent,
                        deposit, room_type, furnished,
                        available_from, available_until,
                        commute_minutes, status
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        provider_id,
                        title,
                        description,
                        city + ", Germany",
                        city,
                        None,
                        None,
                        rent,
                        deposit,
                        room_type,
                        furnished,
                        available_from,
                        available_until,
                        commute_minutes,
                        "AVAILABLE"
                    )
                )


        # ==========================================================
        # SAVE DATABASE
        # ==========================================================

        db.commit()


    finally:

        db.close()