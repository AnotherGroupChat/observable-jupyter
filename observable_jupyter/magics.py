__all__ = ["embed_observable"]


from observable_jupyter import embed
from typing import Optional

try:
    from IPython.core.magic import register_line_cell_magic
except ImportError:
    print("Expected a Jupyter environment.")
    raise

@register_line_cell_magic
def embed_observable(line: str, payload: Optional[str]=None):
    """Jupyter magic for cell embedding.
    """
    args = list(filter(lambda x: x, line.split()))
    cells = None
    notebook_name = args[0]
    payload_args = {}
    if '--' in args:
        # Split arguments at the dash
        if args.index('--') != 1:
            if payload is None:
                raise Exception("Usage: %embed_observable notebook_name -- cell1 cell2 ...")
            if args[1] in ('+js', '+css'):
              if args[1] == '+js':
                payload_args = {"js_injection": payload}
              elif args[1] == '+css':
                payload_args = {"css_injection": payload}
            else:
                raise Exception("Usage: %%embed_observable +js|+css notebook_name -- cell1 cell2 ...")
        cells = args[2:]
        cells = ['viewof ' + cell[1:] if cell.startswith("@") else cell for cell in cells]
    return embed(notebook_name, cells=cells, **payload_args)
