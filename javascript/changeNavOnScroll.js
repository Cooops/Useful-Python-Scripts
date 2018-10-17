// Used to force the navbar to follow you when you scroll down a page.
$(function () {
    $(document).scroll(function () {
        var $nav = $("#mainNav");
        $nav.toggleClass('scrolled', $(this).scrollTop() > $nav.height());
        });
    });
    
// You would then append styling to the css `<id>.scrolled` below.
// ...
