window.APP.fetch.push({
    url: '/api/users',
    key: 'users',
    interval: 10000,
});


window.APP.update_funcs.push({
    interval: 10000,
    func: function (event) {
        try {
            var d = window.APP.page_data.users;

            $('#loggedin').find('tbody').html('');

            for (var i = 0; i < d['logged_in'].length; i++) {
                var rd = d['logged_in'][i];
                var row = "<tr><td>"+rd.name+"</td><td>"+rd.terminal+"</td><td>"+rd.host+"</td><td>"+rd.process_name+"</td></tr>";
                $('#loggedin').find('tbody').append(row);
            }
        } catch (e) {

            $('#loggedin').find('tbody').html('<tr><td colspan="4" style="text-align:center;">An Error Occurred!</td></tr>');

            console.log("Error on: users\n", e);

        }

        try {

            $('#lastlog').find('tbody').html('');
            for (var i = 0; i < d.last_logins.length; i++) {
                var rd = d.last_logins[i];

                var m = moment(rd.timestamp);
                var row = "<tr><td>"+rd.name+"</td><td>"+m.fromNow()+"</td><td>"+rd.host+"</td></tr>";
                $('#lastlog').find('tbody').append(row);
            }

        } catch (e) {

            $('#lastlog').find('tbody').html('<tr><td colspan="3" style="text-align:center;">An Error Occurred!</td></tr>');

            console.log("Error on: users\n", e);

        }
    }
});
