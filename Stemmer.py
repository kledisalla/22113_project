# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 14:40:57 2024

@author: dimsl
"""

class Stemming:

    def is_not_a_vowel(self,letter):
        ''' Function which checks if a letter is a vowel or not.
            Return True is it not, False if it is'''
        
        if letter in ["a","e","o","i","u"]:
            return False
        else:
            return True
        
    def is_not_a_vowel_before(self,word,i):
        ''' Function that checks if a letter is a position is not a vowel like
            in is_not_a_vowel function.Then, it checks if letter is "y" if it is
            it returns False if the previous letter in that position is also not a vowel
        '''
        letter=word[i]
        if self.is_not_a_vowel(letter):
            if letter=="y" and self.is_not_a_vowel(word[i-1]):
                return False
            else:
                return True
        else:
            return False
    

    def get_word_form(self,word):
        '''Function that returns how the word is structured. It analyzes each letter
           of the parameter "word" and returns a string in the form CV where C means 
           consonant (Not a vowel) and V vowel '''
        form=''
        for i in range(len(word)):
            if self.is_not_a_vowel_before(word,i):
                if i!=0:
                    previous_letter=form[-1]
                    if previous_letter!="C":
                        form+="C"
                else:
                    form+="C"
            else:
                if i!=0:
                    previous_letter=form[-1]
                    if previous_letter!="V":
                        form+="V"
                else:
                    form+="V"
                        
        return form
    
    def cvc_form(self,word):
        
        if len(word)>=3:
            if self.is_not_a_vowel_before(word,-3) and not self.is_not_a_vowel_before(word,-2) and self.is_not_a_vowel_before(word,-1):
                return True if word[-1] not in ["w","x","y"] else False
            else:
                return False
        else:
            return False
                
        
    
    def remove_endings(self,word):
        '''Step 1 of stemming: It removes common word endings, sses,ies,s.
           For example:
            classes----> class
            theories---> theori
            '''
        
        #Deal with sses,ises and s
        if word.endswith("sses"):
            word=word.replace("sses","ss")
        elif word.endswith("ies"):
            word=word.replace("ies","i")
        elif word.endswith("s"):
            word=word.replace("s","")
        else:
            pass
        
        return word
    
    def remove_more_endings(self,word):
        '''Step 2 of stemming: It removes more common word endings
           For example:
               agreed---> agree
        '''
        
        if word.endswith("eed"):
            #remove the endig eed
            base_word=word[:-(len("eed"))]
            #check if the structure of the word has at least a vowel+non vowel pair 
            if self.get_word_form(word).count("VC")>0:
                #keep the word after removing "eed" and add "ee".
                word=base_word
                word+="ee"
                
        elif word.endswith("ed"):
            base_word=word[:-(len("ed"))]
            
            for letter in base_word:
                if not self.is_not_a_vowel(letter):
                    word=base_word
                    word=self.fix_stem_ending(word)
        elif word.endswith("ing"):
            base_word=word[:-(len("ing"))]
            for letter in base_word:
                if not self.is_not_a_vowel(letter):
                    word=base_word
                    word=self.fix_stem_ending(word)
        return word
    
    
    
    def fix_stem_ending(self,word): #step 2
        if word.endswith(("at","bl","iz")):
            word+="e"
        if len(word)>=2:
            if (self.is_not_a_vowel_before(word,-1) and self.is_not_a_vowel_before(word,-2)) and (not word.endswith(("l", "s", "z"))):
                    word=word[:-1]
        if self.get_word_form(word).count("VC")==1 and self.cvc_form(word):
            word+="e"
        return word
    
    def replace_terminal_y(self,word):
        if word.endswith("y"):
            for letter in word[:-1]:
                if not self.is_not_a_vowel(letter):
                    word=word[:-1]
                    word+="i"
        return word
                    
    def handle_suffixes(self,word,suffix,replaced_suffix):
        result=word.rfind(suffix)
        base = word[:result]
        if self.get_word_form(base).count("VC") >=0:
            replaced = base + replaced_suffix
            return replaced
        else:
            return word
        
    def replace_suffixes(self,word): #step2c
        suffix_replacements = {
            'ational': 'ate',
            'tional': 'tion',
            'enci': 'ence',
            'anci': 'ance',
            'izer': 'ize',
            'abli': 'able',
            'alli': 'al',
            'entli': 'ent',
            'eli': 'e',
            'ousli': 'ous',
            'ization': 'ize',
            'ation': 'ate',
            'ator': 'ate',
            'alism': 'al',
            'iveness': 'ive',
            'fulness': 'ful',
            'ousness': 'ous',
            'aliti': 'al',
            'iviti': 'ive',
            'biliti': 'ble',
            'al': '',
            'ance': '',
            'ence': '',
            'er': '',
            'ic': '',
            'able': '',
            'ible': '',
            'ant': '',
            'ement': '',
            'ment': '',
            'ent': '',
            'ou': '',
            'ism': '',
            'ate': '',
            'iti': '',
            'ous': '',
            'ive': '',
            'ize': '',
            'icate': 'ic',
            'ative': '',
            'alize': 'al',
            'iciti': 'ic',
            'ful': '',
            'ness': ''
        }
        
        for suffix, replaced_suffix in suffix_replacements.items():
            if word.endswith(suffix):
                return self.handle_suffixes(word, suffix, replaced_suffix)
        if word.endswith('ion'):
            result = word.rfind('ion')
            base = word[:result]
            if self.get_word_form(base).count("VC") > 1 and base.endswith("s","t"):
                word = base
            word = self.replaceM1(word, '', '')
        return word
        
    def handle_terminal_e(self,word): #step 4a
        if word.endswith("e"):
            if self.get_word_form(word[:-1]).count("VC") >1:
                return word[:-1]
            elif self.get_word_form(word[:-1]).count("VC") ==1 and not self.cvc_form(word[:-1]):
                return word[:-1]
            else:
                return word
        else:
            return word
            
    def remove_double_non_vowel(self,word): #step 4b
        
        if self.get_word_form(word).count("VC") >1:
            if len(word)>=2:
                if (self.is_not_a_vowel_before(word,-1) and self.is_not_a_vowel_before(word,-2)):
                    if word.endswith("l"):
                        return word[:-1]  
                    else:
                        return word
                else:
                    return word
            else:
                return word
        else:
            return word
    
    def stem_word(self,word):
        word = self.remove_endings(word)
        word = self.remove_more_endings(word)
        word = self.replace_terminal_y(word)
        word = self.replace_suffixes(word)
        word = self.handle_terminal_e(word)
        word= self.remove_double_non_vowel(word)

        return word
            
test=Stemming()
result=test.stem_word("created")

    


    
