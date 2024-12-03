import pytest
from pydantic import ValidationError
from typing import List
from models.resource_model import NonCompliantResource

# Test data
data_list = [
    {
        "ComplianceType": "Association",
        "ResourceType": "ManagedInstance",
        "ResourceId": "i-1234567890abcdef0",
        "Status": "NON_COMPLIANT",
        "ExtraField1": "value1",
        "ExtraField2": "value2",
    },
    {
        "ComplianceType": "Association",
        "ResourceType": "ManagedInstance",
        "ResourceId": "i-abcdef01234567890",
        "Status": "NON_COMPLIANT",
        "ExtraField1": "value3",
        "ExtraField2": "value4",
    },
    {
        "ComplianceType": "Association",
        "ResourceType": "ManagedInstance",
        "ResourceId": "x-abcdef01234567891",
        "Status": "NON_COMPLIANT",
        "ExtraField1": "value5",
        "ExtraField2": "value6",
    },
    {
        "ComplianceType": "Association",
        "ResourceType": "ManagedInstance",
        "ResourceId": "i-abcdef01234567892",
        "Status": "COMPLIANT",
        "ExtraField1": "value7",
        "ExtraField2": "value8",
    },
    {
        "ComplianceType": "Patch",
        "ResourceType": "ManagedInstance",
        "ResourceId": "i-abcdef01234567892",
        "Status": "NON_COMPLIANT",
        "ExtraField1": "value7",
        "ExtraField2": "value8",
    },
    {
        "ComplianceType": "Association",
        "CompliantSummary": {
            "CompliantCount": 3,
            "SeveritySummary": {
                "CriticalCount": 0,
                "HighCount": 1,
                "InformationalCount": 0,
                "LowCount": 0,
                "MediumCount": 0,
                "UnspecifiedCount": 2,
            },
        },
        "ExecutionSummary": {"ExecutionTime": 1585766022},
        "NonCompliantSummary": {
            "NonCompliantCount": 0,
            "SeveritySummary": {
                "CriticalCount": 0,
                "HighCount": 0,
                "InformationalCount": 0,
                "LowCount": 0,
                "MediumCount": 0,
                "UnspecifiedCount": 0,
            },
        },
        "OverallSeverity": "HIGH",
        "ResourceId": "i-04bf6ad63bEXAMPLE",
        "ResourceType": "ManagedInstance",
        "Status": "COMPLIANT",
    },
    {
        "ComplianceType": "Patch",
        "CompliantSummary": {
            "CompliantCount": 27,
            "SeveritySummary": {
                "CriticalCount": 0,
                "HighCount": 0,
                "InformationalCount": 0,
                "LowCount": 0,
                "MediumCount": 0,
                "UnspecifiedCount": 27,
            },
        },
        "ExecutionSummary": {
            "ExecutionId": "b95523e7-28e5-488e-a753-fd1d3EXAMPLE",
            "ExecutionTime": 1585244656,
            "ExecutionType": "Command",
        },
        "NonCompliantSummary": {
            "NonCompliantCount": 1,
            "SeveritySummary": {
                "CriticalCount": 0,
                "HighCount": 0,
                "InformationalCount": 0,
                "LowCount": 0,
                "MediumCount": 0,
                "UnspecifiedCount": 1,
            },
        },
        "OverallSeverity": "UNSPECIFIED",
        "ResourceId": "i-04bf6ad63bEXAMPLE",
        "ResourceType": "ManagedInstance",
        "Status": "NON_COMPLIANT",
    },
]


@pytest.mark.parametrize(
    "data,expected_count",
    [
        (data_list, 5),  # We now expect 4 valid models since only `Status` is checked
    ],
)
def test_non_compliant_ec2_validation(data, expected_count):
    """
    Test that only valid NonCompliantResource models are created when filtering and validating the data.
    """
    valid_compliance_items: List[NonCompliantResource] = []

    for item in data:
        try:
            compliance_item = NonCompliantResource(**item)
            valid_compliance_items.append(compliance_item)
        except ValidationError:
            pass

    # Assert that the number of valid items is as expected
    assert len(valid_compliance_items) == expected_count

    # Optional: Validate individual properties
    for item in valid_compliance_items:
        assert item.status == "NON_COMPLIANT"


def test_invalid_status():
    """
    Test that a ValidationError is raised when the status is not 'NON_COMPLIANT'.
    """
    invalid_data = {
        "ComplianceType": "Association",
        "ResourceType": "ManagedInstance",
        "ResourceId": "i-abcdef01234567892",
        "Status": "COMPLIANT",
        "ExtraField1": "value7",
        "ExtraField2": "value8",
    }

    # Assert that a ValidationError is raised
    with pytest.raises(ValidationError):
        NonCompliantResource(**invalid_data)
