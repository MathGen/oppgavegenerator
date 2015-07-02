$(document).ready(function () {
    set_title('#content_title', $('#get_content_title').text());
    init_sortable();
    load_search_view($('.search_container').attr('id').replace(/search_/g, ""));

    // Delete the specific content.
    $(document).on('click', '.btn_content_del', function(){
        delete_content($(this).closest('li'));
    });

    // Edit the specific content.
    $(document).on('click', '.btn_content_edit', function(){
        edit_content($(this).closest('li'));
    });

    // Save changes
    $('#btn_save_set').click(function(e){
        e.preventDefault();
        save_changes();
    });

    // Adding new content from the input-field. Posting to server.
    $(document).on('focusout', '.new_content', function(){ //TODO: make grid element if in grid-view.
		add_new_content($(this));
	}).on('keyup', '.new_content', function(e){
		if(/(13)/.test(e.which)) $(this).focusout(); // Add chapter if one of these keys are pressed.
	});
});

function save_changes(content_id){
    var valid_form = true;
    var form_submit = {};
    var title = $('#content_title').val();
    var order = get_content_order();
    var content = $('#edit_container');
    if (content.hasClass('edit_chapters')){
        content = 'set';
        form_submit['set_id'] = content_id;
        form_submit['title'] = title;
        form_submit['order'] = order;
    } else if (content.hasClass('edit_levels')){
        content = 'chapter';
        form_submit['chapter_id'] = content_id;
        form_submit['title'] = title;
        form_submit['order'] = order;
    } else if (content.hasClass('edit_templates')){
        content = 'level';
        form_submit['level_id'] = content_id;
        form_submit['title'] = title;
        //form_submit['k_factor'] = 1; // TODO: implement k_factor in the editor.
    } else {
        window.console.log('#edit_container is missing a required class for POST.');
        valid_form = false;
    }
    if(valid_form) {
        form_submit["csrfmiddlewaretoken"] = getCookie('csrftoken');
        $.post('../../../' + content + '/update/', form_submit, function(result){
            if(result[0] == 'c'){
                $('#update_success').show(100).delay(5000).hide(100).queue(function () {
                    $(this).remove();
                });
            }
        });
    }
}

/**
 * Iterates and write the order of the content to an Array.
 * @returns {Array} The order represented as a list.
 */
function get_content_order(){
    var order = [];
    $('#edit_container').find('li').each(function(){
        order.push($(this).attr('id').match(/\d+/));
    });
    return order;
}

/**
 * Set the title of the set/chapter/level
 * @param {string} input - which input-field to write to.
 * @param {string} title - the title.
 */
function set_title(input, title){
    $(input).val(title);
}

function add_new_content(input){
    var text = input.val();
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

function load_search_view(type){ // TODO: make the search result load with AJAX.
    var search_container = $('.search_container');
    switch (type) {
        case 'chapters':
            search_container.load('../../../minisearch/chapters', function(){
                //callback function
            });
            break;
        case 'levels':
            search_container.load('../../../minisearch/levels', function(){
                //callback function
            });
            break;
        case 'templates':
            search_container.load('../../../minisearch/templates', function(){
                //callback function
            });
            break;
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
            $(this).load('../../../'+content_type+'/'+content_id+'/edit/ #set_editor > *').fadeIn('fast', function(){
                set_title('#content_title', $('#get_content_title').text());
                init_sortable();
                scroll_to($('#set_editor'));
                redraw_mathquill_elements(); //TODO: redraw after the content is displayed. BUG: delayed content.
            });
        });
    }
}

/**
 * Initialize the drag-and-drop functionality for the listed contents. Sortable.
 */
function init_sortable(){
    //TODO: make it switchable (from list to grid)
    $('#edit_container').sortable({placeholder:"list_content_highlight", containment:"#set_editor", axis:"y"}).disableSelection();
    //$('#chapter_container').sortable({containment:"#chapter_container"}).disableSelection();
    //$('.list_chapter').draggable({containment:"#chapter_container", axis:"y"});
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