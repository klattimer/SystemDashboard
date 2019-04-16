window.APP.fetch.push({
    url: '/api/network',
    key: 'network',
    interval: 10000
});

window.APP.fetch.push({
    url: '/api/radar',
    key: 'radar',
    interval: 10000
});

var traffic_config = {
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
                    callback: function(value) {
                        var ranges = [
                            { divider: 1e6, suffix: 'G' },
                            { divider: 1e6, suffix: 'M' },
                            { divider: 1e3, suffix: 'k' }
                        ];
                        function formatNumber(n) {
                            n = n / 10; // Data comes in once every 10s
                            for (var i = 0; i < ranges.length; i++) {
                               if (n >= ranges[i].divider) {
                                  return (n / ranges[i].divider).toString() + ranges[i].suffix;
                               }
                            }
                            return n;
                        }
                        return formatNumber(value) +'B/s';
                    }
                }
            }]
        },
    }
};

var radar_config = {
    type: 'radar',
    data: {
        labels: [
            "192.168.1.1 - 34ms",
            "192.168.1.11 - 88ms",
            "192.168.1.12 - 43ms",
            "192.168.1.142 - 12ms",
            "192.168.1.13 - 124ms",
            "192.168.1.8 - 152ms",
            "192.168.1.15 - 34ms",
            "192.168.1.9 - 45ms",
            "192.168.1.19 - 12ms",
            "192.168.1.21 - 144ms",
            "192.168.1.41 - 122ms",
            "192.168.1.40 - 44ms",
            "192.168.1.56 - 95ms",
        ],
        datasets: [{
            data: [
                34,
                88,
                43,
                12,
                124,
                152,
                34,
                45,
                12,
                144,
                122,
                44,
                95
            ],
            pointBackgroundColor: window.chartColors.red,
            fill: false,
            borderWidth:0,
            borderColor:"rgba(0,0,0,0)"

        }]
    },
    options: {
        legend: {
            display: false
        },
        scale: {
            // Hides the scale
            display: true,
            pointLabels: {
                // Boolean - if true, show point labels
                display: false
            }
        }
    }
}

window.APP.load.push(function() {
    labels = [];
    for (var i = 0; i < 61; i++){
        labels.push(-600 + (i * 10));
    }
    traffic_config.data.labels = labels;

    var ctx = document.getElementById('traffic-chart-area').getContext('2d');
    window.APP.charts.traffic = new Chart(ctx, traffic_config);

    var ctx = document.getElementById('radar-chart-area').getContext('2d');
    window.APP.charts.radar = new Chart(ctx, radar_config);

    window.APP.net_history = [[], []];
    window.APP.net_out_last = 0;
    window.APP.net_in_last = 0;
});

window.APP.update_funcs.push({
    interval: 10000,
    func: function () {
        try {

            var size = 61;
            var dev = Object.keys(window.APP.page_data.network.io)[0];

            var last = window.APP.net_in_last;
            if (last == 0) last = window.APP.page_data.network.io[dev].bytes_recv;
            window.APP.net_in_last = window.APP.page_data.network.io[dev].bytes_recv;
            var in_bps = (window.APP.net_in_last - last) / 10;

            last = window.APP.net_out_last;
            if (last == 0) last = window.APP.page_data.network.io[dev].bytes_sent;
            window.APP.net_out_last = window.APP.page_data.network.io[dev].bytes_sent;
            var out_bps = (window.APP.net_out_last - last) / 10;

            window.APP.net_history[0].push(in_bps);
            window.APP.net_history[1].push(out_bps);

            datasets = [];
            for (var i = 0; i < window.APP.net_history.length; i++) {
                var len = window.APP.net_history[i].length;
                if (len > size) {
                    window.APP.net_history[i] = window.APP.net_history[i].slice(len - size, len);
                } else {
                    for (var j = 0; j < size - len; j++) {
                        window.APP.net_history[i].splice(0, 0, 0);
                    }
                }
            }

            dataset = {
                data: window.APP.net_history[0],
                borderColor: window.chartColors.blue,
                pointBackgroundColor: window.chartColors.blue,
                borderWidth: 1,
                fill: false,
                pointRadius: 0,
                pointHoverRadius: 0
            };
            datasets.push(dataset);

            dataset = {
                data: window.APP.net_history[1],
                borderColor: window.chartColors.red,
                pointBackgroundColor: window.chartColors.red,
                borderWidth: 1,
                fill: false,
                pointRadius: 0,
                pointHoverRadius: 0
            };
            datasets.push(dataset);

            window.APP.charts.traffic.data.datasets = datasets;
            window.APP.charts.traffic.update();

            dataset = [];
            labels = [];
            var blips = window.APP.page_data.radar;

            for (var i = 0; i < blips.length; i++) {
                var blip = blips[i];
                var ms = blip[1] * 1000;
                var msi = parseInt(ms);
                if (msi == 0) {
                    ns = blip[1] * 1000000;
                    nsi = parseInt(ns)
                    time = ns + 'ns';
                } else {
                    time = ms + 'ms';
                }
                dataset.push(blip[1]);
                labels.push(blip[0]); // + ',  ' + time)
            }

            window.APP.charts.radar.data.datasets[0].data = dataset;
            window.APP.charts.radar.data.labels = labels;
            window.APP.charts.radar.update();
        } catch (e) {

            console.log("Error on: network\n", e);

        }
    }
});
