class Group:
    
    def __init__(self,presentation_string, identity_symbol = "e", abelian=False):
        self.identity_symbol = identity_symbol
        presentation_string_split = presentation_string[1:-1].split("|")
        self.alphabet = presentation_string_split[0].split(",")
        self.constraints = presentation_string_split[1].split(",")
        self.words = self.generate_reduced_words(self.alphabet, self.constraints, abelian=abelian)
        self.order = len(self.words)
        self.table = self.multiplication_table()
        
    def generate_reduced_words(self,alphabet, constraints, abelian = False, word_length_limit = 10):
        reduced_words = set()
        constraints = self.clean_constraints(alphabet,constraints,abelian=abelian)

        def dfs(word):
            if len(word)>word_length_limit:
                return
            if self.satisfies_constraints(word, constraints):
                reduced_words.add(word)
            
            for letter in alphabet:
                new_word = word + letter
                if not self.violates_constraints(new_word, constraints):
                    dfs(new_word)
        
        dfs("")
        reduced_words = list(reduced_words)
        reduced_words.sort(key= lambda x: (len(x), x))
        reduced_words[0] = self.identity_symbol
        return reduced_words

    def clean_constraints(self, alphabet,constraints,abelian=False):
        
        e = self.identity_symbol
        
        for i in range(len(constraints)):
            constraints[i] = self.expand_powers(constraints[i])
        
        if abelian:
            for i in range(len(alphabet)):
                for j in range(i+1,len(alphabet)):
                    constraints.append(alphabet[j] + alphabet[i] + "=" + alphabet[i] + alphabet[j])
                    
        for i in range(len(constraints)):
            a,b = constraints[i].split("=")
            while a[0]==b[0]:
                a = a[1:]
                b = b[1:]
                if b=="":
                    b = e
                    break
                if a=="":
                    a = e
                    break
            while a[-1]==b[-1]:
                a = a[:-1]
                b = b[:-1]
                if b=="":
                    b = e
                    break
                if a=="":
                    a = e
                    break
            if a==e or (not b==e and a<b):
                constraints[i] = b + "=" + a
            else:
                constraints[i] = a + "=" + b
        
        constraints.append(e + e + "=" + e)
        for a in alphabet:
            constraints.append(f'{a}{e}={a}')
            constraints.append(f'{e}{a}={a}')
            
        return constraints
        
    def satisfies_constraints(self, word, constraints):
        for constraint in constraints:
            if not self.matches_constraint(word, constraint):
                return False
        return True

    def matches_constraint(self, word, constraint):
        a, b = constraint.split("=")
        return not a in word

    def violates_constraints(self, word, constraints):
        for constraint in constraints:
            if not self.matches_constraint(word, constraint):
                return True
        return False

    def expand_powers(self, word):
        expanded_word = ""
        i = 0
        while i < len(word):
            if i+2 < len(word) and word[i+2].isdigit():
                expanded_word += word[i]*int(word[i+2])
                i += 3
            else:
                expanded_word += word[i]
                i += 1
        return expanded_word
    def collect_powers(self, word):
        collected_word = ""
        i = 0
        while i < len(word):
            count = 1
            while i+1 < len(word) and word[i] == word[i+1]:
                count += 1
                i += 1
            if count == 1:
                collected_word += word[i]
            else:
                collected_word += word[i] + "^" + str(count)
            i += 2
        return collected_word

    def simplify(self, word, constraints):
        original_word = word
        for constraint in constraints:
            a,b = constraint.split("=")
            word = word.replace(a,b)
        if word == original_word:
            return self.collect_powers(word)
        else:
            return self.simplify(word, constraints)

    def multiplication_table(self):
        table = []
        for a in self.words:
            row = []
            for b in self.words:
                row.append(self.simplify(a+b,self.constraints))
            table.append(row)
        return table

    def show_table(self, padding=4):
        
        for row in self.table:
            for word in row:
                if len(word)+2 > padding:
                    padding = len(word)+2
        
        
        print(''.ljust(padding), end='|'.ljust(padding))
        for word in self.table[0]:
            print(word.ljust(padding), end='')
        print()
        for word in self.table[0]:
            print("-"*(len(word.ljust(padding))+2), end='')
        print()
        for row in self.table:
            print(row[0].ljust(padding), end='|'.ljust(padding))
            for word in row:
                print(word.ljust(padding), end='')
            print()
            
    def __str__(self):
        string = ""
        padding = 4
        for row in self.table:
            for word in row:
                if len(word)+2 > padding:
                    padding = len(word)+2
        string += ''.ljust(padding) + '|'.ljust(padding)
        for word in self.table[0]:
            string += word.ljust(padding)
        string += '\n'
        for word in self.table[0]:
            string += "-"*(len(word.ljust(padding))+2)
        string += '\n'
        for row in self.table:
            string += row[0].ljust(padding) + '|'.ljust(padding)
            for word in row:
                string += word.ljust(padding)
            string += '\n'
        return string
        


fourth_roots_of_unity = Group("<i|i^4=1>",abelian=True,identity_symbol="1")
print("Order:",fourth_roots_of_unity.order)
print(fourth_roots_of_unity)