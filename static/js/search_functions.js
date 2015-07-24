var MILLS_TO_IGNORE_REQUESTS = 500;
var VARIABLES = ['a','b','c','d'];

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

var processAdd = function () {

    var $button_just_clicked = $(this);

    var template_id = $button_just_clicked.data('template_id');
    console.log($button_just_clicked.data('template_id'));

    var processServerResponse = function (serverResponse_data, textStatus_ignored, jqXHR_ignored) {
        //console.log("sf serverResponse_data='" + serverResponse_data + "', textStatus_ignored='" + textStatus_ignored + "', jqXHR_ignored='" + jqXHR_ignored + "', template_id='" + template_id + "'");
        $('#toggle_template_add_id_' + template_id).html(serverResponse_data);
    };

    var config = {
        url: "/user/level/template/" + template_id + "/toggle/",
        dataType: 'html',
        success: processServerResponse,
        fail: 'error!'
    };

    $.ajax(config);
};

$(document).ready(function () {

    $('.span__toggle_template_add_button').click(_.debounce(processAdd,
        MILLS_TO_IGNORE_REQUESTS, true
    ));

    $('.span__toggle_template_preview_button').click(function () {


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