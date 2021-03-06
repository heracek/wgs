function DQFInitializeForm() {
    DQFstates = {
        'old_fields_select_types_by_id': { },
        'old_integer_operator_types_by_id': { }
    };
    
    function DQGInit() {
        $('.dqf_add_button').each(function() {
            $(this).click(_dqf_add_button_click);
        });
        
        $('.dqf_remove_button').each(function() {
            $(this).click(_dqf_remove_button_click);
        });
        
        _dqf_save_old_fields_select_types()
        
        $('.fields_select').change(_dqf_fields_select_change);
        $('.integer_operator').change(_dqf_integer_operator_change);
        
        $('#dqf_head_add_button:first').click(function () {
            var dqf_fields_ul = $("ul#dqf_fields")[0];
            _dqf_create_field_li($(dqf_fields_ul), prepend=true);
        });
        
        $('#dqf_head_remove_button:first').click(function () {
            $("li.dqf_field", "ul#dqf_fields").remove();
        });
        
        $('#dqf_form').submit(function () {
            dqf_update_fields_field();
            return true;
        });
        
        /*$('#dqf_fields').sortable({
                    cursor: 'move',
                });*/
    }
    
    function dqf_get_free_field_name() {
        for (var i = 0; true; i++) {
            var widget_id_str = '#id_q_' + i + '_0'
            if ($(widget_id_str).length == 0) {
                return 'q_' + i
            }
        }
    }
    
    function dqf_update_fields_field() {
        
        var field_names_list = [];
        
        $('.dqf_field', 'ul#dqf_fields').each(function () {
            var first_cildren = $('.dqf_field_body:first', this).children()[0];
            var widget_id = $(first_cildren).attr('id');
            var splited_id = widget_id.split('_');
            var field_name = [splited_id[1], splited_id[2]].join('_');
            field_names_list.push(field_name);
        });
        
        $('#id_fields').attr('value', field_names_list.join(','));
    }
    
    function _dqf_create_field_li(where, prepend) {
        var field_name = dqf_get_free_field_name()
        
        var field_options = []
        
        for (var i = 0; i < DQFfields.fields_order.length; i++) {
            var option_name = DQFfields.fields_order[i];
            var option_label = DQFfields.fields_descriptios[option_name].label;
            field_options.push('<option value="' + option_name + '">' + option_label + '</option>');
        }
        
        var field_li_text = '<li class="dqf_field"><span class="dqf_add_remove_controls">' + 
            '<img width="24" heignt="24" alt="remove" src="/site-media/img/dqf/remove.png" ' + 
                'class="dqf_button dqf_remove_button"/>' +
            '<img width="24" heignt="24" alt="add" src="/site-media/img/dqf/add.png" ' + 
                'class="dqf_button dqf_add_button"/>' + 
            '</span><span class="dqf_field_body">' + 
            '<select id="id_' + field_name + '_0" name="' + field_name + '_0" class="fields_select">' + 
            '<option selected="selected" value=""/>' + 
            field_options.join('\n') +
            '</select>' + 
            '</span></li>';
        
        var added_dqf_field_li;
        
        if (! prepend) {
            added_dqf_field_li = where.after(field_li_text).next().hide().fadeIn("fast");
        } else {
            added_dqf_field_li = $(where.prepend(field_li_text).children()[0]).hide().fadeIn("fast");
        }
        
        $('.fields_select').change(_dqf_fields_select_change);
        
        $('.dqf_add_button:first', added_dqf_field_li).click(_dqf_add_button_click);
        
        $('.dqf_remove_button:first', added_dqf_field_li).click(_dqf_remove_button_click);
    }
    
    function _dqf_add_button_click() {
        var dqf_field_li = $(this).parents("li.dqf_field")[0];
        _dqf_create_field_li($(dqf_field_li))
    }
    
    function _dqf_remove_button_click() {
        var dqf_field_li = $($(this).parents("li.dqf_field")[0]);
        dqf_field_li.fadeOut("fast", function () {
            dqf_field_li.remove();
        });
    }
    
    function _dqf_fields_select_change() {
        var field_id = $(this).attr('id').split('_').slice(1, 3).join('_');
        var field_name = $(this).val();
        if (field_name) {
            var field_type = DQFfields.fields_descriptios[field_name].type;
        } else {
            var field_type = ''
        }
        var old_field_type = DQFstates.old_fields_select_types_by_id[field_id]
        
        if (old_field_type != field_type) {
            DQFstates.old_fields_select_types_by_id[field_id] = field_type
            if (field_type == 'integer') {
                var field_li_text = '<select class="integer_operator" id="id_' + field_id + '_1" name="' + field_id + '_1">' +
                    '<option selected="selected" value="=">=</option>' +
                    '<option value="!=">≠</option>' +
                    '<option value="<"><</option>' +
                    '<option value=">">></option>' +
                    '<option value="<=">≤</option>' +
                    '<option value=">=">≥</option>' +
                    '<option value="between">between</option>' +
                    '</select><input class="operand" type="text" id="id_' + field_id + '_2" value="" name="' + field_id + '_2"/>';
                
                DQFstates.old_integer_operator_types_by_id[field_id] = '';
                
                $(this).after(field_li_text).next().hide().fadeIn("fast");
                $(this).siblings('.integer_operator').change(_dqf_integer_operator_change);
            } else if (field_type == '') {
                var siblings_to_remove = $(this).siblings()
                siblings_to_remove.fadeOut("fast", function () {
                    siblings_to_remove.remove();
                });
                
            }
        }
    }
    
    function _dqf_integer_operator_change() {
        var field_id = $(this).attr('id').split('_').slice(1, 3).join('_');
        var operator_id = $(this).val();
        
        if (operator_id != 'between') {
            operator_id = '';
        }
        
        var old_operator_id = DQFstates.old_fields_select_types_by_id[field_id]
        DQFstates.old_fields_select_types_by_id[field_id] = operator_id;
        
        if (old_operator_id != operator_id) {
            if (operator_id == 'between') {
                $(this).siblings('.operand').after('<input type="text" name="' + field_id + '_3" value="" class="operand_2" id="id_' + field_id + '_3"/>').next().hide().fadeIn("fast");
            } else if (operator_id == '') {
                $(this).siblings('.operand_2').fadeOut("fast", function () {
                    $(this).remove();
                });
            }
        }
    }
    
    function _dqf_save_old_fields_select_types() {
        $('.fields_select').each(function() {
            var field_id = $(this).attr('id').split('_').slice(1, 3).join('_');
            var field_name = $(this).val();
            
            if (field_name) {            
                var field_type = DQFfields.fields_descriptios[field_name].type;
            
                DQFstates.old_fields_select_types_by_id[field_id] = field_type;
            } else {
                DQFstates.old_fields_select_types_by_id[field_id] = '';
            }
        });
        
        $('.integer_operator').each(function() {
            var field_id = $(this).attr('id').split('_').slice(1, 3).join('_');
            var field_name = $(this).val();
            
            if (field_name == 'between') {            
                DQFstates.old_integer_operator_types_by_id[field_id] = 'between';
            } else {
                DQFstates.old_integer_operator_types_by_id[field_id] = '';
            }
        });
    }
    
    DQGInit();
}