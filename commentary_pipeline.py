from llm_output_parser import llm_parser, generate_commentaries
import traceback as tb
rules_set = llm_parser(generate_commentaries(test=True), generate_audio=False)
last_step = [None for _ in range(len(rules_set))] # count of steps_left since the last time the rule was triggered
def commentary_pipeline(observation, previous_observation):
    for index, (rule_func, commentary, audio_path) in enumerate(rules_set):
        try:
            if rule_func(observation, previous_observation):
                if (not last_step[index]) or last_step[index] - observation['steps_left'] > 100:
                    last_step[index] = observation['steps_left']
                    return commentary, audio_path
        except:
            continue
    return None, None