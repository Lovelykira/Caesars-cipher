window.onload = function () {
    this.send = function (method, url, callback, data) {
        var xhr = new XMLHttpRequest();
        xhr.open(method, url, true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader("X-CSRFToken", document.getElementsByName('csrfmiddlewaretoken')[0].value);
        xhr.send(JSON.stringify(data));
        xhr.onreadystatechange = function () {
            if (xhr.readyState != 4) return;
            if (xhr.status != 200) {
                alert(xhr.status + ': ' + xhr.statusText);
            } else {
                callback(JSON.parse(xhr.responseText));
            }
        }
    };


    this.encrypt = function (encryption) {
        var text = document.getElementById('origin_text').value;
        var offset = document.getElementById('offset').value;

        this.send('POST', '', function (response) {
            document.getElementById('result_text').value = response.result_text;
            var PredictionDiv = document.getElementById('prediction');
            if(!response.encryption) {
                if (response.prediction == 'a') {
                    PredictionDiv.innerHTML = "Most likely the text is not encrypted";
                }
                else {
                    PredictionDiv.innerHTML = "It seems that the text is encrypted.\nThe encryption bias can be: " + response.prediction;
                }
            }
            else{
                PredictionDiv.innerHTML = "Try to decrypt the text";
            }
            this.addHistory(response);
        }, {original_text: text, offset: offset, encryption: encryption});

    };


    this.getHistory = function () {
        this.send('GET', 'history/', function (response) {
            response.histories.reverse().forEach(function (history) {
                this.addHistory(history);
            })
        })
    };


    this.addHistory = function (history) {
        var history_div = document.getElementById('history');
        div = document.createElement('div');
        div.className = 'row history';
        div.onclick = function () {
            document.getElementById('origin_text').value = history.original_text;
            document.getElementById('result_text').value = history.result_text;
            document.getElementById('offset').value = history.offset;
            document.getElementById('prediction').innerHTML = "Try to decrypt the text";
            draw_diagram();
        };
        var d = new Date(Date.parse(history.created_at));
        history.created_at = d.toLocaleString('ru');
        div.innerHTML = ''.concat(history.id, ' ', history.created_at, ' ', history.offset);
        history_div.insertBefore(div, history_div.children[0]);
        if(history_div.children.length > 15) {
            history_div.removeChild(history_div.children[15]);
        }
    };


    this.getHistory();


    this.generateAlphabet = function () {
        var alphabet = [];
        var startLetter = 'a';
        var endLetter = 'z';
        while (true) {
            alphabet.push(startLetter);
            startLetter = String.fromCharCode(startLetter.charCodeAt(0) + 1);
            if (startLetter == endLetter) {
                alphabet.push(endLetter);
                break;
            }
        }
        var select = document.getElementById('offset');
        var option;
        alphabet.forEach(function (char) {
            option = document.createElement('option');
            option.text = char;
            option.value = char;
            select.appendChild(option);
        })
    };


    this.generateAlphabet();


    this.draw_diagram = function() {
        if(google) {
            google.load('visualization', '1.0', {
                packages: ['corechart'],
                callback: function () {
                    var alphabet = this.generateAlphabet;
                    var text = document.getElementById("origin_text").value;
                     var diagram = document.getElementById('diagram');
                    this.send('POST', 'diagram', function (response) {
                        var chart = new google.visualization.ColumnChart(diagram);
                        var data = google.visualization.arrayToDataTable(response.return_data);
                        if (data.Gf.length != 0) {
                            diagram.style.display = 'block';
                            chart.draw(data, response.return_options);
                        }
                        else
                        {
                            diagram.style.display = 'none';
                        }

                    }, {text: text});}
            })
         }
    };
};