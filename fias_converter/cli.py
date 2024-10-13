import argparse
import importlib
import sys
from typing import Optional

from fias_converter.adapters import sqlalchemy
from fias_converter.core import process_data, process_schema


def _create_argparser() -> argparse.ArgumentParser:
    def help_str(text: Optional[str] = None) -> str:
        default = "по умолчанию: %(default)s"
        if text is None:
            return default
        return f"{text} ({default})"

    parser = argparse.ArgumentParser(description="Универсальный конвертер файлов ФИАС")
    parser.add_argument("--schema-files", nargs="+", default=[])
    parser.add_argument("--data-files", nargs="+", default=[])
    parser.add_argument("--delta-files", nargs="+", default=[])
    parser.add_argument(
        "--adapter-name", default=sqlalchemy.__name__, help=help_str("Имя адаптера")
    )
    parser.add_argument(
        "--out-url",
        default="sqlite:///out.db",
        help=help_str("Путь к файлу базы данных"),
    )
    return parser


def main():
    parser = _create_argparser()
    args = parser.parse_args()
    if not any((args.schema_files, args.data_files, args.delta_files)):
        print("Должен быть указан хотя бы один файл")
        parser.print_help()
        return 1

    sys.path.append(".")
    adapter_cls = importlib.import_module(args.adapter_name).fias_converter_adapter

    adapter = adapter_cls(args.out_url)
    for schema_name in args.schema_files:
        print(f"Обработка схемы {schema_name}")
        process_schema(schema_name, adapter)
    for data_name in args.data_files:
        print(f"Обработка данных {data_name}")
        process_data(data_name, adapter)
    for delta_name in args.delta_files:
        print(f"Обработка изменений {delta_name}")
        try:
            process_data(delta_name, adapter, True)
        except NotImplementedError:
            print("Данный адаптер не поддерживает изменения")

    adapter.close()
