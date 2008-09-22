function DQFInitializeForm() {
    DQFstates = {
        'old_fields_select_types_by_id': { }
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
        var field_id = $(this).attr('id');
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
                alert('ha');
            }
        }
    }
    
    function _dqf_save_old_fields_select_types() {
        $('.fields_select').each(function() {
            var field_id = $(this).attr('id');
            var field_name = $(this).val();
            
            if (field_name) {            
                var field_type = DQFfields.fields_descriptios[field_name].type;
            
                DQFstates.old_fields_select_types_by_id[field_id] = field_type;
            } else {
                DQFstates.old_fields_select_types_by_id[field_id] = '';
            }
        });
        
    }
    
    DQGInit();
}