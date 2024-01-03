from typing import Annotated, Any

from astropy.time import Time
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

from ._adaptor_tags import asdf_tags
from ._base import Adaptor

__all__ = ["AstropyTime"]


class _AstropyTimePydanticAnnotation(Adaptor):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        def validate_from_str(value: str) -> Time:
            return Time(value)

        validate_from_str = core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(validate_from_str),
            ],
        )

        return core_schema.json_or_python_schema(
            json_schema=validate_from_str,
            python_schema=core_schema.is_instance_schema(Time),
            serialization=core_schema.plain_serializer_function_ser_schema(lambda value: value),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        _core_schema: core_schema.CoreSchema,
        handler: GetJsonSchemaHandler,
    ) -> JsonSchemaValue:
        return {
            "title": None,
            "tag": asdf_tags.ASTROPY_TIME.value,
        }

    @classmethod
    def make_default(cls, **kwargs) -> Time:
        """
        Create a default instance of the time

        Returns
        -------
        The default time: 2020-01-01T00:00:00.0
        """

        return Time("2020-01-01T00:00:00.0", format="isot", scale="utc")


AstropyTime = Annotated[Time, _AstropyTimePydanticAnnotation]
