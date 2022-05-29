'use strict'

let options = document.getElementsByClassName("menu-option");

for(let option of options) {
    option.addEventListener("mouseover", function() {
    this.classList.add("bg-primary");
    });

    option.addEventListener("touchstart", function() {
    this.classList.add("bg-primary");
    });

    option.addEventListener("mouseout", function() {
    this.classList.remove("bg-primary");
    });

    option.addEventListener("focusout", function() {
    this.classList.remove("bg-primary");
    });

    option.addEventListener("touchend", function() {
    this.classList.remove("bg-primary");
    });

    option.addEventListener("load", function() {
    this.classList.remove("bg-primary");
    });
}

let logout = document.getElementById("btn-logout");

logout.addEventListener("mouseover", function() {
    this.classList.add("bg-danger");
});

logout.addEventListener("touchstart", function() {
    this.classList.add("bg-danger");
});

logout.addEventListener("mouseout", function() {
    this.classList.remove("bg-danger");
});

logout.addEventListener("focusout", function() {
    this.classList.remove("bg-danger");
});

logout.addEventListener("touchend", function() {
    this.classList.remove("bg-danger");
});

logout.addEventListener("load", function() {
    this.classList.remove("bg-primary");
});