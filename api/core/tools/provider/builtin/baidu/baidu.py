from core.tools.entities.tool_entities import ToolInvokeMessage, ToolProviderType
from core.tools.tool.tool import Tool
from core.tools.provider.builtin_tool_provider import BuiltinToolProviderController
from core.tools.errors import ToolProviderCredentialValidationError

from core.tools.provider.builtin.google.tools.google_search import GoogleSearchTool

from typing import Any, Dict

class GoogleProvider(BuiltinToolProviderController):
    def _validate_credentials(self, credentials: Dict[str, Any]) -> None:
        try:
            # 1. 此处需要使用 GoogleSearchTool()实例化一个 GoogleSearchTool，它会自动加载 GoogleSearchTool 的 yaml 配置，但是此时它内部没有凭据信息
            # 2. 随后需要使用 fork_tool_runtime 方法，将当前的凭据信息传递给 GoogleSearchTool
            # 3. 最后 invoke 即可，参数需要根据 GoogleSearchTool 的 yaml 中配置的参数规则进行传递
            GoogleSearchTool().fork_tool_runtime(
                meta={
                    "credentials": credentials,
                }
            ).invoke(
                user_id='',
                tool_Parameters={
                    "query": "test",
                    "result_type": "link"
                },
            )
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
