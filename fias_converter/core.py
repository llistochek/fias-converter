import os
from typing import Union

from lxml import etree  # type: ignore

from .adapters.base import BaseAdapter

AnyPath = Union[str, os.PathLike]


def process_schema(schema_path: AnyPath, adapter: BaseAdapter):
    schema_f = open(schema_path, "rb")
    columns = []
    attr_name = None
    tablename = None
    for _, elem in etree.iterparse(
        schema_f,
        events=("start",),
        tag=("{*}element", "{*}attribute", "{*}restriction"),
    ):
        localname = etree.QName(elem).localname
        raw_type = None
        if localname == "element" and tablename is None:
            tablename = elem.get("name")
        elif localname == "attribute":
            attr_name = elem.get("name")
            if rtype := elem.get("type"):
                raw_type = rtype
        elif localname == "restriction":
            raw_type = elem.get("base")
        if raw_type:
            columns.append((attr_name, raw_type))
    if not tablename:
        raise ValueError("No tablename found")
    adapter.create_table(tablename, columns)
    schema_f.close()
    adapter.commit()


def process_data(data_path: AnyPath, adapter: BaseAdapter, is_delta=False):
    data_f = open(data_path, "rb")
    context = etree.iterparse(data_f, events=("start", "end"))
    _, root = next(context)
    tablename = root.tag
    for ev, element in context:
        if ev != "end":
            continue

        attributes = dict(element.attrib)
        if len(attributes) != 0:
            if is_delta:
                adapter.upsert_row(tablename, attributes)
            else:
                adapter.insert_row(tablename, attributes)
        root.clear()  # Thanks! https://stackoverflow.com/a/12161185

    data_f.close()
    adapter.commit()
