

var memory_config = {
    type: 'line',
    data: {
        datasets: [],
        labels: []
    },
    options: {
        tooltips: {
            enabled: false
        },
        hover: {mode: null},
        animation: false,
        legend: {
            display: false
        },
        scales: {
            yAxes: [{
                stacked: true,
                gridLines: {
                    drawTicks: true
                },
                display: true,
                ticks: {
                    beginAtZero: true,
                    max: 100,
                    min: 0,
                    stepSize: 25,
                    callback: function(value) {
                        return value + '%';
                    }
                }
            }],
            xAxis: [{
                ticks: {
                    beginAtZero: true,
                    max: 0,
                    min: -600,
                    stepSize: 100,
                    callback: function(value) {
                        return value + 's';
                    }
                }
            }]
        },
    }
};

window.APP.load.push(function (event) {
    labels = [];
    for (var i = 0; i < 61; i++){
        labels.push(-600 + (i * 10));
    }
    memory_config.data.labels = labels;
    var ctx = document.getElementById('memory-chart-area').getContext('2d');
    window.APP.charts.memory = new Chart(ctx, memory_config);

    window.APP.memory_history = [];
});


window.APP.update_funcs.push({
    interval: 10000,
    func: function () {
        try {

            var size = 61;
            var cpud = window.APP.page_data.cpu;

            s = cpud.memory.used / cpud.memory.total;
            s = parseInt(s * 100);
            window.APP.memory_history.push(s);
            var len = window.APP.memory_history.length;
            if (len > size) {
                window.APP.memory_history = window.APP.memory_history.slice(len - size, len);
            } else {
                for (var j = 0; j < size - len; j++) {
                    window.APP.memory_history.splice(0, 0, 0);
                }
            }
            dataset = {
                data: window.APP.memory_history,
                borderColor: getRootVar("--color-orange"),
                pointBackgroundColor: getRootVar("--color-orange"),
                borderWidth: 1,
                fill: true,
                backgroundColor: getRootVar("--color-yellow"),
                pointRadius: 0,
                pointHoverRadius: 0
            };
            window.APP.charts.memory.data.datasets = [dataset];
            window.APP.charts.memory.update();

        } catch (e) {

            $('#sensors').find('tbody').html('<tr><td colspan="3" style="text-align:center;">An Error Occurred!</td></tr>');

            console.log("Error on: load\n", e);

        }

    }
});
