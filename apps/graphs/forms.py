# -*- encoding: utf-8 -*-
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
)

FIELDS_CHOICES = (
    ('', ''),
    ('num_components', 'Number of components')
)

class IntegerQueryWidget(forms.MultiWidget):
    """
    A Widget that splits datetime input into two <input type="text"> boxes.
    """
    def __init__(self, fields_choices, operands, attrs=None):
        widgets = (
            forms.Select(attrs=attrs, choices=fields_choices),
            forms.Select(attrs=attrs, choices=operands),
            forms.TextInput(attrs=attrs)
        )
        
        super(IntegerQueryWidget, self).__init__(widgets, attrs)
        
    def decompress(self, value):
        return ()
    
    def format_output(self, rendered_widgets):
        return '<span class="dqf_field_body">%s</span>' % (u''.join(rendered_widgets))
        
class IntegerQueryField(forms.MultiValueField):
    def __init__(self, required=False, label=None, widget=None, initial=0):
        fields = (
            forms.ChoiceField(choices=FIELDS_CHOICES, required=False),
            forms.ChoiceField(choices=INTEGER_OPERATOR_CHOICES),
            forms.IntegerField(initial=initial)
        )
        
        widget = widget or IntegerQueryWidget(
            fields_choices=FIELDS_CHOICES,
            operands=INTEGER_OPERATOR_CHOICES
        )
        
        super(IntegerQueryField, self).__init__(fields, required, widget, label)
        
        
    def compress(self, data_list):
        if len(data_list) != 3:
            # print self
            return {'does_apply': False}
        does_apply = data_list[0] is not None and data_list[2] is not None
        return {'field': data_list[0], 'operator': data_list[1], 'operand': data_list[2], 'does_apply': does_apply}

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
        js = ('js/jquery.js', 'js/django-query-form.js')

def query_form_factory(data):
    initial_qf = QueryForm(data)
    
    if initial_qf.is_valid():
        attrs = dict([(field_name, IntegerQueryField()) for field_name in initial_qf.cleaned_data['fields']])
        
        return type('QueryForm', (QueryForm,), attrs)

