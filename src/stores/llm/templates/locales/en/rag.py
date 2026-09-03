from string import Template

#### RAG Prompts ####

#### System #####

system_prompt = Template("\n".join([  # noqa: FLY002
    "You are a helpful assistant to generate responses for the user.",
    "You will be provided with a user query and a set of retrieved documents.",
    "Your task is to generate a response to the user query based on the information contained in the retrieved documents.",
    "Ignore the documents that are not relevant to the user query.",
    "You can apologize to the user if you are not able to generate a response.",
    "You have to generate response in the same language as the user query.",
    "Be polite and professional in your response.",
    "Be precise and concise in your response. Avoid unnecessary information.",
])
)
#### Document ####

document_prompt = Template(
    "\n".join([  # noqa: FLY002
        "## Document NO: $doc_no",
        "### Content: $chunk_text",
    ])
)

#### Footer ####

footer_prompt = Template(
    "\n".join([  # noqa: FLY002
        "Based on the above documents, generate a response to the user query.",
        "## Query:",
        "$query",
        "",
        "## Answer:",
    ])
)