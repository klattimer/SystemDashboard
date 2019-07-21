

window.APP.fetch.push({
    url: '/api/diskio',
    key: 'diskio',
    interval: 1000
});


var diskrw_config = {
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
            }],
            xAxis: [{
                gridLines: {
                    drawTicks: true
                },
                display: true,
                ticks: {
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
    diskrw_config.data.labels = labels;
    var ctx = document.getElementById('diskrw-chart-area').getContext('2d');
    window.APP.charts.diskrw = new Chart(ctx, diskrw_config);

    window.APP.diskrw_history = [[], []];
    window.APP.disk_out_last = 0;
    window.APP.disk_in_last = 0;
});


window.APP.update_funcs.push({
    interval: 1000,
    func: function() {
        try {

            var size = 61;

            var last = window.APP.disk_in_last;
            if (last == 0) last = window.APP.page_data.diskio.total_io.read_bytes;
            window.APP.disk_in_last = window.APP.page_data.diskio.total_io.read_bytes;
            var in_bps = window.APP.disk_in_last - last;

            last = window.APP.disk_out_last;
            if (last == 0) last = window.APP.page_data.diskio.total_io.write_bytes;
            window.APP.disk_out_last = window.APP.page_data.diskio.total_io.write_bytes;
            var out_bps = window.APP.disk_out_last - last;

            window.APP.diskrw_history[0].push(in_bps);
            window.APP.diskrw_history[1].push(out_bps);

            datasets = [];
            for (var i = 0; i < window.APP.diskrw_history.length; i++) {
                var len = window.APP.diskrw_history[i].length;
                if (len > size) {
                    window.APP.diskrw_history[i] = window.APP.diskrw_history[i].slice(len - size, len);
                } else {
                    for (var j = 0; j < size - len; j++) {
                        window.APP.diskrw_history[i].splice(0, 0, 0);
                    }
                }
            }

            dataset = {
                data: window.APP.diskrw_history[0],
                borderColor: getRootVar("--color-blue"),
                pointBackgroundColor: getRootVar("--color-blue"),
                borderWidth: 1,
                fill: false,
                pointRadius: 0,
                pointHoverRadius: 0
            };
            datasets.push(dataset);

            dataset = {
                data: window.APP.diskrw_history[1],
                borderColor: getRootVar("--color-red"),
                pointBackgroundColor: getRootVar("--color-red"),
                borderWidth: 1,
                fill: false,
                pointRadius: 0,
                pointHoverRadius: 0
            };
            datasets.push(dataset);

            window.APP.charts.diskrw.data.datasets = datasets;
            window.APP.charts.diskrw.update();

        } catch (e) {

            console.log("Error on: diskio\n", e);

        }

    }
});
