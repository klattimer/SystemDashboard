window.APP.fetch.push({
    url: '/api/top',
    key: 'top',
    interval: 10000,
});


window.APP.update_funcs.push({
    interval: 10000,
    func: function (event) {
        try {

            var td = window.APP.page_data.top;

            $('#top_cpu_usage').find('tbody').html('');

            for (var i = 0; i < td.top_cpu_usage.length; i++) {
                var t = td.top_cpu_usage[i];
                var name = t.cmdline[0];
                if (name === undefined || name === null) {
                    name = t.exe;
                }
                if (name === undefined || name === null) {
                    name = t.name;
                }
                if (name === undefined || name === null) {
                    name = "";
                }
                ns = name.split('@');
                name = ns[0];
                ns = name.split('/');
                name = ns[ns.length-1];

                var row = "<tr><td class='small'>"+t.pid+"</td><td>"+name+"</td><td>"+t.username+"</td><td class='medium'>"+t.nice+"</td><td class='mediumplus'>"+parseInt(t.cpu_percent)+"%</td></tr>";
                $('#top_cpu_usage').find('tbody').append(row);
            }

        } catch (e) {

            $('#top_cpu_usage').find('tbody').html('<tr><td colspan="5" style="text-align:center;">An Error Occurred!</td></tr>');

            console.log("Error on: top\n", e);

        }

        try {

            $('#top_memory_usage').find('tbody').html('');
            for (var i = 0; i < td.top_memory_usage.length; i++) {
                var t = td.top_memory_usage[i];
                if (name === undefined) {
                    name = t.exe;
                }
                var name = t.cmdline[0];
                ns = name.split('@');
                name = ns[0];
                ns = name.split('/');
                name = ns[ns.length-1];

                var row = "<tr><td class='small'>"+t.pid+"</td><td>"+name+"</td><td>"+t.username+"</td><td>"+parseInt(t.memory_percent * 1000)/1000.0+"%</td></tr>";
                $('#top_memory_usage').find('tbody').append(row);
            }

        } catch (e) {

            $('#top_memory_usage').find('tbody').html('<tr><td colspan="3" style="text-align:center;">An Error Occurred!</td></tr>');

            console.log("Error on: top\n", e);

        }

    }
});
