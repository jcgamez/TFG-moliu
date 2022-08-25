"use strict";


// VARIABLES DECLARATION //
class Point {
    constructor(x, y, duration, number) {
        this.x = x;
        this.y = y;
        this.duration = duration;
        this.number = number;
    }
}

const Points = []; // Same as new Array()
const pointSize = 10;
let numberOfPoints = 0;
let defaultDuration = 5;
let isBackgroundSelected = false;
let isShapeSelected = false;
let isShowingItems = true;

const backgroundImage = document.getElementById("background");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const pointsTable = document.getElementById("points");
const addActivityForm = document.getElementsByTagName("form")[0];
const sendFormButton = document.getElementById("sendForm");
const selectBackgroundButton = document.getElementById("selectBackground");
const selectShapeButton = document.getElementById("selectShape");
const selectMusicButton = document.getElementById("selectMusic");
const showItemsButton = document.getElementById("showItems");
const shapesDiv = document.getElementById("shapes");
const backgroundsDiv = document.getElementById("backgrounds");
const musicDiv = document.getElementById("music");
const selectedShape = document.getElementById("selectedShape");
const selectedBackground = document.getElementById("selectedBackground");
const selectedMusic = document.getElementById("selectedMusic");

const backgroundInput = document.getElementById("id_background");
const pointsJSONInput = document.getElementById("id_points");


// MAIN CODE //
backgroundImage.style.backgroundSize = "cover";
backgroundImage.style.backgroundImage = "url('https://images3.alphacoders.com/855/85585.jpg')";
backgroundImage.style.cursor = "crosshair";

canvas.style.width = "100%";
canvas.style.height = "100%";
canvas.width = canvas.offsetWidth;
canvas.height = canvas.offsetHeight;

canvas.addEventListener("click", function(e) {
    const [x, y] = getPosition(e);
    numberOfPoints++;

    drawPoint(x, y);
    addPoint(x, y);
});

function getPosition(event) {
    let rect = canvas.getBoundingClientRect();
    let x = event.clientX - rect.left;
    let y = event.clientY - rect.top;

    return [x, y];
}

function drawPoint(x,y) {
    ctx.fillStyle = "#ff2626";

    ctx.beginPath();
    ctx.arc(x, y, pointSize, 0, Math.PI * 2, true);
    ctx.fill();
}

function drawPoints() {
    for(let i=0; i<Points.length; i++)
        drawPoint(Points[i].x, Points[i].y);
}

function addPoint(x, y) {
    Points.push(new Point(x, y, defaultDuration, numberOfPoints));
    addPointToTable(x, y);
}

function addPointToTable(x, y, duration=defaultDuration, number=numberOfPoints) {
    let newRow = pointsTable.insertRow(number);

    let pointNumberCell = newRow.insertCell(0);
    let coordinatesCell = newRow.insertCell(1);
    let pointDurationCell = newRow.insertCell(2);
    let deletePointCell = newRow.insertCell(3);

    pointNumberCell.innerHTML = number;
    pointNumberCell.setAttribute("contenteditable", "true");
    addInteractiveClasses(pointNumberCell);
    // To not call the function during addEventListener, bind() method has to be used
    pointNumberCell.addEventListener("blur", changePointNumber.bind(this, pointNumberCell, newRow));

    coordinatesCell.innerHTML = Math.round(x) + ", " + Math.round(y);

    pointDurationCell.innerHTML = duration;
    pointDurationCell.setAttribute("contenteditable", "true");
    addInteractiveClasses(pointDurationCell);
    pointDurationCell.addEventListener("blur", changeDuration.bind(this, pointDurationCell, newRow));

    deletePointCell.innerHTML = "<span style=\"cursor: pointer\" class=\"badge bg-danger deletePoint\">Eliminar</span>";
    deletePointCell.firstChild.addEventListener("click", deletePoint.bind(this, newRow));
}

function changePointNumber(numberCell, row) {
    let oldPoint = Points[row.rowIndex-1];
    let oldNumber = oldPoint.number;
    let newNumber = Number(numberCell.innerText);
    let newPoint = new Point(oldPoint.x, oldPoint.y, oldPoint.duration, newNumber);

    let rows = pointsTable.rows;
    let numberOfRows = rows.length;

    if(newNumber === oldNumber)
        return;

    if(isNaN(newNumber) || newNumber <= 0) {
        window.alert("El valor debe ser un número entero mayor que 0.");
        numberCell.innerText = oldNumber;
        return;
    }

    if(newNumber > numberOfPoints)
        newNumber = numberOfPoints;

    // Delete row with oldNumber
    deletePoint(row);

    // Add row to table at position newNumber
    addPointToTable(oldPoint.x, oldPoint.y, oldPoint.duration, newNumber);
    numberOfPoints++;

    // Add point to array at position newNumber
    Points.splice(newNumber-1, 0, newPoint);

    // Update following points in table and array
    for(let i=newNumber+1; i<numberOfRows; i++) {
        rows[i].firstChild.innerHTML = Number(rows[i].firstChild.innerText) + 1;
        Points[i-1].number += 1;
    }

    drawPoints();
}

function changeDuration(durationCell, row) {
    let newDuration = Number(durationCell.innerText.trim());

    if(isNaN(newDuration) || newDuration <= 0) {
        window.alert("La duración debe ser un número entero mayor que 0.");
        durationCell.innerText = Points[row.rowIndex-1].duration;
    } else {
        Points[row.rowIndex-1].duration = newDuration;
        durationCell.innerText = newDuration;
    }
}

function addInteractiveClasses(element) {
    ["mouseover","touchstart"].forEach( evt =>
        element.addEventListener(evt, function() {
            this.classList.add("bg-primary");
        })
    );

    element.addEventListener("focusin", function() {
        this.classList.remove("bg-primary");
        this.classList.add("bg-lightblue");
    });

    ["mouseout", "touchend", "load"].forEach( evt =>
        element.addEventListener(evt, function() {
            this.classList.remove("bg-primary");
        })
    );

    ["focusout", "load"].forEach( evt =>
        element.addEventListener(evt, function() {
            this.classList.remove("bg-lightblue");
        })
    );
}

function deletePoint(row) {
    let rows = pointsTable.rows;
    let numberOfRows = rows.length;
    let rowIndex = row.rowIndex;

    for(let i=rowIndex+1; i<numberOfRows; i++) {
        rows[i].firstChild.innerHTML -= 1;
        Points[i-1].number -= 1;
    }

    Points.splice(rowIndex-1, 1);
    numberOfPoints--;
    pointsTable.deleteRow(rowIndex);

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    drawPoints();
}

sendFormButton.addEventListener("click", function() {
    if(Points.length === 0)
        pointsJSONInput.value = "";
    else pointsJSONInput.value = JSON.stringify(Points);
});

selectShapeButton.addEventListener("click", function() {
    shapesDiv.style.display = "block";
    backgroundsDiv.style.display = "none";
    musicDiv.style.display = "none";

    if(!isShowingItems)
        showItemsButton.click();
});

selectBackgroundButton.addEventListener("click", function() {
    backgroundsDiv.style.display = "block";
    shapesDiv.style.display = "none";
    musicDiv.style.display = "none";

    if(!isShowingItems)
        showItemsButton.click();
});

selectMusicButton.addEventListener("click", function() {
    musicDiv.style.display = "block";
    shapesDiv.style.display = "none";
    backgroundsDiv.style.display = "none";

    if(!isShowingItems) {
        showItemsButton.click();
    }

});

showItemsButton.addEventListener("click", function() {
    if(isShowingItems) {
        this.style.display  = "none";
        isShowingItems = false;
    } else {
        this.style.display  = "inline-block";
        isShowingItems = true;
    }
});

window.onload = () => {
    showItemsButton.click();
    pointsJSONInput.value = "";
};

function changeShape(shape) {
    console.log(shape);
}


function changeBackground(newBackground) {
    backgroundImage.style.backgroundImage = "url("+ newBackground + ")";
    selectedBackground.value = newBackground;

    let backgroundName = newBackground.split("/")[newBackground.split("/").length-1];
    selectedBackground.value = backgroundName;

    backgroundInput.value = newBackground;
}

function changeMusic() {
}
