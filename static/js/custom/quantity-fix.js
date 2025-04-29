/**
 * Quantity Input Fix
 * This script specifically fixes the quantity input buttons functionality
 * that appears to be conflicting with other scripts.
 */
(function($) {
    "use strict";
    
    $(document).ready(function() {
        // Remove any existing click handlers from quantity buttons to avoid conflicts
        $('.btn-number').off('click');
        
        // Apply our own click handler for the quantity buttons
        $('.btn-number').on('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            var fieldName = $(this).attr('data-field');
            var type = $(this).attr('data-type');
            var input = $("input[name='" + fieldName + "']");
            
            // If the button is inside a modal, we need to get the right input
            if ($(this).closest('.modal').length > 0) {
                input = $(this).closest('.modal').find("input[name='" + fieldName + "']");
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
            
            // Log to console for debugging
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
        });
        
        // Prevent non-numeric input
        $('.input-number').on('keypress', function(e) {
            if (e.which !== 8 && e.which !== 0 && (e.which < 48 || e.which > 57)) {
                return false;
            }
        });
        
        // Initialize the quantity inputs on page load
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
    
})(jQuery);