import pyperclip
import os

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
        print("\nTemplate for creating the background research file has been copied to clipboard! 📋")
        
        # Create the background research file
        output_dir = f"output/{historical_figure.replace(' ', '_')}"
        os.makedirs(output_dir, exist_ok=True)
        
        # Create empty file only if it doesn't exist
        if not os.path.exists(f"{output_dir}/background_research.txt"):
            open(f"{output_dir}/background_research.txt", 'w').close()

