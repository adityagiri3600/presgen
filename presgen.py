class Group:
    
    def __init__(self,presentation_string):
        
        presentation_string_split = presentation_string[1:-1].split("|")
        self.alphabet = presentation_string_split[0].split(",")
        self.constraints = presentation_string_split[1].split(",")
        self.words = self.generate_reduced_words(self.alphabet, self.constraints)
        self.table = self.multiplication_table()
        
    def generate_reduced_words(self,alphabet, constraints,word_length_limit=10):
        reduced_words = set()
        constraints = self.clean_constraints(alphabet,constraints)

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
        reduced_words.sort()
        reduced_words[0] = 'e'
        return reduced_words

    def clean_constraints(self, alphabet,constraints):
        
        for i in range(len(constraints)):
            a,b = constraints[i].split("=")
            while a[0]==b[0]:
                a = a[1:]
                b = b[1:]
                if b=="":
                    b = "e"
                    break
                if a=="":
                    a = "e"
                    break
            while a[-1]==b[-1]:
                a = a[:-1]
                b = b[:-1]
                if b=="":
                    b = "e"
                    break
                if a=="":
                    a = "e"
                    break
            if a=="e" or (not b=="e" and a<b):
                constraints[i] = b + "=" + a
            else:
                constraints[i] = a + "=" + b
        
        constraints.append("ee=e")
        for a in alphabet:
            constraints.append(f'{a}e={a}')
            constraints.append(f'e{a}={a}')
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


    def multiply(self, a,b,constraints):
        word = a+b
        def replace_till_no_change(word):
            original_word = word
            for constraint in constraints:
                a,b = constraint.split("=")
                word = word.replace(a,b)
            if word == original_word:
                return word
            else:
                return replace_till_no_change(word)
        return replace_till_no_change(word)

    def multiplication_table(self):
        table = []
        for a in self.words:
            row = []
            for b in self.words:
                row.append(self.multiply(a,b,self.constraints))
            table.append(row)
        return table

    def show_table(self, padding=4):
        
        for row in self.table:
            for word in row:
                if len(word)+2 > padding:
                    padding = len(word)+2
        
        
        print(''.ljust(padding), end='')
        for word in self.table[0]:
            print(word.ljust(padding), end='')
        print()
        for row in self.table:
            print(row[0].ljust(padding), end='')
            for word in row:
                print(word.ljust(padding), end='')
            print()


klein_group = Group("<a,b|aa=e,bb=e,ab=ba>")
klein_group.show_table()