var MILLS_TO_IGNORE_REQUESTS = 500;
var VARIABLES = ['a', 'b', 'c', 'd'];

var templateText_latex = "";
var templateSolution_latex = {};
var text_wrapper = $('#modal_template_text');
var solution_wrapper = $('#modal_template_solution');

var refresh_preview = function () {
    text_wrapper.children().remove();
    solution_wrapper.children().remove();
    text_wrapper.append('<div class="input_field"><span id="preview_template_text" class="static-math input_mathquill"></span>');
    MathQuill.StaticMath($('#preview_template_text')[0]).latex(templateText_latex);
    for (var s = 0; s < templateSolution_latex.length; s++) {
        solution_wrapper.append('<div class="input_field"><div id="preview_solution_step_' + s + '" class="static-math"></div></div><br/>');
        MathQuill.StaticMath($('#preview_solution_step_' + s)[0]).latex(templateSolution_latex[s]);
    }
};

var processToggle = function () {
    var $toggle_button = $(this);
    var template_id = $toggle_button.data('template_id');
    var post_url = '/user/level/template/' + template_id + '/toggle/';
    console.log($toggle_button.data('template_id'));

    $.post(post_url, {'csrfmiddlewaretoken': getCookie('csrftoken')}, function (result) {
        console.log(result);
        $('#toggle_button_id_' + template_id).toggleClass('btn-primary btn-danger').children().toggleClass('glyphicon-plus glyphicon-minus');
        $('#current_level_button').effect('highlight',{ 'color': '#5cb85c' });


    })
};

/**
 * Add an error message under the given element.
 * @param {string} selector - id or class-name of the element to apply error message to.
 * @param {string} message - the error message.
 */
function notification(selector, message) {
    var element = $(selector);
    if (selector[0] != "." && selector[0] != "#") {
        element = $('#' + selector);
    }
    $(document).ready(function () {
        element.after('<p class="notification_content">* ' + message + '</p>');
        $('.notification_content').show(100).delay(1000).hide(100).queue(function () {
            $(this).remove();
        });
    });
}

$(document).ready(function () {

    $('.ajax-toggle-button').click(_.debounce(processToggle,
        MILLS_TO_IGNORE_REQUESTS, true
    ));

    $('.preview-button').click(function () {


        var button = $(this);
        var template_id = button.data('template_id'); // Extract info from data-* attributes
        var template_title = button.data('template_title');
        var json_url = '/template/' + template_id + '/preview/';

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
    });

});

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
});