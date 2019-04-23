

window.APP.load.push(function () {
    window.APP.power_visible = false;
    $('#power').click(function(event) {
        if (window.APP.power_visible === true) {
            $('power-menu').hide();
            window.APP.power_visible = false;
        } else {
            $('.power-menu').show();
            window.APP.power_visible = true;
        }
    });
    window.APP.decrement_interval = null;
    window.APP.release_timeout = null;
    $('.power-menu .slider').mouseup(function (event) {
        clearInterval(window.APP.release_timeout);
        window.APP.release_timeout = setTimeout(function() {
            var max = parseInt(event.target.max);
            var min = parseInt(event.target.min);
            var value = parseInt(event.target.value);
            if (value < .9 * max) {
                window.APP.decrement_interval = setInterval(function () {
                    console.log("Decrement interval running " + event.target.value);
                    if (parseInt(event.target.value) == 1) {
                        console.log("Decrement interval stopping");
                        clearInterval(window.APP.decrement_interval);
                        window.APP.decrement_interval = null;
                        return;
                    }
                    event.target.value = parseInt(parseInt(event.target.value) * 0.8)
                }, 10);
            } else {
                event.target.value = max;

                // Trigger a shutdown event.
            }
        }, 90);
    });
});
