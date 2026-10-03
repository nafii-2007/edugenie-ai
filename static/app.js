const task =
    document.getElementById("task");

const inputText =
    document.getElementById("inputText");

const submitBtn =
    document.getElementById("submitBtn");

const statusElement =
    document.getElementById("status");

const result =
    document.getElementById("result");

const resultContent =
    document.getElementById("resultContent");


const endpoints = {

    qa: "/qa",

    explain: "/explain",

    quiz: "/quiz",

    summarize: "/summarize",

    learn: "/learn/recommendations"

};


/* ---------------------------------------------------------
   PLACEHOLDER
--------------------------------------------------------- */

task.addEventListener(
    "change",
    function () {

        const placeholders = {

            qa:
                "Example: Which is the largest ocean?",

            explain:
                "Example: Explain the Pythagoras theorem",

            quiz:
                "Paste an educational passage here",

            summarize:
                "Paste the long passage you want summarized",

            learn:
                "Example: SQL"

        };


        inputText.placeholder =
            placeholders[
                task.value
            ];

    }
);


/* ---------------------------------------------------------
   HTML ESCAPE
--------------------------------------------------------- */

function escapeHTML(
    value
) {

    return String(value)
        .replace(
            /[&<>"']/g,
            function (character) {

                const entities = {

                    "&": "&amp;",

                    "<": "&lt;",

                    ">": "&gt;",

                    '"': "&quot;",

                    "'": "&#039;"

                };

                return entities[
                    character
                ];

            }
        );

}


/* ---------------------------------------------------------
   RENDER RESULT
--------------------------------------------------------- */

function renderResult(
    data
) {


    /* Q&A */

    if (data.answer) {

        resultContent.innerHTML = `
            <div class="answer">
                ${escapeHTML(data.answer)}
            </div>
        `;

        return;
    }


    /* EXPLANATION */

    if (data.explanation) {

        resultContent.innerHTML = `
            <div class="answer">
                ${escapeHTML(data.explanation)}
            </div>
        `;

        return;
    }


    /* SUMMARY */

    if (data.summary) {

        resultContent.innerHTML = `
            <div class="answer">
                ${escapeHTML(data.summary)}
            </div>
        `;

        return;
    }


    /* QUIZ */

    if (data.questions) {

        let html = "";


        data.questions.forEach(
            function (question, index) {

                html += `

                    <div
                        class="quiz-question"
                    >

                        <strong>
                            ${index + 1}.
                            ${escapeHTML(
                                question.question
                            )}
                        </strong>
                `;


                question.options.forEach(
                    function (option, optionIndex) {

                        const letter =
                            String.fromCharCode(
                                65 + optionIndex
                            );


                        html += `

                            <label
                                class="option"
                            >

                                <input
                                    type="radio"
                                    name="question-${index}"
                                    value="${escapeHTML(option)}"
                                >

                                ${letter}.
                                ${escapeHTML(option)}

                            </label>

                        `;

                    }
                );


                html += `

                        <div
                            id="feedback-${index}"
                            class="feedback"
                        ></div>

                        <details>

                            <summary>
                                Explanation
                            </summary>

                            <p>
                                ${escapeHTML(
                                    question.explanation
                                )}
                            </p>

                        </details>

                    </div>

                `;

            }
        );


        html += `

            <button
                id="checkQuiz"
                class="generate-btn"
            >
                Check Answers
            </button>

        `;


        resultContent.innerHTML =
            html;


        document
            .getElementById("checkQuiz")
            .addEventListener(
                "click",
                function () {

                    data.questions.forEach(
                        function (
                            question,
                            index
                        ) {

                            const selected =
                                document.querySelector(
                                    `input[name="question-${index}"]:checked`
                                );


                            const feedback =
                                document.getElementById(
                                    `feedback-${index}`
                                );


                            if (!selected) {

                                feedback.textContent =
                                    "Please choose an answer.";

                                return;
                            }


                            if (
                                selected.value ===
                                question.correct_answer
                            ) {

                                feedback.textContent =
                                    "Correct!";

                            } else {

                                feedback.textContent =
                                    `Incorrect. Correct answer: ${question.correct_answer}`;

                            }

                        }
                    );

                }
            );


        return;
    }


    /* LEARNING PATH */

    if (
        data.recommendations
    ) {

        let html = "";


        data.recommendations.forEach(
            function (step) {

                html += `

                    <div
                        class="learning-step"
                    >

                        <h3>
                            ${escapeHTML(
                                step.level
                            )}
                        </h3>

                        <p>
                            <strong>
                                Timeline:
                            </strong>

                            ${escapeHTML(
                                step.timeline
                            )}
                        </p>

                        <p>
                            <strong>
                                Topics:
                            </strong>

                            ${step.topics
                                .map(
                                    escapeHTML
                                )
                                .join(", ")
                            }
                        </p>

                        <p>
                            <strong>
                                Resources:
                            </strong>

                            ${step.resources
                                .map(
                                    escapeHTML
                                )
                                .join(" • ")
                            }
                        </p>

                    </div>

                `;

            }
        );


        resultContent.innerHTML =
            html;

    }

}


/* ---------------------------------------------------------
   SUBMIT
--------------------------------------------------------- */

submitBtn.addEventListener(
    "click",
    async function () {

        const text =
            inputText.value.trim();


        if (!text) {

            statusElement.innerHTML =
                `<span class="error">
                    Please enter some text.
                </span>`;

            return;
        }


        submitBtn.disabled = true;

        statusElement.textContent =
            "EduGenie is thinking...";


        result.hidden = true;


        try {

            const response =
                await fetch(
                    endpoints[
                        task.value
                    ],
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            text: text
                        })
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Something went wrong."
                );

            }


            renderResult(
                data
            );


            result.hidden =
                false;


            statusElement.textContent =
                "Completed successfully.";


        } catch (error) {

            statusElement.innerHTML =
                `
                <span class="error">
                    ${escapeHTML(
                        error.message
                    )}
                </span>
                `;

        } finally {

            submitBtn.disabled =
                false;

        }

    }
);