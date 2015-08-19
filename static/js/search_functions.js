var MILLS_TO_IGNORE_REQUESTS = 500; // client side button delay for ajax-callable actions
// this is done with the debounce()-function from the underscore.js-library

var objects_added_count = 0; // Integer used to indicate how many objects have been added to a level

var templateText_latex = "";
var templateSolution_latex = {};
var text_wrapper = $('#modal_template_text');
var solution_wrapper = $('#modal_template_solution');

function displayPreview() {
    var button = $(this);
    var template_id = button.data('template_id'); // Extract info from the buttons data-* attributes
    var template_title = button.data('template_title');
    var json_url = '/template/' + template_id + '/preview/'; // build the ajax request url with the button data

    // this Json-request returns a json object with a
    // templates' unmodified LaTeX-data for the question text and every solution step
    $.getJSON(json_url, function (data) {
        templateText_latex = data.template_text;
        templateSolution_latex = data.template_solution.split('§');
        console.log('getJSON - template_text: ' + templateText_latex + ", solution: " + templateSolution_latex);
    });

    $('#previewModal').modal('show').on('shown.bs.modal', function () {
        var modal = $(this);
        refresh_preview();
        modal.find('.modal-title').text('Forhåndsvisning av ' + '"' + template_title + '"');
        redraw_mathquill_elements();
    });
}

function refresh_preview() {
    // update preview modal contents
    // (must be called after .show() has been called otherwise the LaTeX won't render correctrly
    text_wrapper.children().remove();
    solution_wrapper.children().remove();
    text_wrapper.append('<div class="input_field"><span id="preview_template_text" class="static-math input_mathquill"></span>');
    MathQuill.StaticMath($('#preview_template_text')[0]).latex(templateText_latex);
    for (var s = 0; s < templateSolution_latex.length; s++) {
        solution_wrapper.append('<div class="input_field"><div id="preview_solution_step_' + s + '" class="static-math"></div></div><br/>');
        MathQuill.StaticMath($('#preview_solution_step_' + s)[0]).latex(templateSolution_latex[s]);
    }
}

function processToggle() {
    var $toggle_button = $(this);
    var template_id = $toggle_button.data('template_id');
    var post_url = '/user/level/template/' + template_id + '/toggle/';
    console.log($toggle_button.data('template_id'));

    $.post(post_url, {'csrfmiddlewaretoken': getCookie('csrftoken')}, function (result) {
        console.log(result);
        $('#toggle_button_id_' + template_id).toggleClass('btn-primary btn-danger').children().toggleClass('glyphicon-plus glyphicon-minus');
        $('#current_level_button').effect('highlight',{ 'color': '#5cb85c' });
    })
}

function processCopy() {
    // send an ajax request to copy a template and add it to a users "current level"
    var copied_objects_counter = $('#objects_added_amount');
    var button = $(this); // get the button object that was clicked on
    var template_id = button.data('template-id'); // get the data-template-id attribute from the button
    var post_url = '/level/' + current_level + '/template/' + template_id + '/add/'; // build the AJAX url to be used
    // the "current_level" variable is instantiated in the file template_search.html

    $.post(post_url, {'csrfmiddlewaretoken': getCookie('csrftoken')}, function (result) {
        // on copy action success:
        objects_added_count++; // add 1 to the counter
        $('#object_copied_indicator_' + template_id).fadeIn('fast'); // display an indicator that this object has been copied and added
        var current_level_button = $('#current_level_button');
        // animate a transfer effect and display the "objects added" counter on the current level indicator
        button.effect('transfer', { to: current_level_button }, 400,
            function() {
                current_level_button.effect('highlight',{ 'color': '#5cb85c' });
                copied_objects_counter.text(objects_added_count); // rewrite the new count on the current level indicator
                $('#objects_added_container').show(); // show the counter if it wasn't already shown
            });
        console.log(result);
    })
}

$(document).ready(function () {

/*  button listener for toggling template to level relations
    deprecated in favor of always copying wanted objects
    $('.ajax-toggle-button').click(_.debounce(processToggle,
        MILLS_TO_IGNORE_REQUESTS, true
    ));*/

    // Instantiate button listeners for any preview button
    $('.preview-button').click(displayPreview);

    // Instantiate button listener for any copy button
    $('.btn-copy-template').click(_.debounce(processCopy, MILLS_TO_IGNORE_REQUESTS, true));

});

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
});