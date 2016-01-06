/**
 * Created by eirikk on 04/01/16.
 */
/** Making a separate file for this as to not add even more lines to gen.js
 *  These are functions for hiding/showing the variable overview drawer and
 *  displaying everything correctly. */

$(document).ready(function () {
    build_overview();
    $('#draggable-overview').draggable();
    $('#variable-overview').resizable({
        handles: "n,s,e,w",
        minWidth: 165
    });

    $(document).on('input', '.ow_domain_from', function() {
        var input = $(this);
        var var_id = input.data('var-id');
        $('#o_adv_from_' + var_id).val(input.val());
    });
    $(document).on('input', '.ow_domain_to', function() {
        var input = $(this);
        var var_id = input.data('var-id');
        $('#o_adv_to_' + var_id).val(input.val());
    });
    $(document).on('input', '.ow_domain_dec', function() {
        var input = $(this);
        var var_id = input.data('var-id');
        $('#o_adv_dec_' + var_id).val(input.val());
    })

});

var overview = $('#variable-overview');
var calc_overview = $('#calculations_overview');
var vars_overview = $('#vars_overview');
var centered_content = $('#centeredContent');

$('.variable-overview-show').click(function () {
    centered_content.css('margin-left', '10px');
    overview.show('slide', {'direction': 'right'});
    redraw_mathquill_elements();
    refresh_all_char_colors()
});

$('.variable-overview-close').click(function () {
    centered_content.css('margin', 'auto');
    overview.hide('slide', {'direction': 'right'});
});

$('.variable-overview-refresh').click(function () {
    build_overview();
});

function build_overview() {
    calc_overview.empty();
    vars_overview.empty();
    var calc_variables = [];
    // get and display calculation variables
    if (Object.keys(dict_calc_unchanged).length > 0) {
        for (var c in dict_calc_unchanged) {
            var c_char = "A";
            var c_index = parseInt(c);
            var c_latex = dict_calc_unchanged[c];
            c_char = String.fromCharCode(c_char.charCodeAt(0) + c_index);
            calc_variables.push({
                calc_char: c_char,
                calc_content: c_latex
            });
            calc_overview.append(
                '<div class="overview-calc-entry">' +
                '<button class="pull-right btn btn-xs btn-success btn_calc_edit btn_calc_edit_' + c_index + '"><span class="glyphicon glyphicon-pencil"></span></button>' +
                '<div class="pull-left content_calc">' +
                '<div class="input_field">' +
                '<span class="static-math input_mathquill mq-math-mode">' +
                '<var class="content_calc">' + c_char + '</var></span></div></div>' +
                '<div class="input_field">' +
                '<span class="static-math input_mathquill mq-math-mode">' + c_latex + '</span></div></div><hr>')
        }
    } else {
        calc_overview.append(
            '<p>Ingen utregninger enda.</p>'
        )
    }

    // get and display random variables
    // this is a toughie since random variable definitions aren't stored in a dictionary like calculation variables
    // and we need to check input fields to display them
    var variables = [];
    if (Object.keys(VARIABLES).length > 0) {
        for (var v in VARIABLES) {
            var v_rdomain = [];
            var v_sequence = [];
            var v_char_split = VARIABLES[v].split('§');
            var v_char = v_char_split[1];
            // get values from sequence type variable
            if ($('#o_adv_sequence_' + v).is(':checked')) {
                $('#o_adv_sequence_container_' + v).find('.o_seq').each(function () {
                    v_sequence.push(get_latex_from_mathfield($(this).find('.static-math-sm')));
                });
                v_content = v_sequence.join();
                variables.push({
                    var_char: v_char,
                    var_content: v_content
                })
            } else { // get random domain for variable
                var v_from = $('#o_adv_from_' + v).val();
                var v_to = $('#o_adv_to_' + v).val();
                var v_dec = $('#o_adv_dec_' + v).val();
                var v_content = "Fra " + v_from + " til " + v_to + ".<br>" + v_dec + " desimaler.";
                variables.push({
                    var_char: v_char,
                    var_from: v_from,
                    var_to: v_to,
                    var_dec: v_dec
                })
            }
        }
        for (var n in variables) {
            vars_overview.append(
                '<div class="overview-var-entry">' +
                '<div class="pull-left content_var" style="font-size: 14px">' +
                variables[n].var_char +
                '</div>' +
                '<span class="form-inline">' +
                '<input id="ow_adv_from_' + n + '" type="number" class="form-control input-sm ow_domain_from" placeholder="Fra" data-var-id="'+ n +'">' +
                '<input id="ow_adv_to_' + n + '" type="number" class="form-control input-sm ow_domain_to" placeholder="Til" data-var-id="'+ n +'">' +
                '<input id="ow_adv_dec_' + n + '" type="number" class="form-control input-sm ow_domain_dec" placeholder="Desi" data-var-id="'+ n +'">' +
                '</span>' +
                '</div><hr>'
            );
            $('#ow_adv_from_' + n).val(variables[n].var_from);
            $('#ow_adv_to_' + n).val(variables[n].var_to);
            $('#ow_adv_dec_' + n).val(variables[n].var_dec);
        }
    } else {
        vars_overview.append(
            '<p>Ingen variabler enda.</p>'
        )
    }
    redraw_mathquill_elements();
    refresh_all_char_colors();
}
