from datetime import datetime, timedelta
from pathlib import Path


critical_keywords = {
    "data_loss": [
        "data loss",
        "lost my data",
        "data was deleted",
        "files are missing",
        "lost files"
    ],
    "service_outage": [
        "service outage",
        "service is down",
        "system is down",
        "service unavailable"
    ],
    "security_breach": [
        "security breach",
        "account hacked",
        "hacked my account",
        "unauthorized access"
    ]
}


category_keywords = {
    "Billing": [
        "refund",
        "payment",
        "charged",
        "invoice",
        "billing",
        "subscription"
    ],
    "Technical": [
        "error",
        "bug",
        "not working",
        "cannot login",
        "cannot log in",
        "technical",
        "login problem"
    ],
    "Feedback": [
        "feedback",
        "suggestion",
        "recommendation",
        "review"
    ]
}


def load_knowledge_base():
    file_path = Path(__file__).parent / "knowledge_base" / "support_faq.txt"

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def check_critical_issue(email):
    email = email.lower()
    reasons = []

    for reason, keywords in critical_keywords.items():
        for keyword in keywords:
            if keyword in email:
                reasons.append(reason)
                break

    return reasons


def contacted_more_than_three_times(contact_dates):
    current_date = datetime.now()
    seven_days_ago = current_date - timedelta(days=7)

    recent_contacts = 0

    for date in contact_dates:
        if seven_days_ago <= date <= current_date:
            recent_contacts += 1

    return recent_contacts > 3


def classify_email(email):
    email = email.lower()

    for category, keywords in category_keywords.items():
        for keyword in keywords:
            if keyword in email:
                return category

    return "General Support"


def get_category_information(category):
    knowledge_base = load_knowledge_base()

    sections = knowledge_base.split("\n\n")

    for section in sections:
        if category.lower() in section.lower():
            return section

    return ""


def can_answer_email(email, category):
    email = email.lower()

    if "refund" in email:
        return False, "Refund eligibility cannot be confirmed automatically."

    information = get_category_information(category)

    if information == "":
        return False, "No relevant information was found in the knowledge base."

    return True, ""


def create_response(email, category):
    email = email.lower()

    if "refund" in email:
        return (
            "Thank you for contacting support. "
            "Refund eligibility depends on the specific transaction "
            "and account circumstances. Our billing team will review "
            "your transaction and confirm the next steps."
        )

    if category == "Billing":
        return (
            "Thank you for contacting support. "
            "Please provide your account details and transaction "
            "information so our billing team can review the issue."
        )

    if category == "Technical":
        return (
            "Thank you for contacting support. "
            "Please check that you are using the correct account "
            "credentials. If the problem continues, our technical "
            "support team can investigate it further."
        )

    if category == "Feedback":
        return (
            "Thank you for your feedback. "
            "We appreciate your suggestion and will forward it "
            "to the appropriate team for review."
        )

    return (
        "Thank you for contacting support. "
        "We will review your request and get back to you."
    )


def route_email(email, contact_dates=None):
    if contact_dates is None:
        contact_dates = []

    # Critical checks are done before classification or response generation.
    critical_reasons = check_critical_issue(email)

    if contacted_more_than_three_times(contact_dates):
        critical_reasons.append("more_than_three_contacts_in_7_days")

    if critical_reasons:
        return {
            "route": "human_agent",
            "critical": True,
            "category": None,
            "reasons": critical_reasons,
            "response": None
        }

    category = classify_email(email)

    can_answer, reason = can_answer_email(email, category)

    if not can_answer:
        return {
            "route": "human_agent",
            "critical": False,
            "category": category,
            "reasons": [reason],
            "response": None
        }

    response = create_response(email, category)

    return {
        "route": "automated_processing",
        "critical": False,
        "category": category,
        "reasons": [],
        "response": response
    }


if __name__ == "__main__":
    current_date = datetime.now()

    test_cases = [
        (
            "Billing",
            "I was charged twice for my subscription.",
            []
        ),
        (
            "Technical",
            "I cannot login to my account because I get an error.",
            []
        ),
        (
            "Feedback",
            "I have a suggestion for improving the service.",
            []
        ),
        (
            "Security issue",
            "Someone hacked my account and there was unauthorized access.",
            []
        ),
        (
            "Data loss",
            "I lost my data and some files are missing.",
            []
        ),
        (
            "Too many contacts",
            "I need help with my account.",
            [
                current_date - timedelta(days=1),
                current_date - timedelta(days=2),
                current_date - timedelta(days=3),
                current_date - timedelta(days=5)
            ]
        ),
        (
            "Refund request",
            "Can I get a RM500 refund?",
            []
        )
    ]

    for name, email, contact_dates in test_cases:
        print("\nTest:", name)
        print("Email:", email)

        result = route_email(email, contact_dates)

        print("Result:", result)