from langchain_community.utilities import GoogleSerperAPIWrapper

def web_search(query: str) -> str:
    print(f"Performing web search for query using tool: {query}")

    # temporary code to avoid calling this api during testing

    if 'microsoft' in query.lower():
        return "Microsoft Corporation is an American multinational technology conglomerate headquartered in Redmond, Washington. Founded in 1975, the company became ... Microsoft creates platforms and tools powered by AI to deliver innovative solutions that meet the evolving needs of our customers. Our mission is to empower every person and every organization on the planet to achieve more. Learn more about Microsoft, our commitments, and values. Friends Bill Gates and Paul Allen started Microsoft – sometimes Micro-Soft, for microprocessors and software – to develop software for the Altair 8800, an ... The name microsoft was actually coined by paul allen. It's a combination of two words micro computer and software back in the 1970s. Microsoft is the largest producer of computer software and one of the largest tech companies in the world, famous for Windows and Azure. On April 4th, 1975, Bill Gates and Paul Allen started a little company named Microsoft. You probably know the story from there: Gates went ... Explore Microsoft products and services and support for your home or business. Shop Microsoft 365, Copilot, Teams, Xbox, Windows, Azure, Surface and more. Bill Gates and Paul Allen found Microsoft in 1975 to develop software for the alter 8800 an early personal computer."

    serper = GoogleSerperAPIWrapper()
    print("Initialized GoogleSerperAPIWrapper")
    response = serper.run(query)
    print("Web search response:", response)

    return response
