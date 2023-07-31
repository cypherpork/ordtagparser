import re

class MassageData(object):

    def isTagno(self, in_word):
        if len(in_word) == 2:
            if in_word.isdigit:
                int_word = int(in_word, base=16)
                if int_word % 2 == 0:
                    return -1 * int_word
                else:
                    return int_word
            else:
                return -1
        else:
            return -1

    def sanitize(self, s):
        s = s.replace("\t", "    ")
        return re.sub(r"[^ -~]", "", s)

    def purifyTags(self, in_words):
        tag1_is_present = False
        check_tag1 = False
        expect_tagno = True
        out_words = []
        for word in in_words:
            v_istagno = self.isTagno(word)
            if expect_tagno:
                if v_istagno > 0:
                    if v_istagno == 1:
                        check_tag1 = True
                        tag1_is_present = True
                    out_words.append(word)
                    expect_tagno = 0
            else:
                if v_istagno > -1:
                    out_words.append('NO VALUE')
                    if v_istagno == 1:
                        check_tag1 = True
                        tag1_is_present = True
                    out_words.append(word)
                else:
                    out_words.append(word)
                    expect_tagno = True
                    if check_tag1:
                        check_tag1 = False
        if not expect_tagno:
            out_words.append('NO VALUE')
        return tag1_is_present, out_words

    def shapeTagArray(self,tags):
        tag_cols = 2
        return [tags[i:i + tag_cols] for i in range(0, len(tags), tag_cols)]

    def reverseTag(self,in_str):
        ba = (bytearray.fromhex(in_str))
        ba.reverse()
        return ba.hex()

    def guessTag(self, in_tagno, in_tagvalue):
        guess = 'can\'t guess'
        note = 'maybe new notation'
        notation_id = -1
        if in_tagno == '03':
            taglength = len(in_tagvalue)
            if taglength > 131:
                guess = bytes.fromhex(in_tagvalue).decode("utf-8").replace("\"", "\\\"")
                if taglength > 254:
                    note = 'utf8-encoded rarity traits'
                    notation_id = 5
                elif taglength == 132:
                    note = 'utf8-encoded big-endian parent inscription id'
                    notation_id = 2
            elif taglength == 72:
                parent = self.reverseTag(in_tagvalue[:64])
                guess = 'Parent Inscr Genesis TrxTD: ' + parent
                note = 'Notation: Input-0-for-Parent'
                if in_tagvalue[-8:] == '00000000':
                    guess = guess + ', no grandparent.'
                elif in_tagvalue[-8:] == '00000001':
                    guess = guess + ', it also has a grandparent.'
                notation_id = 3
            elif taglength == 64:
                guess = self.reverseTag(in_tagvalue)+'i0'
                note = 'binary little-endian parent inscription id on second output'
                notation_id = 4
        elif in_tagno == '01':
            try:
                guess = bytes.fromhex(in_tagvalue).decode("utf-8").replace("\"", "\\\"")
                guess_sanitized = self.sanitize(guess)
                if guess_sanitized != guess:
                    note = 'content format; illegal characters were present and sanitized'
                    guess = guess_sanitized
                    notation_id = 1
                else:
                    note = 'content format'
                    notation_id = 0
            except:
                pass
        elif in_tagno == '15':
            try:
                guess = guess = bytes.fromhex(in_tagvalue).decode("utf-8").replace("\"", "\\\"")
                note = 'Metadata'
                notation_id = 6
            except:
                notation_id = 255
                pass
        elif in_tagno == '00' and in_tagvalue == 'INVALID_ENVELOPE':
            guess = 'error'
            note = 'envelope could not be parsed'
            notation_id = -1
        return guess, note, notation_id


