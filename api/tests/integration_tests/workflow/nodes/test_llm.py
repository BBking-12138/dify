import os
from unittest.mock import MagicMock

import pytest

from core.app.entities.app_invoke_entities import ModelConfigWithCredentialsEntity
from core.entities.provider_configuration import ProviderModelBundle, ProviderConfiguration
from core.entities.provider_entities import SystemConfiguration, CustomConfiguration, CustomProviderConfiguration
from core.model_manager import ModelInstance
from core.model_runtime.entities.model_entities import ModelType
from core.model_runtime.model_providers import ModelProviderFactory
from core.workflow.entities.node_entities import SystemVariable
from core.workflow.entities.variable_pool import VariablePool
from core.workflow.nodes.base_node import UserFrom
from core.workflow.nodes.llm.llm_node import LLMNode
from extensions.ext_database import db
from models.provider import ProviderType
from models.workflow import WorkflowNodeExecutionStatus

"""FOR MOCK FIXTURES, DO NOT REMOVE"""
from tests.integration_tests.model_runtime.__mock.openai import setup_openai_mock


@pytest.mark.parametrize('setup_openai_mock', [['chat']], indirect=True)
def test_execute_llm(setup_openai_mock):
    node = LLMNode(
        tenant_id='1',
        app_id='1',
        workflow_id='1',
        user_id='1',
        user_from=UserFrom.ACCOUNT,
        config={
            'id': 'llm',
            'data': {
                'title': '123',
                'type': 'llm',
                'model': {
                    'provider': 'openai',
                    'name': 'gpt-3.5-turbo',
                    'mode': 'chat',
                    'completion_params': {}
                },
                'prompt_template': [
                    {
                        'role': 'system',
                        'text': 'you are a helpful assistant.\ntoday\'s weather is {{#abc.output#}}.'
                    },
                    {
                        'role': 'user',
                        'text': '{{#sys.query#}}'
                    }
                ],
                'memory': None,
                'context': {
                    'enabled': False
                },
                'vision': {
                    'enabled': False
                }
            }
        }
    )

    # construct variable pool
    pool = VariablePool(system_variables={
        SystemVariable.QUERY: 'what\'s the weather today?',
        SystemVariable.FILES: [],
        SystemVariable.CONVERSATION: 'abababa'
    }, user_inputs={})
    pool.append_variable(node_id='abc', variable_key_list=['output'], value='sunny')

    credentials = {
        'openai_api_key': os.environ.get('OPENAI_API_KEY')
    }

    provider_instance = ModelProviderFactory().get_provider_instance('openai')
    model_type_instance = provider_instance.get_model_instance(ModelType.LLM)
    provider_model_bundle = ProviderModelBundle(
        configuration=ProviderConfiguration(
            tenant_id='1',
            provider=provider_instance.get_provider_schema(),
            preferred_provider_type=ProviderType.CUSTOM,
            using_provider_type=ProviderType.CUSTOM,
            system_configuration=SystemConfiguration(
                enabled=False
            ),
            custom_configuration=CustomConfiguration(
                provider=CustomProviderConfiguration(
                    credentials=credentials
                )
            )
        ),
        provider_instance=provider_instance,
        model_type_instance=model_type_instance
    )
    model_instance = ModelInstance(provider_model_bundle=provider_model_bundle, model='gpt-3.5-turbo')
    model_config = ModelConfigWithCredentialsEntity(
        model='gpt-3.5-turbo',
        provider='openai',
        mode='chat',
        credentials=credentials,
        parameters={},
        model_schema=model_type_instance.get_model_schema('gpt-3.5-turbo'),
        provider_model_bundle=provider_model_bundle
    )

    # Mock db.session.close()
    db.session.close = MagicMock()

    node._fetch_model_config = MagicMock(return_value=tuple([model_instance, model_config]))

    # execute node
    result = node.run(pool)

    assert result.status == WorkflowNodeExecutionStatus.SUCCEEDED
    assert result.outputs['text'] is not None
    assert result.outputs['usage']['total_tokens'] > 0
