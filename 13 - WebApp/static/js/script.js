/*=========================================================
  HEART DISEASE RISK PREDICTION SYSTEM
  Common JavaScript File
  Author : Tanmay Awate
=========================================================*/

"use strict";

/*=========================================================
  DOM READY
=========================================================*/

document.addEventListener("DOMContentLoaded", () => {

    initializeNavigation();
    initializeSmoothScroll();
    initializeScrollAnimation();
    initializeStatisticsCounter();
    initializeHeroAnimation();
    initializeButtonEffects();
    initializeBackToTop();
    updateFooterYear();

});


/*=========================================================
  NAVIGATION ACTIVE LINK
=========================================================*/

function initializeNavigation() {

    const currentPage = window.location.pathname;

    const links = document.querySelectorAll(".nav-links a");

    links.forEach(link => {

        const href = link.getAttribute("href");

        if (href && currentPage.includes(href)) {

            link.classList.add("active");

        }

    });

}


/*=========================================================
  SMOOTH SCROLL
=========================================================*/

function initializeSmoothScroll() {

    const anchors = document.querySelectorAll('a[href^="#"]');

    anchors.forEach(anchor => {

        anchor.addEventListener("click", function (e) {

            const target = document.querySelector(this.getAttribute("href"));

            if (target) {

                e.preventDefault();

                target.scrollIntoView({

                    behavior: "smooth",
                    block: "start"

                });

            }

        });

    });

}


/*=========================================================
  SCROLL ANIMATION
=========================================================*/

function initializeScrollAnimation() {

    const elements = document.querySelectorAll(

        ".card,.feature-box,.stat-card,.step,.information,.features,.statistics,.cta"

    );

    function reveal() {

        elements.forEach(element => {

            const top = element.getBoundingClientRect().top;

            if (top < window.innerHeight - 100) {

                element.classList.add("show");

            }

        });

    }

    reveal();

    window.addEventListener("scroll", reveal);

}


/*=========================================================
  STATISTICS COUNTER
=========================================================*/

function initializeStatisticsCounter() {

    const cards = document.querySelectorAll(".stat-card h3");

    if (!cards.length) return;

    let started = false;

    function animateCounter() {

        if (started) return;

        const section = document.querySelector(".statistics");

        if (!section) return;

        const top = section.getBoundingClientRect().top;

        if (top < window.innerHeight - 100) {

            started = true;

            cards.forEach(card => {

                const value = card.innerText;

                if (value === "XGBoost") return;

                let target = parseFloat(value);

                let suffix = "";

                if (value.includes("%")) suffix = "%";

                let current = 0;

                const speed = target / 80;

                const timer = setInterval(() => {

                    current += speed;

                    if (current >= target) {

                        current = target;

                        clearInterval(timer);

                    }

                    if (suffix === "%") {

                        card.innerText = current.toFixed(2) + suffix;

                    }

                    else {

                        card.innerText = Math.floor(current);

                    }

                }, 20);

            });

        }

    }

    animateCounter();

    window.addEventListener("scroll", animateCounter);

}


/*=========================================================
  HERO IMAGE ANIMATION
=========================================================*/

function initializeHeroAnimation() {

    const image = document.querySelector(".hero-image img");

    if (!image) return;

    image.addEventListener("mouseenter", () => {

        image.style.transform = "scale(1.08) rotate(2deg)";

        image.style.transition = "0.4s";

    });

    image.addEventListener("mouseleave", () => {

        image.style.transform = "scale(1) rotate(0deg)";

    });

}


/*=========================================================
  BUTTON RIPPLE EFFECT
=========================================================*/

function initializeButtonEffects() {

    const buttons = document.querySelectorAll(".btn,.btn-outline");

    buttons.forEach(button => {

        button.addEventListener("click", function () {

            this.style.transform = "scale(0.95)";

            setTimeout(() => {

                this.style.transform = "scale(1)";

            }, 150);

        });

    });

}


/*=========================================================
  BACK TO TOP BUTTON
=========================================================*/

function initializeBackToTop() {

    const button = document.createElement("button");

    button.className = "back-top";

    button.innerHTML = "↑";

    document.body.appendChild(button);

    window.addEventListener("scroll", () => {

        if (window.scrollY > 400) {

            button.classList.add("show-top");

        }

        else {

            button.classList.remove("show-top");

        }

    });

    button.addEventListener("click", () => {

        window.scrollTo({

            top: 0,

            behavior: "smooth"

        });

    });

}


/*=========================================================
  FOOTER YEAR
=========================================================*/

function updateFooterYear() {

    const copyright = document.querySelector(".copyright");

    if (!copyright) return;

    const year = new Date().getFullYear();

    copyright.innerHTML =
        `© ${year} Heart Disease Risk Prediction. All Rights Reserved.`;

}


/*=========================================================
  WINDOW RESIZE
=========================================================*/

window.addEventListener("resize", () => {

    console.log("Window resized");

});

window.addEventListener("load", () => {

    document.body.classList.add("loaded");

    console.log("Website Loaded Successfully");

});