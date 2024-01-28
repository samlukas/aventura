import text_gen
import image_gen

OPTION_SETUP = "Provide 3 possible actions that the character can take as the story progresses. \
    Use 3 to 7 words to write each options. \
    The user will choose one option within their next input. You will continue generating the story \
    with the user's choice of action. The format for the list of options should be formatted like \
    this:\nOptions:\n1.\n2.\n3."

INITIAL_SETUP = ", provide the beginning of the fun, intriguing, whimsical and adventurous fantasy story. Use 100 to 150 words to \
    create this story. Do not write explanations. Do not ask questions to the user. Do not type \
    commands. Do not ask the user for the next action. Do not write anything else except the story."

STORY_SETUP = ". The story should be around 100 words. Do not write anything else except the story. \
    Do not ask questions to the user. Do not type commands. Do not ask the user for the next action. \
    Do not write explanations. "


def setup(chat_history: list[str]):
    # call this function before the first call of story()
    text_gen.setup(chat_history)


def story(chat_history: list[str], story_lst: list[str], prompt = None, choice = None) -> str:
    # promt and choice parameters are optional; None or str ('1', '2', or '3')
    # the first call of this function should have prompt as a str
    # the later calls of this function should have choice as a str
    n = len(story_lst)
    if n == 0:
        message = "Given the theme or subject \"" + prompt + INITIAL_SETUP
    else: 
        message = "Continue writing the story following option " + choice + STORY_SETUP
    story = text_gen.story_gen(chat_history, story_lst, message)
    dalle_prompt = text_gen.dalle_prompt_gen(story)
    image_gen.image(dalle_prompt, n+1)

    return story


def options(chat_history: list[str], story_list_length: int) -> list[str]:
    if story_list_length == 1:
        message = OPTION_SETUP
    else:
        message = "Again, provide a list of 3 possible actions like before."
    options = text_gen.options_gen(chat_history, message)
    return options


# if __name__ == "__main__":
#     max_turns = 2

#     chat_history = []
#     story_lst = []

#     setup(chat_history)

#     prompt = input("Enter the initial prompt: ")

#     # title = text_gen.title_gen(prompt) # title of the book
#     # print("TITLE: " + title)

#     # cover_image_prompt = text_gen.cover_image_prompt_gen(story)
#     # image_gen.image(cover_image_prompt, 1)

#     print("_____\n" + story(chat_history,story_lst, prompt) + "\n_____")

#     for n in range(max_turns):
#         print(options(chat_history, len(story_lst)))

#         user_choice = input("Enter 1, 2, or 3: ") # user input
#         print("_____\n" + story(chat_history, story_lst, choice=user_choice) + "\n_____")


#     print("THE END")