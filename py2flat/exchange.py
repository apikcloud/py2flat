from py2flat.schemas import Schema
from py2flat.segment import Segment


class Exchange:
    schema: Schema
    segments: list[Segment] = []

    def __init__(self, schema: Schema) -> None:
        self.schema = schema

    def set_header(self, **vals: dict) -> None:
        seg = self.schema.create_segment("Header", vals)
        self.segments.insert(0, seg)

    def add_segment(self, identifier: str, vals: dict) -> None:
        seg = self.schema.create_segment(identifier, vals)
        self.segments.append(seg)

    def dump(self) -> str:
        return "\n".join([seg.dump(fill=self.schema.fill) for seg in self.segments])
