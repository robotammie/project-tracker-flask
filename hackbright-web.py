from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/create_student")
def get_new_student_form():
  """Show form for entering a new student into the database"""

  return render_template("create_student.html")

@app.route("/new_student", methods=['POST'])
def add_student():
  """Add student to database and display confirmation"""

  # get student data from form
  first_name = request.form.get('fname')
  last_name = request.form.get('lname')
  github = request.form.get('github')

  # insert student info into table
  hackbright.make_new_student(first_name, last_name, github)

  # render confirmation page (with link to student page)
  return render_template("new_student.html",
                         first=first_name,
                         last=last_name,
                         github=github)

@app.route("/student")
def get_student():
    """Show information about a student."""

    # run select statement, bind 'github' to resulting tuple
    github = request.args.get('github', 'jhacks')

    # unpack tuple
    first, last, github = hackbright.get_student_by_github(github)
    
    # list of tuples (project, grade)
    all_grades = hackbright.get_grades_by_github(github)

    # render student info page
    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           all_grades=all_grades)
    return html

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")






if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
