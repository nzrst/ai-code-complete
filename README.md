# OpenAI Replace for Sublimt Text 3+

This plugin will allow you to convert comments in your code into actual code on the fly. The plugin will recognize the langauge you're working in based on the file extension.

# Create Plugin
		Tools > Developer > New Plugin...
		Use the source in openai_replace.py

# Obtain OpenAI API Key
		Register and create key here: https://beta.openai.com/account/api-keys
		When you have an API key paste it into the code for the following variable;
			api_key = "[YOUR_KEY]"

# Save Plugin
		Save as "openai_replace.py"

# Create shortcut key for plugin
		Preferenced > Key Bindings
   		Add and save the following binding
			  {"keys": ["ctrl+shift+p"],"command": "openai_replace"}
        
# Finally
		Create and save a new php/py file, the file extension is used to determine the AI completion language to insert.
		Add a comment for a function you're interested in, make sure cursor is on the line, press ctrl+shift+p

