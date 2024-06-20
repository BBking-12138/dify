from pydantic import BaseModel, Field


class DeploymentConfigs(BaseModel):
    """
    Deployment configs
    """
    EDITION: str = Field(
        description='deployment edition',
        default='SELF_HOSTED',
    )

    DEPLOY_ENV: str = Field(
        description='deployment environment, default to PRODUCTION.',
        default='PRODUCTION',
    )
