from googletrans import Translator, constants
from googletrans import LANGCODES as LANGUAGES

class Translate:
    def __init__(self):
        self.translator = Translator()
    
    def process(self, text, language_code="auto"):
        if language_code == 'cn':
            language_code = 'zh-cn'
        if isinstance(text, bytes):
            text = str(text.decode('utf8'))[2:-1]

        result = ''
        chunks = []
        active_slice = ''
        i = 0
        while len(text) > 0:
            i += 1
            if len(text[:i]) > 2500:
                chunks.append(text[:i-1])
                text = text[i:]
                i = 0
            elif len(text) <= 2500:
                chunks.append(text)
                text = ""

        for chunk in chunks:
            translation = self.translator.translate(chunk,src=language_code)
            result += translation.text
        return result
        

        
        


