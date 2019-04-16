window.APP.fetch.push({
    url: '/api/overview',
    key: 'overview',
    interval: 60000
});

window.APP.fetch.push({
    url: '/api/cpu',
    key: 'cpu',
    interval: 1000
});

var overview_chart_config = {
    type: 'bar',
    data: {
        datasets: [{
            data: [
                4,
                22,
                2,
            ],
            backgroundColor: [
                window.chartColors.orange,
                window.chartColors.green,
                window.chartColors.yellow
            ]
        },
        {
            data: [
                4,
                22,
                2,
            ],
            backgroundColor: [
                window.chartColors.yellow,
                window.chartColors.orange,
                window.chartColors.green
            ]
        }],
        labels: [
            'CPU',
            'Memory',
            'Swap'
        ]
    },
    options: {
        animation: false,
        legend: {
            display: false
        },
        scales: {
            xAxes: [{
                stacked: true
            }],
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
                    stepSize: 25
                }
            }]
        },
    }
};

window.APP.load.push(function (event) {
    var ctx = document.getElementById('overview-chart-area').getContext('2d');
	window.APP.charts.overview = new Chart(ctx, overview_chart_config);
});

window.APP.update_funcs.push({
    interval: 1000,
    func: function () {
        try {
            var cpud = window.APP.page_data.cpu;
            var cpu_data = [];
            for (var i = 0; i < cpud.cpu_percent.length;i++) {
                var pc = (cpud.cpu_percent[i] / (100.0 * cpud.cpu_percent.length)) * 100.0;
                cpu_data.push(pc);
            };
            s = cpud.swap.used / cpud.swap.total;
            s = parseInt(s * 100);
            f = 100 - s;
            swap_data = [s];

            s = cpud.memory.used / cpud.memory.total;
            s = parseInt(s * 100);
            f = 100 - s;
            memory_data = [s];

            t = Math.max(cpu_data.length, swap_data.length, memory_data.length);

            if (swap_data.length < t) {
                for (var i = 0; i < t - swap_data.length + 1;i++) {
                    swap_data.push(0);
                }
            }
            if (memory_data.length < t) {
                for (var i = 0; i < t - memory_data.length + 1;i++) {
                    memory_data.push(0);
                }
            }
            if (cpu_data.length < t) {
                for (var i = 0; i < t - cpu_data.length + 1;i++) {
                    cpu_data.push(0);
                }
            }
            var new_datasets = [];
            for (var i = 0; i < t; i++) {
                var d = [];
                d.push(cpu_data[i]);
                d.push(memory_data[i]);
                d.push(swap_data[i]);
                var c = [];

                k = Object.keys(window.chartColors);
                var c = [
                            window.chartColors[k[i % k.length]] ,
                            window.chartColors[k[(i+1) % k.length]],
                            window.chartColors[k[(i+2) % k.length]],
                        ];

                new_datasets.push({data:d, backgroundColor: c});
            }
            window.APP.charts.overview.data.datasets = new_datasets;
            window.APP.charts.overview.update();
        } catch (e) {

            console.log("Error on: overview\n", e);

        }
    }
});

window.APP.update_funcs.push({
    interval: 60000,
    func: function () {
        try {

            var ovd = window.APP.page_data.overview;
            var cpud = window.APP.page_data.cpu;

            $('.overview-cpu').html(ovd.cpus.cpus + ' x ' + ovd.cpus.type);
            $('.overview-platform').html(ovd.osname || 'Not Available');
            $('.overview-kernel').html(ovd.kernel || 'Not Available');
            $('.overview-uptime').html(ovd.uptime || 'Not Available');
            $('.overview-hostname').html(ovd.hostname || 'Not Available');
            $('.overview-ip').html(ovd.primary_ip || 'Not Available');

        } catch (e) {

            console.log("Error on: overview\n", e);

        }
    }
});
