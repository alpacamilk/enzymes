document.getElementById('numPairs').addEventListener('input', function() {
    var numPairs = parseInt(this.value);
    var inputFields = '';
    var maxPairs = 100;

    if (numPairs > maxPairs) {
        alert(`Please enter a number less than or equal to ${maxPairs}`);
        this.value = maxPairs;
        numPairs = maxPairs;
    }

    for (var i = 1; i <= numPairs; i++) {
        inputFields += `
            <label for="xInput${i}">X:</label>
            <input type="number" id="xInput${i}">
            <label for="yInput${i}">Y:</label>
            <input type="number" id="yInput${i}"><br><br>
        `;
    }

    document.getElementById('inputFields').innerHTML = inputFields;
});

function generate() {
    var numPairs = parseInt(document.getElementById('numPairs').value);
    var results = 0;
    var xInput = document.getElementById("x1").value;
    var yInput = document.getElementById("y1").value;
    var gInput = document.getElementById("g1").value;

    for (var i = 1; i <= numPairs; i++) {
        var x = parseFloat(document.getElementById('xInput' + i).value);
        var y = parseFloat(document.getElementById('yInput' + i).value);
        
        results += x + y;
    }

    document.getElementById('resultFields').innerHTML = "Result: " + results;
    document.getElementById('xName').innerHTML = "X-Axis Name: " + xInput;
    document.getElementById('yName').innerHTML = "Y-Axis Name: " + yInput;
    document.getElementById('gName').innerHTML = "Graph Name: " + gInput;
}
