

window.APP = {
    page_data: {},
    fetch: [],
    load: [],
    update: [],
    update_funcs: [],
    charts: {},
    _getcount: 0,
    _gotcount: 0,
    _loaded: false,
    _intervals: [],
    _recalc_base_size: function () {
        var base_size = $('.widget-grid').width() / 4;
        document.documentElement.style.setProperty('--base-size', base_size + 'px');
        var containers = $('.chart-container');
        for (var i = 0; i < containers.length; i++) {
            var canvas = $(containers[i]).find('canvas')[0];

            $(canvas).attr('width', $(containers[i]).width());
            $(canvas).attr('height', $(containers[i]).height());
        }
    },
    _load: function () {
        window.APP._recalc_base_size();
        for (var i = 0;i < window.APP.load.length; i++) {
            window.APP.load[i](event);
        }

        for (var i = 0;i < window.APP.update_funcs.length; i++) {
            (function(index) {
                var int = setInterval(function() {
                    try {
                        window.APP.update_funcs[index].func();
                    } catch (e) {}
                }, window.APP.update_funcs[index].interval);
                window.APP._intervals.push(int);
            })(i);
            try {
                window.APP.update_funcs[i].func();
            } catch (e) {}
        }
        $('.widget-grid-container').masonry({
            columnWidth: $('.widget-grid').width() / 4
        });
    },
    _get: function (fetch_obj, inc_get) {
        $.get( fetch_obj.url, function(data) {

            window.APP.page_data[fetch_obj.key] = data;

            if (inc_get === true) {
                window.APP._gotcount++;
            }

            if (window.APP._getcount == window.APP._gotcount && window.APP._loaded === false) {
                window.APP._loaded = true;
                window.APP._load();
            }
        }, "json")
        .fail(function() {

            if (inc_get === true) {
                window.APP._gotcount++;
            }

            if (window.APP._getcount == window.APP._gotcount && window.APP._loaded === false) {
                window.APP._loaded = true;
                window.APP._load();
            }

        });
    },
    onload: function (event) {
        window.APP._recalc_base_size();
        window.onresize = window.APP._recalc_base_size;

        for (var i = 0;i < window.APP.fetch.length; i++) {
            window.APP._get(window.APP.fetch[i], true);
            window.APP._getcount++;

            (function(index) {
                var int = setInterval(function() {
                    window.APP._get(window.APP.fetch[index], false);
                }, window.APP.fetch[index].interval);
                window.APP._intervals.push(int);
                console.log("Setting interval: " + window.APP.fetch[index].interval + "ms " + window.APP.fetch[index].url);
            })(i);
        }
    },
};
function getRootVar(variable) {
    return getComputedStyle(document.documentElement).getPropertyValue(variable);
}
window.onload = window.APP.onload
