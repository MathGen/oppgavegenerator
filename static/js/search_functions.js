var MILLS_TO_IGNORE_REQUESTS = 500;

$('#previewModal').on('show.bs.modal', function (event) {
    var modal = $(this);
    var button = $(event.relatedTarget); // Button that triggered the modal
    var template_id = button.data('template_id'); // Extract info from data-* attributes
    var template_title = button.data('template_title');
    var jsonurl = '/template/' + template_id + '/preview/';

    $.getJSON(jsonurl, function (data) {
        modal.find('.template-text').html(data.template_text);
        modal.find('.template-solution').text(data.template_solution);
        redraw_mathquill_elements()
    });
});

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
//    $( '#nav_level_name' ).effect( "highlight" )
};

$(document).ready(function () {

    $('.span__toggle_template_add_button').click(_.debounce(processAdd,
        MILLS_TO_IGNORE_REQUESTS, true
    ));
});