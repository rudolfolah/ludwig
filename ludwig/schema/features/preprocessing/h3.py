from marshmallow_dataclass import dataclass

from ludwig.constants import H3, MISSING_VALUE_STRATEGY_OPTIONS, PREPROCESSING
from ludwig.schema import schema_utils as schema_utils
from ludwig.schema.features.preprocessing.base import BasePreprocessingConfig
from ludwig.schema.features.preprocessing.utils import register_preprocessor
from ludwig.schema.metadata.feature_metadata import FEATURE_METADATA


@register_preprocessor(H3)
@dataclass(repr=False)
class H3PreprocessingConfig(BasePreprocessingConfig):

    missing_value_strategy: str = schema_utils.StringOptions(
        MISSING_VALUE_STRATEGY_OPTIONS,
        default="fill_with_const",
        allow_none=False,
        description="What strategy to follow when there's a missing value in an h3 column",
        parameter_metadata=FEATURE_METADATA[H3][PREPROCESSING]["missing_value_strategy"],
    )

    fill_value: int = schema_utils.PositiveInteger(
        default=576495936675512319,
        allow_none=False,
        description="The value to replace missing values with in case the missing_value_strategy is fill_with_const",
        parameter_metadata=FEATURE_METADATA[H3][PREPROCESSING]["fill_value"],
    )
