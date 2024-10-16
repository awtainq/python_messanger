from censure import Censor

censor_ru = Censor.get(lang='ru')
censor_en = Censor.get(lang='en')
def check_message(message):
    line_ru = censor_ru.check_line(message)
    line_en = censor_en.check_line(message)
    if line_ru['is_good'] and line_en['is_good']:
        return True
    else:
        return False