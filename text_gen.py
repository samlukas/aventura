import re
import os
import cohere
co = cohere.Client(os.environ.get("COHERE_API_KEY"))

EXAMPLE_PROMPTS = "\nExample: An icy landscape under a starlit sky, where a magnificent frozen \
    waterfall flows over a cliff. In the center of the scene, a fire burns bright, its flames \
    seemingly frozen in place, casting a shimmering glow on the surrounding ice and snow.\n\
    Example: A swirling, multicolored portal emerges from the depths of an ocean of coffee, with \
    waves of the rich liquid gently rippling outward. The portal engulfs a coffee cup, which \
    serves as a gateway to a fantastical dimension. The surrounding digital art landscape reflects \
    the colors of the portal, creating an alluring scene of endless possibilities.\nExample: A \
    mischievous ferret with a playful grin squeezes itself into a large glass jar, surrounded by \
    colorful candy. The jar sits on a wooden table in a cozy kitchen, and warm sunlight filters \
    through a nearby window.\nExample: A fierce garden gnome warrior, clad in armor crafted from \
    leaves and bark, brandishes a tiny sword and shield. He stands valiantly on a rock amidst a \
    blooming garden, surrounded by colorful flowers and towering plants. A determined expression is \
    painted on his face, ready to defend his garden kingdom."

WARNING = "Do not write explanations. Do not ask questions to the user. Do not type commands. \
    Do not ask the user for the next action. Do not write anything else except the story."

SETUP = "You are a creative storyteller who will help me build an iterative story that is \
    adventurous, vivid, descriptive and intriguing. The story will be in third-person point of view. \
    Your task is to generate story. You will first receive a general theme or the subject of the \
    story from the user. Respond with ‘.’ If you understand."


DALLE_SETUP_1 = "You are an expert prompt engineer who writes short, concise and descriptive short \
    synthetic captions to create a prompt for text to image ML model, Dall-E. Your task is to write \
    short synthetic captions for Dall-E to generate an image from a story provided by the user. The \
    generated image should describe a core scene of the story. The generated image should be creative \
    and involve storytelling. You will receive a story from the user. Respond with ‘.’ If you understand."
DALLE_SETUP_2 = "These are some examples of the prompt for Dall-E. You will receive a story from \
    the user. Respond with ‘.’ If you understand." 
DALLE_SETUP_3 ="\"\nProvide a prompt with short synthetic captions describing the subject of the \
    story and the style of the image. Use 20 to 30 words to create the prompt for Dall-E."

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

    prompt = answer.strip() + " Digital art."

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