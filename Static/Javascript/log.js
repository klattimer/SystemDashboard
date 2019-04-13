
var log_state = {
    num_lines: 0,
    last_line: 0,
    first_line: 0,
    size: 30,
    at_end: true
};

window.APP.update_funcs.push({
    interval: 10000,
    func: function () {
        if (log_state.at_end === false) {
            return;
        }
        params = {
            'size': log_state.size,
            'file': 'syslog'
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
    }
});
