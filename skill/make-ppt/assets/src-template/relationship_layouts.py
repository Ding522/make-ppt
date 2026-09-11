"""Optional relationship layouts. Dates, categories and states come from the outline."""
from pptx.util import Inches
import theme as T
import primitives as P


def _label(slide, x, y, w, h, text, **options):
    _, tf = P.textbox(slide, x, y, w, h)
    P.rich_par(tf, [(text, options)], first=True, space_after=0)


def add_status_matrix(slide, x, y, w, h, *, headers, rows, states,
                      groups=(), col_widths=None):
    """Native table with explicit state mapping and optional outside category rails.

    rows: [row_label, state_key, ...]. states maps keys to
    {symbol, label, color}. Unknown/missing evidence needs its own explicit key.
    groups: {start, end, color}, inclusive zero-based BODY row indices.
    h includes the legend. No status is inferred from missing evidence.
    """
    rows, headers, groups = list(rows), list(headers), list(groups)
    if len(headers) < 2 or not rows or not states:
        raise ValueError("Matrix needs labels, records and an explicit state legend")
    if any(len(row) != len(headers) for row in rows):
        raise ValueError("Matrix rows must match headers")
    used = set()
    for group in groups:
        start, end = group['start'], group['end']
        if not 0 <= start <= end < len(rows):
            raise ValueError("Category rail must reference existing body rows")
        indices = set(range(start, end + 1))
        if indices & used:
            raise ValueError("Category rails must not overlap")
        used |= indices
    converted = []
    for row in rows:
        cells = [row[0]]
        for key in row[1:]:
            if key not in states:
                raise ValueError(f"Unknown state: {key!r}; define its meaning explicitly")
            state = states[key]
            cells.append([(state['symbol'], {'color': state['color']})])
        converted.append(cells)
    legend_h = Inches(0.42)
    table_h = h - legend_h
    if table_h < T.TABLE_HEADER_H + len(rows) * Inches(0.34):
        raise ValueError("Matrix is too dense; split rows and repeat header/legend")
    frame = P.add_native_table(
        slide, x, y, w, table_h, headers=headers, rows=converted,
        col_widths=col_widths or [2.4] + [1] * (len(headers) - 1),
        alignments=['left'] + ['center'] * (len(headers) - 1))
    for row in list(frame.table.rows)[1:]:
        for cell in row.cells:
            cell.fill.fore_color.rgb = T.PANEL_BG
    for group in groups:
        top = y + sum(frame.table.rows[i].height for i in range(group['start'] + 1))
        height = sum(frame.table.rows[i + 1].height
                     for i in range(group['start'], group['end'] + 1))
        P.add_panel(slide, x - Inches(0.075), top, Inches(0.075), height,
                    fill=group['color'], line=None, radius=False)
    segments = []
    for state in states.values():
        segments.extend([(state['symbol'] + ' ', {'color': state['color']}),
                         (state['label'] + '    ', {'color': T.INK})])
    _, tf = P.textbox(slide, x, y + table_h + Inches(0.08), w, Inches(0.32))
    P.rich_par(tf, segments, first=True, space_after=0)
    return frame


def add_multitrack_timeline(slide, x, y, w, h, *, ticks, tracks):
    """ticks: ordered (numeric_position, visible_label); dates can use ordinal().

    tracks: {label, color, intervals: [(start,end)], note?, connect_gaps?: bool}.
    Numeric coordinates share a real scale; disjoint intervals remain disjoint.
    Dashed continuity is opt-in and needs source support, not an inferred activity.
    """
    ticks, tracks = list(ticks), list(tracks)
    if len(ticks) < 2 or not tracks:
        raise ValueError('Timeline needs at least two ticks and one track')
    if any(b[0] <= a[0] for a, b in zip(ticks, ticks[1:])):
        raise ValueError('Ticks must be strictly increasing')
    lo, hi = ticks[0][0], ticks[-1][0]
    pitch = (h - Inches(0.6)) / len(tracks)
    if pitch < Inches(0.95):
        raise ValueError('Timeline tracks need more height; split the slide')
    for track in tracks:
        previous = lo
        for start, end in track['intervals']:
            if not lo <= start < end <= hi or start < previous:
                raise ValueError('Intervals must be ordered, non-overlapping and within axis')
            previous = end
    def px(value):
        return x + w * (value - lo) / (hi - lo)
    for index, track in enumerate(tracks):
        top = y + index * pitch
        color = track['color']
        _label(slide, x, top, w, Inches(0.3), track['label'],
               color=color, bold=True, size=T.S_SUPPORT)
        bar_y = top + Inches(0.36)
        previous = None
        for start, end in track['intervals']:
            if previous is not None and start > previous and track.get('connect_gaps', False):
                P.add_arrow(slide, px(previous), bar_y + Inches(0.1),
                            px(start), bar_y + Inches(0.1),
                            color=T.HAIRLINE, dashed=True, arrow=False)
            P.add_panel(slide, px(start), bar_y, px(end) - px(start), Inches(0.2),
                        fill=color, line=None, radius=False)
            previous = end
        if track.get('note'):
            _label(slide, x, top + Inches(0.64), w, Inches(0.3), track['note'],
                   color=T.MUTED, size=T.S_LABEL)
    axis_y = y + h - Inches(0.42)
    P.add_hairline(slide, axis_y, x=x, w=w)
    for value, label in ticks:
        label_x = max(x, min(px(value) - Inches(0.35), x + w - Inches(0.85)))
        _label(slide, label_x, axis_y + Inches(0.08), Inches(0.85), Inches(0.3),
               label, color=T.MUTED, size=T.S_MONO, mono=True)


def add_layered_list(slide, x, y, w, h, *, groups, label_ratio=0.56):
    """groups: {label, description?, color, items: [(name, evidence)]}.

    Editorial groups, not a substitute for a table with repeated column headers.
    Height follows item count. Uses native text, dividers and category rails.
    """
    groups = list(groups)
    if not groups or any(not group['items'] for group in groups):
        raise ValueError('Each layer needs at least one item')
    if not 0.3 <= label_ratio <= 0.7:
        raise ValueError('label_ratio must leave readable space for both columns')
    header_h, gap = Inches(0.35), Inches(0.12)
    count = sum(len(group['items']) for group in groups)
    item_h = (h - len(groups) * header_h - (len(groups) - 1) * gap) / count
    if item_h < Inches(0.32):
        raise ValueError('Layered list is too dense; split at a group boundary')
    top = y
    for index, group in enumerate(groups):
        group_h = header_h + len(group['items']) * item_h
        P.add_panel(slide, x, top, Inches(0.075), group_h,
                    fill=group['color'], line=None, radius=False)
        _, tf = P.textbox(slide, x + Inches(0.2), top, w - Inches(0.2), header_h)
        parts = [(group['label'], {'color': group['color'], 'bold': True, 'size': T.S_SUPPORT})]
        if group.get('description'):
            parts.append(('  — ' + group['description'], {'color': T.MUTED, 'size': T.S_BODY}))
        P.rich_par(tf, parts, first=True, space_after=0)
        for i, (name, evidence) in enumerate(group['items']):
            row_y = top + header_h + i * item_h
            _label(slide, x + Inches(0.3), row_y, w * label_ratio - Inches(0.4),
                   item_h, name, bold=True, size=T.S_BODY)
            _label(slide, x + w * label_ratio, row_y, w * (1 - label_ratio),
                   item_h, evidence, color=T.MUTED, size=T.S_BODY)
        top += group_h + gap
        if index < len(groups) - 1:
            P.add_hairline(slide, top - gap / 2, x=x, w=w)
