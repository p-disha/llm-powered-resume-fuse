import json
import openai
from fs_tools import read_file, list_files, write_file, search_in_file

class LLMFileAssistant:
    def __init__(self, api_key: str, model_name: str = "gpt-4o-mini"):
        self.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key)
        self.model_name = model_name
        
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Read content from a file (PDF, TXT, DOCX) and return the text.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filepath": {
                                "type": "string",
                                "description": "The path to the file to read."
                            }
                        },
                        "required": ["filepath"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_files",
                    "description": "List files in a directory.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "directory": {
                                "type": "string",
                                "description": "The directory to list files from."
                            },
                            "extension": {
                                "type": "string",
                                "description": "Optional file extension filter (e.g., '.pdf', '.txt')."
                            }
                        },
                        "required": ["directory"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "write_file",
                    "description": "Write text content to a file.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filepath": {
                                "type": "string",
                                "description": "The path to the file to write to."
                            },
                            "content": {
                                "type": "string",
                                "description": "The text content to write."
                            }
                        },
                        "required": ["filepath", "content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_in_file",
                    "description": "Search for a keyword in a file and return the context around matches.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filepath": {
                                "type": "string",
                                "description": "The path to the file to search in."
                            },
                            "keyword": {
                                "type": "string",
                                "description": "The keyword to search for."
                            }
                        },
                        "required": ["filepath", "keyword"]
                    }
                }
            }
        ]
        
    def execute_tool(self, tool_call) -> str:
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        
        if name == "read_file":
            result = read_file(args.get("filepath"))
        elif name == "list_files":
            result = list_files(args.get("directory"), args.get("extension"))
        elif name == "write_file":
            result = write_file(args.get("filepath"), args.get("content"))
        elif name == "search_in_file":
            result = search_in_file(args.get("filepath"), args.get("keyword"))
        else:
            result = {"error": f"Unknown function {name}"}
            
        return json.dumps(result)

    def process_query(self, query: str, messages: list = None) -> tuple:
        """
        Process a user query, handle tool calling, and return the response along with message history.
        """
        if messages is None:
            messages = [
                {"role": "system", "content": "You are a helpful file system assistant. You can read, write, list, and search files locally using the tools provided. When a user asks you to interact with 'resumes' or the 'Downloads folder', assume the path is 'C:/Users/disha/Downloads'. Always use the tools when users ask you to interact with files. If a user asks to summarize a file, read it first, then summarize."}
            ]
            
        messages.append({"role": "user", "content": query})
        
        # Initial call to LLM
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            tools=self.tools,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        messages.append(response_message)
        
        # Handle tool calls
        tool_calls = response_message.tool_calls
        if tool_calls:
            for tool_call in tool_calls:
                tool_result = self.execute_tool(tool_call)
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": tool_call.function.name,
                    "content": tool_result
                })
                
            # Second call to LLM with tool results
            second_response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages
            )
            final_message = second_response.choices[0].message
            messages.append(final_message)
            return final_message.content, messages
            
        return response_message.content, messages
