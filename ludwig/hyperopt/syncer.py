from typing import Callable, Dict, List, Optional, Tuple

from ray.air._internal.remote_storage import delete_at_uri, download_from_uri, upload_to_uri
from ray.tune.syncer import _BackgroundSyncer

from ludwig.backend import Backend
from ludwig.utils.data_utils import use_credentials


class RemoteSyncer(_BackgroundSyncer):
    def __init__(self, backend: Backend, sync_period: float = 300.0):
        super().__init__(sync_period=sync_period)
        self.backend = backend

    def _sync_up_command(self, local_path: str, uri: str, exclude: Optional[List] = None) -> Tuple[Callable, Dict]:
        with use_credentials(self.backend.hyperopt_sync_manager.credentials):
            return (
                upload_to_uri,
                dict(local_path=local_path, uri=uri, exclude=exclude),
            )

    def _sync_down_command(self, uri: str, local_path: str) -> Tuple[Callable, Dict]:
        with use_credentials(self.backend.hyperopt_sync_manager.credentials):
            return (
                download_from_uri,
                dict(uri=uri, local_path=local_path),
            )

    def _delete_command(self, uri: str) -> Tuple[Callable, Dict]:
        with use_credentials(self.backend.hyperopt_sync_manager.credentials):
            return (
                delete_at_uri,
                dict(uri=uri),
            )