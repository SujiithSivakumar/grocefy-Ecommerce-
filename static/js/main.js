(function($) {
    "use strict";
    
    // Preloader
    $(window).on('load', function() {
        if($('.preloader').length) {
            $('.preloader').fadeOut('slow');
        }
    });

    // Nice Select
    $('select').niceSelect();
    
    // Sticky Header
    $(window).scroll(function() {
        if ($(this).scrollTop() > 100) {
            $('.header').addClass('sticky');
        } else {
            $('.header').removeClass('sticky');
        }
    });

    // Mobile Menu
    $('.main-menu').slicknav({
        prependTo: '.mobile-nav',
        duration: 300,
        closeOnClick: true,
    });

    // Owl Carousel
    $('.hero-slider').owlCarousel({
        loop: true,
        nav: true,
        dots: false,
        autoplay: true,
        smartSpeed: 500,
        autoplayTimeout: 5000,
        navText: ['<i class="ti-angle-left"></i>', '<i class="ti-angle-right"></i>'],
        responsive: {
            0: { items: 1 },
            768: { items: 1 },
            1024: { items: 1 }
        }
    });

    // Product Carousel
    $('.product-carousel').owlCarousel({
        loop: true,
        nav: true,
        dots: false,
        margin: 30,
        autoplay: true,
        smartSpeed: 500,
        autoplayTimeout: 4000,
        navText: ['<i class="ti-angle-left"></i>', '<i="ti-angle-right"></i>'],
        responsive: {
            0: { items: 1 },
            576: { items: 2 },
            768: { items: 3 },
            992: { items: 4 }
        }
    });

    // Magnific Popup
    $('.image-popup').magnificPopup({
        type: 'image',
        gallery: { enabled: true }
    });

    // FIXED: Quantity Buttons - Direct implementation
    $('.btn-number').on('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        var fieldName = $(this).attr('data-field');
        var type = $(this).attr('data-type');
        var input = $("input[name='" + fieldName + "']");
        
        // If the button is inside a modal, we need to get the right input
        if ($(this).closest('.modal').length > 0) {
            input = $(this).closest('.modal').find("input[name='" + fieldName + "']");
        } else {
            input = $(this).closest('.input-group').find("input[name='" + fieldName + "']");
        }
        
        var currentVal = parseInt(input.val());
        
        if (!isNaN(currentVal)) {
            if (type === 'minus') {
                var minValue = parseInt(input.attr('data-min')) || 1;
                
                if (currentVal > minValue) {
                    input.val(currentVal - 1);
                    input.trigger('change');
                }
                if (parseInt(input.val()) === minValue) {
                    $(this).attr('disabled', true);
                }
                // Enable the plus button
                var plusButton = $(this).closest('.input-group').find(".btn-number[data-type='plus']");
                plusButton.attr('disabled', false);
            } else if (type === 'plus') {
                var maxValue = parseInt(input.attr('data-max')) || 999;
                
                if (currentVal < maxValue) {
                    input.val(currentVal + 1);
                    input.trigger('change');
                }
                if (parseInt(input.val()) === maxValue) {
                    $(this).attr('disabled', true);
                }
                // Enable the minus button
                var minusButton = $(this).closest('.input-group').find(".btn-number[data-type='minus']");
                minusButton.attr('disabled', false);
            }
            
            // Force the input to update visually
            input.css({
                'color': 'black',
                'background': 'white',
                'display': 'block',
                'font-size': '16px',
                'border': '1px solid #ccc',
                'padding': '0 5px'
            });
        } else {
            input.val(1);
        }
        
        // Log for debugging
        console.log("Button clicked: " + type + ", New value: " + input.val());
    });
    
    // Handle the input change event
    $('.input-number').on('change keyup', function() {
        var minValue = parseInt($(this).attr('data-min')) || 1;
        var maxValue = parseInt($(this).attr('data-max')) || 999;
        var valueCurrent = parseInt($(this).val()) || 0;
        var name = $(this).attr('name');
        var inputGroup = $(this).closest('.input-group');
        
        if (valueCurrent >= minValue) {
            inputGroup.find(".btn-number[data-type='minus']").attr('disabled', false);
        } else {
            $(this).val(minValue);
            inputGroup.find(".btn-number[data-type='minus']").attr('disabled', true);
        }
        
        if (valueCurrent <= maxValue) {
            inputGroup.find(".btn-number[data-type='plus']").attr('disabled', false);
        } else {
            $(this).val(maxValue);
            inputGroup.find(".btn-number[data-type='plus']").attr('disabled', true);
        }
        
        // Force the input to update visually
        $(this).css({
            'color': 'black',
            'background': 'white',
            'display': 'block',
            'font-size': '16px',
            'border': '1px solid #ccc',
            'padding': '0 5px'
        });
    });
    
    // Prevent non-numeric input
    $('.input-number').on('keypress', function(e) {
        if (e.which !== 8 && e.which !== 0 && (e.which < 48 || e.which > 57)) {
            return false;
        }
    });
    
    // Initialize the quantity inputs on document ready
    $(document).ready(function() {
        $('.input-number').each(function() {
            // Force the display of the input
            $(this).css({
                'color': 'black',
                'background': 'white',
                'display': 'block',
                'font-size': '16px',
                'border': '1px solid #ccc',
                'padding': '0 5px'
            });
            
            // Trigger change to update button states
            $(this).trigger('change');
            
            console.log("Quantity input initialized: " + $(this).attr('name') + ", Value: " + $(this).val());
        });
    });

    // Price Range Slider
    if($('#price-range').length) {
        $("#price-range").slider({
            range: true,
            min: 0,
            max: 1000,
            values: [0, 1000],
            slide: function(event, ui) {
                $("#min-price").val(ui.values[0]);
                $("#max-price").val(ui.values[1]);
            }
        });
        $("#min-price").val($("#price-range").slider("values", 0));
        $("#max-price").val($("#price-range").slider("values", 1));
    }

    // ScrollUp
    $.scrollUp({
        scrollName: 'scrollUp',
        scrollDistance: 300,
        scrollFrom: 'top',
        scrollSpeed: 500,
        easingType: 'linear',
        animation: 'fade',
        animationSpeed: 200,
        scrollTrigger: false,
        scrollTarget: false,
        scrollText: '<i class="ti-arrow-up"></i>',
        scrollTitle: false,
        scrollImg: false,
        activeOverlay: false,
        zIndex: 2147483647
    });

    // Counter Up
    $('.counter').counterUp({
        delay: 10,
        time: 1000
    });

})(jQuery);