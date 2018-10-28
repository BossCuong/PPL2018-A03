
"""
 * @author nhphung
"""
from AST import * 
from Visitor import *
from Utils import Utils
from StaticError import *

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

    def __mergeEnvironment(self,inner,outter):
        for x in outter:
            if self.lookup(x.name,inner,lambda x: x.name) is None:
                inner.append(x)

    def __init__(self,ast):
        self.ast = ast

    def check(self):
        return self.visit(self.ast,StaticChecker.global_envi)
    
    def visitProgram(self,ast, c):
        print("new program")
        global_envi = c.copy()

        return [self.visit(x,global_envi) for x in ast.decl]

    def visitVarDecl(self,ast, c):
        # Get ID
        id = self.visit(ast.variable,c)
        
        # Check if have redeclares in environment c
        res = self.lookup(id,c,lambda x: x.name)

        if res: 
            raise Redeclared(Variable(),res.name)
        
        # Add var declare to environment c
        c.append(Symbol(id,ast.varType))

        return c[-1]

    def visitFuncDecl(self,ast, c):

        # Check global invironment
        id = self.visit(ast.name,c)

        # Function have all outter enviroments and its enviroment
        local_envi = []
        
        # Check if have redeclares in its own environment
        res = self.lookup(id,c,lambda x: x.name)
        
        if res:
            raise Redeclared(Function(),res.name)

        paramlst = [self.visit(x,local_envi) for x in ast.param]
        
        locallst = [self.visit(x,local_envi) for x in ast.local]
        
        mtype  = MType(paramlst,ast.returnType)

        func_symbol = Symbol(id,mtype)
        
        # Add symbol to it's own enviroment and outter environemnt
        local_envi.append(func_symbol)
        
        c.append(func_symbol)
        

        # Get block environment,its a merge of outter and its own local,apply most closed nested rule
        block_envi = local_envi.copy()

        self.__mergeEnvironment(block_envi,c)

        for x in block_envi:
            print(x.name + ' ' + str(x.mtype))

        list(map(lambda x: self.visit(x,block_envi),ast.body)) 

        return local_envi[-1]
    

    def visitWith(self, ast, c):
        block_envi = []

        decl = [self.visit(x,block_envi) for x in ast.decl]

        self.__mergeEnvironment(block_envi,c)

        print("with")
        for x in block_envi:
            print(x.name + ' ' + str(x.mtype))

        stmt = [self.visit(x,block_envi) for x in ast.stmt]

    def visitCallStmt(self, ast, c): 
        # at = [self.visit(x,c) for x in ast.param]
        
        # res = self.lookup(ast.method.name,c,lambda x: x.name)

        # if res is None or not type(res.mtype) is MType or not type(res.mtype.rettype) is VoidType:
        #     raise Undeclared(Procedure(),ast.method.name)
        # elif len(res.mtype.partype) != len(at):
        #     raise TypeMismatchInStatement(ast)            
        # else:
        #     return res.mtype.rettype

        return None
    

    def visitId(self, ast, param):
        return ast.name

    def visitIntLiteral(self,ast, c): 
        return IntType()
    
    def visitFloatLiteral(self, ast, c):
        return FloatType()
    
    def visitBooleanLiteral(self, ast, c):
        return BoolType()
    
    def visitStringLiteral(self, ast, c):
        return StringType()
