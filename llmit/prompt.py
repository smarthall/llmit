from haystack.dataclasses import ChatMessage
from haystack.components.builders.chat_prompt_builder import ChatPromptBuilder

prompt_template = [
    ChatMessage.from_system(
        """
        You are an AI Assistant that helps developers understand the changes
        in a git repository. You will be given a list of commit ids and the
        short summary of the change.

        Focus on the changes which introduce new features, and the changes
        which fix bugs. Dependency updates, documentation changes and code
        refactoring should be listed as bullet points at the end. You should
        use tools to read the full commit messages of any commits you suspect
        to be features so that you can understand the changes in detail.

        Some of these changes might not be clear, please make sure to lookup
        the full commit message using the `get_commit_message` tool. Do not
        ask to use tools, just go ahead and use them.
        """
    ),
    ChatMessage.from_user(
        """
        Using the tools available, please make a user-friendly message about the changes in the repository.

        Here are the settings the user has suggested:
        Tone: {{tone}}
        Language: {{language}}
        Emoji: {{emoji}}
        Format: Plain text

        You can use this git reference to identify where the changes are from: {{ref}}
        
        Here is the list of changes on one line each. You should use the tools to look up the full commit messages:
        {{log_summary}}
        """
    ),
]

prompt_builder = ChatPromptBuilder(
    template=prompt_template, required_variables=["log_summary", "tone", "language", "emoji"]
)
