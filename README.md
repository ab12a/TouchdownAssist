# TouchdownAssist

Student accommodation and arrival assistant (Flask + SQLite + plain HTML/CSS/JS).

## Run

    pip install -r requirements.txt
    python app.py              # http://localhost:5000

    docker build -t touchdownassist .
    docker run -p 5000:5000 touchdownassist

## Demo login

| Email | Password |
|-------|----------|
| student@test.com | password123 |

Created automatically on the first start (the password is stored hashed).
New accounts can also be created with the Register button.

## Tests

    python -m unittest -v

## Files

| File | Job |
|------|-----|
| app.py | Flask routes (REST API), login check |
| matching.py | filtering + scoring, no database inside |
| database.py | tables, sample universities and rooms |
| templates/index.html, static/ | page, styles, JavaScript (EN/DE texts) |
| tests/ | unit tests (matching), database tests, integration tests (API) |

## Matching score

A room is dropped if it fails one mandatory wish: city of the university, rent,
rent + deposit, room type, furnished (if wanted), available from/until, commute.
Remaining rooms get 65 points, +15 furnished wish met, +10 rent <= 90% of the
maximum, +10 commute <= 75% of the limit (max. 100). Commute is an estimate:
3 min per km straight-line distance from the room to the university + 5 min.
Real route calculation is future work.

## Requirements -> code -> tests

| Requirement | Code | Test |
|---|---|---|
| F1 Login | /api/register, /api/login | test_register_and_login, test_wrong_password |
| F2 Profile | /api/profile | test_profile_and_matches, test_profile_can_be_updated, test_invalid_profile_is_rejected |
| F3 University selection | /api/universities, profile form | test_profile_and_matches |
| F4 University anchor | matching.commute_minutes, city filter | test_long_commute_is_removed, test_wrong_city_is_removed |
| F5 Filtering | matching.find_matches | test_*_is_removed |
| F6 Ranking | match_score, sort | test_best_score_comes_first |
| F7 Explanation | match_reasons | test_reasons_are_given |
| F8 Saved | /api/saved | test_save_and_remove, test_saving_twice_is_stored_once |
| F9 Expression of interest | /api/interest | test_expression_of_interest, test_interest_twice_is_stored_once |
| F10 Arrival planner | /api/tasks | test_arrival_tasks |
| F11 EN/DE | TEXT in static/app.js | manual |
| NF3 Security | password hashing (werkzeug) | test_password_is_not_stored_as_plain_text |
| NF8 Deployment | Dockerfile, /api/health | test_health |
| NF6 Reliability | input checks, 401/404/400 | test_duplicate_email_and_bad_input_do_not_crash, test_unknown_accommodation_gives_404 |
