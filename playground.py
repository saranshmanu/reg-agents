import yfinance as yf
from langchain_ollama import ChatOllama
from langchain.agents import initialize_agent, Tool
from langchain.agents.tools import tool
from langchain.memory import ConversationBufferMemory
from src.utils.search import get_ticker

# Define tools
@tool("sensex_stock_data")
def get_stock_details(company_name: str) -> str:
    """
    Get details of a Sensex stock (price, market cap, PE ratio, dividend yield, etc.).
    Input: Ticker symbol (e.g., RELIANCE.BO)
    """
    try:
        ticker = get_ticker(company_name)
        if "Error" in ticker or "Could not find" in ticker:
            return ticker
        stock = yf.Ticker(ticker)
        info = stock.info
        name = info.get("shortName", "Unknown")
        long_name = info.get("longName", "Unknown")
        sector = info.get("sector", "N/A")
        current_price = info.get("currentPrice", "Unknown")
        market_cap = info.get("marketCap", "N/A")
        pe_ratio = info.get("trailingPE", "N/A")
        dividend_yield = info.get("dividendYield", "N/A")

        return (
            f"{name} - Market Cap: ₹{market_cap}, "
            f"PE Ratio: {pe_ratio}, Dividend Yield: {dividend_yield}"
            f"Current price: {current_price}"
        )
    except Exception as e:
        return f"Error fetching stock details for {ticker}: {str(e)}"

llm = ChatOllama(model="llama3.2", temperature=0, verbose=True)

# Setup LangChain
tools = [
    Tool(name="Stock Details", func=get_stock_details, description="Get stock price, market cap, PE ratio, etc.")

]

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
agent = initialize_agent(tools, llm, agent="chat-conversational-react-description", memory=memory, verbose=False)

if __name__ == "__main__":
    print("Sensex Finance Chatbot (powered by Llama) is live! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        response = agent.run(user_input)
        print(f"Bot: {response}")
