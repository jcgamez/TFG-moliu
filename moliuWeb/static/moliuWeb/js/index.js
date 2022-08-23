'use strict'

let options = document.getElementsByClassName("menu-option");

for(let option of options) {
    ["mouseover", "touchstart"].forEach( evt =>
        option.addEventListener(evt, function() {
            this.classList.add("bg-primary");
        })
    );

    ["mouseout", "focusout", "touchend", "load"].forEach( evt =>
        option.addEventListener(evt, function() {
            this.classList.remove("bg-primary");
        })
    );
}

let logout = document.getElementById("btn-logout");

["mouseover", "touchstart"].forEach( evt =>
    logout.addEventListener(evt, function() {
        this.classList.add("bg-danger");
    })
);

["mouseout", "focusout", "touchend", "load"].forEach( evt =>
    logout.addEventListener(evt, function() {
        this.classList.remove("bg-danger");
    })
);
