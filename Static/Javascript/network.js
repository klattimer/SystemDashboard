window.APP.fetch.push({
    url: '/api/network',
    key: 'network',
    interval: 10000
});

var traffic_config = {
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
                    callback: function(value) {
                        var ranges = [
                            { divider: 1e9, suffix: 'G' },
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


window.APP.load.push(function() {
    labels = [];
    for (var i = 0; i < 61; i++){
        labels.push(-600 + (i * 10));
    }
    traffic_config.data.labels = labels;

    var ctx = document.getElementById('traffic-chart-area').getContext('2d');
    window.APP.charts.traffic = new Chart(ctx, traffic_config);

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
                borderColor: getRootVar("--color-blue"),
                pointBackgroundColor: getRootVar("--color-blue"),
                borderWidth: 1,
                fill: false,
                pointRadius: 0,
                pointHoverRadius: 0
            };
            datasets.push(dataset);

            dataset = {
                data: window.APP.net_history[1],
                borderColor: getRootVar("--color-red"),
                pointBackgroundColor: getRootVar("--color-red"),
                borderWidth: 1,
                fill: false,
                pointRadius: 0,
                pointHoverRadius: 0
            };
            datasets.push(dataset);

            window.APP.charts.traffic.data.datasets = datasets;
            window.APP.charts.traffic.update();
        } catch (e) {

            console.log("Error on: network\n", e);

        }
    }
});
