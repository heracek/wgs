function DQFInitializeForm() {
    function DQGInit() {
        $('.dqf_add_button').each(function() {
            $(this).click(_dqf_add_button_click);
        });
        
        $('.dqf_remove_button').each(function() {
            $(this).click(_dqf_remove_button_click);
        });
        
        $('#dqf_head_add_button').each(function() {
            $(this).click(function () {
                var dqf_fields_ul = $("ul#dqf_fields")[0];
                _dqf_create_field_li($(dqf_fields_ul), prepend=true)
            });
        })
        
        $('#dqf_head_remove_button').each(function() {
            $(this).click(function () {
                $("li.dqf_field", "ul#dqf_fields").remove();
            });
        })
    }
    
    function _dqf_create_field_li(where, prepend) {
        field_li_text = '<li class="dqf_field"><span class="dqf_add_remove_controls right">' +
            '<img width="24" heignt="24" alt="remove" src="/site-media/img/dqf/remove.png" class="dqf_button dqf_remove_button"/>' +
            '<img width="24" heignt="24" alt="add" src="/site-media/img/dqf/add.png" class="dqf_button dqf_add_button"/>' +
            '</span><span id="None"><select id="id_q_1_0" name="q_1_0">' +
            '<option selected="selected" value=""/>' +
            '<option value="num_components">Number of components</option>' +
            '</select>' +
            '</span></li>';
            /*            
                        <select id="id_q_1_1" name="q_1_1">
                        <option value="=">=</option>
                        <option selected="selected" value="!=">≠</option>
                        <option value="<"><</option>
                        <option value=">">></option>
                        <option value="<=">≤</option>
                        <option value=">=">≥</option>
                        </select><input type="text" id="id_q_1_2" value="12" name="q_1_2"/>
            */            

        
        var added_dqf_field_li;
        
        if (! prepend) {
            added_dqf_field_li = where.after(field_li_text).next();
        } else {
            added_dqf_field_li = where.prepend(field_li_text).children()[0];
        }
        
        $('.dqf_add_button', added_dqf_field_li).each(function(b){
            $(this).click(_dqf_add_button_click);
        });
        
        $('.dqf_remove_button', added_dqf_field_li).each(function() {
            $(this).click(_dqf_remove_button_click);
        });
    }
    
    function _dqf_add_button_click() {
        var dqf_field_li = $(this).parents("li.dqf_field")[0];
        _dqf_create_field_li($(dqf_field_li))
    }
    
    function _dqf_remove_button_click() {
        var dqf_field_li = $(this).parents("li.dqf_field")[0];
        $(dqf_field_li).remove();
    }
    
    DQGInit();
}