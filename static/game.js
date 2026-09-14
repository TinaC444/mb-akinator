const gameElement = document.querySelector("#game");
const questionElement = document.querySelector("#question");
const answersElement = document.querySelector("#answers");
const remainingElement = document.querySelector("#remaining");
const restartElement = document.querySelector("#restart");
const errorElement = document.querySelector("#error");
const buttons = document.querySelectorAll("[data-answer]");

let game = JSON.parse(document.querySelector("#initial-game").textContent);
let waiting = false;

function renderGame(nextGame) {
    game = nextGame;
    questionElement.textContent = game.message;
    const noun = game.remaining === 1 ? "character" : "characters";
    remainingElement.textContent = `(${game.remaining} ${noun} remaining)`;
    answersElement.hidden = game.done;
    restartElement.hidden = !game.done;
    if (game.done) {
        restartElement.focus();
    }
}

async function submitAnswer(answer) {
    if (waiting || game.done) {
        return;
    }

    waiting = true;
    errorElement.hidden = true;
    gameElement.setAttribute("aria-busy", "true");
    buttons.forEach((button) => { button.disabled = true; });

    try {
        const response = await fetch(gameElement.dataset.answerUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ answer, question_index: game.question_index }),
        });
        const result = await response.json();
        if (!response.ok) {
            if (result.game) {
                renderGame(result.game);
            }
            throw new Error(result.error || "Couldn't submit your answer. Please try again.");
        }
        renderGame(result);
    } catch (error) {
        errorElement.textContent = error.message || "Couldn't reach the game. Please try again.";
        errorElement.hidden = false;
    } finally {
        waiting = false;
        gameElement.setAttribute("aria-busy", "false");
        buttons.forEach((button) => { button.disabled = game.done; });
    }
}

buttons.forEach((button) => {
    button.addEventListener("click", () => submitAnswer(Number(button.dataset.answer)));
});
