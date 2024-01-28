import re
import os
import cohere
co = cohere.Client(os.environ.get("COHERE_API_KEY"))


EXAMPLE_PROMPTS = "\nExample:a teenage sorcerer experimenting with spellbooks and mystical artifacts in a magical workshop filled with glowing crystals and levitating potions.\n\
    Example: a cowboy gunslinger walking the neon lit streets and alleys of a futuristic tokyo covered in a dense fog.\n\
    Example: a big large happy kawaii fluffy cutest baby Shiba-inu puppy wearing kimono enjoy shopping in a futuristic abandoned city\n"

WARNING = "Do not write explanations. Do not ask questions to the user. Do not type commands. \
    Do not ask the user for the next action. Do not write anything else except the story."

SETUP = "You are a creative storyteller who will help me build an iterative story that is \
    adventurous, descriptive and intriguing. The story will be in third-person point of view. \
    Your task is to generate the story. You will first receive a general theme or the subject of the \
    story from the user. Respond with ‘.’ If you understand."

DALLE_SETUP_1 = "You are an expert prompt engineer who writes short, concise and descriptive short \
    synthetic captions to create a prompt for text to image ML model, Dall-E. Your task is to write \
    short synthetic captions for Dall-E to generate an image from a story provided by the user. The \
    generated image should describe a core scene of the story. You will receive a story from the user. Respond with ‘.’ If you understand."
DALLE_SETUP_2 = "These are some examples of the prompt for Dall-E. You will receive a story from \
    the user. Respond with ‘.’ If you understand." 
DALLE_SETUP_3 =r"\"\nFrom the given story, pick a scene that describe the main event of \
    the story. You will provide a prompt for Dall-E describing the scene. The prompt should not contain the name of the character, rather it should describe the character's appearence. \
    Use 10 to 20 words to create the prompt for Dall-E. \
    The response should be in a format like this:\nScene:\nPrompt:\n"

COVER_SETUP_1 = "You are an expert prompt engineer who writes short, concise and descriptive short \
    synthetic captions to create a prompt for text to image ML model, Dall-E. Your task is to write \
    short synthetic captions for Dall-E to generate a book cover image from a short scenario or \
    concept provided by the user. The generated image should depict the user’s description. The \
    generated image should be creative. You will receive a description from the user. Respond with \
    ‘.’ If you understand."
COVER_SETUP_2 = "These are some examples of the prompt for Dall-E. You will receive a description \
    from the user. Respond with ‘.’ If you understand."
COVER_SETUP_3 = r"\"\nHere is the description: Provide a prompt with short synthetic captions \
    describing the subject of the story and the style of the image. Use 20 to 30 words to create \
    a prompt for Dall-E. The prompt should be in a bracket like this: {Prompt}."


def setup(chat_history: list[str]) -> str:
    message = SETUP
    answer = chat(chat_history, message)


def chat(chat_history: list[str], message: str) -> str:
    response = co.chat(
        message,
        model="command-nightly",
        temperature=0.9,
        chat_history=chat_history
    )
    answer = response.text

    user_message = {"user_name": "User", "text": message}
    bot_message = {"user_name": "Chatbot", "text": answer}
    chat_history.append(user_message)
    chat_history.append(bot_message)

    return answer


def options_gen(chat_history: list[str], message: str) -> list[str]:
    answer = chat(chat_history, message)

    options = re.findall(r"\d\..+\s", answer)
    for i in range(3):
        options[i] = re.sub(r"\d\.\s", "", options[i].strip())

    return options


def story_gen(chat_history: list[str], story_lst: list[str], message: str) -> str:
    answer = chat(chat_history, message)
    story_lst.append(answer)

    return answer


def dalle_prompt_gen(story: str) -> str:
    chat_history = []

    message = DALLE_SETUP_1
    answer = chat(chat_history, message)

    message = DALLE_SETUP_2 + EXAMPLE_PROMPTS
    answer = chat(chat_history, message)

    message = "Here is the story:\n\"" + story + DALLE_SETUP_3
    answer = chat(chat_history, message)
    # print("DALLE PROMPT: " + answer)

    answer = re.findall(r"Prompt:\s.+\.", answer)[0][8:]

    prompt = "Create a digital art for a fantasy book. The scene is about" + answer
    return prompt


def cover_image_prompt_gen(prompt: str) -> str:
    chat_history = []
    message = COVER_SETUP_1
    answer = chat(chat_history, message)

    message = COVER_SETUP_2 + EXAMPLE_PROMPTS    
    answer = chat(chat_history, message)

    message = "Here is the description:\n\"" + prompt + COVER_SETUP_3
    answer = chat(chat_history, message)

    answer_ = re.findall(r"{.+}", answer)
    if len(answer_) == 0:
        answer_ = prompt
    else:
        answer_ = re.findall(r"{.+}", answer)[0][1:-1]

    cover_prompt = "Create a book cover image of a fictional story about " + answer_ + " Digital art."
    return cover_prompt


def title_gen(prompt: str) -> str:
    message = "Create a title of a fictional book with the provided theme or subject: \"" + prompt \
        + r"\". The title should be in a bracket like this: {Title}."
    print(message)
    answer = chat([], message)
    title = re.findall(r"{.+}", answer)
    if len(title) == 0:
        title = prompt
    else:
        title = re.findall(r"{.+}", answer)[0][1:-1]    

    return title