from typing import Any

from langchain.tools import BaseTool

from core.app.app_config.entities import DatasetRetrieveConfigEntity
from core.app.entities.app_invoke_entities import InvokeFrom
from core.callback_handler.index_tool_callback_handler import DatasetIndexToolCallbackHandler
from core.rag.retrieval.dataset_retrieval import DatasetRetrieval
from core.tools.entities.common_entities import I18nObject
from core.tools.entities.tool_entities import (
    ToolDescription,
    ToolIdentity,
    ToolInvokeMessage,
    ToolParameter,
    ToolProviderType,
)
from core.tools.tool.tool import Tool


class DatasetRetrieverTool(Tool):
    langchain_tool: BaseTool

    @staticmethod
    def get_dataset_tools(tenant_id: str,
                          dataset_ids: list[str],
                          retrieve_config: DatasetRetrieveConfigEntity,
                          return_resource: bool,
                          invoke_from: InvokeFrom,
                          hit_callback: DatasetIndexToolCallbackHandler
                          ) -> list['DatasetRetrieverTool']:
        """
        get dataset tool
        """
        # check if retrieve_config is valid
        if dataset_ids is None or len(dataset_ids) == 0:
            return []
        if retrieve_config is None:
            return []

        feature = DatasetRetrieval()

        # save original retrieve strategy, and set retrieve strategy to SINGLE
        # Agent only support SINGLE mode
        original_retriever_mode = retrieve_config.retrieve_strategy
        retrieve_config.retrieve_strategy = DatasetRetrieveConfigEntity.RetrieveStrategy.SINGLE
        langchain_tools = feature.to_dataset_retriever_tool(
            tenant_id=tenant_id,
            dataset_ids=dataset_ids,
            retrieve_config=retrieve_config,
            return_resource=return_resource,
            invoke_from=invoke_from,
            hit_callback=hit_callback
        )
        # restore retrieve strategy
        retrieve_config.retrieve_strategy = original_retriever_mode

        # convert langchain tools to Tools
        tools = []
        for langchain_tool in langchain_tools:
            tool = DatasetRetrieverTool(
                langchain_tool=langchain_tool,
                identity=ToolIdentity(provider='', author='', name=langchain_tool.name, label=I18nObject(en_US='', zh_Hans='')),
                parameters=[],
                is_team_authorization=True,
                description=ToolDescription(
                    human=I18nObject(en_US='', zh_Hans=''),
                    llm=langchain_tool.description),
                runtime=DatasetRetrieverTool.Runtime()
            )

            tools.append(tool)

        return tools

    def get_runtime_parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter(name='query',
                          label=I18nObject(en_US='', zh_Hans=''),
                          human_description=I18nObject(en_US='', zh_Hans=''),
                          type=ToolParameter.ToolParameterType.STRING,
                          form=ToolParameter.ToolParameterForm.LLM,
                          llm_description='Query for the dataset to be used to retrieve the dataset.',
                          required=True,
                          default=''),
        ]
    
    def tool_provider_type(self) -> ToolProviderType:
        return ToolProviderType.DATASET_RETRIEVAL

    def _invoke(self, user_id: str, tool_parameters: dict[str, Any]) -> ToolInvokeMessage | list[ToolInvokeMessage]:
        """
        invoke dataset retriever tool
        """
        query = tool_parameters.get('query', None)
        if not query:
            return self.create_text_message(text='please input query')

        # invoke dataset retriever tool
        result = self.langchain_tool._run(query=query)

        return self.create_text_message(text=result)

    def validate_credentials(self, credentials: dict[str, Any], parameters: dict[str, Any]) -> None:
        """
        validate the credentials for dataset retriever tool
        """
        pass
