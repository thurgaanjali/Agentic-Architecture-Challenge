import re
from pathlib import Path
from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph


class AgentState(TypedDict, total=False):
    question: str
    answer: str
    action: str
    name: str
    history: list


def load_support_guide():
    file_path = Path(__file__).parent / "knowledge_base" / "support_guide.txt"

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def remember_information(state):
    question = state["question"]
    history = state.get("history", [])

    name_match = re.search(
        r"my name is ([a-zA-Z ]+)",
        question,
        re.IGNORECASE
    )

    result = {
        "history": history + [question]
    }

    if name_match:
        result["name"] = name_match.group(1).strip()

    return result


def is_calculation(question):
    question = question.lower()

    calculation_words = [
        "plus",
        "add",
        "minus",
        "subtract",
        "times",
        "multiplied",
        "multiply",
        "divide",
        "divided"
    ]

    has_numbers = bool(re.search(r"\d", question))

    for word in calculation_words:
        if word in question and has_numbers:
            return True

    return False


def decide_action(state):
    question = state["question"].lower()

    if is_calculation(question):
        return {"action": "calculator"}

    if "my name" in question or "what did i tell you" in question:
        return {"action": "memory"}

    guide_words = [
        "password",
        "locked",
        "login",
        "support hours",
        "security",
        "breach",
        "outage",
        "hardware request",
        "replacement",
        "response time"
    ]

    for word in guide_words:
        if word in question:
            return {"action": "guide"}

    return {"action": "unknown"}


def get_section(heading):
    guide = load_support_guide()
    lines = guide.splitlines()

    for i, line in enumerate(lines):
        if line.strip().lower() == heading.lower():
            section = [line.strip()]

            for next_line in lines[i + 1:]:
                next_line = next_line.strip()

                if next_line == "":
                    if len(section) > 1:
                        break
                    continue

                section.append(next_line)

            return "\n".join(section)

    return ""


def find_guide_answer(question):
    question = question.lower()

    if "price" in question or "cost" in question or "how much" in question:
        return "That information is not covered in the support guide."

    if "support hours" in question or "when is support available" in question:
        answer = get_section("Support Hours")

        if answer:
            return answer

    if "password" in question:
        answer = get_section("Password Reset")

        if answer:
            return answer

    if "locked" in question or "unsuccessful login" in question:
        answer = get_section("Account Lockout")

        if answer:
            return answer

    if "security" in question or "breach" in question or "outage" in question:
        answer = get_section("Critical Issues")

        if answer:
            return answer

    if "hardware" in question or "replacement" in question:
        answer = get_section("Hardware Requests")

        if answer:
            return answer

    if "response time" in question or "how long" in question:
        answer = get_section("Response Time")

        if answer:
            return answer

    return "That information is not covered in the support guide."


def guide_node(state):
    return {
        "answer": find_guide_answer(state["question"])
    }


def memory_node(state):
    name = state.get("name")

    if name:
        return {"answer": "Your name is " + name + "."}

    return {"answer": "I do not have your name yet."}


def calculate(a, b, operation):
    if operation == "add":
        return a + b

    if operation == "subtract":
        return a - b

    if operation == "multiply":
        return a * b

    if operation == "divide":
        if b == 0:
            return "Cannot divide by zero."

        return a / b

    return "Invalid calculation."


def calculate_from_question(question):
    match = re.search(
        r"(\d+(?:\.\d+)?)\s*"
        r"(plus|add|minus|subtract|times|multiplied by|multiply|divide by|divided by)"
        r"\s*(\d+(?:\.\d+)?)",
        question.lower()
    )

    if not match:
        return "I could not understand the calculation."

    a = float(match.group(1))
    operation = match.group(2)
    b = float(match.group(3))

    if operation in ["plus", "add"]:
        result = calculate(a, b, "add")

    elif operation in ["minus", "subtract"]:
        result = calculate(a, b, "subtract")

    elif operation in ["times", "multiplied by", "multiply"]:
        result = calculate(a, b, "multiply")

    elif operation in ["divide by", "divided by"]:
        result = calculate(a, b, "divide")

    else:
        return "I could not understand the calculation."

    if isinstance(result, float) and result.is_integer():
        result = int(result)

    return "The answer is " + str(result) + "."


def calculator_node(state):
    return {
        "answer": calculate_from_question(state["question"])
    }


def unknown_node(state):
    return {
        "answer": "I do not have enough information to answer that."
    }


def route_action(state):
    action = state["action"]

    if action == "calculator":
        return "calculator"

    if action == "memory":
        return "memory"

    if action == "guide":
        return "guide"

    return "unknown"


workflow = StateGraph(AgentState)

workflow.add_node("remember", remember_information)
workflow.add_node("decide", decide_action)
workflow.add_node("guide", guide_node)
workflow.add_node("memory", memory_node)
workflow.add_node("calculator", calculator_node)
workflow.add_node("unknown", unknown_node)

workflow.add_edge(START, "remember")
workflow.add_edge("remember", "decide")

workflow.add_conditional_edges(
    "decide",
    route_action,
    {
        "guide": "guide",
        "memory": "memory",
        "calculator": "calculator",
        "unknown": "unknown"
    }
)

workflow.add_edge("guide", END)
workflow.add_edge("memory", END)
workflow.add_edge("calculator", END)
workflow.add_edge("unknown", END)

memory = InMemorySaver()
agent = workflow.compile(checkpointer=memory)


def ask_agent(question, thread_id="support-demo"):
    result = agent.invoke(
        {"question": question},
        {
            "configurable": {
                "thread_id": thread_id
            }
        }
    )

    return result["answer"]


def main():
    print("IT Support Agent")
    print("Type 'exit' to stop.\n")

    while True:
        question = input("You: ")

        if question.lower() == "exit":
            break

        try:
            answer = ask_agent(question)
            print("Agent:", answer)

        except Exception as error:
            print("There was a problem:", error)


if __name__ == "__main__":
    main()