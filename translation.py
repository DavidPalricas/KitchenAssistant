#
# https://github.com/uliontse/translators
#
# install translators: 
#   pip install --upgrade translators
# conda install:
#   conda install -c conda-forge translators
# source intall:
#   git clone https://github.com/UlionTse/translators.git
#   cd translators
#   python setup.py install

import translators as ts

# teste com varios idiomas
#q_text= "Hello, how are you?"
#q_text= "In a large sauce pot, heat the olive oil on medium heat and add the chopped rosemary and garlic, letting it cook for about 2 minutes."
#q_text = "Buenos días, ¿cómo estás?" 
#q_text = "Bonjour, comment ça va?"
#q_text = "Guten Morgen, wie geht es dir?"
q_text = "In a large sauce pot"

#
# ['alibaba', 'apertium', 'argos', 'baidu', 'bing', 'caiyun', 
# 'cloudTranslation', 'deepl', 'elia', 'google', 'iciba', 'iflytek', 
# 'iflyrec', 'itranslate', 'judic', 'languageWire', 'lingvanex', 
# 'niutrans', 'mglip', 'mirai', 'modernMt', 'myMemory', 'papago', 
# 'qqFanyi', 'qqTranSmart', 'reverso', 'sogou', 'sysTran', 'tilde', 
# 'translateCom', 'translateMe', 'utibet', 'volcEngine', 'yandex', 
# 'yeekit', 'youdao']
# 
# pool com todos os tradutores possiveis
# print(ts.translators_pool)

# 
# translate_text(text, provider, to_language, from_language)
#   
#   translate_text : função para traduzir texto
# print(ts.translate_text(q_text,"deepl", "en", "pt")) 
#
#   transtale_html : função para traduzir html
# print(ts.translate_html(html_text,"deepl", "en", "pt"))


res = ts.translate_text(q_text, "google", "auto", "pt") 
print("\n")
print("Frase a traduzir: \n", q_text)
print("\n")
print("Resultado da tradução: \n", res)     
print("\n")