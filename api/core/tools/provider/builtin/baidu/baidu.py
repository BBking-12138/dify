from typing import Any
from core.tools.errors import ToolProviderCredentialValidationError
from core.tools.provider.builtin.baidu.tools.baidu_search import BaiduSearchTool
from core.tools.provider.builtin_tool_provider import BuiltinToolProviderController

class BaiduProvider(BuiltinToolProviderController):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            # 创建百度搜索工具的实例
            BaiduSearchTool().fork_tool_runtime(
                runtime={
                    "credentials": credentials,
                }
            ).invoke(
                user_id="",
                tool_parameters={"query": "test", "result_type": "link"},
            )
        except Exception as e:
            # 捕获异常并抛出凭证验证错误
            raise ToolProviderCredentialValidationError(str(e))

