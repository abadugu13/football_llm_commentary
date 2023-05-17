from tqdm import tqdm

def llm_parser(llm_output, generate_audio=True):
    rules_set_str_list = llm_output.split('\n\n')
    rules_set = []
    for index,rule_set_str in tqdm(enumerate(rules_set_str_list)):
        commentary_str, rule_str = rule_set_str.split('\n')
        rule_func = eval("lambda state, previous_state:" + rule_str.split("[Trigger]:")[-1].strip())
        commentary = commentary_str.split("[Commentary]:")[-1].strip()
        if generate_audio:
            from tortoise_tts import generate_audio
            audio_path = generate_audio(commentary)
        else:
            audio_path = f'./test/test_audio/generated_{index}.wav'
        rules_set.append((rule_func, commentary, audio_path))
    return rules_set

def generate_commentaries(init_prompt="", test=False):
    if test:
        with open('./test/test_commentaries.txt', 'r') as f:
            llm_output = f.read()
    else:
        state_variable_descr = """
        """

        examples_str = """
        """

        prompt = init_prompt + state_variable_descr + examples_str

        llm_output = llm(prompt)
    return llm_output

if __name__ == "__main__":
    print(llm_parser(generate_commentaries(test=True), generate_audio=False))