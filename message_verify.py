from censure import Censor

censor = Censor.get(lang='ru')
def check_message(message):
    line_info = censor.check_line(message)
    if line_info['is_good']:
        return True
    else:
        return False