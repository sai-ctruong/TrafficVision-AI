"""Compatibility launcher for TrafficAI Pro."""

from __future__ import annotations

import sys


class _QFluentWidgetsTipFilter:
    """Suppress the QFluentWidgets Pro promotional tip printed during import."""

    def __init__(self, stream):
        self._stream = stream

    def write(self, text: str) -> int:
        if "QFluentWidgets Pro is now released" in text:
            return len(text)
        return self._stream.write(text)

    def flush(self) -> None:
        self._stream.flush()

    def __getattr__(self, name: str):
        return getattr(self._stream, name)


_stdout = sys.stdout
sys.stdout = _QFluentWidgetsTipFilter(sys.stdout)
try:
    from TrafficAIPro.main import main
finally:
    sys.stdout = _stdout


if __name__ == "__main__":
    raise SystemExit(main())
