import pyperclip

def print_background_search_template(historical_figure: str) -> None:
    """
    Prints the background search template and copies it to clipboard.
    
    Args:
        historical_figure (str): Name of the historical figure to research
    """
    with open('src/prompts/historical_background_research.hbr', 'r', encoding='utf-8') as file:
        hbr_template = file.read()
        formatted_template = hbr_template.format(historical_figure=historical_figure)
        pyperclip.copy(formatted_template)
        print("\nTemplate for creating the background research file has been copied to clipboard!")

