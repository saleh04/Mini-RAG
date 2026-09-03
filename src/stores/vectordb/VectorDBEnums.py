from enum import Enum  # noqa: N999


class VectorDBEnums(Enum):
    QDRANT = "QDRANT"

class DistanceMethodEnums(Enum):
    COSINE = "cosine"
    DOT = "dot"