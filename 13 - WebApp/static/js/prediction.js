/*==========================================================
    HEART DISEASE RISK PREDICTION SYSTEM
    prediction.js
    PART 1
==========================================================*/

"use strict";

/*==========================================================
    GLOBAL VARIABLES
==========================================================*/

let predictionForm;

let submitButton;

let resetButton;

let resultSection;

let errorSection;

let loadingOverlay;


/*==========================================================
    PAGE LOAD
==========================================================*/

document.addEventListener("DOMContentLoaded", function () {

    initializePredictionPage();

});


/*==========================================================
    INITIALIZE PAGE
==========================================================*/

function initializePredictionPage() {

    predictionForm = document.getElementById("predictionForm");

    resultSection = document.querySelector(".result-section");

    errorSection = document.querySelector(".error-section");

    submitButton = document.querySelector(".btn");

    resetButton = document.querySelector(".btn-reset");

    createLoadingOverlay();

    registerEvents();

    animateExistingResult();

    console.log("Prediction Page Loaded Successfully");

}


/*==========================================================
    REGISTER EVENTS
==========================================================*/

function registerEvents() {

    if (predictionForm) {

        predictionForm.addEventListener(

            "submit",

            startPrediction

        );

    }

    if (resetButton) {

        resetButton.addEventListener(

            "click",

            resetPredictionForm

        );

    }

}


/*==========================================================
    CREATE LOADING OVERLAY
==========================================================*/

function createLoadingOverlay() {

    loadingOverlay = document.createElement("div");

    loadingOverlay.id = "predictionLoading";

    loadingOverlay.style.position = "fixed";

    loadingOverlay.style.top = "0";

    loadingOverlay.style.left = "0";

    loadingOverlay.style.width = "100%";

    loadingOverlay.style.height = "100%";

    loadingOverlay.style.background = "rgba(255,255,255,0.9)";

    loadingOverlay.style.display = "none";

    loadingOverlay.style.justifyContent = "center";

    loadingOverlay.style.alignItems = "center";

    loadingOverlay.style.flexDirection = "column";

    loadingOverlay.style.zIndex = "9999";

    loadingOverlay.innerHTML = `

        <div class="prediction-spinner"></div>

        <h2 style="margin-top:20px;color:#d62828;">

            Predicting Heart Disease...

        </h2>

        <p>

            Please wait while the AI model analyses the patient's data.

        </p>

    `;

    document.body.appendChild(

        loadingOverlay

    );

}


/*==========================================================
    START PREDICTION
==========================================================*/

function startPrediction(event) {

    if (!predictionForm) {

        return;

    }

    if (typeof validateForm === "function") {

        const valid = validateForm(event);

        if (!valid) {

            return;

        }

    }

    showLoading();

    disableSubmitButton();

}


/*==========================================================
    SHOW LOADING
==========================================================*/

function showLoading() {

    if (!loadingOverlay) {

        return;

    }

    loadingOverlay.style.display = "flex";

}


/*==========================================================
    HIDE LOADING
==========================================================*/

function hideLoading() {

    if (!loadingOverlay) {

        return;

    }

    loadingOverlay.style.display = "none";

}


/*==========================================================
    DISABLE SUBMIT BUTTON
==========================================================*/

function disableSubmitButton() {

    if (!submitButton) {

        return;

    }

    submitButton.disabled = true;

    submitButton.innerHTML =

        '<i class="fa-solid fa-spinner fa-spin"></i> Predicting...';

}


/*==========================================================
    ENABLE SUBMIT BUTTON
==========================================================*/

function enableSubmitButton() {

    if (!submitButton) {

        return;

    }

    submitButton.disabled = false;

    submitButton.innerHTML =

        '<i class="fa-solid fa-heart-circle-check"></i> Predict';

}


/*==========================================================
    PLACEHOLDER FUNCTIONS
    (Implemented in Part 2, 3 & 4)
==========================================================*/

function animateExistingResult() {

}

function animateResultCard() {

}

function animateErrorCard() {

}

function resetPredictionForm() {

}

function scrollToResult() {

}

function showSuccessNotification() {

}

function updateProgressBar() {

}
/*==========================================================
    ANIMATE EXISTING RESULT
==========================================================*/

function animateExistingResult() {

    if (resultSection) {

        resultSection.style.opacity = "0";

        resultSection.style.transform = "translateY(40px)";

        setTimeout(function () {

            animateResultCard();

        }, 300);

    }

    if (errorSection) {

        errorSection.style.opacity = "0";

        errorSection.style.transform = "translateY(40px)";

        setTimeout(function () {

            animateErrorCard();

        }, 300);

    }

}


/*==========================================================
    RESULT CARD ANIMATION
==========================================================*/

function animateResultCard() {

    if (!resultSection) {

        return;

    }

    resultSection.style.transition =
        "all 0.8s ease";

    resultSection.style.opacity = "1";

    resultSection.style.transform =
        "translateY(0)";

    scrollToResult();

    showSuccessNotification();

    hideLoading();

    enableSubmitButton();

}


/*==========================================================
    ERROR CARD ANIMATION
==========================================================*/

function animateErrorCard() {

    if (!errorSection) {

        return;

    }

    errorSection.style.transition =
        "all 0.8s ease";

    errorSection.style.opacity = "1";

    errorSection.style.transform =
        "translateY(0)";

    hideLoading();

    enableSubmitButton();

}


/*==========================================================
    SCROLL TO RESULT
==========================================================*/

function scrollToResult() {

    if (resultSection) {

        resultSection.scrollIntoView({

            behavior: "smooth",

            block: "center"

        });

    }

    if (errorSection) {

        errorSection.scrollIntoView({

            behavior: "smooth",

            block: "center"

        });

    }

}


/*==========================================================
    SUCCESS NOTIFICATION
==========================================================*/

function showSuccessNotification() {

    const notification =
        document.createElement("div");

    notification.innerHTML =
        "Prediction Completed Successfully";

    notification.style.position = "fixed";

    notification.style.top = "20px";

    notification.style.right = "20px";

    notification.style.background =
        "#28a745";

    notification.style.color =
        "#ffffff";

    notification.style.padding =
        "15px 25px";

    notification.style.borderRadius =
        "8px";

    notification.style.boxShadow =
        "0 5px 15px rgba(0,0,0,0.2)";

    notification.style.zIndex =
        "10000";

    notification.style.fontWeight =
        "600";

    notification.style.opacity =
        "0";

    notification.style.transition =
        "0.4s";

    document.body.appendChild(
        notification
    );

    setTimeout(function () {

        notification.style.opacity = "1";

    }, 100);

    setTimeout(function () {

        notification.style.opacity = "0";

    }, 3000);

    setTimeout(function () {

        notification.remove();

    }, 3500);

}


/*==========================================================
    RESULT CARD HOVER EFFECT
==========================================================*/

if (resultSection) {

    resultSection.addEventListener(

        "mouseenter",

        function () {

            resultSection.style.transform =
                "scale(1.02)";

        }

    );

    resultSection.addEventListener(

        "mouseleave",

        function () {

            resultSection.style.transform =
                "scale(1)";

        }

    );

}


/*==========================================================
    ERROR CARD HOVER EFFECT
==========================================================*/

if (errorSection) {

    errorSection.addEventListener(

        "mouseenter",

        function () {

            errorSection.style.transform =
                "scale(1.02)";

        }

    );

    errorSection.addEventListener(

        "mouseleave",

        function () {

            errorSection.style.transform =
                "scale(1)";

        }

    );

}
/*==========================================================
    RESET PREDICTION FORM
==========================================================*/

function resetPredictionForm() {

    if (!predictionForm) {

        return;

    }

    predictionForm.reset();

    hideLoading();

    enableSubmitButton();

    clearValidationStyles();

    removeNotifications();

    console.log("Prediction Form Reset Successfully");

}


/*==========================================================
    CLEAR VALIDATION STYLES
==========================================================*/

function clearValidationStyles() {

    const inputs =
        predictionForm.querySelectorAll("input, select");

    inputs.forEach(function (input) {

        input.style.border = "1px solid #cccccc";

        input.style.boxShadow = "none";

    });

}


/*==========================================================
    REMOVE NOTIFICATIONS
==========================================================*/

function removeNotifications() {

    const notifications =
        document.querySelectorAll(".prediction-notification");

    notifications.forEach(function (item) {

        item.remove();

    });

}


/*==========================================================
    INPUT FOCUS EFFECT
==========================================================*/

const formInputs =
    document.querySelectorAll(

        ".prediction-container input, .prediction-container select"

    );

formInputs.forEach(function (input) {

    input.addEventListener("focus", function () {

        input.style.transition = "0.3s";

        input.style.boxShadow =
            "0 0 8px rgba(214,40,40,0.35)";

    });

    input.addEventListener("blur", function () {

        input.style.boxShadow = "none";

    });

});


/*==========================================================
    BUTTON HOVER EFFECT
==========================================================*/

if (submitButton) {

    submitButton.addEventListener("mouseenter", function () {

        submitButton.style.transform = "translateY(-2px)";

    });

    submitButton.addEventListener("mouseleave", function () {

        submitButton.style.transform = "translateY(0px)";

    });

}


if (resetButton) {

    resetButton.addEventListener("mouseenter", function () {

        resetButton.style.transform = "translateY(-2px)";

    });

    resetButton.addEventListener("mouseleave", function () {

        resetButton.style.transform = "translateY(0px)";

    });

}


/*==========================================================
    PROGRESS BAR
==========================================================*/

function updateProgressBar() {

    const inputs =
        predictionForm.querySelectorAll(

            "input, select"

        );

    let completed = 0;

    inputs.forEach(function (input) {

        if (input.value.trim() !== "") {

            completed++;

        }

    });

    const percentage =
        Math.round((completed / inputs.length) * 100);

    console.log(

        "Form Completion : " + percentage + "%"

    );

}


/*==========================================================
    UPDATE PROGRESS WHILE TYPING
==========================================================*/

if (predictionForm) {

    const inputs =
        predictionForm.querySelectorAll(

            "input, select"

        );

    inputs.forEach(function (input) {

        input.addEventListener(

            "input",

            updateProgressBar

        );

        input.addEventListener(

            "change",

            updateProgressBar

        );

    });

}


/*==========================================================
    AUTO SCROLL TO TOP AFTER RESET
==========================================================*/

if (resetButton) {

    resetButton.addEventListener("click", function () {

        window.scrollTo({

            top: 0,

            behavior: "smooth"

        });

    });

}


/*==========================================================
    LOADING TIMEOUT SAFETY
==========================================================*/

setTimeout(function () {

    hideLoading();

    enableSubmitButton();

}, 30000);


/*==========================================================
    PAGE READY MESSAGE
==========================================================*/

console.log(

    "Prediction Page Features Initialized Successfully"

);
/*==========================================================
    KEYBOARD SHORTCUTS
==========================================================*/

document.addEventListener("keydown", function (event) {

    /* Submit Form : Ctrl + Enter */

    if (event.ctrlKey && event.key === "Enter") {

        if (predictionForm) {

            predictionForm.requestSubmit();

        }

    }

    /* Reset Form : Escape */

    if (event.key === "Escape") {

        if (predictionForm) {

            predictionForm.reset();

        }

    }

});


/*==========================================================
    AUTO HIDE LOADING AFTER PAGE RESPONSE
==========================================================*/

window.addEventListener("load", function () {

    hideLoading();

    enableSubmitButton();

});


/*==========================================================
    INPUT ANIMATION
==========================================================*/

const allPredictionInputs =
document.querySelectorAll(
".prediction-container input, .prediction-container select"
);

allPredictionInputs.forEach(function (input) {

    input.addEventListener("focus", function () {

        input.parentElement.classList.add("active-input");

    });

    input.addEventListener("blur", function () {

        input.parentElement.classList.remove("active-input");

    });

});


/*==========================================================
    BUTTON CLICK EFFECT
==========================================================*/

const buttons =
document.querySelectorAll(".btn, .btn-reset");

buttons.forEach(function (button) {

    button.addEventListener("click", function () {

        button.style.transform = "scale(0.96)";

        setTimeout(function () {

            button.style.transform = "scale(1)";

        }, 150);

    });

});


/*==========================================================
    PREVENT MULTIPLE FORM SUBMISSIONS
==========================================================*/

let formSubmitted = false;

if (predictionForm) {

    predictionForm.addEventListener("submit", function (event) {

        if (formSubmitted) {

            event.preventDefault();

            return;

        }

        formSubmitted = true;

        setTimeout(function () {

            formSubmitted = false;

        }, 5000);

    });

}


/*==========================================================
    AUTO SCROLL TO FIRST INVALID INPUT
==========================================================*/

function scrollToFirstInvalidField() {

    const invalidField =
    document.querySelector(".validation-error");

    if (invalidField) {

        invalidField.scrollIntoView({

            behavior: "smooth",

            block: "center"

        });

    }

}


/*==========================================================
    PAGE PERFORMANCE LOG
==========================================================*/

window.addEventListener("load", function () {

    console.log("================================");

    console.log("Heart Disease Prediction System");

    console.log("Prediction Page Ready");

    console.log("JavaScript Loaded Successfully");

    console.log("================================");

});


/*==========================================================
    DISABLE MOUSE WHEEL ON NUMBER INPUTS
==========================================================*/

const numberInputs =
document.querySelectorAll(
'input[type="number"]'
);

numberInputs.forEach(function (input) {

    input.addEventListener("wheel", function (event) {

        event.target.blur();

    });

});


/*==========================================================
    AUTO FORMAT DECIMAL VALUE
==========================================================*/

if (typeof oldpeak !== "undefined" && oldpeak) {

    oldpeak.addEventListener("change", function () {

        if (oldpeak.value !== "") {

            oldpeak.value =
            Number(oldpeak.value).toFixed(1);

        }

    });

}


/*==========================================================
    RESULT CARD ANIMATION
==========================================================*/

if (resultSection) {

    resultSection.animate([

        {

            opacity: 0,

            transform: "translateY(40px)"

        },

        {

            opacity: 1,

            transform: "translateY(0px)"

        }

    ],

    {

        duration: 800,

        easing: "ease"

    });

}


/*==========================================================
    ERROR CARD ANIMATION
==========================================================*/

if (errorSection) {

    errorSection.animate([

        {

            opacity: 0,

            transform: "translateY(40px)"

        },

        {

            opacity: 1,

            transform: "translateY(0px)"

        }

    ],

    {

        duration: 800,

        easing: "ease"

    });

}


/*==========================================================
    REMOVE LOADING IF USER RETURNS
==========================================================*/

window.addEventListener("pageshow", function () {

    hideLoading();

    enableSubmitButton();

});


/*==========================================================
    FINAL INITIALIZATION
==========================================================*/

function initializePredictionSystem() {

    console.log("Prediction Module Initialized");

    updateProgressBar();

}

initializePredictionSystem();


console.log("prediction.js Loaded Successfully");