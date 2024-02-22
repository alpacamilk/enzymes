document.getElementById('numPairs').addEventListener('input', function() {
    var numPairs = parseInt(this.value);
    var inputFields = '';
    maxPairs = 100;

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
