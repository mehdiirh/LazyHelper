from django.utils.safestring import mark_safe

import ast
import json


def optimize_json(_dict) -> [dict, str]:
    """
    optimize json to save in database

    Args:
        _dict: json ( or dictionary ) object

    Returns:
        optimized json
    """

    try:
        _dict = json.dumps(ast.literal_eval(str(_dict)))
    except:
        _dict = str(_dict)

    return _dict


def render_json(_dict, html=False) -> str:
    """
    render a human-readable json

    Args:
        _dict: json or dictionary instance
        html: if is set to `True`, function will return a html-rendered json

    Returns:
        str: rendered json

    """
    if _dict is None:
        return '-'

    try:
        _dict = json.loads(_dict)
        _dict = render_json(_dict)
    except (TypeError, json.decoder.JSONDecodeError):
        if html:
            return mark_safe(f'<pre style="background-color: #9a9a9a5c; padding: 12px;">{_dict}</pre>')
        return _dict

    def pretty(_dict, indent=4):
        bracket_indent = indent + 4
        _text = ""

        if isinstance(_dict, (str, int)):
            return f"\n{' ' * indent}[ {_dict} ]"

        for k, v in _dict.items():

            if isinstance(v, dict):
                _temp = f"\n{' ' * indent}[ {k} ] => "
                _temp += f"\n{' ' * bracket_indent}["
                _temp += pretty(v, indent=indent + 6)
                _temp += f"\n{' ' * bracket_indent}]"
            elif isinstance(v, (list, tuple)):
                _temp = f"\n{' ' * indent}[ {k} ] => "
                _temp += f"\n{' ' * bracket_indent}["
                for i in v:
                    _temp += pretty(i, indent=indent + 6)
                _temp += f"\n{' ' * bracket_indent}]"
            else:
                _temp = f"\n{' ' * indent}[ {k} ] => [ {v} ]"
            _text += _temp
        return _text

    text = "["
    text += pretty(_dict)
    text += "\n]"

    if html:
        return mark_safe(f'<pre style="background-color: #9a9a9a5c; padding: 12px;">{text}</pre>')
    return text
