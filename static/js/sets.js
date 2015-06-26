$(document).ready(function () {
    //TODO: make it switchable (from list to grid)
    $('#edit_container').sortable({placeholder:"list_content_highlight", containment:"#set_editor", axis:"y"}).disableSelection();
    //$('#chapter_container').sortable({containment:"#chapter_container"}).disableSelection();
    //$('.list_chapter').draggable({containment:"#chapter_container", axis:"y"});

    // Delete the specific content.
    $(document).on('click', '.btn_content_del', function(){
        delete_content($(this).closest('li'));
    });

    // Edit the specific content.
    $(document).on('click', '.btn_content_edit', function(){
        edit_content($(this).closest('li'));
    });

    $(document).on('focusout', '.new_content', function(){ //TODO: make grid element if in grid-view.
		add_new_content($(this));
	}).on('keyup', '.new_content', function(e){
		if(/(188|13)/.test(e.which)) $(this).focusout(); // Add chapter if one of these keys are pressed.
	});
});

// TODO: make it work with levels as well.
function add_new_content(input){
    var text = input.val().replace(/[^a-zA-Z0-9\+\-\.#ÆØÅæøåA]/g, ''); // Allowed characters
    if (text) {
        var content_path = '../'+ text +'/new_chapter/';
        if($('#edit_container').hasClass('edit_levels')) {
            content_path = '../../../chapter/'+ $('#chapter_id').text() +'/'+ text +'/new_level/';
        }
        $.post(content_path, {'csrfmiddlewaretoken': getCookie('csrftoken')}, function(result){
            $('#edit_container').append(
                '<li id="content_'+result+'" class="btn list_content">' +
                '<h4 class="content_title">' + text + '<small>  ny</small></h4>' +
                '<a class="btn btn_content_edit">Edit</a>' +
                '<a class="btn btn_content_del"><span class="glyphicon glyphicon-trash"></span></a>' +
                '</li>');
        });
    }
    input.val("");
}

// TODO: make it work with levels as well. set/(\d+)/chapter/(\d+)/remove_chapter
function delete_content(content){
    var content_id = content.attr('id').match(/\d+/);
    if(content_id){
        var content_path = '../chapter/'+ content_id +'/remove_chapter/';
        if($('#edit_container').hasClass('edit_levels')) {
            content_path = '../../../chapter/'+ $('#chapter_id').text() +'/level/'+ content_id +'/remove_level/';
        }
        $.post(content_path, {'csrfmiddlewaretoken': getCookie('csrftoken')}, function(result){
            if(result[0] == 's'){ // if success, delete the visual content.
                content.remove();
            }
            window.console.log(result);
        });
    }
}

function edit_content(content){
    var content_id = content.attr('id').match(/\d+/);
    if(content_id){
        var content_type = "level";
        if($('#edit_container').hasClass('edit_chapters')) {
            content_type = "chapter";
        }
        $('#set_editor').fadeOut('fast', function(){
            $(this).load('../../../'+content_type+'/'+content_id+'/edit/ #set_editor > *').fadeIn('fast');
        });
    }
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