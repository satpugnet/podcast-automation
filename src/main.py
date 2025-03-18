from creation_steps import voice_design
import sys

# Ask user for the character name
character_name = input("Enter the name of the historical character: ")

# Skip voice generation if character name is empty
if not character_name:
    print("No character name provided. Voice generation skipped.")
else:
    # Call the generate_voice_preview function only if user confirms by typing the character name
    voice_design.generate_voice_preview(character_name=character_name)
