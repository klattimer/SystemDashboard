

window.APP.fetch.push({
    url: '/api/radar',
    key: 'radar',
    interval: 10000
});

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
            pointBackgroundColor: getRootVar("--color-red"),
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
    var ctx = document.getElementById('radar-chart-area').getContext('2d');
    window.APP.charts.radar = new Chart(ctx, radar_config);

});

window.APP.update_funcs.push({
    interval: 10000,
    func: function () {
        try {
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
