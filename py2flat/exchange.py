from collections import Counter

from py2flat.schemas import Schema


class Exchange:
    def __init__(self, schema: Schema) -> None:
        self.schema = schema
        self.segments = []

    def set_header(self, **vals: dict) -> None:
        seg = self.schema.create_segment("Header", vals)
        self.segments.insert(0, seg[0])

    def add_segment(self, identifier: str, vals: dict) -> None:
        segments = self.schema.create_segment(identifier, vals)
        self.segments += segments

    def check(self) -> None | ValueError:
        names = [seg.name for seg in self.segments]
        required = [seg.name for seg in self.schema.segments if seg.required]
        multiple = [seg.name for seg in self.schema.segments if seg.multiple]

        for name in required:
            if name not in names:
                raise ValueError(f"Missing required segment: {name}")

        for name, value in Counter(names).items():
            if value > 1 and name not in multiple:
                raise ValueError(f"Too manys segments '{name}' ({value}).")

    def dump(self) -> str:
        self.check()
        return "\n".join([seg.dump(fill=self.schema.fill) for seg in self.segments])
