import re
class Stemmer:
    ''' The class follows the Porter stemmer algorithms '''
    
    def is_vowel(self,letter):
        ''' Function which checks if a letter is a vowel or not.
            Return True is it, False if it is not'''
        
        if letter in ["a","e","o","i","u"]:
            return True
        else:
            return False
        
    def word_structure(self,word):
        '''Function that analyzes the structure of the word. If it encouters a 
            vowel letter it produces a V else C(consonant). What it returns is a sequence
            of Cs and Vs based on the letters. If a there are more than one Cs or Vs 
            in a row, it produces only one letter 
            For example Tree --> CCVV --> CV 
        '''
        form= "V" if self.is_vowel(word[0]) else "C"
        for letter in word[1:]:
            if self.is_vowel(letter):
                if form[-1]=="V":
                    continue
                else:
                    form+="V"
            else:
                if form[-1]=="C":
                    continue
                else:
                    form+="C"
        return form
    
    def get_measure(self,word):
        
        '''Function that return the amount of VC found in the structure of a word '''
        
        return self.word_structure(word).count("VC")  
    
    def contains_vowel(self,word):
        for letter in word:
            if self.is_vowel(letter):
                return True
        return False
    
        
    
    def step_1_part_2_supplementary(self,word):
        ''''Function that suplments step step_1_part_2 '''
        
        #Example: inflated --> inflate
        if word.endswith("at"):
            word=word[:-len("at")] +"ate"
        
        #Example: troubled --> trouble
        elif word.endswith("bl"):
            word=word[:-len("bl")] + "ble"
        
        #Example: sized --> size
        elif word.endswith("iz"):
            word=word[:-len("iz")] + "ize"
        
        #If it ends with double consonant and the last letter is not l,s or z then remove the last element 
        elif (not self.is_vowel(word[-1]) and not self.is_vowel(word[-2])) and not word.endswith(("l", "s", "z")):
            #Example hopp --> hop
            word=word[:-1]
        
        #If it has only one vowel+consonant and it ends with consonant + vowel + consonant and the last letter is not w,x or y
        elif (self.get_measure(word) == 1 and self.word_structure(word[-3:]) == "CVC") and not self.word_structure(word[-1]) in ["w", "x", "y"]:
            #Add an e in the end 
            #Example fil -> file
            word+="e"
            
        return word
        
        
    '''                           First step of the algorithm                         '''
                        
    def step_1_part_1(self,word):
        '''Part 1: The algorithms deals with plural words
            For example : classes -> class
        '''
        
        if word.endswith("sses"):
            return word[:-len("sses")] + "ss"
        
        elif word.endswith("ies"):
            return word[:-len("ies")] + "i"
        elif word.endswith("ss"):
            return word
        
        elif word.endswith("s"):
            return word[:-1]
        
        else:
            return word
            
    def step_1_part_2(self, word):
        '''Part 2: The second part of step 1 deals with past particle and continuous forms
           For example:
               hopping--> hopp --> hop
        '''

        
        include_step_1_part_2_supplementary=False
        #if the word ends with eed and has at least one vowel+ consonant simply replace eed with ee
        # Example agreed--> agree
        
        if word.endswith("eed") :
            if self.get_measure(word[:-len("eed")]) > 0:
                word = word[:-len("eed")] +"ee"
            else:
                return word
        

        for suffix in ["ed","ing"]:
            if word.endswith(suffix):
                stem= word[:-len(suffix)]
                if self.contains_vowel(stem):
                    include_step_1_part_2_supplementary=True
                    break
        if not include_step_1_part_2_supplementary:
            return word
        
        word=self.step_1_part_2_supplementary(stem)
        return word
                
    
    def step_1_part_3(self,word):
        if self.contains_vowel(word[:-1]) and word.endswith("y"):
            return word[:-1] + "i"
        return word
        
        
    '''                           Second step of the algorithm                         '''
    '''                         Step 2-4 primary deal with suffixes                    '''
    
    def step_2(self,word):
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
        }
        
        for suffix, replaced_suffix in suffix_replacements.items():
            if self.get_measure(word)>0 and word.endswith(suffix):
                return word[:-len(suffix)] + replaced_suffix
        return word
    
    '''                           Third step of the algorithm                         ''' 
    
    def step_3(self,word):
            suffix_replacements = {       
                    'icate': 'ic',
                    'ative': '',
                    'alize': 'al',
                    'iciti': 'ic',
                    'ful': '',
                    'ness': '',
                    'ical': 'ic'
                    }
            for suffix, replaced_suffix in suffix_replacements.items():
                if word.endswith(suffix) and self.get_measure(word)>0:
                    return word[:-len(suffix)] + replaced_suffix
                else: 
                    pass
            return word
        
    '''                           Forth step of the algorithm                         ''' 
    
    def step_4(self,word):
        suffix_replacements = {
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
        }
        if (word.endswith("ion") and self.get_measure(word)>1) and word[-4] in ["t","s"]:
            return word[:-len("ion")]
        
        for suffix, replaced_suffix in suffix_replacements.items():
            if word.endswith(suffix) and self.get_measure(word)>1:
                return word[:-len(suffix)] + replaced_suffix
        
        return word
    
    '''                           Fifth step of the algorithm                         '''
    '''  Step 5 deals with fixing the words after the suffixes are removed            '''
    
    def step_5_part_1(self,word):
        if self.get_measure(word) > 1 and word.endswith("e"):
            return word
        elif self.get_measure(word)==1 and not (self.word_structure(word[:-1][-3:]) == "CVC" and self.word_structure(word[:-1][-1]) in ["w", "x", "y"]):
            if word.endswith('e'): 
                return word
        return word
    
    def step_5_part_2(self,word):
        if self.get_measure(word)>1 and (not self.is_vowel(word[-1]) and not self.is_vowel(word[-2])) and word.endswith("l"):
            return word[:-1]
        return word
    
    '''                           Streamlined algorithm                         '''
    
    def stem_word(self,word):
        special_characters=[".","(",")","!","?",",","|","[","]",":",""]
        word=word.strip().lower()
        for char in special_characters:
            word = word.replace(char, "")
        if re.match('^[a-zA-Z]+$', word):
            word=self.step_1_part_1(word)
            word=self.step_1_part_2(word)
            word=self.step_1_part_3(word)
            word=self.step_2(word)
            word=self.step_3(word)
            word=self.step_4(word)
            word=self.step_5_part_1(word)
            word=self.step_5_part_2(word)
            return word
        

st=Stemmer()
print(st.stem_word(""))