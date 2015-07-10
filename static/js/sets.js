var current_set = 0;
var current_chapter = 0;
$(document).ready(function () {
    set_title('#content_title', $('#get_content_title').text());
    init_sortable();
    load_search_view();

    // Delete the specific content.
    $(document).on('click', '.btn_content_del', function(){
        delete_content($(this).closest('li'));
    });

    $(document).on('click', '.btn_set_back', function(){
        load_previous_page();
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

    // Sends the search-query when either the search-button or 'enter' key is pressed.
    $(document).on('click', '#search_submit', function(){
        search_for($('#search_input').val());
    }).on('keyup', '#search_input', function(e){
        if(/(13)/.test(e.which)) $('#search_submit').click();
    });

    $(document).on('click', '.btn_add_content', function(){
        add_new_content_from_search($(this).attr('id').replace(/search_content_/g, ''));
    });

    init_k_factor_slider();
});

function add_new_content_from_search(content_id){
    $.get($('#search_url_' + content_id).text(), function(result){
        window.console.log(result);
        var parsed = JSON.parse(result);

        $('#edit_container').append(
                '<li id="content_' + parsed["id"] + '" class="btn list_content">' +
                '<h4 class="content_title">' + parsed["name"] + '<small>  ny</small></h4>' +
                '<a class="btn btn_content_edit">Edit</a>' +
                '<a class="btn btn_content_del"><span class="glyphicon glyphicon-trash"></span></a>' +
                '</li>');
    });



}

/**
 * Saves changes such as content-order and content-title to the server.
 */
function save_changes(){
    var valid_form = true;
    var form_submit = {};
    var title = $('#content_title').val();
    var order = get_content_order();
    var content = $('#edit_container');
    if (content.hasClass('edit_chapters')){
        content = 'set';
        form_submit['set_id'] = $('#set_id').text();
        form_submit['title'] = title;
        form_submit['order'] = order;
    } else if (content.hasClass('edit_levels')){
        content = 'chapter';
        form_submit['chapter_id'] = $('#chapter_id').text();
        form_submit['title'] = title;
        form_submit['order'] = order;
    } else if (content.hasClass('edit_templates')){
        content = 'level';
        form_submit['level_id'] = $('#level_id').text();
        form_submit['title'] = title;
        form_submit['k_factor'] = $('#k_factor_amount').text();
    } else {
        window.console.log('#edit_container is missing a required class for POST.');
        valid_form = false;
    }
    if(valid_form) {
        form_submit["csrfmiddlewaretoken"] = getCookie('csrftoken');
        $.post('/' + content + '/update/', form_submit, function(result){
            if(result[0] == 'S'){
                $('#update_text').text(result);
                $('#update_success').show(100).delay(5000).hide(100);
            }
            else{
                window.console.log('Failed to update: ' + result);
            }
        });
    }
}

/**
 * Loads the previous page/view.
 */
function load_previous_page(){
    if(current_set != 0 || current_chapter != 0) {
        var content = $('#edit_container');
        var return_to = "set";
        var return_id = 1;
        if (content.hasClass('edit_levels')) {
            return_to = "set";
            return_id = current_set;
        } else if (content.hasClass('edit_templates')) {
            return_to = "chapter";
            return_id = current_chapter;
        }
        $('#set_editor').fadeOut('fast', function () {
            $(this).load('../../../' + return_to + '/' + return_id + '/edit/ #set_editor > *', function () {
                set_title('#content_title', $('#get_content_title').text());
                init_sortable();
                scroll_to($('#set_editor'));
                redraw_mathquill_elements(); //TODO: redraw after the content is displayed. BUG: delayed content.
                load_search_view();
                $(this).fadeIn('fast');
            });
        });
    } else {
        $('#set_editor').fadeOut('fast', function () {
            $(this).load('../../../set #set_editor > *', function () {
                set_title('#content_title', $('#get_content_title').text());
                init_sortable();
                scroll_to($('#set_editor'));
                load_search_view();
                $(this).fadeIn('fast');
            });
        });
    }
}

/**
 * Iterates and write the order of the content to an Array.
 * @returns {String} The order represented as a String.
 */
function get_content_order(){
    var order = [];
    $('#edit_container').find('li').each(function(){
        order.push($(this).attr('id').match(/\d+/));
    });
    return order.join(',');
}

/**
 * Init the slider which sets the progression-speed for the level.
 */
function init_k_factor_slider(){
    var k_value = $('#k_factor_amount').text();
    if(k_value == ''){
        k_value = 3;
    }
    $('#k_factor_slider').slider({
        value: k_value,
        min: 1,
        max: 8,
        step: 1,
        slide: function (event, ui) {
            $('#k_factor_amount').text(ui.value);
        }
    });
}

/**
 * Set the title of the set/chapter/level
 * @param {string} input - which input-field to write to.
 * @param {string} title - the title.
 */
function set_title(input, title){
    $(input).val(title);
}

/**
 * Adding a new content depending on which container-type the user is active in. (Set/Chapter/Level)
 * @param {String} input - the input string that will be the title of the content.
 */
function add_new_content(input){
    var container = $('#edit_container');
    var text = input.val();
    if (text) {
        var content_path = '/set/'+ text +'/new_set/';
        if(container.hasClass('edit_chapters')) {
            content_path = '/set/'+ $('#set_id').text() +'/'+ text +'/new_chapter/';
        } else if(container.hasClass('edit_levels')) {
            content_path = '/chapter/'+ $('#chapter_id').text() +'/'+ text +'/new_level/';
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

/**
 * Delete the specific content.
 * @param {object} content - the content selector
 */
function delete_content(content){
    var container = $('#edit_container');
    var content_id = content.attr('id').match(/\d+/);
    if(content_id){
        var content_path = '/set/'+ content_id + '/remove_set/';
        if(container.hasClass('edit_chapters')) {
            content_path = '/set/'+ $('#set_id').text() +'/chapter/'+ content_id +'/remove_chapter/';
        } else if(container.hasClass('edit_levels')) {
            content_path = '/chapter/'+ $('#chapter_id').text() +'/level/'+ content_id +'/remove_level/';
        }
        $.post(content_path, {'csrfmiddlewaretoken': getCookie('csrftoken')}, function(result){
            if(result[0] == 's'){ // if success, delete the visual content.
                content.remove();
            }
            window.console.log(result);
        });
    }
}

/**
 * Loads the search view, with the specific search-filter for each chapters/levels/templates.
 */
function load_search_view(){ // TODO: make the search result load with AJAX.
    var search_container = $('.search_container');
    var type = search_container.attr('id').replace(/search_/g, "");
    switch (type) {
        case 'sets':
            search_container.remove();
            break;
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

/**
 * Loads the specific element to edit its content.
 * @param {object} content - the content-selector.
 */
function edit_content(content){
    var container = $('#edit_container');
    var content_id = content.attr('id').match(/\d+/);
    if(content_id){
        var content_type = "set";
        if(container.hasClass('edit_chapters')) {
            content_type = "chapter";
            current_set = $('#set_id').text();
        } else if(container.hasClass('edit_levels')){
            content_type = "level";
            current_chapter = $('#chapter_id').text(); // TODO; improve cache of current content-type for loading previous pages.
        }
        $('#set_editor').fadeOut('fast', function(){ // TODO: Improve load callback.
            $(this).load('/'+content_type+'/'+content_id+'/edit/ #set_editor > *', function(){
                set_title('#content_title', $('#get_content_title').text());
                init_sortable();
                scroll_to($('#set_editor'));
                redraw_mathquill_elements(); //TODO: redraw after the content is displayed. BUG: delayed content.
                load_search_view();
                init_k_factor_slider();
                $(this).fadeIn('fast');
            });
        });
    }
}

/**
 * Initialize the drag-and-drop functionality for the listed contents. Sortable.
 */
function init_sortable(){
    //TODO: make it switchable (from list to grid)
    var container = $('#edit_container');
    if(container.hasClass('edit_templates') || container.hasClass('edit_sets')){}
    else {
        container.sortable({
            placeholder: "list_content_highlight",
            containment: "#set_editor",
            axis: "y"
        }).disableSelection();
    }
    //$('#chapter_container').sortable({containment:"#chapter_container"}).disableSelection();
    //$('.list_chapter').draggable({containment:"#chapter_container", axis:"y"});
}

function search_for(search_string){
    var search_container = $('.search_container');
    var type = search_container.attr('id').replace(/search_/g, "");
    search_container.load('/minisearch/'+ type +'?q='+ search_string + ' .search_container > *', function(result){
        search_container.html(result);
    });
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