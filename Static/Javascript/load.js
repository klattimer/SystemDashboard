window.APP.fetch.push({
    url: '/api/loadave',
    key: 'loadave',
    interval: 10000,
});


var load_config = {
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
                gridLines: {
                    drawTicks: true
                },
                display: true,
                ticks: {
                    beginAtZero: true
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

    load_config.data.labels = labels;
    var ctx = document.getElementById('loadave-chart-area').getContext('2d');
    window.APP.charts.load = new Chart(ctx, load_config);

    window.APP.load_history = [[], [], []];
});


window.APP.update_funcs.push({
    interval: 10000,
    func: function () {
        try {

            var size = 61;
            window.APP.load_history[0].push(window.APP.page_data.loadave["1"]);
            window.APP.load_history[1].push(window.APP.page_data.loadave["5"]);
            window.APP.load_history[2].push(window.APP.page_data.loadave["15"]);

            datasets = [];
            for (var i = 0; i < window.APP.load_history.length; i++) {
                var len = window.APP.load_history[i].length;
                if (len > size) {
                    window.APP.load_history[i] = window.APP.load_history[i].slice(len - size, len);
                } else {
                    for (var j = 0; j < size - len; j++) {
                        window.APP.load_history[i].splice(0, 0, 0);
                    }
                }

                k = [
                    getRootVar("--color-red"),
                    getRootVar("--color-orange"),
                    getRootVar("--color-yellow"),
                    getRootVar("--color-green"),
                    getRootVar("--color-blue"),
                    getRootVar("--color-purple"),
                    getRootVar("--color-grey"),
                    getRootVar("--color-pink")
                ]
                var c = k[i % k.length];
                dataset = {
                    data: window.APP.load_history[i],
                    borderColor: c,
                    pointBackgroundColor: c,
                    borderWidth: 1,
                    fill: true,
                    backgroundColor: c,
                    pointRadius: 0,
                    pointHoverRadius: 0
                };
                datasets.push(dataset);
            }
            window.APP.charts.load.data.datasets = datasets;
            window.APP.charts.load.update();

        } catch (e) {

            $('#sensors').find('tbody').html('<tr><td colspan="3" style="text-align:center;">An Error Occurred!</td></tr>');

            console.log("Error on: load\n", e);

        }

    }
});
