// Invertebrate: invrt
// A framework without a backbone

window.invrt = {}
window.invrt.app = {
    // Fetched data
    data: {},

    // Data sources to collect
    sources: [],

    // List of onload functions
    load: [],

    // List of update functions
    update: [],

    // Constructor
    init: function () {

    },

    _init: function () {

    },

    _collect: function () {

    },

    _get: function (fetch_obj, callback) {

    },

    _post: function (post_obj, callback) {

    },

    _baseurl: null,
    _loaded: false,
    _paused: false,
    _tocollect: 0,
    _collected: 0
}


class fetch_object: {
    url: null,
    key: null,
    interval: null,
    prerequisite: false
}

class load: {
    func: null
}

class update: {
    func: null,
    interval: null,
}
