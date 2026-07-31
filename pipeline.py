# ==========================================================
# Imports
# ==========================================================

from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ==========================================================
# Research Pipeline
# ==========================================================

def run_research_pipeline(topic: str) -> dict:

    state = {}

    # ==========================================================
    # Step 1 - Search Agent
    # ==========================================================

    print("\n" + "=" * 50)
    print("Step 1 - Search Agent is working...")
    print("=" * 50)

    search_agent = build_search_agent()

    search_results = search_agent.invoke({
        "messages": [
            ("user", f"Find recent, reliable and detailed information about: {topic}")
        ]
    })

    state["search_results"] = search_results["messages"][-1].content

    print("\nSearch Results\n")
    print(state["search_results"])

    # ==========================================================
    # Step 2 - Reader Agent
    # ==========================================================

    print("\n" + "=" * 50)
    print("Step 2 - Reader Agent is scraping top resources...")
    print("=" * 50)

    reader_agent = build_reader_agent()

    reader_result = reader_agent.invoke({
        "messages": [
            (
                "user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_results'][:800]}"
            )
        ]
    })

    state["scraped_content"] = reader_result["messages"][-1].content

    print("\nScraped Content\n")
    print(state["scraped_content"])

    # ==========================================================
    # Step 3 - Writer Chain
    # ==========================================================

    print("\n" + "=" * 50)
    print("Step 3 - Writer is drafting the report...")
    print("=" * 50)

    research_combined = (
        f"Search Results:\n{state['search_results']}\n\n"
        f"Detailed Scraped Content:\n{state['scraped_content']}\n"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print("\nFinal Report\n")
    print(state["report"])

    # ==========================================================
    # Step 4 - Critic Chain
    # ==========================================================

    print("\n" + "=" * 50)
    print("Step 4 - Critic is reviewing the report...")
    print("=" * 50)

    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })

    print("\nCritic Report\n")
    print(state["feedback"])

    return state

# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    topic = input("\nEnter a research topic: ")

    run_research_pipeline(topic)