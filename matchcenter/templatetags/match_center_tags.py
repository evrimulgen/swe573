from django import template

register = template.Library()

@register.inclusion_tag('_vs_fixture.html', takes_context=True)
def sl_fixture(context, weeks):
    return {"weeks": weeks,
            "STATIC_URL": context["STATIC_URL"]}
