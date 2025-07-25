#!/usr/bin/env python3
"""
Test script to verify the JSON response format matches the requirement.
"""
import json
from pydantic import BaseModel


class HackRxResponse(BaseModel):
    answers: list[str]


def test_response_format():
    """Test if the response format matches the required structure."""

    # Sample answers (like what your pipeline would return)
    sample_answers = [
        "A grace period of thirty days is provided for premium payment after the due date.",
        "There is a waiting period of thirty-six (36) months for pre-existing diseases.",
        "Yes, the policy covers maternity expenses with 24 months continuous coverage requirement.",
    ]

    # Create response using your Pydantic model
    response = HackRxResponse(answers=sample_answers)

    # Convert to JSON
    response_json = response.model_dump()

    print("✅ Response Format Test")
    print("=" * 50)
    print("Response structure:")
    print(json.dumps(response_json, indent=2))

    # Verify it matches the required format
    required_format = {"answers": ["answer1", "answer2", "answer3"]}

    print("\n✅ Format Validation:")
    print("=" * 50)

    # Check if it has the correct structure
    if "answers" in response_json:
        print("✓ Has 'answers' key")
    else:
        print("✗ Missing 'answers' key")
        return False

    if isinstance(response_json["answers"], list):
        print("✓ 'answers' is a list")
    else:
        print("✗ 'answers' is not a list")
        return False

    if all(isinstance(answer, str) for answer in response_json["answers"]):
        print("✓ All answers are strings")
    else:
        print("✗ Not all answers are strings")
        return False

    # Check if there are no extra fields
    if set(response_json.keys()) == {"answers"}:
        print("✓ No extra fields")
    else:
        print(f"✗ Extra fields found: {set(response_json.keys()) - {'answers'}}")
        return False

    print("\n🎯 Response format is CORRECT!")
    return True


if __name__ == "__main__":
    test_response_format()
