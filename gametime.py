"""Game timing utilities.

Provides a small dependency-free fixed-timestep game clock suitable for
game loops and simulations.
"""

from __future__ import annotations

import time
from collections.abc import Iterator
from numbers import Real


class GameClock:
    """Manage real, virtual, and fixed-timestep game time.

    The clock separates elapsed real time from simulation time.  The
    simulation advances in fixed-size ticks, while :attr:`between_frame`
    gives the interpolation fraction between the most recent simulation
    tick and the next one.

    ``game_ticks_per_second`` controls the simulation tick rate.  A speed
    of ``1.0`` means normal time, ``2.0`` runs the simulation twice as
    fast, and ``0.0`` effectively pauses virtual time without setting the
    paused state.
    """

    def __init__(self, game_ticks_per_second: Real = 20) -> None:
        """Create a game clock.

        Args:
            game_ticks_per_second: Number of simulation ticks per second.
        """
        ticks = float(game_ticks_per_second)
        if ticks <= 0.0:
            raise ValueError("game_ticks_per_second must be greater than zero")

        self.game_ticks_per_second = ticks
        self.game_tick = 1.0 / ticks
        self.speed = 1.0

        self.clock_time = 0.0
        self.virtual_time = 0.0
        self.game_time = 0.0
        self.game_frame_count = 0
        self.real_time_passed = 0.0

        self.real_time = self.get_real_time()
        self.started = False
        self.paused = False
        self.between_frame = 0.0

        self.fps_sample_start_time = 0.0
        self.fps_sample_count = 0
        self.average_fps = 0.0
        self.fps = 0.0

    def start(self) -> None:
        """Start or restart the game clock.

        Calling ``start`` on an already-started clock has no effect.
        """
        if self.started:
            return

        self.clock_time = 0.0
        self.virtual_time = 0.0
        self.game_time = 0.0
        self.game_frame_count = 0
        self.real_time_passed = 0.0

        self.real_time = self.get_real_time()
        self.started = True
        self.paused = False

        self.fps = 0.0
        self.average_fps = 0.0
        self.fps_sample_start_time = self.real_time
        self.fps_sample_count = 0

    def set_speed(self, speed: Real) -> None:
        """Set the virtual-time speed multiplier.

        ``1.0`` is normal speed and ``2.0`` is twice normal speed.
        Negative speeds are not supported.
        """
        speed_value = float(speed)
        if speed_value < 0.0:
            raise ValueError("Negative speeds not supported")
        self.speed = speed_value

    def pause(self) -> None:
        """Pause advancement of virtual game time."""
        self.paused = True

    def unpause(self) -> None:
        """Resume advancement of virtual game time."""
        self.paused = False

    def get_real_time(self) -> float:
        """Return the current monotonic real time.

        This method may be overridden by applications or tests that need
        to supply their own clock.
        """
        return time.perf_counter()

    def get_fps(self) -> tuple[float, float]:
        """Return instantaneous FPS and the sampled average FPS."""
        return self.fps, self.average_fps

    def get_between_frame(self) -> float:
        """Return the interpolation fraction between simulation ticks."""
        return self.between_frame

    def update(self, max_updates: int = 0) -> Iterator[tuple[int, float]]:
        """Advance the clock and yield fixed-timestep simulation updates.

        Args:
            max_updates: Maximum number of simulation updates to yield.
                ``0`` means no limit.

        Yields:
            Tuples containing ``(game_frame_count, game_time)``.

        Raises:
            RuntimeError: If ``start()`` has not been called.
            ValueError: If ``max_updates`` is negative.
        """
        if not self.started:
            raise RuntimeError("You must call 'start' before using a GameClock.")

        if max_updates < 0:
            raise ValueError("max_updates must be non-negative")

        real_time_now = self.get_real_time()
        self.real_time_passed = real_time_now - self.real_time

        # A replacement clock should normally be monotonic. Clamp unusual
        # negative deltas so a bad/custom clock cannot move time backwards.
        if self.real_time_passed < 0.0:
            self.real_time_passed = 0.0

        self.real_time = real_time_now
        self.clock_time += self.real_time_passed

        if not self.paused:
            self.virtual_time += self.real_time_passed * self.speed

        update_count = 0
        while (
            self.game_time + self.game_tick <= self.virtual_time
            and (max_updates == 0 or update_count < max_updates)
        ):
            self.game_frame_count += 1
            self.game_time = self.game_frame_count * self.game_tick
            update_count += 1
            yield self.game_frame_count, self.game_time

        self.between_frame = (
            self.virtual_time - self.game_time
        ) / self.game_tick

        if self.real_time_passed > 0.0:
            self.fps = 1.0 / self.real_time_passed
        else:
            self.fps = 0.0

        self.fps_sample_count += 1

        sample_elapsed = self.real_time - self.fps_sample_start_time
        if sample_elapsed > 1.0:
            self.average_fps = self.fps_sample_count / sample_elapsed
            self.fps_sample_start_time = self.real_time
            self.fps_sample_count = 0
