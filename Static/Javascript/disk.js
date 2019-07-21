window.APP.fetch.push({
    url: '/api/disk',
    key: 'disk',
    interval: 60000
});

var disk_config = {
	type: 'doughnut',
    responsive: true,
	data: {
		datasets: [{
			data: [
				34,
				66,
			],
			backgroundColor: [
				getRootVar("--color-red"),
				getRootVar("--color-blue")
			],
			label: 'Disk Usage /'
		}]
	},
	options: {
        tooltips: {
            enabled: false
        },
        hover: {mode: null},
		responsive: true,
		legend: {
			position: 'top',
		},
		title: {
			display: false
		},
		animation: {
			animateScale: true,
			animateRotate: true
		}
	}
};

var rebuild_config = {
	type: 'doughnut',
	data: {
		datasets: [{
			data: [],
			backgroundColor: [
				getRootVar("--color-green"),
				getRootVar("--color-red")
			]
		}]
	},
	options: {
        tooltips: {
            enabled: false
        },
        hover: {mode: null},
		responsive: true,
		legend: {
			position: 'top',
		},
		title: {
			display: false
		},
		animation: {
			animateScale: true,
			animateRotate: true
		}
	}
};

window.APP.load.push(function (event) {
    var dd = window.APP.page_data.disk;

    window.APP.charts.disk_usage = [];
    for (var i = 0; i < Object.keys(dd.partitions).length; i++) {
        var k = Object.keys(dd.partitions)[i];
        var d = dd.partitions[k];
        var name = d.mountpoint;
        if (d.total === undefined || d.used === undefined) {
            window.APP.charts.disk_usage.push(null);
            continue;
        }
        var id = 'disk'+i+'-chart-area';
        var label_id = 'disk'+i+'-percent';

        var html = "<div class='widget-grid-item w1h1'>" +
                   "<div class='widget-grid-item-inner'>" +
                   "<div id='"+id+"-container' class='chart-container'>" +
                   "<canvas id='"+id+"'></canvas></div>" +
                   "<div id='"+label_id+"' class='centre-percent'>"+(100 - parseInt(d.percent))+"%</div>" +
                   "<div class='centre-label'>available</div>" +
                   "<h1><i class='far fa-hdd'></i>"+name+" Disk Usage</h1></div></div>";
        $('a[name=storage] + .widget-grid-header + .widget-grid-container').append(html);

        $(document.getElementById(id)).attr('width', $(document.getElementById(id)).width());
        $(document.getElementById(id)).attr('height', $(document.getElementById(id)).height());

        var ctx = document.getElementById(id).getContext('2d');
        var chart = new Chart(ctx, disk_config);
        window.APP.charts.disk_usage.push(chart);
    }

    window.APP.charts.rebuild_raid = [];
    var chart = {};
    chart.array_data = {};
    if (window.APP.page_data.disk.mdstat.devices !== undefined) {
        for (var i = 0; i < Object.keys(window.APP.page_data.disk.mdstat.devices).length; i++) {
            var k = Object.keys(window.APP.page_data.disk.mdstat.devices)[i];
            var array = window.APP.page_data.disk.mdstat.devices[k];
            if (array.resync !== null) {

                var id = k+'-rebuild-chart-area';
                var label_id = k+'-rebuild-percent';

                var html = "<div class='widget-grid-item w1h1'>" +
                           "<div class='widget-grid-item-inner'>" +
                           "<div id='"+id+"-container' class='chart-container'>" +
                           "<canvas id='"+id+"'></canvas></div>" +
                           "<div id='"+label_id+"' class='centre-percent'>"+array.resync.progress+"</div>" +
                           "<div class='centre-label'>complete</div>" +
                           "<h1><i class='far fa-hdd'></i>"+k+" Rebuild Progress</h1></div></div>";
                $('a[name=storage] + .widget-grid-header + .widget-grid-container').append(html);

                $(document.getElementById(id)).attr('width', $(document.getElementById(id)).width());
                $(document.getElementById(id)).attr('height', $(document.getElementById(id)).height());

                var ctx = document.getElementById(id).getContext('2d');
                var chart = new Chart(ctx, rebuild_config);
                chart.array_data = array;
                chart.array_key = k;
                window.APP.charts.rebuild_raid.push(chart);
            }

            var id = k+'-disk-table';

            var html = "<div class='widget-grid-item w2h1'>" +
                       "<div class='widget-grid-item-inner'>" +
                       "<h1><i class='fas fa-layer-group'></i>RAID "+k+" Disk Status</h1>" +
                       "<table id='"+id+"' class='data-table'><thead><tr>" +
                       "<th>Raid Device </th>" +
                       "<th>Partition</th>" +
                       "<th>Status</th>" +
                       "<th class='narrow'></th></tr></thead>" +
                       "<tbody></tbody></table></div></div>";

            $('a[name=storage] + .widget-grid-header + .widget-grid-container').append(html);

        }
    }
});

window.APP.update_funcs.push({
    interval: 60000,
    func: function () {

        try {

            var dd = window.APP.page_data.disk;
            for (var i = 0; i < Object.keys(dd.partitions).length; i++) {
                var k = Object.keys(dd.partitions)[i];
                var d = dd.partitions[k];
                if (d.total === undefined || d.used === undefined) {
                    continue;
                }
                var label_id = 'disk'+i+'-percent';
                var chart = window.APP.charts.disk_usage[i];
                $('#' + label_id).html(100 - parseInt(d.percent) +'%');
                chart.data.datasets[0].data = [parseInt(d.percent), (100 - parseInt(d.percent))];
                chart.update();
            }

            for (var i = 0; i < window.APP.charts.rebuild_raid.length; i++) {
                var chart = window.APP.charts.rebuild_raid[i];
                var k = chart.array_key;
                var d = window.APP.page_data.disk.mdstat.devices[k];
                var label_id = k+'-rebuild-percent';
                $('#' + label_id).html(d.resync.progress);
                chart.data.datasets[0].data = [parseFloat(d.resync.progress), 100 - parseFloat(d.resync.progress)];
                chart.update();
            }


        } catch (e) {

            console.log("Error on: disk\n", e);
            window.APP._warnings.push({
                "error": "Cannot update disk percentage or raid rebuild status",
                "code": "",
                "timestamp": ""
            });
        }

        try {

            $('#disktemp').find('tbody').html('');
            var c = 0;
            for (var i = 0; i < Object.keys(window.APP.page_data.disk.drives).length; i++) {
                var disk = Object.keys(window.APP.page_data.disk.drives)[i];
                var temp = window.APP.page_data.disk.drives[disk].temperature;
                if (temp === null || temp === undefined) {
                    continue;
                }

                var state = '<i class="fas fa-circle status-blue"></i>';
                if (temp > 60) {
                    state = '<i class="fas fa-circle status-orange"></i>';
                }
                if (temp > 80) {
                    state = '<i class="fas fa-circle status-red"></i>';
                }

                var row = '<tr><td>'+disk+'</td><td>'+temp+'&deg;C</td><td class="narrow">'+state+'</td></tr>';
                $('#disktemp').find('tbody').append(row);
                c++;
            }
            if (c == 0) {
                $('#disktemp').remove();
            }

        } catch (e) {
            $('#disktemp').remove();
            // $('#disktemp').find('tbody').html('<tr><td colspan="3" style="text-align:center;">An Error Occurred!</td></tr>');

            console.log("Error on: disk temperatures\n", e);

        }

        try {

            if (window.APP.page_data.disk.mdstat.devices !== undefined) {
                for (var i = 0; i < Object.keys(window.APP.page_data.disk.mdstat.devices).length; i++) {
                    var k = Object.keys(window.APP.page_data.disk.mdstat.devices)[i];
                    var array = window.APP.page_data.disk.mdstat.devices[k];

                    var id = k+'-disk-table';

                    $('#' + id).find('tbody').html('');
                    for (var j = 0; j < Object.keys(array.disks).length; j++) {
                        var n = Object.keys(array.disks)[j];
                        var dd = array.disks[n];

                        var state = "active sync";
                        var icon = "<i class='fas fa-check-circle status-green'></i>";
                        if (dd.spare && dd.replacement) {
                            state = "spare rebuilding";
                            icon = "<i class='fas fa-check-circle status-orange'></i>";
                        } else if (dd.spare) {
                            state = "spare";
                            icon = "<i class='fas fa-pause-circle status-grey'></i>";
                        } else if (dd.faulty) {
                            state = "faulty";
                            icon = "<i class='fas fa-times-circle status-red'></i>";
                        }
                        var row = "<tr><td>"+dd.number+"</td><td>"+n+"</td><td>"+state+"</td><td class='narrow'>"+icon+"</td></tr>";
                        $('#' + id).find('tbody').append(row);
                    }
                }
            }

        } catch (e) {

            console.log("Error on: disk\n", e);

        }

        try {
            var dd = window.APP.page_data.disk;
            $('#partitions').find('tbody').html('');
            for (var i = 0; i < Object.keys(dd.partitions).length; i++) {
                var k = Object.keys(dd.partitions)[i];
                var d = dd.partitions[k];
                if (k.indexOf('loop') > -1 || d.fstype == null || d.fstype == 'swap') {
                    continue;
                }
                var state = '<i class="fas fa-circle status-red"></i>';
                mp = '';
                if (d.mountpoint !== null ) {
                    mp = d.mountpoint;
                    state = '<i class="fas fa-circle status-green"></i>';
                }

                var ranges = [
                    { divider: 1e12, suffix: 'T' },
                    { divider: 1e9, suffix: 'G' },
                    { divider: 1e6, suffix: 'M' },
                    { divider: 1e3, suffix: 'k' }
                ];
                function formatNumber(n) {
                    for (var i = 0; i < ranges.length; i++) {
                       if (n >= ranges[i].divider) {
                          return parseInt(n / ranges[i].divider).toString() + ranges[i].suffix;
                       }
                    }
                    return n;
                }
                size = formatNumber(d.size) + 'B';
                if (d.free > 0) {
                    available = formatNumber(d.free) +'B';
                    percentage = parseInt(d.percent) + '%';
                    available_row = '<div class="progress-bar-outer"><div class="progress-bar-inner" style="width:'+percentage+'"></div></div>'+available+' Free'
                } else {
                    available_row = '';
                }

                label = d.label;
                if (label == null) {
                    label = '';
                }

                row = '<tr><td class="narrow">'+state+'</td>' +
                        '<td>'+k+'</td>' +
                        '<td>'+d.fstype+'</td>' +
                        '<td>'+label+'</td>' +
                        '<td>'+available_row+'</td>' +
                        '<td>'+size+'</td>' +
                        '<td>'+mp+'</td>' +
                        '<td class="narrow"></td></tr>';

                $('#partitions').find('tbody').append(row)
            }
        } catch (e) {

            console.log("Error on: disk\n", e);
        }
    }
});
