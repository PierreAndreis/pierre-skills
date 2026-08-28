#!/usr/bin/env python3
"""Measure raw row-major RGBA8 shader output and enforce simple nonblank-image gates."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path


def fraction(value: str) -> float:
    parsed = float(value)
    if not math.isfinite(parsed) or parsed < 0 or parsed > 1:
        raise argparse.ArgumentTypeError("expected a finite fraction in [0, 1]")
    return parsed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="raw RGBA8 file from target.read()")
    parser.add_argument("--width", type=int, required=True)
    parser.add_argument("--height", type=int, required=True)
    parser.add_argument("--black-threshold", type=int, default=3)
    parser.add_argument("--alpha-threshold", type=int, default=3)
    parser.add_argument("--max-black-fraction", type=fraction)
    parser.add_argument("--max-transparent-fraction", type=fraction)
    parser.add_argument("--min-luma-stddev", type=float)
    parser.add_argument("--min-unique-colors", type=int)
    parser.add_argument("--unique-cap", type=int, default=100_000, help="stop tracking exact unique colors at this bound")
    parser.add_argument("--max-bytes", type=int, default=64 * 1024 * 1024)
    parser.add_argument("--output")
    args = parser.parse_args()

    try:
        if args.width < 1 or args.height < 1:
            raise ValueError("--width and --height must be positive")
        if not 0 <= args.black_threshold <= 255 or not 0 <= args.alpha_threshold <= 255:
            raise ValueError("thresholds must be integers in [0, 255]")
        if args.unique_cap < 1:
            raise ValueError("--unique-cap must be positive")
        if args.min_unique_colors is not None and args.min_unique_colors > args.unique_cap:
            raise ValueError("--min-unique-colors cannot exceed --unique-cap")
        expected = args.width * args.height * 4
        if expected > args.max_bytes:
            raise ValueError(f"expected {expected} bytes exceeds --max-bytes={args.max_bytes}")
        data = Path(args.input).read_bytes()
        if len(data) != expected:
            raise ValueError(f"expected exactly {expected} bytes for {args.width}x{args.height} RGBA8, got {len(data)}")

        pixels = expected // 4
        channel_min = [255, 255, 255, 255]
        channel_max = [0, 0, 0, 0]
        channel_sum = [0, 0, 0, 0]
        black = transparent = opaque = 0
        colors: set[bytes] = set()
        unique_capped = False
        luma_sum = luma_squared_sum = 0.0
        horizontal_difference = 0
        horizontal_pairs = 0

        previous_row: list[tuple[int, int, int]] = []
        vertical_difference = 0
        vertical_pairs = 0
        for y in range(args.height):
            row: list[tuple[int, int, int]] = []
            previous_pixel: tuple[int, int, int] | None = None
            for x in range(args.width):
                offset = (y * args.width + x) * 4
                rgba = data[offset : offset + 4]
                values = tuple(rgba)
                if len(colors) < args.unique_cap:
                    colors.add(rgba)
                elif rgba not in colors:
                    unique_capped = True
                for channel, value in enumerate(values):
                    channel_min[channel] = min(channel_min[channel], value)
                    channel_max[channel] = max(channel_max[channel], value)
                    channel_sum[channel] += value
                rgb = values[:3]
                if max(rgb) <= args.black_threshold:
                    black += 1
                if values[3] <= args.alpha_threshold:
                    transparent += 1
                if values[3] == 255:
                    opaque += 1
                luma = (0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]) / 255
                luma_sum += luma
                luma_squared_sum += luma * luma
                if previous_pixel is not None:
                    horizontal_difference += sum(abs(rgb[index] - previous_pixel[index]) for index in range(3))
                    horizontal_pairs += 1
                if previous_row:
                    above = previous_row[x]
                    vertical_difference += sum(abs(rgb[index] - above[index]) for index in range(3))
                    vertical_pairs += 1
                row.append(rgb)
                previous_pixel = rgb
            previous_row = row

        mean_luma = luma_sum / pixels
        variance = max(0.0, luma_squared_sum / pixels - mean_luma * mean_luma)
        payload = {
            "width": args.width,
            "height": args.height,
            "pixels": pixels,
            "channel_min": dict(zip("rgba", channel_min)),
            "channel_max": dict(zip("rgba", channel_max)),
            "channel_mean": {name: channel_sum[index] / pixels for index, name in enumerate("rgba")},
            "black_fraction": black / pixels,
            "transparent_fraction": transparent / pixels,
            "opaque_fraction": opaque / pixels,
            "unique_colors": len(colors),
            "unique_colors_is_lower_bound": unique_capped,
            "luma_mean": mean_luma,
            "luma_stddev": math.sqrt(variance),
            "mean_neighbor_rgb_difference": (
                (horizontal_difference + vertical_difference) / (horizontal_pairs + vertical_pairs)
                if horizontal_pairs + vertical_pairs else 0.0
            ),
        }

        failures = []
        if args.max_black_fraction is not None and payload["black_fraction"] > args.max_black_fraction:
            failures.append(f"black_fraction {payload['black_fraction']:.6f} exceeds {args.max_black_fraction}")
        if args.max_transparent_fraction is not None and payload["transparent_fraction"] > args.max_transparent_fraction:
            failures.append(f"transparent_fraction {payload['transparent_fraction']:.6f} exceeds {args.max_transparent_fraction}")
        if args.min_luma_stddev is not None and payload["luma_stddev"] < args.min_luma_stddev:
            failures.append(f"luma_stddev {payload['luma_stddev']:.6f} is below {args.min_luma_stddev}")
        if args.min_unique_colors is not None and payload["unique_colors"] < args.min_unique_colors:
            failures.append(f"unique_colors {payload['unique_colors']} is below {args.min_unique_colors}")
        payload["gate_failures"] = failures
        payload["valid"] = not failures

        rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
        if args.output:
            output = Path(args.output)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(rendered, encoding="utf-8")
        else:
            print(rendered, end="")
        return 0 if not failures else 1
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
