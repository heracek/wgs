# -*- encoding: utf-8 -*-
from django import forms
from django.conf import settings
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
        return '<span id="%s">%s</span>' % \
            (self._id, u''.join(rendered_widgets))#, settings.MEDIA_URL, settings.MEDIA_URL)
        
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
        # from pprint import pprint
        # pprint(dir(self))
        widget._id = self.label
    
    def compress(self, data_list):
        if len(data_list) != 3:
            # print self
            return {'does_apply': False}
        does_apply = data_list[0] is not None and data_list[2] is not None
        return {'field': data_list[0], 'operator': data_list[1], 'operand': data_list[2], 'does_apply': does_apply}

class QueryForm(forms.Form):
    #add_query_field = 
    q_1 = IntegerQueryField()
    #q_2 = IntegerQueryField()
    
    ADD_REMOVE_BUTTONS = """<span class="dqf_add_remove_controls right">
            <img class="dqf_button dqf_remove_button" src="%(MEDIA_URL)simg/dqf/remove.png" alt="remove" width="24" heignt="24" /><img class="dqf_button dqf_add_button" src="%(MEDIA_URL)simg/dqf/add.png" alt="add" width="24" heignt="24" />
        </span>"""
    
    def as_dqf_ul(self):
        return self._html_output(
            normal_row=u'<li class="dqf_field">%%(errors)s%s %%(field)s%%(help_text)s</li>' % (self.ADD_REMOVE_BUTTONS % { 'MEDIA_URL': settings.MEDIA_URL}),
            error_row=u'<li>%s</li>',
            row_ender='</li>',
            help_text_html=u' %s',
            errors_on_separate_row=False
        )
    
    class Media:
        js = ('js/jquery.js', 'js/django-query-form.js',)
