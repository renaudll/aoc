"""
Useful functions and algorithms for quick coding.
"""
from __future__ import annotations

from typing import TypeVar
from dataclasses import dataclass

T = TypeVar("T")
IntOrFloat = TypeVar("IntOrFloat", bound=int|float)


@dataclass
class Vector2D:
    x: IntOrFloat
    y: IntOrFloat

    def __add__(self, other: Vector2D):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2D):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other: Vector2D):
        return Vector2D(self.x * other.x, self.y * other.y)

    def __eq__(self, other: Vector2D):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def __repr__(self):
        return f"Vector2D({self.x}, {self.y})"


def dfs(visited: set, graph: dict[T, list[T]], node: T):
    if node in visited:
        return
    visited.add(node)
    for neighbour in graph[node]:
        dfs(visited, graph, neighbour)
