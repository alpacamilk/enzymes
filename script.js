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

    for (var i = 1; i <= numPairs; i++) {
        var x = parseFloat(document.getElementById('xInput' + i).value);
        var y = parseFloat(document.getElementById('yInput' + i).value);
        
        results += x + y;
    }

    document.getElementById('resultFields').innerHTML = "Result: " + results;
}
