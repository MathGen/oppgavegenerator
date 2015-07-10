var graph;
var helper_expression = {};
$(document).ready(function(){
    var graph_initialized = false;
    // Open the Graph-drawer
	$('#opt_graph').change(function(){
		if($(this).is(':checked')){
			$('#graph_modal').modal('show').one('shown.bs.modal', function(){
                if(!graph_initialized) {
                    dcg_init_graph();
                    graph_initialized = true;
                } else {
                    dcg_refresh_variables();
                }
			});
		}
	});
});

/**
 * Initialize the graph with given options and preferences.
 */
function dcg_init_graph(){
	$('#graph_container').html("");
	var elt = document.getElementById('graph_container');
	graph = Desmos.Calculator(elt, { //Set options for the DCG
		keypad: false
	});
	graph.setExpression({id: 'graph1', latex: 'f(x)='});
    dcg_refresh_variables();
    refresh_char_colors('.dcg-template-mathquill');
    $('.dcg-template-mathquill').addClass('input_mathquill');
}

/**
 * This will update or create a new expression in the DCG. If the provided id already exists, the values for
 * the provided parameters will be updated in the expression (unprovided parameters will remain unchanged).
 * @param {String} id - The id of the expression you want to create or update.
 * @param {String|latex} expression - The LaTeX-expression
 */
function dcg_new_expression(id, expression) {
    graph.setExpression({id: id, latex: expression});
    var expr_cell = $('div[expr-id="'+id+'"]');
    expr_cell.find('.dcg-action-delete').remove();
    expr_cell.find('.dcg-template-dependentlabelhtml');
}

/**
 * This will update or create a new variable in the DCG. If the provided id already exists, the values for
 * the provided parameters will be updated in the variable (unprovided parameters will remain unchanged).
 * @param {String} id - The id of the variable you want to create or update.
 * @param {String} variable_name - The name of the variable.
 * @param {number} min - The minimum range of the variable.
 * @param {number} max - The maximum range of the variable.
 */
function dcg_new_variable(id, variable_name, min, max) {
    graph.setExpression({id: id, latex: variable_name + '=' + min, sliderBounds: {min: min, max: max, step: 0.1}});
    var variable_cell = $('div[expr-id="'+id+'"]');
    variable_cell.find('.dcg-action-delete').remove();
}

/**
 * Removes an specific expression from the expression list in the DCG.
 * @param {String} id - The id of the expression you want to delete.
 */
function dcg_remove_expression(id) {
    graph.removeExpression({id: id});
}

/**
 * Refreshes the variable-settings given from the domain-setter in the template-editor.
 * Automatically adds new variables and sets its range.
 */
function dcg_refresh_variables(){
    if(VARIABLE_COUNT > 0) {
        $('.opt_domain_from').each(function(i){
            var name = $('#o_adv_' + i).text().replace(/:/g, "");
            var from = $(this).val();
            var to = $('#o_adv_to_' + i).val();
            dcg_new_variable('dcg_variable'+i, name, from, to);
        });
    }
    for(var key in dict_calc_unchanged){
        var char = "A";
        char = String.fromCharCode(char.charCodeAt(0) + parseInt(key));
        dcg_new_expression('dcg_variable_'+key, char+'='+dict_calc_unchanged[key]);
    }
    refresh_char_colors('.dcg-template-mathquill');
    $('.dcg-template-mathquill').addClass('input_mathquill');
}

/**
 * Sets a helper-expression which helps to monitor and react when the value of a normal expression or variable
 * changes in the expression-list.
 * @param {String} expression_name - The name of the variable or expression to monitor/react to.
 * @returns {Object} The helper-expression.
 */
function dcg_set_helper_expression(expression_name){
    helper_expression[expression_name] = graph.HelperExpression({latex: expression_name});
}

/**
 * Iterates through the expression-list and stores the expression in an list (sorts out the preset variables).
 * @returns {Array} A list of expressions (without preset variables).
 */
function dcg_get_expressions(){
    var expression_list = graph.getState()['expressions']['list'];
    var expressions = [];
    for(var e = 0; e < expression_list.length; e++){
        if(expression_list[e]['id'].substring(0, 12) != 'dcg_variable'){
            expressions.push(expression_list[e]['latex']);
        }
    }
    return expressions;
}