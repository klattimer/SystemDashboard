
var cpu_config = {
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
                    min: -60,
                    stepSize: 10,
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
        labels.push(-60 + i);
    }
    cpu_config.data.labels = labels;
    var ctx = document.getElementById('cpu-chart-area').getContext('2d');
    window.APP.charts.cpu = new Chart(ctx, cpu_config);

    window.APP.cpu_history = [];
    var cpud = window.APP.page_data.cpu;
    for (var i = 0; i < cpud.cpu_percent.length;i++) {
        window.APP.cpu_history.push([]);
    }
});

window.APP.update_funcs.push({
    interval: 1000,
    func: function () {
        try {
            var size = 61;
            var cpud = window.APP.page_data.cpu;
            var datasets = [];
            for (var i = 0; i < cpud.cpu_percent.length;i++) {
                var pc = cpud.cpu_percent[i];
                window.APP.cpu_history[i].push(pc);
                var len = window.APP.cpu_history[i].length;
                if (len > size) {
                    window.APP.cpu_history[i] = window.APP.cpu_history[i].slice(len - size, len);
                } else {
                    for (var j = 0; j < size - len; j++) {
                        window.APP.cpu_history[i].splice(0, 0, 0);
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
                ];
                var c = k[i % k.length];
                dataset = {
                    data: window.APP.cpu_history[i],
                    borderColor: c,
                    pointBackgroundColor: c,
                    borderWidth: 1,
                    fill: false,
                    pointRadius: 0,
                    pointHoverRadius: 0
                };
                datasets.push(dataset);
            }
            window.APP.charts.cpu.data.datasets = datasets;
            window.APP.charts.cpu.update();

        } catch (e) {

            console.log("Error on: load\n", e);

        }
    }
});
