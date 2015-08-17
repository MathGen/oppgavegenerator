/**
 * @file Manages user interaction in the level editor and handles ajax server-requests for saving changes.
 * Requires jQuery / MathQuill / Bootstrap
 * The file is used in the following HTML-files: todo: list files here
 */

$(document).ready(function () {

    var container = $('#object_container');
    var modal = "";
    var delete_url = "";
    var load_url = "";
    var templateText_latex = "";
    var templateSolution_latex = {};
    var text_wrapper = $('#modal_template_text');
    var solution_wrapper = $('#modal_template_solution');

    // Button listener for previewing items in search results box
    $(document).on('click', '.preview-button', function () {
        var button = $(this);
        var template_id = button.data('template_id'); // Extract info from button data-* attributes
        var template_title = button.data('template_title');
        var json_url = '/template/' + template_id + '/preview/';

        $.getJSON(json_url, function (data) {
            templateText_latex = data.template_text;
            templateSolution_latex = data.template_solution.split('§');
            console.log('getJSON - template_text: ' + templateText_latex + ", solution: " + templateSolution_latex);
        });

        $('#previewModal').modal('show').on('shown.bs.modal', function () {
            modal = $('#previewModal');
            text_wrapper.children().remove();
            solution_wrapper.children().remove();
            text_wrapper.append('<div class="input_field"><span id="preview_template_text" class="static-math input_mathquill"></span>');
            MathQuill.StaticMath($('#preview_template_text')[0]).latex(templateText_latex);
            for (var s = 0; s < templateSolution_latex.length; s++) {
                solution_wrapper.append('<div class="input_field"><div id="preview_solution_step_' + s + '" class="static-math"></div></div><br/>');
                MathQuill.StaticMath($('#preview_solution_step_' + s)[0]).latex(templateSolution_latex[s]);
            }
            modal.find('.modal-title').text('Forhåndsvisning av ' + '"' + template_title + '"');
            redraw_mathquill_elements();
        });
    });

    // Initialize object order-sorting
    $(document).on('click', '.btn-edit-order', function () {
        init_sortable();
        var button = $(this);
        button.toggleClass('btn-default btn-primary');
        button.toggleClass('btn-edit-order btn-save-order');
        button.text('Lagre rekkefølge');
    });

    // Commit changes to object order on click
    $(document).on('click', '.btn-save-order', function () {
        $('.sortable').sortable({
            disabled: true
        });
        var button = $(this);
        button.toggleClass('btn-default btn-primary');
        button.toggleClass('btn-save-order btn-edit-order');
        button.text('Endre rekkefølge');
        $('.sortable-handle').hide();
        $('.object-options').fadeIn();
        save_changes();
    });

    // Open delete confirmation modal
    $(document).on('click', '.btn-delete-object', function () {
        modal = $('#deleteModal');
        var button = $(this);
        var object_id = button.data('object-id');
        var object_title = button.data('object-title');
        var object_type = button.data('object-type');
        console.log("Confirming deletion of object type: " + object_type + " with id: " + object_id);
        if (object_type == 'set') {
            delete_url = '/set/' + object_id + '/remove/';
            load_url = '/user/sets/ #object_container > *';
        } else if (object_type == "chapter") {
            delete_url = '/set/' + current_set + '/chapter/' + object_id + '/remove/';
            load_url = '/set/' + current_set + '/chapters/ #object_container > *';
        } else if (object_type == "level") {
            delete_url = '/chapter/' + current_chapter + '/level/' + object_id + '/remove/';
            load_url = '/chapter/' + current_chapter + '/levels/ #object_container > *'
        } else if (object_type == "template") {
            delete_url = '/level/' + current_level + '/template/' + object_id + '/remove/';
            load_url = '/level/' + current_level + '/templates/ #object_container > *'
        } else {
            console.log('Error: Requested object has no type.');
        }

        modal.find('.modal-alert').text('Bekreft sletting av "' + object_title + '."');
        // debug:
        //console.log('opening confirm deletion modal for object-id: ' + object_id);
        //console.log('current deletion url is: ' + delete_url);
        modal.modal('show');
    });

    // Confirm deletion of object ( Modal delete button )
    $(document).on('click', '#confirmDelete', function () {
        $.post(delete_url, {'csrfmiddlewaretoken': getCookie('csrftoken')}, function (result) {
            $('#deleteModal').modal('hide');
            container.load(load_url);
            window.console.log(result);
        });

    });

    // Open object title-editing modal
    $(document).on('click', '.btn-edit-title', function () {
        modal = $('#titleModal');
        $('.new-title').val($('#current_object_title').text());
        console.log(modal);
        modal.modal('show');
    });

    // Change title and save changes if new object title is input
    $(document).on('click', '#confirmTitleChange', function () {
        title_input = $('.new-title');
        new_title = title_input.val();
        console.log('new title: ' + new_title);
        $('#current_object_title').text(new_title);
        modal.modal('hide');
        save_changes();
        title_input.val("");
    }).on('keyup', '.new-title', function (e) {
        if (/(13)/.test(e.which)) $('#confirmTitleChange').click(); // Change title on key press
    });

    // Close current open Bootstrap modal
    $('.hidemodal').click(function () {
        console.log('closing modal');
        modal.modal('hide');
        //delete_content($(this).closest('li'));
    });

    // Adding new content from the input-field. Posting to server.
    $(document).on('focusout', '.new_content', function () {
        add_new_content($(this));
    }).on('keyup', '.new_content', function (e) {
        if (/(13)/.test(e.which)) $(this).focusout(); // Add chapter if one of these keys are pressed.
    });

    // Sends the search-query when either the search-button or 'enter' key is pressed.
    $(document).on('click', '#search_submit', function () {
        object_search($('#search_input').val());
        //load_search_results();
    }).on('keyup', '#search_input', function (e) {
        if (/(13)/.test(e.which)) $('#search_submit').click();
    });

    // Button listener for copying objects from the search-result box
    $(document).on('click', '.btn-copy-object', function () {
        var button = $(this);
        var add_url = "";
        var object_type = button.data('object-type');
        var object_id = button.data('object-id');
        if (object_type == 'set') {
            add_url = '/set/' + object_id + '/add/';
            load_url = '/user/sets/ #object_container > *';
        } else if (object_type == 'chapter') {
            add_url = '/set/' + current_set + '/chapter/' + object_id + '/add/';
            load_url = '/set/' + current_set + '/chapters/ #object_container > *';
        } else if (object_type == 'level') {
            add_url = '/chapter/' + current_chapter + '/level/' + object_id + '/add/';
            load_url = '/chapter/' + current_chapter + '/levels/ #object_container > *';
        } else if (object_type == 'template') {
            add_url = '/level/' + current_level + '/template/' + object_id + '/add/';
            load_url = '/level/' + current_level + '/templates/ #object_container > *';
        } else {
            console.log("Unkown object type: " + object_type);
        }

        $.post(add_url, {'csrfmiddlewaretoken': getCookie('csrftoken')}, function (result) {
            console.log(result);
            container.load(load_url);
        });
    });

    $(document).on('click', '.btn-add', function () {
        add_new_content_from_search($(this).attr('id').replace(/search_content_/g, ''));
    });

    // Open modal for editing progression factor (level-editor)
    $(document).on('click', '.btn-edit-kfactor', function () {
        init_k_factor_slider();
        modal = $('#progressionModal');
        modal.modal('show')
    });

    // Commit changes on click
    $(document).on('click', '#confirmProgression', function () {
        modal.modal('hide');
        save_changes();
    });

});

function add_new_content_from_search(content_id) {
    $.get($('#search_url_' + content_id).text(), function (result) {
        window.console.log(result);
        $('#object_container').load(window.location.pathname + "#object_container > *");
    });
}

/**
 * Save changes to object.
 */
function save_changes() {
    var valid_form = true;
    var form_submit = {};
    var title = $('#current_object_title').text();
    var order = get_content_order();
    var content = $('#object_container');
    if (content.hasClass('edit_chapters')) {
        content = 'set';
        form_submit['set_id'] = current_set;
        form_submit['title'] = title;
        form_submit['order'] = order;
    } else if (content.hasClass('edit_levels')) {
        content = 'chapter';
        form_submit['chapter_id'] = current_chapter;
        form_submit['title'] = title;
        form_submit['order'] = order;
    } else if (content.hasClass('edit_templates')) {
        content = 'level';
        form_submit['level_id'] = current_level;
        form_submit['title'] = title;
        form_submit['k_factor'] = $('#k_factor_amount').text();
    } else {
        window.console.log('#edit_container is missing a required class for POST.');
        valid_form = false;
    }
    if (valid_form) {
        form_submit["csrfmiddlewaretoken"] = getCookie('csrftoken');
        $.post('/' + content + '/update/', form_submit, function (result) {
            console.log(result);
            show_success_indicator();
        });
    }
}

/**
 * Iterates and write the order of the content to an Array.
 * @returns {String} The order represented as a String.
 */
function get_content_order() {
    var order = [];

    $('#object_container').find('.panel-default').each(function () {
        order.push($(this).data('object_id'));
    });
    return order.join(',');
}

/**
 * Initialize the slider which sets the progression-speed for the level.
 */
function init_k_factor_slider() {
    var k_value = $('#k_factor_amount').text();
    if (k_value == '') {
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
 * Adding a new content depending on which container-type the user is active in. (Set/Chapter/Level)
 * @param {String} input - the input string that will be the title of the content.
 */
function add_new_content(input) {
    var container = $('#object_container');
    var load_url = "";
    var text = input.val();
    if (text) {
        var content_path = '/set/' + text + '/new_set/';
        load_url = '/user/sets/ #object_container > *';
        if (input.hasClass('input-chapter-name')) {
            content_path = '/set/' + current_set + '/' + text + '/new_chapter/';
            load_url = '/set/' + current_set + '/chapters/ #object_container > *'
        } else if (input.hasClass('input-level-name')) {
            content_path = '/chapter/' + current_chapter + '/' + text + '/new_level/';
            load_url = '/chapter/' + current_chapter + '/levels/ #object_container > *'
        }
        $.post(content_path, {'csrfmiddlewaretoken': getCookie('csrftoken')}, function (result) {
            console.log(result);
            container.load(load_url);
            init_sortable();
        });
    }
    input.val("");
}

/**
 * Initialize the drag-and-drop functionality for the listed contents. Sortable.
 */
function init_sortable() {
    //TODO: make it switchable (from list to grid)
    var container = $('.sortable');
    $('.object-options').fadeOut(400, function() {$('.sortable-handle').fadeIn()});
    container.sortable({
        disabled: false,
        placeholder: "list_content_highlight",
        containment: "#object_container",
        axis: "y",
        cursor: "move"
    }).disableSelection();
}

function object_search(search_string) {
    var search_container = $('.search_container');
    var type = search_container.attr('id').replace(/search_/g, "");
    search_container.load('/minisearch/' + type + '?q=' + search_string + ' .search_container > *', function (result) {
        // Show the search results
        search_container.html(result);
        search_container.show("fade", {'direction': 'up'});
    });
}

function show_success_indicator() {
    $('#save_success').show(100).delay(500).hide(500);
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