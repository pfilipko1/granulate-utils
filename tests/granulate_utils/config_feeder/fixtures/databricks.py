from __future__ import annotations

from granulate_utils.config_feeder.core.models.cluster import CloudProvider
from tests.granulate_utils.config_feeder.fixtures.base import NodeMockBase


class DatabricksNodeMock(NodeMockBase):
    def __init__(
        self,
        *,
        provider: CloudProvider = CloudProvider.AWS,
        cluster_id: str = "",
        instance_id: str = "",
        is_master: bool = False,
    ) -> None:
        super().__init__()
        driver_instance_id = instance_id if is_master else "aaa"
        properties = {
            "databricks.instance.metadata.cloudProvider": provider.upper(),
            "databricks.instance.metadata.instanceId": instance_id,
            "spark.databricks.clusterUsageTags.clusterId": cluster_id,
            "spark.databricks.clusterUsageTags.clusterSomeSecretPassword": "password123",
        }

        if is_master:
            properties["spark.databricks.clusterUsageTags.driverInstanceId"] = driver_instance_id

        config = "\n".join([f'{k} = "{v}"' for k, v in properties.items()])
        self.mock_file(
            "/databricks/common/conf/deploy.conf",
            f"""all-projects {{
                {config}
            }}""",
        )
