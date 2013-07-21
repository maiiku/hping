# -*- coding: utf-8 -*-
from django.forms.util import ErrorList
from django.utils.encoding import force_text
from django.utils.html import format_html, format_html_join


class BootstrapErrorList(ErrorList):
    """
    A collection of errors that knows how to display itself in various formats.
    """
    def as_ul(self):
        if not self: return ''
        return format_html('<ul class="errorlist">{0}</ul>',
                           format_html_join('', '<li class="text-error">{0}</li>',
                                            ((force_text(e),) for e in self)
                                            )
                           )