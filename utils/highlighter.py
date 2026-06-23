from pygments import highlight

from pygments.lexers import (
    get_lexer_by_name
)

from pygments.formatters import (
    HtmlFormatter
)


def highlight_code(
    code,
    language="python"
):

    lexer = get_lexer_by_name(
        language,
        stripall=False
    )

    formatter = HtmlFormatter(
        linenos=True,
        full=False
    )

    return highlight(
        code,
        lexer,
        formatter
    )

def get_style():

    formatter = HtmlFormatter()

    return formatter.get_style_defs(
        ".highlight"
    )