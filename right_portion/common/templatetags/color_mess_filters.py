from django import template
register = template.Library()

@register.filter
def color_chart(percent):
        if not percent:
            color = "#B7B7B7"
        elif percent <= 100.0:
            color = "#5fbba1ff"
        elif percent <= 110.0:
            color = "#E1BF00"
        else:
            color = "#A92424";

        return color

@register.filter
def message_perc(percent):
    if not percent:
         return "Time to start the day with a meal!"
    elif percent == 100.0:
         return f"Perfect! {percent}%"
    elif percent < 100.0:
        return f"Still a way to go! - {100 - percent:.1f}% left"
    elif percent <= 110.0:
        return f"Exceeded by {percent - 100:.1f}%!"
    else:
        return f"Exceeded too much - {percent:.1f}%!!"