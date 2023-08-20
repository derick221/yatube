from django import template

register = template.Library()

@register.filter
def add_class(value, arg):
    css_classes = value.field.widget.attrs.get("class", "")
    css_classes += f" {arg}"
    value.field.widget.attrs["class"] = css_classes
    return value