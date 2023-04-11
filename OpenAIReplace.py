import sublime
import sublime_plugin
import subprocess
import json
import os
import http.client

class OpenAIReplace(sublime_plugin.TextCommand):
	command = "openai_replace"

	def run(self, edit):
		# codecs for code completion: code-cushman-001, code-davinci-002
		engine = "code-cushman-001"

		# generate an API key
		# https://beta.openai.com/account/api-keys
		api_key = "[YOUR_KEY]"

		# detect file extension to try and direct the openai query
		filename = self.view.file_name()
		file_extension = ""
		if filename != None:
			file_root, file_extension = os.path.splitext(filename)
			if (file_extension):
				file_extension = file_extension.strip(".")
		
		# define language comment syntax for later use
		language_comment_map = {
			"Python": "#",
			"Bash": "#",
			"PHP": "//"
		}

		# let's try to map the file extension to an appropriate language
		language_map = {
			"py": "Python",
			"sh": "Bash",
			"php": "PHP"
		}

		# get the currently selected line
		current_line = self.view.line(self.view.sel()[0])
		line_text = self.view.substr(current_line)
		final_prompt = line_text

		# try to identify the language we're editing
		completion_language = ""
		if (file_extension in language_map):
			completion_language = language_map[file_extension]

		# if we recognize this language then update the comment line to focus the query
		if (completion_language != ""):
			language_comment = language_comment_map[completion_language]
			if (line_text[0:len(language_comment)] == language_comment):
				# Rework the completion request to include the desired language
				final_prompt = language_comment +" Using "+ completion_language +" "+ line_text.lstrip(language_comment).lstrip(" ")
				#print(clearPrompt)

		# configure openai parameters, this needs more work for ideal responses
		# docs: https://beta.openai.com/docs/api-reference/completions/create
		# note: increase or decrease "temperature", between 0.0 and 1.0, to get less creative (0.0) or more creative (1.0) answers.
		create_params = json.dumps({
			'prompt': final_prompt,
			'max_tokens': 256,
			'temperature': 0.0,
			'n': 1,
			'echo': True
		})

		# openai API query
		api_endpoint = "api.openai.com"
		api_resource = "/v1/engines/"+ engine +"/completions"
		api_headers = {
			"Content-Type": "application/json",
			"Authorization": "Bearer "+ api_key
		}
		conn = http.client.HTTPSConnection(api_endpoint)
		conn.request("POST", api_resource, body=create_params, headers=api_headers)

		# capture the response and get the results
		response = conn.getresponse()
		if response.status == 200 or response.status == 201:
			out = response.read()
			response = json.loads(out.decode("utf-8"))
		else:
			print("Error: "+ str(response.status) +" "+ response.reason)
		conn.close()

		# if there were errros just dump to console, otherwise replace the current line with code
		if response == None or 'error' in response:
			self.view.replace(edit, current_line, "# no results came back")
			print(response['error']['message'])
		else:
			self.view.replace(edit, current_line, response['choices'][0]['text'])
