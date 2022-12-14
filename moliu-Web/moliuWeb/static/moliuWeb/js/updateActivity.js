"use strict";


// VARIABLES DECLARATION //
class Point {
    constructor(x, y, duration, number, shape) {
        this.x = x;
        this.y = y;
        this.duration = duration;
        this.number = number;
        this.shape = shape;
    }
}

class PointUtils {
    constructor(canvasX, canvasY, shapeImg) {
        this.canvasX = canvasX;
        this.canvasY = canvasY;
        this.shapeImg = shapeImg;
    }
}

const Points = []; // Same as new Array()
const PointsUtils  = [];
// const Shapes = Array.from(document.getElementsByClassName("shape-item"));
const pointSize = 20;
const imagePointWidth = 50;
const defaultScreenWidth = 1920;
const defaultScreenHeight = 1080;

let numberOfPoints = 0;
let defaultDuration = 5;
// let isBackgroundSelected = false;
// let isShapeSelected = false;
let isShowingItems = true;
let currentShapePath = "";
let currentShapeImage = "";

const backgroundImage = document.getElementById("background");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const pointsTable = document.getElementById("points");
const pointsTableDiv = document.getElementById("pointsTableDiv")
// const addActivityForm = document.getElementsByTagName("form")[0];
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
const musicInput = document.getElementById("id_music");
const pointsJSONInput = document.getElementById("id_points");


// MAIN CODE //
backgroundImage.style.backgroundSize = "cover";

canvas.style.width = "100%";
canvas.style.height = "100%";
canvas.width = canvas.offsetWidth;
canvas.height = canvas.offsetHeight;
canvas.style.cursor = "crosshair";

canvas.addEventListener("click", function(e) {
    const [x, y] = getPosition(e);
    numberOfPoints++;

    drawPoint(x, y, currentShapeImage);
    addPoint(x, y);
    pointsTableDiv.scrollTo(0, pointsTable.offsetHeight);
});

function getPosition(event) {
    let rect = canvas.getBoundingClientRect();
    let x = event.clientX - rect.left;
    let y = event.clientY - rect.top;

    return [x, y];
}

function drawPoint(x,y, shape="") {
    if(shape === "") {
        // Red
        // ctx.fillStyle = "#ff2626";
        ctx.fillStyle = "#ffffff";

        ctx.beginPath();
        ctx.arc(x, y, pointSize, 0, Math.PI * 2, true);
        ctx.fill();
    } else {
        let scaledHeight = imagePointWidth*shape.height/shape.width;
        let centeredX = x - imagePointWidth/2;
        let centeredY = y - scaledHeight/2;
        ctx.drawImage(shape, centeredX, centeredY, imagePointWidth, scaledHeight);
    }
}

function drawPoints() {
    for(let i=0; i<PointsUtils.length; i++)
        drawPoint(PointsUtils[i].canvasX, PointsUtils[i].canvasY, PointsUtils[i].shapeImg);
}

function addPoint(x, y) {
    let scaledX = (x * defaultScreenWidth / canvas.width).toFixed(2);
    let scaledY = (y * defaultScreenHeight / canvas.height).toFixed(2);

    if (scaledX < 0)
        scaledX = 0;
    if (scaledX > defaultScreenWidth)
        scaledX = defaultScreenWidth;

    if (scaledY < 0)
        scaledY = 0;
    if (scaledY > defaultScreenHeight)
        scaledY = defaultScreenHeight;

    PointsUtils.push(new PointUtils(x, y, currentShapeImage));
    Points.push(new Point(scaledX, scaledY, defaultDuration, numberOfPoints, currentShapePath));
    addPointToTable(scaledX, scaledY);
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
    let oldPointUtils = PointsUtils[row.rowIndex-1];
    let oldNumber = oldPoint.number;
    let newNumber = Number(numberCell.innerText);
    let newPoint = new Point(oldPoint.x, oldPoint.y, oldPoint.duration, newNumber, oldPoint.shape);
    let newPointUtils = new PointUtils(oldPointUtils.canvasX, oldPointUtils.canvasY, oldPointUtils.shapeImg);

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
    PointsUtils.splice(newNumber-1, 0, newPointUtils);

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
    PointsUtils.splice(rowIndex-1, 1);
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

    reloadPoints(JSON.parse(pointsJSONInput.value));
    reloadBackground(backgroundInput.value);
    reloadMusic(musicInput.value);

    const pointsDiv = document.getElementById("pointsDiv");

    if (backgroundImage.clientHeight >= 300)
        pointsDiv.style.height = String(backgroundImage.clientHeight) + "px";
    else pointsDiv.style.height = "300px";
};

function changeShape(shape, shapeId) {
    currentShapePath = shape;
    currentShapeImage = document.getElementById(shapeId);
    selectedShape.value = shape.split("/")[shape.split("/").length-1];
}

function changeBackground(newBackground) {
    backgroundImage.style.backgroundImage = "url("+ newBackground + ")";
    selectedBackground.value = newBackground;

    let backgroundName = newBackground.split("/")[newBackground.split("/").length-1];
    selectedBackground.value = backgroundName;

    backgroundInput.value = newBackground;
}

function changeMusic(newMusic) {
    let songName = newMusic.split("/")[newMusic.split("/").length-1];
    selectedMusic.value = songName;
    musicInput.value = newMusic;
}

function reloadPoints(points) {
    const Shapes = Array.from(document.getElementsByClassName("shape-item"));

    for(let i=0; i<points.length; i++) {
        numberOfPoints++;
        let shapeImage = "";

        let unscaledX = points[i].x * canvas.width / defaultScreenWidth;
        let unscaledY = points[i].y * canvas.height / defaultScreenHeight;

        for(let j=0; j<Shapes.length; j++) {
            if (Shapes[j].getAttribute("src") === points[i].shape) {
                shapeImage = Shapes[j];
                break;
            }
        }

        PointsUtils.push(new PointUtils(unscaledX, unscaledY, shapeImage));

        if(shapeImage === "")
            Points.push(new Point(points[i].x, points[i].y, points[i].duration, numberOfPoints, ""));
        else Points.push(new Point(points[i].x, points[i].y, points[i].duration, numberOfPoints, points[i].shape));

        addPointToTable(points[i].x, points[i].y, points[i].duration);
        drawPoint(PointsUtils[i].canvasX, PointsUtils[i].canvasY, PointsUtils[i].shapeImg);
    }
}

function reloadBackground(background) {
    const Backgrounds = Array.from(document.getElementsByClassName("background-item"));

    for(let i=0; i<Backgrounds.length; i++) {
        if (Backgrounds[i].getAttribute("src") === background) {
            backgroundImage.style.backgroundImage = "url("+ background + ")";
            break;
        }
    }

    let backgroundName = background.split("/")[background.split("/").length-1];
    selectedBackground.value = backgroundName;
}

function reloadMusic(music) {
    const Music = Array.from(document.getElementsByClassName("music-item"));
    let songName = "";

    for(let i=0; i<Music.length; i++) {
        if (Music[i].getAttribute("src") === music) {
            songName = music.split("/")[music.split("/").length-1];
            break;
        }
    }

    selectedMusic.value = songName;
}