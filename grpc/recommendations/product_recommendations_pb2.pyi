from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProductRecommendationRequest(_message.Message):
    __slots__ = ["id", "price", "stock", "title"]
    ID_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    STOCK_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    id: int
    price: int
    stock: int
    title: str
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., price: _Optional[int] = ..., stock: _Optional[int] = ...) -> None: ...

class ProductRecommendationsRequest(_message.Message):
    __slots__ = ["items"]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[ProductRecommendationRequest]
    def __init__(self, items: _Optional[_Iterable[_Union[ProductRecommendationRequest, _Mapping]]] = ...) -> None: ...

class RecommendationRequest(_message.Message):
    __slots__ = ["cat_id", "per_page", "userID"]
    CAT_ID_FIELD_NUMBER: _ClassVar[int]
    PER_PAGE_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    cat_id: int
    per_page: int
    userID: int
    def __init__(self, userID: _Optional[int] = ..., cat_id: _Optional[int] = ..., per_page: _Optional[int] = ...) -> None: ...
