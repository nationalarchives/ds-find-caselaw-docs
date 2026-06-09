from collections.abc import Sequence


def render_markdown_table(rows: Sequence[Sequence[str]]) -> str:
    if not rows:
        msg = "rows must contain at least one row"
        raise ValueError(msg)

    column_count = len(rows[0])
    if column_count == 0:
        msg = "rows must contain at least one column"
        raise ValueError(msg)

    for row in rows:
        if len(row) != column_count:
            msg = "all rows must have the same number of columns"
            raise ValueError(msg)

    widths = [max(len(row[index]) for row in rows) for index in range(column_count)]

    def format_row(row: Sequence[str]) -> str:
        padded_cells = [cell.ljust(widths[index]) for index, cell in enumerate(row)]
        return f"| {' | '.join(padded_cells)} |"

    divider = "| " + " | ".join("-" * max(width, 3) for width in widths) + " |"
    body = [format_row(row) for row in rows]

    return "\n".join([body[0], divider, *body[1:]])
