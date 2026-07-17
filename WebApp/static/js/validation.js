/*==========================================================
    HEART DISEASE RISK PREDICTION SYSTEM
    validation.js
    PART 1
==========================================================*/

"use strict";

/*==========================================================
    WAIT UNTIL PAGE LOADS
==========================================================*/

document.addEventListener("DOMContentLoaded", function () {

    initializeValidation();

});


/*==========================================================
    GLOBAL VARIABLES
==========================================================*/

let form;

let age;
let sex;
let chestPain;
let restingBP;
let cholesterol;
let fastingBS;
let restingECG;
let maxHR;
let exerciseAngina;
let oldpeak;
let stSlope;


/*==========================================================
    INITIALIZE VALIDATION
==========================================================*/

function initializeValidation() {

    form = document.getElementById("predictionForm");

    if (!form) {

        console.log("Prediction Form Not Found");

        return;

    }

    age = document.getElementById("Age");
    sex = document.getElementById("Sex");
    chestPain = document.getElementById("ChestPainType");
    restingBP = document.getElementById("RestingBP");
    cholesterol = document.getElementById("Cholesterol");
    fastingBS = document.getElementById("FastingBS");
    restingECG = document.getElementById("RestingECG");
    maxHR = document.getElementById("MaxHR");
    exerciseAngina = document.getElementById("ExerciseAngina");
    oldpeak = document.getElementById("Oldpeak");
    stSlope = document.getElementById("ST_Slope");

    attachValidationEvents();

}


/*==========================================================
    ATTACH EVENTS
==========================================================*/

function attachValidationEvents() {

    age.addEventListener("input", validateAge);

    restingBP.addEventListener("input", validateRestingBP);

    cholesterol.addEventListener("input", validateCholesterol);

    maxHR.addEventListener("input", validateMaxHR);

    oldpeak.addEventListener("input", validateOldpeak);

    sex.addEventListener("change", validateGender);

    chestPain.addEventListener("change", validateChestPain);

    fastingBS.addEventListener("change", validateFastingBS);

    restingECG.addEventListener("change", validateRestingECG);

    exerciseAngina.addEventListener("change", validateExerciseAngina);

    stSlope.addEventListener("change", validateSTSlope);

    form.addEventListener("submit", validateForm);

}


/*==========================================================
    CREATE ERROR MESSAGE
==========================================================*/

function showError(input, message) {

    removeError(input);

    input.style.border = "2px solid red";

    const error = document.createElement("small");

    error.className = "validation-error";

    error.style.color = "red";

    error.style.display = "block";

    error.style.marginTop = "5px";

    error.style.fontSize = "13px";

    error.innerText = message;

    input.parentNode.appendChild(error);

}


/*==========================================================
    REMOVE ERROR
==========================================================*/

function removeError(input) {

    input.style.border = "1px solid #cccccc";

    const oldError = input.parentNode.querySelector(".validation-error");

    if (oldError) {

        oldError.remove();

    }

}


/*==========================================================
    SUCCESS STYLE
==========================================================*/

function setSuccess(input) {

    removeError(input);

    input.style.border = "2px solid #28a745";

}


/*==========================================================
    EMPTY FIELD CHECK
==========================================================*/

function isEmpty(input) {

    return input.value.trim() === "";

}


/*==========================================================
    VALID NUMBER
==========================================================*/

function isNumber(value) {

    return !isNaN(value);

}


/*==========================================================
    RANGE CHECK
==========================================================*/

function inRange(value, min, max) {

    return value >= min && value <= max;

}


/*==========================================================
    PLACEHOLDER FUNCTIONS
    (Implemented in Part 2 & Part 3)
==========================================================*/

function validateAge() {}

function validateRestingBP() {}

function validateCholesterol() {}

function validateMaxHR() {}

function validateOldpeak() {}

function validateGender() {}

function validateChestPain() {}

function validateFastingBS() {}

function validateRestingECG() {}

function validateExerciseAngina() {}

function validateSTSlope() {}

function validateForm(event) {}

/*==========================================================
    AGE VALIDATION
==========================================================*/

function validateAge() {

    const value = age.value.trim();

    if (value === "") {

        showError(age, "Age is required.");

        return false;

    }

    if (!isNumber(value)) {

        showError(age, "Age must be a valid number.");

        return false;

    }

    const ageValue = Number(value);

    if (!inRange(ageValue, 1, 120)) {

        showError(age, "Age must be between 1 and 120.");

        return false;

    }

    setSuccess(age);

    return true;

}


/*==========================================================
    RESTING BLOOD PRESSURE VALIDATION
==========================================================*/

function validateRestingBP() {

    const value = restingBP.value.trim();

    if (value === "") {

        showError(restingBP, "Resting Blood Pressure is required.");

        return false;

    }

    if (!isNumber(value)) {

        showError(restingBP, "Blood Pressure must be numeric.");

        return false;

    }

    const bp = Number(value);

    if (!inRange(bp, 50, 250)) {

        showError(
            restingBP,
            "Blood Pressure should be between 50 and 250 mmHg."
        );

        return false;

    }

    setSuccess(restingBP);

    return true;

}


/*==========================================================
    CHOLESTEROL VALIDATION
==========================================================*/

function validateCholesterol() {

    const value = cholesterol.value.trim();

    if (value === "") {

        showError(cholesterol, "Cholesterol value is required.");

        return false;

    }

    if (!isNumber(value)) {

        showError(cholesterol, "Cholesterol must be numeric.");

        return false;

    }

    const chol = Number(value);

    if (!inRange(chol, 0, 700)) {

        showError(
            cholesterol,
            "Cholesterol should be between 0 and 700 mg/dL."
        );

        return false;

    }

    setSuccess(cholesterol);

    return true;

}


/*==========================================================
    REAL-TIME NUMERIC INPUT RESTRICTION
==========================================================*/

age.addEventListener("keypress", function (event) {

    if (!/[0-9]/.test(event.key)) {

        event.preventDefault();

    }

});


restingBP.addEventListener("keypress", function (event) {

    if (!/[0-9]/.test(event.key)) {

        event.preventDefault();

    }

});


cholesterol.addEventListener("keypress", function (event) {

    if (!/[0-9]/.test(event.key)) {

        event.preventDefault();

    }

});


/*==========================================================
    AUTO REMOVE EXTRA SPACES
==========================================================*/

age.addEventListener("blur", function () {

    age.value = age.value.trim();

});


restingBP.addEventListener("blur", function () {

    restingBP.value = restingBP.value.trim();

});


cholesterol.addEventListener("blur", function () {

    cholesterol.value = cholesterol.value.trim();

});
/*==========================================================
    MAXIMUM HEART RATE VALIDATION
==========================================================*/

function validateMaxHR() {

    const value = maxHR.value.trim();

    if (value === "") {

        showError(maxHR, "Maximum Heart Rate is required.");

        return false;

    }

    if (!isNumber(value)) {

        showError(maxHR, "Maximum Heart Rate must be numeric.");

        return false;

    }

    const hr = Number(value);

    if (!inRange(hr, 60, 220)) {

        showError(
            maxHR,
            "Maximum Heart Rate should be between 60 and 220 bpm."
        );

        return false;

    }

    setSuccess(maxHR);

    return true;

}


/*==========================================================
    OLDPEAK VALIDATION
==========================================================*/

function validateOldpeak() {

    const value = oldpeak.value.trim();

    if (value === "") {

        showError(oldpeak, "Oldpeak value is required.");

        return false;

    }

    if (isNaN(value)) {

        showError(oldpeak, "Oldpeak must be numeric.");

        return false;

    }

    const peak = parseFloat(value);

    if (peak < -2 || peak > 10) {

        showError(
            oldpeak,
            "Oldpeak should be between -2.0 and 10.0."
        );

        return false;

    }

    setSuccess(oldpeak);

    return true;

}


/*==========================================================
    GENDER VALIDATION
==========================================================*/

function validateGender() {

    if (sex.value === "") {

        showError(sex, "Please select gender.");

        return false;

    }

    setSuccess(sex);

    return true;

}


/*==========================================================
    CHEST PAIN VALIDATION
==========================================================*/

function validateChestPain() {

    if (chestPain.value === "") {

        showError(
            chestPain,
            "Please select chest pain type."
        );

        return false;

    }

    setSuccess(chestPain);

    return true;

}


/*==========================================================
    FASTING BLOOD SUGAR VALIDATION
==========================================================*/

function validateFastingBS() {

    if (fastingBS.value === "") {

        showError(
            fastingBS,
            "Please select fasting blood sugar."
        );

        return false;

    }

    setSuccess(fastingBS);

    return true;

}


/*==========================================================
    RESTING ECG VALIDATION
==========================================================*/

function validateRestingECG() {

    if (restingECG.value === "") {

        showError(
            restingECG,
            "Please select Resting ECG."
        );

        return false;

    }

    setSuccess(restingECG);

    return true;

}


/*==========================================================
    EXERCISE ANGINA VALIDATION
==========================================================*/

function validateExerciseAngina() {

    if (exerciseAngina.value === "") {

        showError(
            exerciseAngina,
            "Please select Exercise Induced Angina."
        );

        return false;

    }

    setSuccess(exerciseAngina);

    return true;

}


/*==========================================================
    ST SLOPE VALIDATION
==========================================================*/

function validateSTSlope() {

    if (stSlope.value === "") {

        showError(
            stSlope,
            "Please select ST Slope."
        );

        return false;

    }

    setSuccess(stSlope);

    return true;

}


/*==========================================================
    NUMERIC INPUT RESTRICTIONS
==========================================================*/

maxHR.addEventListener("keypress", function (event) {

    if (!/[0-9]/.test(event.key)) {

        event.preventDefault();

    }

});


oldpeak.addEventListener("keypress", function (event) {

    const allowed = /[0-9.-]/;

    if (!allowed.test(event.key)) {

        event.preventDefault();

    }

});


/*==========================================================
    REMOVE EXTRA SPACES
==========================================================*/

maxHR.addEventListener("blur", function () {

    maxHR.value = maxHR.value.trim();

});


oldpeak.addEventListener("blur", function () {

    oldpeak.value = oldpeak.value.trim();

});


/*==========================================================
    DROPDOWN CHANGE VALIDATION
==========================================================*/

sex.addEventListener("change", validateGender);

chestPain.addEventListener("change", validateChestPain);

fastingBS.addEventListener("change", validateFastingBS);

restingECG.addEventListener("change", validateRestingECG);

exerciseAngina.addEventListener("change", validateExerciseAngina);

stSlope.addEventListener("change", validateSTSlope);
/*==========================================================
    COMPLETE FORM VALIDATION
==========================================================*/

function validateForm(event) {

    let valid = true;

    if (!validateAge()) {
        valid = false;
    }

    if (!validateGender()) {
        valid = false;
    }

    if (!validateChestPain()) {
        valid = false;
    }

    if (!validateRestingBP()) {
        valid = false;
    }

    if (!validateCholesterol()) {
        valid = false;
    }

    if (!validateFastingBS()) {
        valid = false;
    }

    if (!validateRestingECG()) {
        valid = false;
    }

    if (!validateMaxHR()) {
        valid = false;
    }

    if (!validateExerciseAngina()) {
        valid = false;
    }

    if (!validateOldpeak()) {
        valid = false;
    }

    if (!validateSTSlope()) {
        valid = false;
    }

    if (!valid) {

        event.preventDefault();

        const firstError =
            document.querySelector(".validation-error");

        if (firstError) {

            firstError.scrollIntoView({

                behavior: "smooth",

                block: "center"

            });

        }

        alert(
            "Please correct all highlighted fields before submitting."
        );

        return false;

    }

    return true;

}


/*==========================================================
    RESET FORM
==========================================================*/

form.addEventListener("reset", function () {

    setTimeout(function () {

        const errors =
            document.querySelectorAll(".validation-error");

        errors.forEach(function (error) {

            error.remove();

        });

        const inputs =
            form.querySelectorAll("input, select");

        inputs.forEach(function (input) {

            input.style.border = "1px solid #cccccc";

        });

    }, 100);

});


/*==========================================================
    REMOVE ERROR WHEN USER STARTS TYPING
==========================================================*/

const allInputs =
    form.querySelectorAll("input, select");

allInputs.forEach(function (input) {

    input.addEventListener("input", function () {

        removeError(input);

    });

});


/*==========================================================
    AUTO FOCUS FIRST INPUT
==========================================================*/

window.addEventListener("load", function () {

    if (age) {

        age.focus();

    }

});


/*==========================================================
    ENTER KEY SUPPORT
==========================================================*/

document.addEventListener("keydown", function (event) {

    if (event.key === "Enter") {

        if (document.activeElement.tagName !== "BUTTON") {

            validateForm(event);

        }

    }

});


/*==========================================================
    COPY / PASTE CLEANUP
==========================================================*/

allInputs.forEach(function (input) {

    input.addEventListener("paste", function () {

        setTimeout(function () {

            input.value = input.value.trim();

        }, 10);

    });

});


/*==========================================================
    PREVENT NEGATIVE VALUES
==========================================================*/

const numericInputs = [

    age,

    restingBP,

    cholesterol,

    maxHR

];

numericInputs.forEach(function (input) {

    input.addEventListener("input", function () {

        if (Number(input.value) < 0) {

            input.value = "";

        }

    });

});


/*==========================================================
    OLDPEAK FORMAT
==========================================================*/

oldpeak.addEventListener("change", function () {

    if (oldpeak.value !== "") {

        oldpeak.value =
            parseFloat(oldpeak.value).toFixed(1);

    }

});


/*==========================================================
    SUCCESS MESSAGE
==========================================================*/

form.addEventListener("submit", function () {

    if (

        validateAge() &&
        validateGender() &&
        validateChestPain() &&
        validateRestingBP() &&
        validateCholesterol() &&
        validateFastingBS() &&
        validateRestingECG() &&
        validateMaxHR() &&
        validateExerciseAngina() &&
        validateOldpeak() &&
        validateSTSlope()

    ) {

        console.log(
            "Validation Successful"
        );

    }

});

console.log(
    "Heart Disease Validation Loaded Successfully"
);