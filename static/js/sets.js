$(document).ready(function () {
    //TODO: make it switchable (from list to grid)
    $('#edit_container').sortable({placeholder:"list_content_highlight", containment:"#set_editor", axis:"y"}).disableSelection();
    //$('#chapter_container').sortable({containment:"#chapter_container"}).disableSelection();
    //$('.list_chapter').draggable({containment:"#chapter_container", axis:"y"});

    $('.new_content').on('focusout', function(){ //TODO: make grid element if in grid-view.
		add_new_content($(this));
	}).on('keyup', function(e){
		if(/(188|13)/.test(e.which)) $(this).focusout(); // Add chapter if one of these keys are pressed.
	});
});

function add_new_content(input){
    var text = input.val().replace(/[^a-zA-Z0-9\+\-\.#ÆØÅæøåA]/g, ''); // Allowed characters
    if (text) {
        $.post('../' + text + '/new_chapter/', {'csrfmiddlewaretoken': getCookie('csrftoken')}, function(result){
            $('#edit_container').append(
                '<li id="chapter_'+result+'" class="btn list_content">' +
                '<h4 class="content_title">' + text + '<small>  ny</small></h4>' +
                '<a class="btn btn_content_edit">Edit</a>' +
                '<a class="btn btn_content_del"><span class="glyphicon glyphicon-trash"></span></a>' +
                '</li>');
        });
    }
    input.val("");
}

/**
 *Gets a cookie and returns its value
 * @param {string} name - the name of the cookie to get.
 * @returns {string} - Returns the value of the cookie specified.
 */
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}