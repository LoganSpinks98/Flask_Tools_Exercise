from flask import Flask, request, render_template, redirect, flash, session

from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config["SECRET_KEY"] = "It's-a-SECRET!"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)
@app.route("/")
def survey_start():
    """Show the survey start page."""
    return render_template("start.html", survey=survey)

@app.route("/start", methods=["POST"])
def begin():
    """clear the session before beginning the survey"""

    session[RESPONSES_KEY] = []
    return redirect("/questions/0")

@app.route("/answer", methods=["POST"])
def handle_question():
    """handle the responses and direct to next question"""
    choice = request.form["answer"]
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses
    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/questions/<int:question_id>")
def show_question(question_id):
    """Show the current question"""
    responses = session.get(RESPONSES_KEY)
    if(responses is None):
        # Cannot go to questions page
        return redirect("/")
    if(len(responses) == len(survey.questions)):
        return redirect("/complete")
    if(len(responses) != question_id):
        flash(f"invalid question ID: {question_id}.")
        return redirect(f"/questions/{len(responses)}")
    question = survey.questions[question_id]
    return render_template("question.html", question=question)

@app.route("/complete")
def show_complete():
    """Show the complete page after all questions are answered"""
    return render_template("complete.html")


