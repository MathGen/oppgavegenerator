$(document).ready(function () {
    load_set_editor($('#set_id').text());

    //TODO: make it switchable (from list to grid)
    $('#edit_container').sortable({placeholder:"list_content_highlight", containment:"#set_editor", axis:"y"}).disableSelection();
    //$('#chapter_container').sortable({containment:"#chapter_container"}).disableSelection();
    //$('.list_chapter').draggable({containment:"#chapter_container", axis:"y"});

    $('.new_content').on('focusout', function(){ //TODO: make grid element if in grid-view.
		var text = $(this).val().replace(/[^a-zA-Z0-9\+\-\.#ÆØÅæøåA]/g,''); // Allowed characters
		if(text){
			$('#edit_container').append(
                '<li class="btn list_content">' +
                    '<h4 class="content_title">'+ text +'<small>  ny</small></h4>' +
                    '<a class="btn btn_content_edit">Edit</a>' +
                    '<a class="btn btn_content_del"><span class="glyphicon glyphicon-trash"></span></a>' +
                '</li>');
		}
		$(this).val("");
	}).on('keyup', function(e){
		if(/(188|13)/.test(e.which)) $(this).focusout(); // Add chapter if one of these keys are pressed.
	});
});

function load_set_editor(set_id){
    if(set_id){

    }
    else{

    }
}