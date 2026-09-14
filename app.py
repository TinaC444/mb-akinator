import os
import secrets

from flask import Flask, jsonify, render_template, request, session

from backend.game_logic import game_view, new_game, remove_invalid_char


app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY") or secrets.token_hex(32),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)


@app.get("/")
def index():
    # A fresh page starts a fresh game. Each browser has its own session.
    session["game"] = new_game()
    return render_template("index.html", game=game_view(session["game"]))


@app.post("/api/answer")
def answer():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(error="Please send a Yes or No answer."), 400
    user_ans = payload.get("answer")
    if type(user_ans) is not int or user_ans not in (0, 1):
        return jsonify(error="The answer must be 1 (Yes) or 0 (No)."), 400

    game = session.get("game")
    if game is None:
        return jsonify(error="Your game expired. Refresh the page to start again."), 409

    current = game_view(game)
    if current["done"]:
        return jsonify(current)

    best_q = current["question_index"]
    question_index = payload.get("question_index")
    if type(question_index) is not int or question_index != best_q:
        return jsonify(
            error="The question changed. Please answer the question shown now.",
            game=current,
        ), 409

    game["possible_char"] = remove_invalid_char(
        user_ans, best_q, game["possible_char"]
    )
    game["unasked_q"][best_q] = 0
    # Reassign to let Flask know that the nested session data changed.
    session["game"] = game
    return jsonify(game_view(game))


if __name__ == "__main__":
    app.run()
