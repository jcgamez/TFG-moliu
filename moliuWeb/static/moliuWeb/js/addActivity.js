'use strict';


// VARIABLES DECLARATION //
class Point {
    constructor(x, y, duration, order) {
        this.x = x;
        this.y = y;
        this.duration = duration;
        this.order = order;
    }
}

const Points = []; // Same as new Array()
const pointSize = 10;
let pointsNumber = 0;
let pointDuration = 5;
let isBackgroundSelected = false;
let isShapeSelected = false;

const backgroundImage = document.getElementById("background");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const pointsTable = document.getElementById("points");


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
    pointsNumber++;

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

function addPoint(x, y) {
    let newRow = pointsTable.insertRow();

    let pointNumberCell = newRow.insertCell(0);
    let coordinatesCell = newRow.insertCell(1);
    let pointDurationCell = newRow.insertCell(2);
    let deletePointCell = newRow.insertCell(3);

    Points.push(new Point(x, y, pointDuration, pointsNumber));

    pointNumberCell.innerHTML = pointsNumber;
    pointNumberCell.setAttribute("contenteditable", "true");

    coordinatesCell.innerHTML = Math.round(x) + ", " + Math.round(y);

    pointDurationCell.innerHTML = pointDuration;
    pointDurationCell.setAttribute("contenteditable", "true");

    deletePointCell.innerHTML = "<span style=\"cursor: pointer\" class=\"badge bg-danger deletePoint\">Eliminar</span>";
    // To not call the function during addEventListener, bind() method has to be used
    deletePointCell.firstChild.addEventListener("click", deletePoint.bind(this, newRow));
}

function deletePoint(row) {
    let rows = pointsTable.rows;
    let numberOfRows = rows.length;
    let rowIndex = row.rowIndex;

    Points.splice(rowIndex-1, 1);

    for(let i=rowIndex+1; i<numberOfRows; i++)
        rows[i].firstChild.innerHTML -= 1;

    pointsTable.deleteRow(rowIndex);
    pointsNumber--;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for(let i=0; i<Points.length; i++)
        drawPoint(Points[i].x, Points[i].y);
}