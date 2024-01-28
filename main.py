import text_gen
import image_gen

OPTION_SETUP = "Provide list of 3 possibilities of what can happen next. Each option should \
    briefly introduce the event from the adventure continued after this. Do not write more than \
    5 words for each option. Do not write anything else except the story and the list. Do not \
    ask questions to the user. Do not type commands. Do not ask the user for the next action. \
    Do not write explanations. The user will choose one option within their next input. You will \
    continue generating the story with the choice of the user as the main event of the adventure. \
    The format for the list of options should be formatted like this:\nOptions:\n1.\n2.\n3."
STORY_SETUP = ". The story should be around 200 words. Do not write anything else except the story. \
    Do not ask questions to the user. Do not type commands. Do not ask the user for the next action. \
    Do not write explanations. "

if __name__ == "__main__":
    max_turns = 2

    chat_history = []
    story_lst = []

    prompt = input("Enter the initial prompt: ")

    title = text_gen.title_gen(prompt) # title of the book
    print("TITLE: " + title)
    story = text_gen.story_beginning(chat_history, story_lst,prompt) # story 1
    print("_____\n" + story + "\n_____")

    cover_image_prompt = text_gen.cover_image_prompt_gen(story)
    print("_____\nCOVER_PROMPT: " + cover_image_prompt + "\n_____")
    image_gen.image(cover_image_prompt, 1)
    
    message = OPTION_SETUP
    options = text_gen.options_gen(chat_history, message) # options for story 2
    print(options)
    
    message = input("Enter 1, 2, or 3: ") # user input
    story = text_gen.story_gen(chat_history, story_lst, message) # story 2
    print("_____\n" + story + "\n_____")
    image_gen.image(text_gen.dalle_prompt_gen(story), 2)

    for n in range(max_turns):
        message = "Again, provide a list of 3 possible events like before."
        options = text_gen.options_gen(chat_history, message) # options
        print(options)

        user_choice = input("Enter 1, 2, or 3: ") # user input
        message = "Continue writing the story following option " + user_choice + STORY_SETUP
        story = text_gen.story_gen(chat_history, story_lst, message) # story
        print("_____\n" + story + "\n_____")
        image_gen.image(text_gen.dalle_prompt_gen(story), n+3)

    print("THE END")