window.APP.fetch.push({
    url: '/api/loadave',
    key: 'loadave',
    interval: 10000,
});


var cpu_config = {
    type: 'line',
    data: {
        datasets: [],
        labels: []
    },
    options: {
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

var memory_config = {
    type: 'line',
    data: {
        datasets: [],
        labels: []
    },
    options: {
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

var load_config = {
    type: 'line',
    data: {
        datasets: [],
        labels: []
    },
    options: {
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

    labels = [];
    for (var i = 0; i < 61; i++){
        labels.push(-600 + (i * 10));
    }
    memory_config.data.labels = labels;
    var ctx = document.getElementById('memory-chart-area').getContext('2d');
    window.APP.charts.memory = new Chart(ctx, memory_config);

    window.APP.memory_history = [];

    load_config.data.labels = labels;
    var ctx = document.getElementById('load-chart-area').getContext('2d');
    window.APP.charts.load = new Chart(ctx, load_config);

    window.APP.load_history = [[], [], []];
});


window.APP.update_funcs.push({
    interval: 10000,
    func: function () {
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
            borderColor: window.chartColors.orange,
            pointBackgroundColor: window.chartColors.orange,
            borderWidth: 1,
            fill: true,
            backgroundColor: window.chartColors.yellow,
            pointRadius: 0,
            pointHoverRadius: 0
        };
        window.APP.charts.memory.data.datasets = [dataset];
        window.APP.charts.memory.update();
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

            k = Object.keys(window.chartColors);
            var c = window.chartColors[k[i % k.length]];
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

        $('#sensors').find('tbody').html('');

        for (var i = 0; i < Object.keys(window.APP.page_data.cpu.temperatures).length; i++) {
            var k = Object.keys(window.APP.page_data.cpu.temperatures)[i];
            var v = window.APP.page_data.cpu.temperatures[k];
            for (var j = 0; j < v.length; j++) {
                var t = v[j];
                var name = k + " " + j;
                if (t.label.length > 0) {
                    name = t.label;
                }
                var state = '<i class="fas fa-circle status-blue"></i>';
                if (t.current > t.high) {
                    state = '<i class="fas fa-circle status-orange"></i>';
                }
                if (t.current > t.critical) {
                    state = '<i class="fas fa-circle status-red"></i>';
                }

                var row = '<tr><td>'+name+'</td><td>'+t.current+'&deg;C</td><td class="narrow">'+state+'</td></tr>';
                $('#sensors').find('tbody').append(row);
            }
        }
    }
});

window.APP.update_funcs.push({
    interval: 1000,
    func: function () {
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
            k = Object.keys(window.chartColors);
            var c = window.chartColors[k[i % k.length]];
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
    }
});
