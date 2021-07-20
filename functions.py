import random


class Fraction:
    def __init__(self, z, n):
        self.z = z
        self.n = n
        
    def to_tex(self):
        if self.n.to_tex() != '1':
            return "\\frac{" + self.z.to_tex() + "}{" + self.n.to_tex() + "}"
        else:
            return self.z.to_tex()
        
    def solution(self):
        exponents = {}
        if type(self.z) == Mult and type(self.n) == Mult:
            sol_z = self.z.solution()
            sol_n = self.n.solution()
            
            keys_z = list(sol_z.keys())
            keys_n = list(sol_n.keys())
            
            keys = set(keys_z + keys_n)
            
            for key in keys:
                exponents[key] = sol_z[key] - sol_n[key]
                
            return exponents
            
            

class Power:
    def __init__(self, b, e):
        self.b = b
        self.e = e
        
    def solution(self):
        exponents = {}
        if type(self.e) == int and (type(self.b) == Fraction or type(self.b) == Mult):
            sol_b = self.b.solution()
            
            for key in sol_b:
                exponents[key] = sol_b[key]*self.e
        elif type(self.e) == int and type(self.b) == Literal:
            exponents[self.b.s] = self.e
        return exponents

        
    def to_tex(self):
        if type(self.e) is int and type(self.b) is Fraction:
            if self.e == 1:
                return self.b.to_tex()
            elif self.e == 0:
                return '1'
            else:
                return "\\left(" + self.b.to_tex() + "\\right)^{" + str(self.e) + "}" 
        if type(self.e) is int and type(self.b) is Literal:
            if self.e == 1:
                return self.b.to_tex()
            elif self.e == 0:
                return '1'
            else:
                return self.b.to_tex() + "^{" + str(self.e) + "}"
        return self.b.to_tex() + "^{" + self.e.to_tex() + "}"
    

class Mult:
    def __init__(self):
        self.plist = []
    
    def add(self, element):
        self.plist.append(element)
        
    def to_tex(self):
        result = ""
        first = True
        for element in self.plist:
            element_tex = element.to_tex()
            if element_tex != '1':
                if first:
                    first = False
                else:
                    result += "\\cdot "
                result += element_tex
        if result == "":
            result = '1'
        return result
    
    
    def solution(self):
        exponents = {}
        
        for element in self.plist:               
            if type(element) == Fraction or type(element) == Power:
                sol_f = element.solution()
                keys_f = sol_f.keys()
                for key in keys_f:
                    if key in exponents:
                        exponents[key] += sol_f[key]
                    else:
                        exponents[key] = sol_f[key]
                        
        return exponents
        
    
class Literal:
    def __init__(self, s):
        self.s = s
    
    def to_tex(self):
        return self.s
    
    def __str__(self):
        return self.s
    

def rand_exp():
    sign = random.randint(0,1)
    value = random.randint(1,4)
    return (-1)**sign * value

def randLiteral():
    std_literals = ['a', 'b', 'c', 'd', 'f', 'g', 'm', 'n', 'p', 'q', 'r', 's', 't', 'x', 'y', 'z']
    return Literal(std_literals[random.randint(0, len(std_literals)-1)])


def randterm():
    while True:
        literals = [randLiteral() for i in range(3)]
        if literals[0].s == literals[1].s:
            continue
        if literals[0].s == literals[2].s:
            continue
        if literals[1].s == literals[2].s:
            continue
        break
        
        
    m = Mult()
    m.add(Power(randfraction(literals), rand_exp()))
    m.add(Power(randfraction(literals), rand_exp()))
    m.add(Power(randfraction(literals), rand_exp()))
    
    return m

def randfraction(literals):
    m1 = Mult()
    m2 = Mult()
    
    
    for literal in literals:
        m1.add(Power(literal, random.randint(-7,7)))
        m2.add(Power(literal, random.randint(-7,7)))
    
    return Fraction(m1,m2)



def dict_to_tex(d):
    keys = d.keys()
    z = Mult()
    n = Mult()
    
    for key in keys:
        if d[key] > 0:
            z.add(Power(Literal(key),d[key]))
        elif d[key] < 0:
            n.add(Power(Literal(key),-d[key]))
    f = Fraction(z,n)
    return f.to_tex()
    
    
    

f = open("tasks.tex", "w")
g = open("sol.tex", "w")
for i in range(100):
    term = randterm()
    f.write("\\begin{align}\n")
    f.write(term.to_tex())
    f.write("\n\\end{align}\n")
    
    g.write("\\begin{align}\n")
    g.write(str(dict_to_tex(term.solution())))
    g.write("\n\\end{align}\n")
    
f.close()


