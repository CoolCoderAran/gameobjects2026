"""Two-dimensional grid utilities."""

from __future__ import annotations

from collections.abc import Callable, Iterator
from typing import Generic, TypeVar


WRAP_REPEAT = 0
WRAP_CLAMP = 1
WRAP_ERROR = 2

NodeT = TypeVar("NodeT")


class Grid(Generic[NodeT]):
    """A two-dimensional grid of nodes."""

    def __init__(
        self,
        node_factory: Callable[[int, int], NodeT],
        width: int,
        height: int,
        x_wrap: int = WRAP_ERROR,
        y_wrap: int = WRAP_ERROR,
    ) -> None:
        if width < 0 or height < 0:
            raise ValueError("width and height must be non-negative")

        self.node_factory = node_factory
        self.width = width
        self.height = height
        self.nodes = [
            [node_factory(x, y) for x in range(width)]
            for y in range(height)
        ]

        self._x_wrap = x_wrap
        self._y_wrap = y_wrap
        self._wrap_functions = [
            self._make_wrap(x_wrap, width),
            self._make_wrap(y_wrap, height),
        ]

    @property
    def x_wrap(self) -> int:
        return self._x_wrap

    @x_wrap.setter
    def x_wrap(self, value: int) -> None:
        self._x_wrap = value
        self._wrap_functions[0] = self._make_wrap(value, self.width)

    @property
    def y_wrap(self) -> int:
        return self._y_wrap

    @y_wrap.setter
    def y_wrap(self, value: int) -> None:
        self._y_wrap = value
        self._wrap_functions[1] = self._make_wrap(value, self.height)

    def _make_wrap(self, wrap: int, edge: int) -> Callable[[int], int]:
        if wrap == WRAP_NONE:
            return lambda value: value

        if wrap == WRAP_REPEAT:
            if edge <= 0:
                raise ValueError("repeat wrapping requires a non-empty grid")
            return lambda value: value % edge

        if wrap == WRAP_CLAMP:
            def do_wrap(value: int) -> int:
                if edge <= 0:
                    raise IndexError("coordinate out of range")
                if value < 0:
                    return 0
                if value >= edge:
                    return edge - 1
                return value
            return do_wrap

        if wrap == WRAP_ERROR:
            def do_wrap(value: int) -> int:
                if value < 0 or value >= edge:
                    raise IndexError("coordinate out of range")
                return value
            return do_wrap

        raise ValueError(f"Unknown wrap mode: {wrap!r}")

    def wrap(self, coord: tuple[int, int]) -> tuple[int, int]:
        x, y = coord
        return self._wrap_functions[0](x), self._wrap_functions[1](y)

    def wrap_x(self, x: int) -> int:
        return self._wrap_functions[0](x)

    def wrap_y(self, y: int) -> int:
        return self._wrap_functions[1](y)

    def get_size(self) -> tuple[int, int]:
        return self.width, self.height

    def __getitem__(
        self,
        coord: tuple[int | slice, int | slice],
    ) -> NodeT | list[NodeT]:
        x, y = coord

        if isinstance(x, slice) or isinstance(y, slice):
            x_indices = (
                range(*x.indices(self.width)) if isinstance(x, slice) else (x,)
            )
            y_indices = (
                range(*y.indices(self.height)) if isinstance(y, slice) else (y,)
            )

            result: list[NodeT] = []
            try:
                wrap_x, wrap_y = self._wrap_functions
                for y_index in y_indices:
                    nodes_y = self.nodes[wrap_y(y_index)]
                    for x_index in x_indices:
                        result.append(nodes_y[wrap_x(x_index)])
            except IndexError as exc:
                raise IndexError("Slice out of range") from exc
            return result

        x, y = self.wrap((x, y))
        return self.nodes[y][x]

    def __iter__(self) -> Iterator[NodeT]:
        for row in self.nodes:
            yield from row

    def __contains__(self, value: object) -> bool:
        return any(value in row for row in self.nodes)

    def clear(self) -> None:
        node_factory = self.node_factory
        self.nodes[:] = [
            [node_factory(x, y) for x in range(self.width)]
            for y in range(self.height)
        ]

    def get(
        self,
        coord: tuple[int, int],
        default: NodeT | None = None,
    ) -> NodeT | None:
        try:
            x, y = self.wrap(coord)
            return self.nodes[y][x]
        except IndexError:
            return default

    def get_nodes(
        self,
        coord: tuple[int, int],
        size: tuple[int, int],
        wrap: bool = False,
    ) -> list[list[NodeT]]:
        x, y = coord
        width, height = size

        if width < 0:
            x += width
            width = -width
        if height < 0:
            y += height
            height = -height

        if wrap:
            wrap_x, wrap_y = self._wrap_functions
            return [
                [
                    self.nodes[wrap_y(y_coord)][wrap_x(x_coord)]
                    for x_coord in range(x, x + width)
                ]
                for y_coord in range(y, y + height)
            ]

        x1 = max(0, x)
        y1 = max(0, y)
        x2 = min(self.width, x + width)
        y2 = min(self.height, y + height)

        if x1 >= x2 or y1 >= y2:
            return []

        return [self.nodes[y_coord][x1:x2] for y_coord in range(y1, y2)]


__all__ = ["Grid"]
