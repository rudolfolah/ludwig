from abc import ABC
from typing import Dict

from marshmallow_dataclass import dataclass

from ludwig.api_annotations import DeveloperAPI
from ludwig.constants import LOSS, TEST, TRAIN, VALIDATION
from ludwig.schema import utils as schema_utils
from ludwig.schema.features.utils import output_config_registry
from ludwig.schema.hyperopt.executor import ExecutorConfig, ExecutorDataclassField
from ludwig.schema.hyperopt.search_algorithm import BaseSearchAlgorithmConfig, SearchAlgorithmDataclassField


@DeveloperAPI
@dataclass
class HyperoptConfig(schema_utils.BaseMarshmallowConfig, ABC):
    """Basic hyperopt settings."""

    def get_hyperopt_metric_options():
        all_metrics = []
        for oftype in output_config_registry:
            ofcls = output_config_registry[oftype]
            all_metrics += ofcls.get_output_metric_functions().keys()
        return all_metrics

    output_feature: str = "combined"  # TODO: make more restrictive

    goal: str = schema_utils.StringOptions(
        options=["minimize", "maximize"],
        default="minimize",
        allow_none=False,
        description=(
            "Indicates if to minimize or maximize a metric or a loss of any of the output features on any of the "
            "dataset splits. Available values are: minimize (default) or maximize."
        ),
    )

    metric: str = schema_utils.StringOptions(
        options=get_hyperopt_metric_options(),
        default=LOSS,
        allow_none=False,
        description=(
            "The metric that we want to optimize for. The default one is loss, but depending on the type of the "
            "feature defined in output_feature, different metrics and losses are available. Check the metrics section "
            "of the specific output feature type to figure out what metrics are available to use."
        ),
    )

    split: str = schema_utils.StringOptions(
        options=[TRAIN, VALIDATION, TEST],
        default=VALIDATION,
        allow_none=False,
        description=(
            "The split of data that we want to compute our metric on. By default it is the validation split, but "
            "you have the flexibility to specify also train or test splits."
        ),
    )

    search_alg: BaseSearchAlgorithmConfig = SearchAlgorithmDataclassField(
        description=(
            "Specifies the algorithm to sample the defined parameters space. Candidate algorithms are those "
            "found in Ray Tune's Search Algorithms."
        )
    )

    executor: ExecutorConfig = ExecutorDataclassField(
        description=(
            "specifies how to execute the hyperparameter optimization. The execution could happen locally in a serial "
            "manner or in parallel across multiple workers and with GPUs as well if available. The executor section "
            "includes specification for work scheduling and the number of samples to generate."
        )
    )

    parameters: Dict = schema_utils.Dict()


@DeveloperAPI
def get_hyperopt_jsonschema():
    props = schema_utils.unload_jsonschema_from_marshmallow_class(HyperoptConfig)["properties"]

    return {
        "type": "object",
        "properties": props,
        "title": "hyperopt_options",
        "description": "Settings for hyperopt",
    }
