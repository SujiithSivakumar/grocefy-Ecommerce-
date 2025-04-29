(function($) {
    "use strict";

    var header = $('.header.shop');
    var win = $(window);
    var headerHeight = header.height();

    win.on('scroll', function() {
        var scroll = win.scrollTop();

        if (scroll < headerHeight) {
            header.removeClass('sticky');
        } else {
            header.addClass('sticky');
        }

        if (scroll == 0) {
            header.removeClass('sticky');
        }
    });

    // Mobile Menu
    $('.category-trigger').on('click', function(e) {
        $('.category-menu').slideToggle(500);
        $('.category-trigger .right').toggleClass('ti-minus ti-plus');
        e.preventDefault();
    });

    $('.menu-trigger').on('click', function() {
        $('.mobile-menu').toggleClass('active');
        $('.overlay').toggleClass('active');
    });

    $('.mobile-menu .dropdown').on('click', function() {
        $(this).find('ul').slideToggle(500);
        $(this).toggleClass('active');
    });

})(jQuery); 