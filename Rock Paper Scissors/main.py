import random
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

youDict = {"r": 1, "p": 0, "s": -1}
reverseDict = {1: "Rock", 0: "Paper", -1: "Scissor"}

# Initialize scores
user_score = 0
computer_score = 0

@app.route('/')
def index():
    return render_template('index.html')  # HTML file for UI

@app.route('/play', methods=['POST'])
def play_game():
    global user_score, computer_score

    data = request.json
    youStr = data.get("choice", "").strip().lower()
    if youStr not in youDict:
        return jsonify({"error": "Invalid input. Please enter 'r', 'p', or 's'."}), 400

    you = youDict[youStr]

    # Computer choice
    computer = random.choice([-1, 0, 1])

    # Determine the result
    result_text = f"You chose {reverseDict[you]}, Computer chose {reverseDict[computer]}. "
    if computer == you:
        result_text += "MATCH DRAW!"
    else:
        if(computer == -1 and you == 1):
            result_text += "YOU WIN!"
            user_score += 1
        elif(computer == -1 and you == 0):
            result_text += "YOU LOSE!"
            computer_score += 1
        elif(computer == 1 and you == -1):
            result_text += "YOU LOSE!"
            computer_score += 1
        elif(computer == 1 and you == 0):
            result_text += "YOU WIN!"
            user_score += 1
        elif(computer == 0 and you == 1):
            result_text += "YOU LOSE!"
            computer_score += 1
        elif(computer == 0 and you == -1):
            result_text += "YOU WIN!"
            user_score += 1
        else:
            result_text += "Something went wrong."

    # Prepare response
    response = {
        "result": result_text,
        "user_score": user_score,
        "computer_score": computer_score
    }
    return jsonify(response)

@app.route('/restart', methods=['POST'])
def restart_game():
    global user_score, computer_score
    
    user_score = 0
    computer_score = 0
    return jsonify({"message": "Game restarted successfully!", "user_score": user_score, "computer_score": computer_score})

app.config['TEMPLATES_AUTO_RELOAD'] = True

if __name__ == "__main__":
    app.run(debug=True)
