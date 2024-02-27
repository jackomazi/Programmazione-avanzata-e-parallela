# ANDREA GIACOMAZZI SM3201257

import numpy as np

class EmptyStackException(Exception):
    pass


class Stack:

    def __init__(self):
        self.data = []

    def push(self, x):
        self.data.append(x)

    def pop(self):
        if self.data == []:
            raise EmptyStackException
        res = self.data[-1]
        self.data = self.data[0:-1]
        return res

    def __str__(self):
        return " ".join([str(s) for s in self.data])

class Expression:

    def __init__(self):
        raise NotImplementedError()

    # Metodo che costruisce un'espressione a partire da una stringa, utilizzando la stack
    # se il token è un'operazione estrae gli argomenti dalla stack pari al numero arity 
    # e inserisce il risultato
    # se il token è un numero inserisce un oggetto di tipo costante
    # se il token è una variabile inserisce una variabile
    @classmethod
    def from_program(cls, text, dispatch):
        s = Stack()
        for token in text.split():
            if token in dispatch:
                op = dispatch[token]
                args = [s.pop() for _ in range(op.arity)]
                s.push(op(args))
            elif token.isdigit():

                s.push(Constant(token))
            else:
                s.push(Variable(token))
        
        return s.pop()

    def evaluate(self, env):
        raise NotImplementedError()


class MissingVariableException(Exception):
    pass

class Variable(Expression):
    def __init__(self, name):
        self.name = name

    def evaluate(self, env):
        if self.name not in env:
            raise MissingVariableException
        return env[self.name] 
    def __str__(self):
        return self.name


class Constant(Expression):

    def __init__(self, value):
        self.value = value

    def evaluate(self, env):
        return int(self.value)

    def __str__(self):
        return self.value


class Operation(Expression):

    def __init__(self, args):
        self.args = args

    # Metodo che valuta l'operazione passando come argomenti l'ambiente e gli argomenti dell'operazione
    # saranno poi le specifiche operazioni a valutare gli argomenti e restituire il risultato
    def evaluate(self, env):
        return self.op(env, self.args)
    
    def op(self, *args):
        raise NotImplementedError()

    def __str__(self):
        pass

class ZeryOp(Operation):
    arity = 0
class UnaryOp(Operation):
    arity = 1
class BinaryOp(Operation):
    arity = 2
class TernaryOp(Operation):
    arity = 3
class QuaternaryOp(Operation):
    arity = 4

class NotACostantException(Exception):
    pass


# Specifiche operazioni
# ogni operazione riceve come argomenti l'ambiente e gli argomenti, valuta gli argomenti così che:
#  -se sono variabili le valuta e gli attribuisce il valore corrispondente
#  -se sono costanti le valuta e restituisce il valore stesso
#  -se sono operazioni le valuta e restituisce il risultato dell'operazione
# in questo modo è possibile passare come argomenti sia costanti che variabili che operazioni

class Addition(BinaryOp):
    def op(self, env, args):
        x, y = args
        x = x.evaluate(env)
        y = y.evaluate(env)

        # Se dopo la valutazine x e y non sono costanti, solleva un'eccezione
        try:
            int(x)
            int(y)
        except:
            raise NotACostantException
        return x + y
    
    def __str__(self):
        return "(+ {} {})".format(self.args[0], self.args[1])
    
class Subtraction(BinaryOp):
    def op(self, env, args):
        x, y = args
        x = x.evaluate(env)
        y = y.evaluate(env)

        # Se dopo la valutazine x e y non sono costanti, solleva un'eccezione
        try:
            int(x)
            int(y)
        except:
            raise NotACostantException
        return x - y
    def __str__(self):
        return "(- {} {})".format(self.args[0], self.args[1])
    
class Division(BinaryOp):
    def op(self, env, args):
        x, y = args
        x = x.evaluate(env)
        y = y.evaluate(env)

        # Se dopo la valutazine x e y non sono costanti, solleva un'eccezione
        try:
            int(x)
            int(y)
        except:
            raise NotACostantException
        return x / y
    def __str__(self):
        return "(/ {} {})".format(self.args[0], self.args[1])

class Multiplication(BinaryOp):
    def op(self, env, args):
        x, y = args
        x = x.evaluate(env)
        y = y.evaluate(env)

        # Se dopo la valutazine x e y non sono costanti, solleva un'eccezione
        try:
            int(x)
            int(y)
        except:
            raise NotACostantException
        return x * y
    def __str__(self):
        return "(* {} {})".format(self.args[0], self.args[1])

class Power(BinaryOp):
    def op(self,env, args):
        x, y = args
        x = x.evaluate(env)
        y = y.evaluate(env)

        # Se dopo la valutazine x e y non sono costanti, solleva un'eccezione
        try:
            int(x)
            int(y)
        except:
            raise NotACostantException
        return x ** y
    def __str__(self):
        return "(** {} {})".format(self.args[0], self.args[1])

class Modulus(BinaryOp):
    def op(self, env, args):
        x, y = args
        x = x.evaluate(env)
        y = y.evaluate(env)

        # Se dopo la valutazine x e y non sono costanti, solleva un'eccezione
        try:
            int(x)
            int(y)
        except:
            raise NotACostantException
        return x % y
    def __str__(self):
        return "(% {} {})".format(self.args[0], self.args[1])

class Reciprocal(UnaryOp):
    def op(self, env, args):
        x = args[0]
        x = x.evaluate(env)

        # Se dopo la valutazine x non è una costante, solleva un'eccezione
        try:
            int(x)
        except:
            raise NotACostantException
        return 1 / x
    
    def __str__(self):
        return "(1/ {})".format(self.args[0])

class AbsoluteValue(UnaryOp):
    def op(self, env, args):
        x = args[0]
        x = x.evaluate(env)

        try:
            int(x)
        except:
            raise NotACostantException
        return abs(x)
    def __str__(self):
        return "(abs {})".format(self.args[0])

class NotAVariableException(Exception):
    pass

class Alloc(UnaryOp):
    def op(self,env, args):
        var = args[0]

        # var deve essere una variabile, altrimenti solleva un'eccezione
        if type(var) != Variable:
            raise NotAVariableException
        env[str(var)] = 0
        return env
    
    def __str__(self):
        return ("(alloc {})".format(self.args[0]))


class VAlloc(BinaryOp):
    def op(self, env, args):
        var,n  = args

        if type(var) != Variable:
            raise NotAVariableException
        if type(n) != Constant:
            raise NotAVariableException
        z = np.zeros(int(str(n))) # crea un array di zeri di dimensione y e lo aggiunge all'ambiente, con chiave var
        env[str(var)] = z
        return env

    def __str__(self):
        return ("(valloc {} {})".format(self.args[0], self.args[1]))

class SetQ(BinaryOp):
    def op(self, env, args):
        x,expr = args
        if type(x) != Variable:
            raise NotAVariableException
        env[str(x)] = expr.evaluate(env)
        return env
    
    def __str__(self):
        return ("(setq {} {})".format(self.args[0], self.args[1]))

class SetV(TernaryOp):
    def op(self, env, args):
        x, n, expr = args
        if type(x) != Variable:
            raise NotAVariableException
        env[str(x)][int(n.evaluate(env))] = expr.evaluate(env) # assegna a x[n] il valore di expr 
        return env
    
    def __str__(self):
        return ("(setv {} {} {})".format(self.args[0], self.args[1], self.args[2]))       

class Prog2(BinaryOp):
    def op(self, env, args):
        expr2, expr1 = args
        expr2.evaluate(env) # valuta expr2 e ritorna il risultato di expr1
        return expr1.evaluate(env)
    
    def __str__(self):
        return ("(prog2 {} {})".format(self.args[0], self.args[1]))

class Prog3(TernaryOp):
    def op(self, env, args):
        expr3, expr2, expr1 = args
        expr3.evaluate(env) # valuta expr3, poi expr2 e infine expr1
        expr2.evaluate(env)
        return expr1.evaluate(env)
    def __str__(self):
        return ("(prog3 {} {} {})".format(self.args[0], self.args[1], self.args[2]))

class Prog4(QuaternaryOp):
    def op(self, env, args):
        expr4, expr3, expr2, expr1 = args
        expr4.evaluate(env) # valuta expr4, poi expr3, poi expr2 e infine expr1
        expr3.evaluate(env)
        expr2.evaluate(env)
        return expr1.evaluate(env)
    def __str__(self):
        return ("(prog4 {} {} {} {})".format(self.args[0], self.args[1], self.args[2], self.args[3]))

class GreaterThan(BinaryOp):
    def op(self, env, args):
        x, y = args
        x = x.evaluate(env)
        y = y.evaluate(env)
        try:
            int(x)
            int(y)
        except:
            raise NotACostantException
        return x > y
    def __str__(self):
        return "(> {} {})".format(self.args[0], self.args[1])

class LessThan(BinaryOp):
    def op(self, env,args):
        x, y = args
        x = x.evaluate(env)
        y = y.evaluate(env)
        try:
            int(x)
            int(y)
        except:
            raise NotACostantException
        return x < y
    def __str__(self):
        return "(< {} {})".format(self.args[0], self.args[1])

class GreaterOrEqualThan(BinaryOp):
    def op(self, env,args):
        x, y = args
        x = x.evaluate(env)
        y = y.evaluate(env)
        try:
            int(x)
            int(y)
        except:
            raise NotACostantException

        return x >= y
    def __str__(self):
        return "(>= {} {})".format(self.args[0], self.args[1])

class LessOrEqualThan(BinaryOp):
    def op(self,env, args):
        x, y = args
        x = x.evaluate(env)
        y = y.evaluate(env)
        try:
            int(x)
            int(y)
        except:
            raise NotACostantException
        return x <= y
    def __str__(self):
        return "(<= {} {})".format(self.args[0], self.args[1])

class equal(BinaryOp):
    def op(self,env, args):
        x, y = args
        x = x.evaluate(env)
        y = y.evaluate(env)
        try:
            int(x)
            int(y)
        except:
            raise NotACostantException
        return x == y
    def __str__(self):
        return "(== {} {})".format(str(self.args[0]), str(self.args[1]))

class different(BinaryOp):
    def op(self,env, args):
        x, y = args
        x = x.evaluate(env)
        y = y.evaluate(env)
        try:
            int(x)
            int(y)
        except:
            raise NotACostantException
        return x != y
    def __str__(self):
        return "(!= {} {})".format(str(self.args[0]), str(self.args[1]))

class If(TernaryOp):
    def op(self,env, args):
        cond, yes, no = args
        if cond.evaluate(env): # valuta cond, se è vera valuta yes, altrimenti valuta no
            return yes.evaluate(env)
        else:
            return no.evaluate(env)
    def __str__(self):
        return "(if {} {} else {})".format(str(self.args[0]), str(self.args[1]), str(self.args[2]))
    
class While(BinaryOp):
    def op(self, env, args):
        cond, expr = args
        while cond.evaluate(env): # valuta cond, finchè è vera valuta expr
            expr.evaluate(env)
    def __str__(self):
        return "(while {} {})".format(str(self.args[0]), str(self.args[1]))

class For(QuaternaryOp):
    def op(self,env, args):
        i, start, end, expr = args
        end = end.evaluate(env) # valuta end e start
        start = start.evaluate(env)
        for k in range(start, end, 1): 
            # per ogni valore di k tra start e end, assenga a i il valore di k nell'ambiente e poi, valuta expr con l'ambiente aggiornato
            env[str(i)] = k
            expr.evaluate(env)
    def __str__(self):
        return "(for {} {} {} {})".format(str(self.args[0]), str(self.args[1]), str(self.args[2]), str(self.args[3]))

class defsub(BinaryOp):
    def op(self, env, args):
        f, expr = args
        if type(f) != Variable:
            raise NotAVariableException
        env[str(f)] = expr # assegna a f il valore di expr e lo aggiunge all'ambiente
        return env
    def __str__(self):
        return "(defsub {} {})".format(str(self.args[0]), str(self.args[1]))

class Call(UnaryOp):
    def op(self, env, args):
        f = args[0]
        if type(f) != Variable:
            raise NotAVariableException
        function = env[str(f)] # cerca f nell'ambiente e valuta la funzione
        function.evaluate(env) # valuta 

    def __str__(self):
        return "(call {})".format(str(self.args[0]))

class Print(UnaryOp):
    def op(self, env, args):
        x = args[0]
        print(x.evaluate(env)) # valuta x e stampa il risultato
    def __str__(self):
        return "(print {})".format(str(self.args[0]))
    
class Nop(ZeryOp):
    def op(self, env, args):
        pass
    def __str__(self):
        return "(nop)"

d = {"+": Addition, "*": Multiplication, "**": Power, "-": Subtraction,
     "/": Division, "%": Modulus, "1/": Reciprocal, "abs": AbsoluteValue, "alloc": Alloc, "valloc": VAlloc, 'setq': SetQ, 'setv': SetV,
     'prog2': Prog2, 'prog3': Prog3, 'prog4': Prog4, '>': GreaterThan, '<': LessThan, '>=': GreaterOrEqualThan,
     '<=': LessOrEqualThan, '=': equal, '!=': different, 'if': If, 'while': While,
     'for': For, 'defsub': defsub, 'call': Call, 'print': Print,'nop': Nop}

#example = "2 3 + x * 6 5 - / abs 2 ** y 1/ + 1/"
#e = Expression.from_program(example, d)
#print(type(e))
#print(e)
#res = e.evaluate({"x": 3, "y": 7})
#print(res)
#
## Ouput atteso:
## (1/ (+ (1/ y) (** 2 (abs (/ (- 5 6) (* x (+ 3 2)))))))
## 0.84022932953024
#
## array of 10 elements
#
#example1 = "x 1 + x setq x 10 > while x alloc prog2"
#example2 = "v print i i * i v setv prog2 10 0 i for 10 v valloc prog2"
#example3 = "x print f call x alloc x 4 + x setq f defsub prog4"
#example4 = "nop i print i x % 0 = if 1000 1 i for 783 x setq x alloc prog3"
#example5 = "nop x print prime if nop 0 0 != prime setq i x % 0 = if 1 x - 2 i for 0 0 = prime setq prime alloc prog4 100 2 x for"
#example6 = "v print i j * 1 i - 10 * 1 j - + v setv 11 1 j for 11 1 i for 100 v valloc prog3"
#example7 = "x print 1 3 x * + x setq 2 x / x setq 2 x % 0 = if prog2 1 x != while 50 x setq x alloc prog3"
#example8 = "1 print 10 1 i for"
#ex = [example1, example2, example3, example4, example5, example6, example7]
#for i in ex:
#    print("--------------------")
#    e = Expression.from_program(i, d)
#    print(e)
#    print("--------------------")
#    res = e.evaluate({})
#    res
#    #print(res)
#    print("--------------------")