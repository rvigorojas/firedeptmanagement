# -*- coding: utf-8 -*-
"""
Minimal, local replacement for the (unmaintained, unavailable-on-PyPI)
``django-bootstrap-toolkit`` package, providing only the ``as_bootstrap``
filter used by this project's templates. It renders a Django Form/FormSet
as Bootstrap-style form groups, close enough to the original for local
development purposes.
"""
from django import forms
from django.template import Library
from django.utils.safestring import mark_safe

register = Library()


def _render_field(field):
    widget = field.field.widget
    css_classes = field.css_classes()
    is_checkbox = isinstance(widget, forms.CheckboxInput)

    if is_checkbox:
        inner = (
            '<label class="checkbox">%s %s</label>'
            % (field, field.label)
        )
    else:
        label = field.label_tag() if field.label else ''
        inner = '%s%s' % (label, field)

    errors = ''.join('<span class="help-inline">%s</span>' % e for e in field.errors)
    help_text = (
        '<span class="help-block">%s</span>' % field.help_text
        if field.help_text else ''
    )

    control_group_class = 'control-group'
    if field.errors:
        control_group_class += ' error'

    return (
        '<div class="%s %s">'
        '<div class="controls">%s%s%s</div>'
        '</div>'
    ) % (control_group_class, css_classes, inner, errors, help_text)


def as_bootstrap(form):
    """Renders a Form or FormSet in a Bootstrap-ish layout."""
    if hasattr(form, 'forms'):
        # FormSet
        parts = []
        management_form = getattr(form, 'management_form', None)
        if management_form is not None:
            parts.append(str(management_form))
        for subform in form.forms:
            parts.append(as_bootstrap(subform))
        return mark_safe(''.join(parts))

    if hasattr(form, 'empty_form'):
        return as_bootstrap(form.empty_form)

    parts = []
    non_field_errors = getattr(form, 'non_field_errors', None)
    if non_field_errors:
        for error in non_field_errors():
            parts.append('<div class="alert alert-error">%s</div>' % error)

    for field in form:
        if field.is_hidden:
            parts.append(str(field))
        else:
            parts.append(_render_field(field))

    return mark_safe(''.join(parts))


register.filter('as_bootstrap', as_bootstrap)
