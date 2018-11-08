
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
    			   Symbol("putIntLn",MType([IntType()],VoidType()))]
    
    def __flatten(self,lst):
        lst = [x if isinstance(x,list) else [x] for x in lst] 
        return functools.reduce(lambda x,y : x + y , lst , [])

    def __mergeEnvironment(self,inner,outter):
        temp = []
        for x in outter:
            if self.lookup(x.name,inner,lambda x: x.name) is None:
                temp.append(x)

        return inner + temp

    def __init__(self,ast):
        self.ast = ast

    def check(self):
        return self.visit(self.ast,StaticChecker.global_envi)
    
    def visitProgram(self,ast, c):
        print("\n\n\n")
        global_envi = c.copy()
    
    
        program = reduce(lambda x,y : [self.visit(y,
                        {
                            'envi' : x,
                            'global_mode' : True
                        })] + x, 
                        ast.decl,
                        global_envi)

        print("\nglobal")
        for x in program:
            print(x.name + ' ' + str(x.mtype))

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

        res = self.lookup(id,envi,lambda x : x.name.lower())

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
            res = self.lookup(id,global_envi,lambda x : x.name.lower())

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

        
        local_envi = self.__mergeEnvironment(local_envi,c['envi'])
        
        
        if global_mode:
            return Symbol(id,mtype)

        print("\n" + id)
        for x in local_envi:
            print(x.name + ' ' + str(x.mtype))

        body = self.__flatten(list(map(lambda x: self.visit(x,{'envi' : local_envi}),ast.body)))
        
        return_list = list(filter(lambda x : type(x) is Return,body))
        
        if ast.returnType is VoidType:
            if any(x.expr is not None for x in return_list):
                raise TypeMismatchInStatement(ast)
        else:
            if any(type(x.expr) is not ast.returnType for x in return_list):
                raise TypeMismatchInStatement(ast)
    

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

        print("\nwith")
        for x in block_envi:
            print(x.name + ' ' + str(x.mtype))

        return [self.visit(x,{
                'envi' : block_envi
                                }) for x in ast.stmt]

    def visitCallStmt(self, ast, c):
        envi = c['envi']

        at = [self.visit(x,envi)for x in ast.param]
        
        res = self.lookup(ast.method.name,envi,lambda x: x.name.lower())
        
        # if res:
        #     for x in res.mtype.partype:
        #         print(x)
        if res is None or not type(res.mtype) is MType or not type(res.mtype.rettype) is VoidType:
            raise Undeclared(Procedure(),ast.method.name)
        elif len(res.mtype.partype) != len(at) or True in [type(a) != type(b) for a,b in zip(at,res.mtype.partype)]:
            #print([print(str(type(a))+ ' ' + str(type(b))) for a,b in zip(at,res.mtype.partype)])
            raise TypeMismatchInStatement(ast)            
        else:
            return res.mtype.rettype
    
    def visitCallExpr(self, ast, c):
        envi = c['envi']

        at = [self.visit(x,envi)for x in ast.param]
        
        res = self.lookup(ast.method.name,envi,lambda x: x.name.lower())

        if res is None or not type(res.mtype) is MType or type(res.mtype.rettype) is VoidType:
            raise Undeclared(Function(),ast.method.name)
        elif len(res.mtype.partype) != len(at) or True in [type(a) != type(b) for a,b in zip(at,res.mtype.partype)]:
            raise TypeMismatchInStatement(ast)   
        else:
            return res.mtype.rettype

    def visitUnaryOp(self, ast, c):

        body = self.visit(ast.body,c)

        op = ast.op
        
        if op == 'not':
            if type(body) is not BoolType :
                raise TypeMismatchInExpression(ast)

        else: # - (subtraction)
            if type(body) not in [IntType,FloatType] :
                raise TypeMismatchInExpression(ast)
        
        return body
    
    def visitArrayCell(self, ast, c):

        arr = self.visit(ast.arr,c)

        idx = self.visit(ast.idx,c)

        if(type(arr) is not ArrayType
           or type(idx) is not IntType) :
            raise TypeMismatchInExpression(ast)

        return arr.eleType

    def visitBinaryOp(self, ast, c):

        left  = self.visit(ast.left,c)

        right = self.visit(ast.right,c)
        
        op = ast.op
        
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
            if type(left) is not BoolType() or type(right) is not BoolType() :
                raise TypeMismatchInExpression(ast)
            
            return BoolType()

    def visitIf(self, ast, c):
        #expr:Expr
        #thenStmt:list(Stmt)
        #elseStmt:list(Stmt)
        envi = c['envi']

        expr = self.visit(ast.expr,envi)
        thenStmt = [self.visit(x,envi) for x in ast.thenStmt]
        elseStmt = [self.visit(x,envi) for x in ast.elseStmt]

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
        loop = [self.visit(x,envi) for x in ast.loop]

        if not isinstance(iden,IntType) or not isinstance(expr1,IntType) or not isinstance(expr2,IntType):
            raise TypeMismatchInStatement(ast)

        return loop
    
    def visitWhile(self,ast,c):

        #sl:list(Stmt)
        #exp: Expr
        envi = c['envi']

        sl = [self.visit(x,envi) for x in ast.sl]

        exp = self.visit(ast.exp,envi)

        if not isintance(exp,BoolType()):
            raise TypeMismatchInStatement(ast)

        return sl

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
    
    def visitReturn(self, ast, c):
        #expr:Expr
        envi = c['envi']

        expr = self.visit(expr,envi) if expr else None

        return Return(expr)
     
    def visitId(self, ast, c):
        res = self.lookup(ast.name,c,lambda x : x.name.lower())
        
        if res is None:
            raise Undeclared(Variable(),res.name)

        return res.mtype

    def visitIntLiteral(self,ast, c): 
        return IntType()
    
    def visitFloatLiteral(self, ast, c):
        return FloatType()
    
    def visitBooleanLiteral(self, ast, c):
        return BoolType()
    
    def visitStringLiteral(self, ast, c):
        return StringType()
    
    def visitVoidType(self, ast, c):
        return VoidType()

    def visitArrayType(self, ast, c):
        return ast
   