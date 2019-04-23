
window.APP.load.push(function () {
    $( ".menu a" ).click(function(event) {
        event.preventDefault();
        var href = $(this).attr("href");
        href = href.replace('#', '');
        href = "a[name=" + href + "]";
        $("html, body").animate({
            scrollTop: $(href).offset().top
        }, 500, "linear");
    });
});
