# Part 1 - Customer Support Email Processing Agent

## Objective

The system is designed to automate basic customer support email processing while making sure that critical cases are sent to a human support agent.

The system should:

* Identify critical issues before generating a response.
* Classify normal emails into categories such as Billing, Technical, and Feedback.
* Use a knowledge base to provide safe responses.
* Avoid making unsupported claims about refunds.
* Escalate cases that require human investigation.

## System Flow

```text
Customer Email
      |
      v
Critical Issue Check
      |
      +---- Critical ----> Human Support Agent
      |
      v
Email Classification
      |
      v
Knowledge Base Check
      |
      +---- Not enough information ----> Human Support Agent
      |
      v
Response Generation
      |
      v
Automated Response
```

## Critical Conditions

The system checks for critical conditions before classification or response generation.

A case is escalated when:

1. The email mentions possible data loss.
2. The email mentions a service outage.
3. The email mentions a security breach or unauthorized access.
4. The customer contacted support more than three times within seven days.

This order is important because a critical email should not receive an automated response before it is reviewed by a human.

## Email Classification

Normal emails are classified into:

* Billing
* Technical
* Feedback
* General Support

The current prototype uses simple keyword matching for classification. A production version could use an LLM classifier with confidence scores.

## Knowledge Base

The system uses a local support FAQ file as its knowledge base.

The knowledge base contains information about:

* Billing
* Refund policy
* Technical support
* Critical issues
* Feedback

The response should only use information that is supported by the knowledge base.

## Refund Safety

Refund requests are handled conservatively.

The knowledge base does not provide enough information to automatically decide whether a specific customer is eligible for a refund.

Therefore, the system does not promise or approve a refund. Instead, it sends the request to a human support agent.

This reduces the risk of the system hallucinating a refund policy.

## Human Escalation

A case is sent to a human support agent when:

* A critical condition is detected.
* The customer has contacted support more than three times in seven days.
* Refund eligibility cannot be confirmed.
* Relevant information is not available in the knowledge base.

## Agentic Decision Making

The system makes decisions at several stages:

1. Check whether the email is critical.
2. Decide whether the case needs human intervention.
3. Classify the email.
4. Check whether the knowledge base contains relevant information.
5. Generate a response only when the case can be handled safely.

This allows the system to stop processing a case when it detects a risk instead of always generating an answer.

## Reliability and Error Handling

The system uses a conservative approach.

If the system cannot safely answer an email, it escalates the case instead of guessing.

For example, an unsupported refund request is sent to a human agent instead of creating a refund promise.

For a production system, additional features could include structured logging, monitoring, retry handling, confidence thresholds, and an audit trail for every decision.

## Example Decisions

| Email                                       | Decision                     |
| ------------------------------------------- | ---------------------------- |
| "I was charged twice."                      | Automated Billing response   |
| "I cannot login."                           | Automated Technical response |
| "I have a suggestion."                      | Automated Feedback response  |
| "My account was hacked."                    | Human support                |
| "I lost my data."                           | Human support                |
| "I contacted support four times this week." | Human support                |
| "Can I get a RM500 refund?"                 | Human support                |

## Main Trade-off

The main trade-off is between automation and safety.

A more aggressive system could automatically answer more emails, but this increases the risk of incorrect responses.

This prototype chooses a safer approach: when the available information is not enough, the case is escalated to a human.
