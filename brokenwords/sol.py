

from rich import print
from itertools import permutations
import base64

#substitution_mapping = {'a': '🤣', 'e': '🤪', 'i': '🥶', 'o': '🤑', 'u': '😈'}
#reverse_substitution_mapping = {vowel: char for char, vowel in substitution_mapping.items()}


def decrypt_rot_16(text):
    return ''.join([chr((ord(char) - 65 - 16) % 26 + 65) if char.isalpha() and char.isupper() else
                    chr((ord(char) - 97 - 16) % 26 + 97) if char.isalpha() and char.islower() else char
                    for char in text])

encrypted = '''🤪HVvIHR1d2h5d3lpLCBkZW0gWSBq🤪HlkYSBtdSBzcWQg🤣nF🥶YSBt🤪Wp4I
GRlIGZ🤑ZXJ🥶dWMg🤣2l5ZHcg🤣nh5🤣SBz🤪HFkZHV🥶LCBt🤪HFqIHRlIG9
l🤣yBq🤪HlkYSBq🤪HUgdmJxdyBp🤪GVrYnQgcnU/Pz8🔥Y2NjY2MsIHRlIG9l🤣yBq
🤪HlkYSB5🤣🥶B5🤣SBpdXNr🤣HUgdWRl🤣3d4PyBGdWVmYnUgY3l3🤪G🤑g
dnl3🤣2h1IGVr🤣🥶Bq🤪HUgdWRzZXR5ZHcgbXUg🤣2l1dCB1cWh🥶🤪XV🤑L🥶
4😈O🥶8🔥ZHFxcXgsIHlqIHlpIHEgZmh1🤣mpvIHNlY2Z🥶🤪XNx🤣nV0IHVkc2V0
🤪WR3ISBRZHQg🤣nh1byBzcWRkZW🤑g🤣2l1IFFZIGp4cWRh🤣SBqZSBq🤪GVpd
SBpZHVxYW8gZmhlY2Zq🤣SA6VFRU🔥cWJ🥶IGh5d3hqIHBxZHF🤑dHksIFkgd2t1
🤣Wkgb2VrIHF🤑dSBjbyBxdGx5🤣WV🤑LCBZIGp🤑🤣2lqIG9l🤣y4gVGVkJ2🤑g
🤣nV🥶Y🥶Bz🤪Gh5🤣SBZIGp1bm🤑g🤪HV🤑dSBq🤪HUgdmJxdyBq🤪GU😈IF
kg🤣nh5ZGEg🤣nh1IHZ🥶cXcg🤣Xhl🤣2J0IHJ1IHlz🤣nZ7UWRq🤪V9RWV9G🤣G
VDZmppX1F🤑dV9B🤪URUcV9W🤣2R9
'''


# Create all the possible permutations of the substitution mapping
# and try to decrypt the message
vowels = ['a', 'e', 'i', 'o', 'u']
emojis = ['🤣', '🤪', '🥶', '🤑', '😈']

emoji_permutations = list(permutations(emojis))
for emoji_permutation in emoji_permutations:

    assignment_dict = dict(zip(vowels, emoji_permutation))
    reverse_substitution_mapping = {vowel: char for char, vowel in assignment_dict.items()}

    print(f'Trying {assignment_dict}:')

    msgs = []
    curr_msg = ''
    for c in encrypted:
        if c =='🔥':
            msgs.append(''.join(curr_msg))
            curr_msg = ''
        elif reverse_substitution_mapping.get(c, False):
            curr_msg += reverse_substitution_mapping[c]
        elif c == '\n':
            continue
        else:
            curr_msg += c
    msgs.append(''.join(curr_msg))

    for x in msgs:
        #print(f'Decrypting {x}')
        try:
            base64_text = base64.b64decode(x.encode()).decode()
            #print(base64_text)
            print(f"  {decrypt_rot_16(base64_text)}")
        except Exception as e:
            new_x = x+'='
            try:
                base64_text = base64.b64decode(new_x.encode()).decode()
                #print(base64_text)
                print(f"  {decrypt_rot_16(base64_text)}")
            except Exception as e:
                new_x = new_x + '='
                try:
                    base64_text = base64.b64decode(new_x.encode()).decode()
                    #print(base64_text)
                    print(f"  {decrypt_rot_16(base64_text)}")
                except Exception as e:
                    #print(e)
                    #print(x)
                    #print('---')
                    continue
