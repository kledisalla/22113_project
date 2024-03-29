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
        ''' Function that returns True if a word contains at least 1 vowel'''
        
        for letter in word:
            if self.is_vowel(letter):
                return True
        return False
    
    def ends_with_same_consonant_doubled(self,word):
        ''' Function that returns True if a word contains double of the same consonant(non-vowel)
            in the end of it
            hiss --> True 
        '''
        
        if not self.is_vowel(word[-1]) and word[-1]==word[-2]:
            return True
        else:
            return False
    
    
    def ending_form(self,word):
        ''' Function that returns true if the word ends with consonant-vowel-consonant'''
        if self.word_structure(word[-3:]) == "CVC":
            return True
        else:
            return False
        
    def step_1_part_2_supplementary(self,word):
        ''' Function that supplements step 2 if the second or third conditions are met'''
        
        # created--> create
        if word.endswith("at"):
            word=word[:-len("at")]+"ate"
            
        #crumbled --> crumble
        elif word.endswith("bl"):
            word=word[:-len("bl")]+"ble"
            
        #criticizing--> criticize
        elif word.endswith("iz"):
            word=word[:-len("iz")]+"ize"
        
        #hopped -->  hop
        elif self.ends_with_same_consonant_doubled(word):
            if not word[-1] in ["l","s","z"]:
             word=word[:-1]
        #filing --> file    
        elif self.get_measure(word)==1:
            if self.ending_form(word) and self.word_structure(word[-1]) not in ["x","w","y"]:
                word=word+"e"
        return word
            
            
    '''                           First step of the algorithm                         '''
                        
    def step_1_part_1(self,word):
        '''Part 1: The algorithms deals with plural words'''
        
        #The length of word is checked so the algorithm does not stem words like 'this' 	
        if len(word)>4:
            
            #caresses --> caress
            if word.endswith("sses"):
                return word[:-len("sses")] + "ss"
            
            #ponies	 --> ponni	
            elif word.endswith("ies"):
                return word[:-len("ies")] + "i"
            
            #caress --> caress
            elif word.endswith("ss"):
                return word
            
            #cats --> cat
            elif word.endswith("s"):
                return word[:-1]
            
            else:
                return word
        return word

    def step_1_part_2(self,word):
        
        '''Part 2: Past simple and present continuous forms '''
        
        stemmed_word=word 
        #Flag that tells the algorithm that the supplementary step is required
        supplementary_step_required=False
        
        #feed --> feed 
        if stemmed_word.endswith("eed") and len(word)>3:
            if self.get_measure(stemmed_word[:-len("eed")]):
                stemmed_word=word[:-len("eed")] + "ee"
            else:
                return stemmed_word
            
        stem=stemmed_word
        #If the word ends with ed or ing then the supplementary step is required
        #cared --> care
        #hissing --> hiss
        for suffix in ["ed","ing"]:
            #We also check for the length of the word so as not stem word that may be 
            #incorrently written giving and error. For example a random alone 'ing' in the text
            
            if word.endswith(suffix) and len(word)>3:
                stem= stemmed_word[:-len(suffix)]
                
                if self.contains_vowel(stem):
                    supplementary_step_required=True
                    break
                
        if not supplementary_step_required:
            return stem
        
        word=self.step_1_part_2_supplementary(stem)
        return word
    
    #Step 3 states that words that end with y and the stem has a vowel need to be changed to end with an 'i'
    def step_1_part_3(self,word):
        if word.endswith("y") and self.contains_vowel(word[:-1]):
            return word[:-1]+"i"
        else:
            return word

    '''                           Second step of the algorithm                         '''
    '''                         Steps 2-4 primary deal with suffixes                    '''
     
    def step_2(self,word):
        
        #relational --> relate
        
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
            
            #Word with length bigger than the suffix are stemmed only
            #Example restfulness --> restful
            if len(word)>len(suffix):
                
                if self.get_measure(word[:-len(suffix)])>0 and word.endswith(suffix):
                    return word[:-len(suffix)] + replaced_suffix
                
        return word   

    '''                           Third step of the algorithm                         '''     
    
    def step_3(self,word):
        
        #formative --> form
        
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
            
            if len(word)>len(suffix):
                
                if word.endswith(suffix) and self.get_measure(word[:-len(suffix)])>0:
                    return word[:-len(suffix)] + replaced_suffix
                
        return word
    
    '''                           Fourth step of the algorithm                         '''
    def step_4(self,word):
        
        #allowance --> allow
       
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
        
        if word.endswith("ion") and len(word)>4:
            
            if self.get_measure(word[:-len("ion")])>1 and word[-4] in ["t","s"]:
                return word[:-len("ion")]
        
        for suffix, replaced_suffix in suffix_replacements.items():
            
            if len(word)>len(suffix):
                
                if word.endswith(suffix) and self.get_measure(word[:-len(suffix)])>1:
                    return word[:-len(suffix)] + replaced_suffix
        
        return word    
    
    '''                           Fifth step of the algorithm                         '''
    '''  Step 5 deals with fixing the words after the suffixes are removed            '''
    
    def step_5_part_1(self,word):
        
        #check the length of the word to prevent stemming words like "ate"
        if len(word)>1:
            
            if self.get_measure(word[:-1]) > 1 and word.endswith("e"):
                 return word[:-1]
             
        else:
            
            if len(word)>1:
                if self.get_measure(word[:-1])==1 and not (self.ending_form(word[:-1]) and word[:-1] not in ["w","x","y"]):
                    
                    if word.endswith('e'): 
                        return word[:-1]
        return word
    
    def step_5_part_2(self,word):
        
        #fill --> fill
        if self.get_measure(word)>1 and self.ends_with_same_consonant_doubled(word) and word[-1]=="l":
            return word[:-1]
        
        return word    

    '''                           Streamlined algorithm                         '''
    
    def stem_word(self,word):
        #turn the word being stemmed to lower case
        word=word.strip().lower()
        
        #Run each step sequentially
        word=self.step_1_part_1(word)
        word=self.step_1_part_2(word)
        word=self.step_1_part_3(word)
        word=self.step_2(word)
        word=self.step_3(word)
        word=self.step_4(word)
        word=self.step_5_part_1(word)
        word=self.step_5_part_2(word)
        return word