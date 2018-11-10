
"""
 * @author nhphung
"""
from AST import * 
from Visitor import *
from Utils import Utils
from StaticError import *
from functools import reduce
class MType:
    def __init__(self,partype,rettype):
        self.partype = partype
        self.rettype = rettype

class Symbol:
    def __init__(self,name,mtype,value = None):
        self.name = name
        self.mtype = mtype
        self.value = value

class StaticChecker(BaseVisitor,Utils):

    global_envi = [Symbol("getInt",MType([],IntType())),
    			   Symbol("putIntLn",MType([IntType()],VoidType())),
                   Symbol("putInt",MType([IntType()],VoidType())),
                   Symbol("getFloat",MType([],FloatType())),
                   Symbol("putFloat",MType([FloatType()],VoidType())),
                   Symbol("putFloatLn",MType([FloatType()],VoidType())),
                   Symbol("putBool",MType([BoolType()],VoidType())),
                   Symbol("putBoolLn",MType([BoolType()],VoidType())),
                   Symbol("putString",MType([StringType()],VoidType())),
                   Symbol("putStringLn",MType([StringType()],VoidType())),
                   Symbol("putLn",MType([],VoidType()))]
    
    def __flatten(self,lst):
        lst = [x if isinstance(x,list) else [x] for x in lst] 
        return reduce(lambda x,y : x + y , lst , [])

    def __mergeEnvironment(self,inner,outter):
        temp = []
        for x in outter:
            if self.lookup(x.name.lower(),inner,lambda x: x.name.lower()) is None:
                temp.append(x)

        return inner + temp
    
    def __checkType(self,lhs,rhs):

        if type(lhs) is not type(rhs):
            if not(type(lhs) is FloatType and not type(rhs) is IntType):
                return False

        if(type(rhs) is ArrayType):
            if (rhs.lower != lhs.lower 
                or rhs.upper != lhs.upper
                or rhs.eleType != lhs.eleType):
                return False
        
        return True

    def __init__(self,ast):
        self.ast = ast

    def check(self):
        return self.visit(self.ast,StaticChecker.global_envi)

    def visitProgram(self,ast, c):
        global_envi = c.copy()
    
        program = reduce(lambda x,y : [self.visit(y,
                        {
                            'envi' : x,
                            'global_mode' : True
                        })] + x, 
                        ast.decl,
                        global_envi)
        
        ast.decl = list(filter(lambda x : isinstance(x,FuncDecl),ast.decl))

        list(map(lambda x : self.visit(x,{
                                             'envi' : program,
                                             'global_mode' : False
                                         }),
                ast.decl))
        
        res = self.lookup("main",program,lambda x : x.name.lower()) ## lower upper case

        if (res is None 
                or not isinstance(res.mtype,MType) 
                or not isinstance(res.mtype.rettype,VoidType)):
            raise NoEntryPoint()

        return program
    
    def visitVarDecl(self,ast, c):

        envi = c['envi']
        
        # Get ID
        id = ast.variable.name

        res = self.lookup(id.lower(),envi,lambda x : x.name.lower())

        if res:
            raise Redeclared(Variable(),id)

        return Symbol(id,ast.varType)

    def visitFuncDecl(self,ast, c):

        global_envi = c['envi']

        global_mode = c['global_mode']
        
        local_envi = []
        # Check global invironment
        id = ast.name.name

        mtype  = MType([x.varType for x in ast.param],ast.returnType)
        
        if global_mode:
        # Check if have redeclares
            res = self.lookup(id.lower(),global_envi,lambda x : x.name.lower())
            if res:
                kind = Procedure() if isinstance(ast.returnType,VoidType) else Function()
                raise Redeclared(kind,id)

        try:
            local_envi = reduce(lambda x,y : [self.visit(y,
                        {
                            'envi' : x,
                        })] + x, 
                        ast.param,
                        local_envi)
        except Redeclared as e:
            raise Redeclared(Parameter(),e.n)
        
        local_envi = reduce(lambda x,y : [self.visit(y,
                        {
                            'envi' : x,
                        })] + x, 
                        ast.local,
                        local_envi)

        if global_mode:
            return Symbol(id,mtype)
        
        local_envi = self.__mergeEnvironment(local_envi,c['envi'])

        t = {
            'envi' : local_envi,
            'returnlst' : [],
            'isInLoop' : False,
            'isReturn' : False
        }


        list(map(lambda x: self.visit(x,t),ast.body))
        
        for x in t['returnlst'] :
            print(x[1])
        
        if type(ast.returnType) is VoidType:
            for x,y in t['returnlst'] :
                if y is not None:
                    raise TypeMismatchInStatement(x)
        else:
            if not t['isReturn']:
                raise FunctionNotReturn(id)
            for x,y in t['returnlst'] :
                if not self.__checkType(ast.returnType,y):
                    raise TypeMismatchInStatement(x)
                    
    
    def visitBinaryOp(self, ast, c):

        left  = self.visit(ast.left,c)

        right = self.visit(ast.right,c)
        
        op = ast.op.lower()
        
        compare_op = ['<','<=','>','>=','<>','=']

        arithmetic_op = ['+','-','*','/','div','mod']

        logic_op = ['and','or','and then','or else']

        if (op in compare_op) or (op in arithmetic_op):
            # Raise error for the left over
            if type(left) not in [IntType,FloatType] or type(right) not in [IntType,FloatType] :
                raise TypeMismatchInExpression(ast)
            
            # Return type for comparasion
            if op in compare_op:
                return BoolType()
            
            if type(left) is IntType and type(right) is IntType :
                if (op == '/'):
                    return FloatType()
                else:
                    return IntType()
            else: #One of those operands or both is floattype
                if op in ['div','mod'] :
                    raise TypeMismatchInExpression(ast)
                else:    
                    return FloatType()
        ##Logic op part
        else:
            if type(left) is not BoolType or type(right) is not BoolType :
                raise TypeMismatchInExpression(ast)
            
            return BoolType()
    
    def visitUnaryOp(self, ast, c):

        body = self.visit(ast.body,c)

        op = ast.op.lower()
        
        if op == 'not':
            if type(body) is not BoolType :
                raise TypeMismatchInExpression(ast)

        else: # - (subtraction)
            if type(body) not in [IntType,FloatType] :
                raise TypeMismatchInExpression(ast)
        
        return body
    
    def visitCallExpr(self, ast, c):
        envi = c

        at = [self.visit(x,envi)for x in ast.param]
        
        res = self.lookup(ast.method.name.lower(),envi,lambda x: x.name.lower())

        if res is None or not type(res.mtype) is MType or type(res.mtype.rettype) is VoidType:
            raise Undeclared(Function(),ast.method.name)
        elif (len(res.mtype.partype) != len(at) 
             or True in [not self.__checkType(b,a) for a,b in zip(at,res.mtype.partype)]):
            raise TypeMismatchInStatement(ast)   
        else:
            return res.mtype.rettype
    
    def visitId(self, ast, c):
        res = self.lookup(ast.name.lower(),c,lambda x : x.name.lower())
        
        if res is None:
            raise Undeclared(Identifier(),ast.name)

        return res.mtype
    
    def visitArrayCell(self, ast, c):

        arr = self.visit(ast.arr,c)

        idx = self.visit(ast.idx,c)

        if(type(arr) is not ArrayType
           or type(idx) is not IntType) :
            raise TypeMismatchInExpression(ast)

        return arr.eleType
    
    def visitAssign(self, ast, c):
        #lhs:Expr
        #exp:Expr
        envi = c['envi']
        print("\nAssign")
        lhs = self.visit(ast.lhs,envi)
        
        rhs = self.visit(ast.exp,envi)
        print(str(lhs) + " " +  str(rhs))
        ## Note:string type ????
        if type(lhs) in [ArrayType,StringType] :
            raise TypeMismatchInStatement(ast)

        if type(lhs) is not type(rhs):
            if not(type(lhs) is FloatType and type(rhs) is IntType):
                raise TypeMismatchInStatement(ast)

        return lhs
    
    def visitWith(self, ast, c):

        envi = c['envi']

        block_envi = []

        block_envi = reduce(lambda x,y : [self.visit(y,
                        {
                            'envi' : x
                        })] + x, 
                        ast.decl,
                        block_envi)

        block_envi = self.__mergeEnvironment(block_envi,envi)

        t = c.copy()

        t['envi'] = block_envi

        [self.visit(x,t) for x in ast.stmt]

        c['isReturn'] = t['isReturn']
    
    def visitIf(self, ast, c):
        #expr:Expr
        #thenStmt:list(Stmt)
        #elseStmt:list(Stmt)
        envi = c['envi']

        temp = c['isReturn']

        expr = self.visit(ast.expr,envi)
        
        c['isReturn'] = False
        thenStmt = [self.visit(x,c) for x in ast.thenStmt]
        temp1 = c['isReturn']

        c['isReturn'] = False
        elseStmt = [self.visit(x,c) for x in ast.elseStmt]
        temp2 = c['isReturn']

        
        if temp1 and temp2:
            c['isReturn'] = True
        else:
            c['isReturn'] = temp
         
        if type(expr) is not BoolType :
            raise TypeMismatchInStatement(ast)
       
        return thenStmt + elseStmt
    
    def visitFor(self, ast, c):
        #id:Id
        #expr1,expr2:Expr
        #loop:list(Stmt)
        #up:Boolean #True => increase; False => decrease
        envi = c['envi']
        
        id = self.visit(ast.id,envi)
        expr1 = self.visit(ast.expr1,envi)
        expr2 = self.visit(ast.expr2,envi)

        c['isInLoop'] = True
        loop = [self.visit(x,c) for x in ast.loop]
        c['isInLoop'] = False

        if not isinstance(id,IntType) or not isinstance(expr1,IntType) or not isinstance(expr2,IntType):
            raise TypeMismatchInStatement(ast)

        return loop
    
    def visitContinue(self, ast, c):
        if not c['isInLoop']:
            raise ContinueNotInLoop()
    
    def visitBreak(self, ast, c):
        if not c['isInLoop']:
            raise BreakNotInLoop()
    
    def visitReturn(self, ast, c):
        #expr:Expr
        envi = c['envi']

        if not c['isInLoop']:
            c['isReturn'] = True

        expr = self.visit(ast.expr,envi) if ast.expr else None
        
        c['returnlst'].append((ast,expr))
    
    def visitWhile(self,ast,c):

        #sl:list(Stmt)
        #exp: Expr
        envi = c['envi']

        exp = self.visit(ast.exp,envi)

        c['isInLoop'] = True
        sl = [self.visit(x,c) for x in ast.sl]
        c['isInLoop'] = False

        if type(exp) is not BoolType :
            raise TypeMismatchInStatement(ast)

        return sl
    
    def visitCallStmt(self, ast, c):
        envi = c['envi']

        at = [self.visit(x,envi)for x in ast.param]
        
        res = self.lookup(ast.method.name.lower(),envi,lambda x: x.name.lower())
        
        # if res:
        #     for x in res.mtype.partype:
        #         print(x)
        if res is None or not type(res.mtype) is MType or not type(res.mtype.rettype) is VoidType:
            raise Undeclared(Procedure(),ast.method.name)
        elif (len(res.mtype.partype) != len(at) 
             or True in [not self.__checkType(b,a) for a,b in zip(at,res.mtype.partype)]):
            #print([print(str(type(a))+ ' ' + str(type(b))) for a,b in zip(at,res.mtype.partype)])
            raise TypeMismatchInStatement(ast)            
        else:
            return res.mtype.rettype
    
    def visitIntLiteral(self,ast, c): 
        return IntType()
    
    def visitFloatLiteral(self, ast, c):
        return FloatType()
    
    def visitBooleanLiteral(self, ast, c):
        return BoolType()
    
    def visitStringLiteral(self, ast, c):
        return StringType()
    
    def visitIntType(self, ast, param):
        return None
    
    def visitFloatType(self, ast, param):
        return None
    
    def visitBoolType(self, ast, param):
        return None
    
    def visitStringType(self, ast, param):
        return None
    
    def visitVoidType(self, ast, param):
        return None
    
    def visitArrayType(self, ast, param):
        return None

    
    
    
    
    
    

    

    


    
    
     
    

    
   