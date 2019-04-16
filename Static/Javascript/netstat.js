window.APP.fetch.push({
    url: '/api/netstat',
    key: 'netstat',
    interval: 10000
});


window.APP.update_funcs.push({
    interval: 10000,
    func: function (event) {
        try {
            var d = window.APP.page_data.netstat;

            $('#listeners').find('tbody').html('');
            for (var i = 0; i < d.length; i++) {
                var t = d[i];
                if (t.state != "LISTEN") {
                    continue;
                }
                var name = t.executable
                if (name !== null) {
                    ns = name.split('/');
                    name = ns[ns.length-1];
                }
                var row = "<tr><td>"+name+"</td><td>"+t.uid+"</td><td class=''>"+t.local_port+"</td><td class=''>"+t.service+"</td></tr>";
                $('#listeners').find('tbody').append(row);
            }

        } catch (e) {

            $('#listeners').find('tbody').html('<tr><td colspan="4" style="text-align:center;">An Error Occurred!</td></tr>');

            console.log("Error on: netstat\n", e);

        }

        try {

            $('#connections').find('tbody').html('');
            for (var i = 0; i < d.length; i++) {
                var t = d[i];
                if (t.state != "ESTABLISHED") {
                    continue;
                }
                var row = "<tr><td>"+t.service+"</td><td>"+t.remote_address+"</td></tr>";
                $('#connections').find('tbody').append(row);
            }
        } catch (e) {

            $('#connections').find('tbody').html('<tr><td colspan="2" style="text-align:center;">An Error Occurred!</td></tr>');

            console.log("Error on: netstat\n", e);

        }
    }
});
