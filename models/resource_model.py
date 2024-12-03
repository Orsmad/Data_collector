from pydantic import BaseModel, Field, field_validator


class NonCompliantResource(BaseModel):
    resource_id: str = Field(..., alias="ResourceId")
    status: str = Field(..., alias="Status")

    class ConfigDict:
        populate_by_name = True

    @field_validator("status")
    def check_status(cls, value):
        if value != "NON_COMPLIANT":
            raise ValueError("status must be 'NON_COMPLIANT'")
        return value
