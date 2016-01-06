$(document).ready(function () {

});

var user_pw = '';
var join_button = $('.btn_add_user_to_set');
var user_to_remove_id = 0;
var confirm_remove_button = $('#confirmRemoveUser');
var modal = '';

join_button.click(function () {
    console.log('hellooo');
    var pw_required = join_button.data('pw-required');
    console.log(pw_required);
    if (pw_required) {
        var pw_input = $('#joinSetPassword');
        user_pw = pw_input.val();
        if (user_pw == '') {
            window.alert('Vennligst tast inn passord for å bli med i kurset.')
        } else {
            add_user_to_set();
        }
    } else {
        add_user_to_set();
    }
});

$(document).on('click', '.btn-remove-student', function () {
    button = $(this);
    modal = $('#removeUserModal');
    modal.modal('show');
    user_to_remove_id = button.data('object-id');
    console.log('confirming removal of user with id:' + user_to_remove_id + ' from set-id:' + current_set)
});

confirm_remove_button.click(function () {
    remove_user_from_set();
    modal.modal('hide');
});

$('.hidethemodal').click(function () {
    console.log('closing modal');
    modal.modal('hide');
});

function add_user_to_set() {
    $.post('/add-user-to-set/', {
        'csrfmiddlewaretoken': getCookie('csrftoken'),
        'set_id': set_id,
        'password': user_pw
    }, function (result) {
        console.log(result);
        location.reload();
    });
}

function remove_user_from_set() {
    $.post('/remove-user-from-set/', {
        'csrfmiddlewaretoken': getCookie('csrftoken'),
        'set_id': current_set,
        'user_id': user_to_remove_id
    }, function (result) {
        console.log(result);
        location.reload();
    });
}
