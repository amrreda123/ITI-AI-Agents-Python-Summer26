from crewai import Agent, Task, Crew, Process

analyst = Agent(
    role="Support Analyst",
    goal="Draft a factual response for customer tickets",
    backstory="You inspect the customer request carefully and draft professional initial responses.",
    verbose=False,
)

reviewer = Agent(
    role="Quality Reviewer",
    goal="Check the response for clarity, accuracy, and customer satisfaction",
    backstory="You verify policy guidelines and ensure communications are polished before delivery.",
    verbose=False,
)

draft_task = Task(
    description="Draft a response for: 'My order #104 is delayed by 3 days. Where is it?'",
    expected_output="A concise customer-facing draft explaining the delay.",
    agent=analyst,
)

review_task = Task(
    description="Review the draft and return a polite, finalized response.",
    expected_output="A final approved response ready to send.",
    agent=reviewer,
)

crew = Crew(
    agents=[analyst, reviewer],
    tasks=[draft_task, review_task],
    process=Process.sequential,
)

if __name__ == "__main__":
    try:
        result = crew.kickoff()
        print("CrewAI Output:")
        print(result)
    except Exception as e:
        print("CrewAI execution requires configured LLM API keys:", e)
