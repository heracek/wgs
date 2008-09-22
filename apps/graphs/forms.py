# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../django')))

from django import forms
from django.conf import settings
from django.utils.html import escape
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
import datetime
import time


INTEGER_OPERATOR_CHOICES = (
  ('=', '='),
  ('!=', '≠'),
  ('<', '<'),
  ('>', '>'),
  ('<=', '≤'),
  ('>=', '≥'),
  ('between', 'between')
)

FIELDS_CHOICES = (
    ('', ''),
    ('num_components', 'Number of components'),
    ("order", "Order"),
    ("size", "Size"),
)

FIELD_TYPES = {
    'num_components': 'integer',
    'order': 'integer',
    'size': 'integer',
}

class DQFDynamicWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [ forms.Select(attrs={ 'class': 'fields_select' }, choices=FIELDS_CHOICES), ]
        self._dqf_added_widgets_level = 0
        super(DQFDynamicWidget, self).__init__(widgets, attrs)
        
    def decompress(self, value):
        return value
    
    def format_output(self, rendered_widgets):
        return '<span class="dqf_field_body">%s</span>' % (u''.join(rendered_widgets))
    
    def value_from_datadict(self, data, files, name):
        return_list = super(DQFDynamicWidget, self).value_from_datadict(data, files, name)
        
        while(self._extend_widgets_by_field(return_list)):
            return_list = super(DQFDynamicWidget, self).value_from_datadict(data, files, name)
        
        return return_list
    
    def render(self, name, value, attrs=None):
        while self._extend_widgets_by_field(value):
            pass
        
        return super(DQFDynamicWidget, self).render(name=name, value=value, attrs=attrs)
    
    def _extend_widgets_by_field(self, values):
        '''
        Returns: True  ... extended widgets
                 False ... not extended widgets
        '''
        if len(values) > 0:
            field = values[0]
            field_type = FIELD_TYPES.get(field, '')
            
            if self._dqf_added_widgets_level < 1:
                if field_type == 'integer':
                    self.widgets += [
                        forms.Select(attrs={ 'class': 'integer_operator' }, choices=INTEGER_OPERATOR_CHOICES),
                        forms.TextInput(attrs={ 'class': 'operand' }),
                    ]
                    
                    self._dqf_added_widgets_level = 1
                    
                    return True
            if self._dqf_added_widgets_level < 2 and len(values) >= 2:
                secundary_field = values[1]
                if field_type == 'integer':
                    if secundary_field == 'between':
                        self.widgets += [
                            forms.TextInput(attrs={ 'class': 'operand_2' }),
                        ]
                    
                    self._dqf_added_widgets_level = 2
                    
                    return True
        return False
        
class DQFDynamicField(forms.MultiValueField):
    def __init__(self, required=False, label=None, widget=None, initial=None):
        widget = widget or DQFDynamicWidget()
        
        super(DQFDynamicField, self).__init__([ forms.ChoiceField(choices=FIELDS_CHOICES, required=False) ],
            required, widget, label
        )
        
        self._dqf_added_fields_level = 0
    
    def clean(self, value):
        while self._extend_fields(super(DQFDynamicField, self).clean(value)):
            pass
        
        return super(DQFDynamicField, self).clean(value)
    
    def _extend_fields(self, return_dict):
        field = return_dict.get('field', None)
        field_type = FIELD_TYPES.get(field, '')
        if field:
            if self._dqf_added_fields_level == 0:
                if field_type == 'integer':
                    self.fields += [
                        forms.ChoiceField(choices=INTEGER_OPERATOR_CHOICES, required=False),
                        forms.IntegerField(required=False)
                    ]
                    self._dqf_added_fields_level = 1
                    return True
            elif self._dqf_added_fields_level == 1:
                if field_type == 'integer':
                    operator = return_dict.get('operator', '')
                    if operator == 'between':
                        self.fields += [
                            forms.IntegerField(required=False)
                        ]
                        self._dqf_added_fields_level = 2
                        return True
        return False
        
    
    def compress(self, data_list):
        if len(data_list) == 0:
            return {'does_apply': False}
        
        field = data_list[0]
        field_type = FIELD_TYPES.get(field, '')
        return_dict = {'field': field, 'does_apply': False}
        
        if field_type == 'integer' and len(data_list) >= 2:
            operator = data_list[1]
            operand = data_list[2]
            
            does_apply = None not in (operator, operand)
            
            return_dict.update({
                'operator': operator,
                'operand': operand,
                'does_apply': does_apply
            })
            
            if operator == 'between' and len(data_list) > 3:
                return_dict['operand_2'] = data_list[3]
                if return_dict['operand_2'] is None:
                    return_dict['does_apply'] = False
        
        return return_dict

class DQFFieldsField(forms.CharField):
    def __init__(self, *args, **kwargs):
        self.max_length, self.min_length = None, None
        kwargs['required'] = False
        kwargs['widget'] = forms.HiddenInput()
        super(DQFFieldsField, self).__init__(*args, **kwargs)
    
    def clean(self, value):
        "Validates max_length and min_length. Returns a Unicode object."
        super(DQFFieldsField, self).clean(value)
        if value in forms.fields.EMPTY_VALUES:
            return []
        
        try:
            value = str(value)
        except UnicodeEncodeError:
            raise forms.ValidationError('Field contains invalid character.')
        
        return value.split(',')


class QueryForm(forms.Form):
    fields = DQFFieldsField()
    
    ADD_REMOVE_BUTTONS = """<span class="dqf_add_remove_controls">
            <img class="dqf_button dqf_remove_button" src="%(MEDIA_URL)simg/dqf/remove.png" """ \
            """alt="remove" width="24" heignt="24" />""" \
            """<img class="dqf_button dqf_add_button" src="%(MEDIA_URL)simg/dqf/add.png" """ \
            """alt="add" width="24" heignt="24" />
        </span>"""
    
    def as_dqf_ul(self):
        return self._html_output(
            normal_row=u'<li class="dqf_field">%%(errors)s%s %%(field)s%%(help_text)s</li>' % \
                (self.ADD_REMOVE_BUTTONS % { 'MEDIA_URL': settings.MEDIA_URL}),
            error_row=u'<li>%s</li>',
            row_ender='</li>',
            help_text_html=u' %s',
            errors_on_separate_row=False,
            insert_hidden_in_the_last_row=False
        )
    
    def _html_output(self, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row, insert_hidden_in_the_last_row=True):
        "Helper function for outputting HTML. Used by as_table(), as_ul(), as_p()."
        top_errors = self.non_field_errors() # Errors that should be displayed above all fields.
        output, hidden_fields = [], []
        for name, field in self.fields.items():
            bf = forms.forms.BoundField(self, field, name)
            bf_errors = self.error_class([escape(error) for error in bf.errors]) # Escape and cache in local variable.
            if bf.is_hidden:
                if bf_errors:
                    top_errors.extend([u'(Hidden field %s) %s' % (name, force_unicode(e)) for e in bf_errors])
                hidden_fields.append(unicode(bf))
            else:
                if errors_on_separate_row and bf_errors:
                    output.append(error_row % force_unicode(bf_errors))
                if bf.label:
                    label = escape(force_unicode(bf.label))
                    # Only add the suffix if the label does not end in
                    # punctuation.
                    if self.label_suffix:
                        if label[-1] not in ':?.!':
                            label += self.label_suffix
                    label = bf.label_tag(label) or ''
                else:
                    label = ''
                if field.help_text:
                    help_text = help_text_html % force_unicode(field.help_text)
                else:
                    help_text = u''
                output.append(normal_row % {
                    'errors': force_unicode(bf_errors),
                    'label': force_unicode(label),
                    'field': unicode(bf),
                    'help_text': help_text
                })
        if top_errors:
            output.insert(0, error_row % force_unicode(top_errors))
        if hidden_fields: # Insert any hidden fields in the last row.
            str_hidden = u''.join(hidden_fields)
            if output and insert_hidden_in_the_last_row:
                last_row = output[-1]
                # Chop off the trailing row_ender (e.g. '</td></tr>') and
                # insert the hidden fields.
                output[-1] = last_row[:-len(row_ender)] + str_hidden + row_ender
            else:
                # If there aren't any rows in the output, just append the
                # hidden fields.
                output.append(str_hidden)
        return mark_safe(u'\n'.join(output))
    
    class Media:
        js = ('js/jquery.js', 'js/jquery-ui.js', 'js/django-query-form.js')

def query_form_factory(data):
    initial_qf = QueryForm(data)
    
    if initial_qf.is_valid():
        attrs = dict([(field_name, DQFDynamicField()) for field_name in initial_qf.cleaned_data['fields']])
        
        return type('QueryForm', (QueryForm,), attrs)


# x = DQFDynamicWidget()
# print x.render('{ aaa }', ('num_components', 'between', '{ val_1 }', '{ val_2 }'))
