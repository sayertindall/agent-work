#!/usr/bin/env python3
"""Small command-line fixture used to validate a public command reference."""

import argparse


RECORDS = {
    "alpha": "First fixture record",
    "beta": "Second fixture record",
}


def list_records(_: argparse.Namespace) -> None:
    for record_id in RECORDS:
        print(record_id)


def show_record(args: argparse.Namespace) -> None:
    try:
        print(f"{args.record_id}: {RECORDS[args.record_id]}")
    except KeyError as exc:
        raise SystemExit(f"unknown record: {args.record_id}") from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fixture-cli",
        description="Inspect the small public record fixture.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    list_command = commands.add_parser("list", help="List available record IDs.")
    list_command.set_defaults(handler=list_records)

    show_command = commands.add_parser("show", help="Show one record by ID.")
    show_command.add_argument("record_id", help="Record ID to display.")
    show_command.set_defaults(handler=show_record)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()
