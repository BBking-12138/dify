from collections.abc import Mapping, Sequence
from typing import Any

from core.workflow.constants import SYSTEM_VARIABLE_NODE_ID
from core.workflow.entities.node_entities import NodeRunResult
from core.workflow.nodes.base_node import BaseNode
from core.workflow.nodes.start.entities import StartNodeData
from enums import NodeType
from models.workflow import WorkflowNodeExecutionStatus


class StartNode(BaseNode):
    _node_data_cls = StartNodeData
    _node_type = NodeType.START

    def _run(self) -> NodeRunResult:
        """
        Run node
        :return:
        """
        node_inputs = dict(self.graph_runtime_state.variable_pool.user_inputs)
        system_inputs = self.graph_runtime_state.variable_pool.system_variables

        # TODO: System variables should be directly accessible, no need for special handling
        # Set system variables as node outputs.
        for var in system_inputs:
            node_inputs[SYSTEM_VARIABLE_NODE_ID + "." + var] = system_inputs[var]

        return NodeRunResult(status=WorkflowNodeExecutionStatus.SUCCEEDED, inputs=node_inputs, outputs=node_inputs)

    @classmethod
    def _extract_variable_selector_to_variable_mapping(
        cls, graph_config: Mapping[str, Any], node_id: str, node_data: StartNodeData
    ) -> Mapping[str, Sequence[str]]:
        """
        Extract variable selector to variable mapping
        :param graph_config: graph config
        :param node_id: node id
        :param node_data: node data
        :return:
        """
        return {}
