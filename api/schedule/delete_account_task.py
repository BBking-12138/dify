import logging
import time

import app
import click
from extensions.ext_database import db
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError

from api.libs.helper import get_current_datetime
from api.models.account import (Account, AccountDeletionLog,
                                AccountDeletionLogStatus, AccountIntegrate,
                                Tenant, TenantAccountJoin,
                                TenantAccountJoinRole)
from api.models.api_based_extension import APIBasedExtension
from api.models.dataset import (AppDatasetJoin, Dataset, DatasetPermission,
                                Document, DocumentSegment)
from api.models.model import (ApiToken, App, AppAnnotationSetting,
                              AppModelConfig, Conversation,
                              DatasetRetrieverResource, EndUser, InstalledApp,
                              Message, MessageAgentThought, MessageAnnotation,
                              MessageChain, MessageFeedback, MessageFile,
                              RecommendedApp, Site, Tag, TagBinding)
from api.models.provider import (LoadBalancingModelConfig, Provider,
                                 ProviderModel, ProviderModelSetting,
                                 TenantDefaultModel,
                                 TenantPreferredModelProvider)
from api.models.source import (DataSourceApiKeyAuthBinding,
                               DataSourceOauthBinding)
from api.models.tools import (ApiToolProvider, BuiltinToolProvider,
                              ToolConversationVariables)
from api.models.web import PinnedConversation, SavedMessage
from api.tasks.mail_account_deletion_done_task import \
    send_deletion_success_task

logger = logging.getLogger(__name__)


def _delete_app(app: App, account_id):
    """Actual deletion of app and related tables.

    Args:
        app: App object
        account_id: Account ID
    """

    # api_tokens
    db.session.query(ApiToken).filter(ApiToken.app_id == app.id).delete()

    # app_annotation_settings
    db.session.query(AppAnnotationSetting).filter(AppAnnotationSetting.app_id == app.id).delete()

    # app_dataset_joins
    db.session.query(AppDatasetJoin).filter(AppDatasetJoin.app_id == app.id).delete()

    # app_model_configs
    db.session.query(AppModelConfig).filter(AppModelConfig.app_id == app.id).delete()

    # conversations
    db.session.query(Conversation).filter(Conversation.app_id == app.id).delete()

    # end_users
    db.session.query(EndUser).filter(EndUser.app_id == app.id).delete()

    # installed_apps
    db.session.query(InstalledApp).filter(InstalledApp.app_id == app.id).delete()

    ### messages ###
    message_ids = db.session.query(Message.id).filter(Message.app_id == app.id).all()
    # message_agent_thoughts
    db.session.query(MessageAgentThought).filter(MessageAgentThought.message_id.in_(message_ids)).delete()
    # message_chains
    db.session.query(MessageChain).filter(MessageChain.message_id.in_(message_ids)).delete()
    # message_files
    db.session.query(MessageFile).filter(MessageFile.message_id.in_(message_ids)).delete()
    # message_feedbacks
    db.session.query(MessageFeedback).filter(MessageFeedback.message_id.in_(message_ids)).delete()

    # message_annotations
    db.session.query(MessageAnnotation).filter(MessageAnnotation.app_id == app.id).delete()

    # pinned_conversations
    db.session.query(PinnedConversation).filter(PinnedConversation.app_id == app.id).delete()

    # recommended_apps
    db.session.query(RecommendedApp).filter(RecommendedApp.app_id == app.id).delete()

    # saved_messages
    db.session.query(SavedMessage).filter(SavedMessage.app_id == app.id).delete()

    # sites
    db.session.query(Site).filter(Site.app_id == app.id).delete()

    db.session.delete(app)


def _delete_tenant_as_owner(tenant_account_join: TenantAccountJoin):
    """Actual deletion of tenant as owner. Related tables will also be deleted.

    Args:
        tenant_account_join (TenantAccountJoin): _description_
    """
    tenant_id, account_id = tenant_account_join.tenant_id, tenant_account_join.account_id

    member_ids = db.session.query(TenantAccountJoin.account_id).filter(TenantAccountJoin.tenant_id == tenant_id).all()

    # api_based_extensions
    db.session.query(APIBasedExtension).filter(APIBasedExtension.tenant_id == tenant_id).delete()

    # delete all apps of this tenant
    apps = db.session.query(App).filter(App.tenant_id == tenant_id).all()
    for app in apps:
        _delete_app(app, account_id)

    # dataset_permissions
    db.session.query(DatasetPermission).filter(DatasetPermission.tenant_id == tenant_id).delete()

    # datasets
    dataset_ids = db.session.query(Dataset.id).filter(Dataset.tenant_id == tenant_id).all()
    db.session.query(Dataset).filter(Dataset.tenant_id == tenant_id).delete()

    # documents
    document_ids = db.session.query(Document.id).filter(Document.tenant_id == tenant_id).all()
    db.session.query(Document).filter(Document.tenant_id == tenant_id).delete()

    # data_source_api_key_auth_bindings
    db.session.query(DataSourceApiKeyAuthBinding).filter(DataSourceApiKeyAuthBinding.tenant_id == tenant_id).delete()

    # data_source_oauth_bindings
    db.session.query(DataSourceOauthBinding).filter(DataSourceOauthBinding.tenant_id == tenant_id).delete()

    # document_segments
    db.session.query(DocumentSegment).filter(DocumentSegment.tenant_id == tenant_id).delete()

    # load_balancing_model_configs
    db.session.query(LoadBalancingModelConfig).filter(LoadBalancingModelConfig.tenant_id == tenant_id).delete()

    # provider_models
    db.session.query(ProviderModel).filter(ProviderModel.tenant_id == tenant_id).delete()

    # provder_model_settings
    db.session.query(ProviderModelSetting).filter(ProviderModelSetting.tenant_id == tenant_id).delete()

    # skip provider_orders (TODO: confirm this)

    # providers
    db.session.query(Provider).filter(Provider.tenant_id == tenant_id).delete()

    # tag_bindings
    db.session.query(TagBinding).filter(TagBinding.tenant_id == tenant_id).delete()

    # tags
    db.session.query(Tag).filter(Tag.tenant_id == tenant_id).delete()

    # tenant_default_models
    db.session.query(TenantDefaultModel).filter(TenantDefaultModel.tenant_id == tenant_id).delete()

    # tenant_preferred_model_providers
    db.session.query(TenantPreferredModelProvider).filter(TenantPreferredModelProvider.tenant_id == tenant_id).delete()

    # tool_api_providers
    db.session.query(ApiToolProvider).filter(ApiToolProvider.tenant_id == tenant_id).delete()

    # tool_built_in_providers
    db.session.query(BuiltinToolProvider).filter(BuiltinToolProvider.tenant_id == tenant_id).delete()

    # tool_conversation_variables
    db.session.query(ToolConversationVariables).filter(ToolConversationVariables.tenant_id == tenant_id).delete()

    # Delete all tenant_account_joins of this tenant
    db.session.query(TenantAccountJoin).filter(TenantAccountJoin.tenant_id == tenant_id).delete()

    # Delete tenant
    db.session.query(Tenant).filter(Tenant.id == tenant_id).delete()


def _delete_tenant_as_non_owner(tenant_account_join: TenantAccountJoin):
    """Actual deletion of tenant as non-owner. Related tables will also be deleted.

    Args:
        tenant_account_join (TenantAccountJoin): _description_
    """

    db.session.delete(tenant_account_join)


def _delete_user(log: AccountDeletionLog, account: Account) -> bool:
    """Actual deletion of user account.

    Args:
        log (AccountDeletionLog): Account deletion log object

    Returns:
        bool: True if deletion is successful, False otherwise
    """
    success = True
    account_id = log.account_id

    # Wrap in transaction
    try:
        db.session.begin()

        # find all tenants this account belongs to
        tenant_account_joins = db.session.query(TenantAccountJoin).filter(TenantAccountJoin.account_id == account_id).all()

        # process all tenants
        for tenant_account_join in tenant_account_joins:
            if tenant_account_join.role == TenantAccountJoinRole.OWNER.value:
                _delete_tenant_as_owner(tenant_account_join)
            else:
                _delete_tenant_as_non_owner(tenant_account_join)

        # account_integrates
        db.session.query(AccountIntegrate).filter(AccountIntegrate.account_id == account_id).delete()

        # dataset_retriever_resources
        db.session.query(DatasetRetrieverResource).filter(DatasetRetrieverResource.created_by == account_id).delete()

        # delete account
        db.session.delete(account)

        # update log status
        log.status = AccountDeletionLogStatus.COMPLETED
        log.updated_at = get_current_datetime()

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.exception(click.style(f"Failed to delete account {log.account_id}, error: {e}", fg="red"))
        log.status = AccountDeletionLogStatus.FAILED
        log.updated_at = get_current_datetime()
        success = False
    finally:
        db.session.commit()
        db.session.close()
        return success


@app.celery.task(queue="dataset")
def delete_account_task():
    logger.info(click.style("Start delete account task.", fg="green"))
    start_at = time.perf_counter()

    # Query avaliable deletion tasks from database
    queue_size = (
        db.session.query(AccountDeletionLog)
        .filter(or_(AccountDeletionLog.status == AccountDeletionLogStatus.PENDING,
                    AccountDeletionLog.status == AccountDeletionLogStatus.FAILED))  # retry failed tasks
        .count()
    )
    logger.info(f"Found {queue_size} delete account tasks in queue.")

    # execute deletion in batch
    batch_size = 50
    n_batches = (queue_size + batch_size - 1) // batch_size
    for i in range(n_batches):
        offset = i * batch_size
        limit = min(queue_size - offset, batch_size)

        logger.info(f"Start delete account task batch {i+1}/{n_batches}.")

        delete_logs = (
            db.session.query(AccountDeletionLog)
            .filter(or_(AccountDeletionLog.status == AccountDeletionLogStatus.PENDING,
                    AccountDeletionLog.status == AccountDeletionLogStatus.FAILED))
            .order_by(AccountDeletionLog.created_at.desc())
            .offset(offset)
            .limit(limit)
        )

        if delete_logs:
            for log in delete_logs:
                account = db.session.query(Account).filter(Account.id == log.account_id).first()
                if not account:
                    logger.exception(click.style(f"Account {log.account_id} not found.", fg="red"))
                    log.status = AccountDeletionLogStatus.FAILED
                    log.updated_at = get_current_datetime()
                    db.session.commit()
                    continue

                # Delete and notify
                if (_delete_user(log)):
                    send_deletion_success_task.delay(account.interface_language, account.email)

    end_at = time.perf_counter()
    logger.info(click.style("Delete account tasks of size {} completed with latency: {}".format(len(delete_logs), end_at - start_at), fg="green"))

    db.session.remove()
