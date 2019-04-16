
var log_state = {
    num_lines: 0,
    last_line: 0,
    first_line: 0,
    size: 30,
    at_end: true,
    file: 'syslog'
};

window.APP.load.push(function (event) {
    $('.logfile').click(function (event) {
        log_state.log_file = $(event.target).data("logfile");
        log_state.num_lines = 0;
        log_state.last_line = 0;
        log_state.first_line = 0;
        log_state.size = 30;
        log_state.at_end = true;
        window.APP.Log.update_log();
    });
});

window.APP.Log = {};
window.APP.Log.update_log = function () {
    try {
        if (log_state.at_end === false) {
            return;
        }
        params = {
            'size': log_state.size,
            'file': log_state.file
        }
        if (log_state.num_lines > 0) {
            params.start = log_state.last_line + 1;
        }
        p = $.param( params );
        console.log(params);
        $.get( '/api/log?'+p, function(data) {
            console.log(data);
            if (log_state.num_lines == 0) {
                $('.log-content pre').append(data.data);
                log_state.last_line = data.end;
                log_state.first_line = data.start;
                log_state.num_lines = data.num_lines;
            } else if (data.num_lines > log_state.num_lines) {
                if (data.end > log_state.last_line) {
                    if (log_state.last_line + 1 == data.start) {
                        // Append data to the log viewer
                        $('.log-content pre').append(data.data);
                        log_state.last_line = data.end
                    } else {
                        // Something isn't quiet right there...
                    }
                }
                log_state.num_lines = data.num_lines;
            }
            $('.log-content').scrollTop($('.log-content pre').height());
        }, "json");

    } catch (e) {

        console.log("Error on: log\n", e);

    }
};

window.APP.update_funcs.push({
    interval: 10000,
    func: window.APP.Log.update_log
});
