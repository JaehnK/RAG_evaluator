from dataclasses import dataclass


@dataclass
class BEIRSample:
    query: str
    positive_doc: str
    negative_doc: str
