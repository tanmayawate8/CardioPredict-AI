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

    initializeThemeToggle();
    initializeNavigation();
    initializeMobileMenu();
    initializeSmoothScroll();
    initializeScrollAnimation();
    initializeStatisticsCounter();
    initializeHeroAnimation();
    initializeButtonEffects();
    initializeBackToTop();
    updateFooterYear();

});


/*=========================================================
  DARK / LIGHT THEME TOGGLE
=========================================================*/

function initializeThemeToggle() {

    const toggle = document.getElementById("theme-toggle");

    if (!toggle) return;

    const icon = toggle.querySelector("i");

    function setIcon(theme) {

        if (!icon) return;

        icon.className = theme === "dark" ? "fa-solid fa-sun" : "fa-solid fa-moon";

    }

    // Reflect whatever the anti-flash inline script already set
    const currentTheme = document.documentElement.getAttribute("data-theme") || "light";

    setIcon(currentTheme);

    toggle.addEventListener("click", () => {

        const html = document.documentElement;

        const isDark = html.getAttribute("data-theme") === "dark";

        const nextTheme = isDark ? "light" : "dark";

        html.setAttribute("data-theme", nextTheme);

        localStorage.setItem("theme", nextTheme);

        setIcon(nextTheme);

    });

}


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
  MOBILE MENU TOGGLE
=========================================================*/

function initializeMobileMenu() {

    const toggle = document.querySelector(".menu-toggle");
    const navLinks = document.querySelector(".nav-links");

    if (!toggle || !navLinks) return;

    toggle.addEventListener("click", () => {

        navLinks.classList.toggle("active");

    });

    // Close the menu whenever a nav link is tapped
    navLinks.querySelectorAll("a").forEach(link => {

        link.addEventListener("click", () => {

            navLinks.classList.remove("active");

        });

    });

    // Close the menu if the viewport is resized back to desktop width
    window.addEventListener("resize", () => {

        if (window.innerWidth > 768) {

            navLinks.classList.remove("active");

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