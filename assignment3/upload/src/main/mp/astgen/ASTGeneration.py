from MPVisitor import MPVisitor
from MPParser import MPParser
from AST import *
import functools

class ASTGeneration(MPVisitor):
    
    def flatten(self,lst):
        lst = list(map(lambda x : [x] if not isinstance(x,list) else x,lst))
    
        return functools.reduce(lambda x,y: x + y,lst,[])

    def toBool(self,x):
        return x.lower() == 'true'

    # program  : decl+ EOF;
    def visitProgram(self,ctx:MPParser.ProgramContext):
        decl = self.flatten([self.visit(x) for x in ctx.decl()]) #List of decl AST
        
        return Program(decl) #Return ast prog
    
    # decl : vardecl | funcdecl | procdecl;
    def visitDecl(self,ctx:MPParser.DeclContext):
        return self.visit(ctx.getChild(0)) 

    # mptype: primtype | comptype ;
    def visitMptype(self,ctx:MPParser.MptypeContext):
        return self.visit(ctx.getChild(0))
    
    # primtype : INTEGER | BOOLEAN | REAL | STRING ;
    def visitPrimtype(self,ctx:MPParser.PrimtypeContext):
        if ctx.INTEGER():
            return IntType()

        elif ctx.BOOLEAN():
            return BoolType()
            
        elif ctx.REAL():
            return FloatType()

        elif ctx.STRING():
            return StringType()
    
    # comptype : ARRAY LSB SUBOP INTLIT DDOT SUBOP INTLIT RSB OF primtype ;
    def visitSignint(self,ctx:MPParser.SignintContext):
        signed_int = int(ctx.INTLIT().getText())
        
        if(ctx.SUBOP()):
            signed_int = -signed_int

        return signed_int

    # comptype : ARRAY LSB SUBOP INTLIT DDOT SUBOP INTLIT RSB OF primtype ;
    def visitComptype(self,ctx:MPParser.ComptypeContext):
       
        lower,upper = [self.visit(x) for x in ctx.signint()]

        eleType = self.visit(ctx.primtype())

        return ArrayType(lower,upper,eleType)
    
    # idlst : ID (COMMA ID)* ;
    # Return list of ID AST
    def visitIdlst(self,ctx:MPParser.IdlstContext):
        return [Id(x.getText()) for x in ctx.ID()] 
    
    # param : idlst COLON mptype ;
    # Return list of tuple (ID,mptype)
    def visitParam(self,ctx:MPParser.ParamContext):
        id_lst = self.visit(ctx.idlst()) # Get list of ID

        mptype = self.visit(ctx.mptype()) # Get mptype correspond to all of element in id list
        
        param = [(id,mptype) for id in id_lst] # Map all element of idlist to mptype

        return param;
    
    # vardecl : VAR paramlst SEMI;
    # return list of VarDecl
    def visitVardecl(self,ctx:MPParser.VardeclContext):

        param_lst = self.visit(ctx.paramlst()) #List of tuple (id,mptype)

        vardecl = [VarDecl(*param) for param in param_lst]

        return vardecl

    # paramlst : param (SEMI param)* ;
    # Return list of param,it's a list of tupe (id,mptype)
    def visitParamlst(self,ctx:MPParser.ParamlstContext):
        # Because one param is a list,so param_lst is list of list,we need to flatten it
        param_lst = self.flatten([self.visit(x) for x in ctx.param()])

        return param_lst
    

    # Funcdecl : FUNCTION ID LB paramlst? RB COLON mptype SEMI vardecl? compstmt ;
    def visitFuncdecl(self,ctx:MPParser.FuncdeclContext):
        name = Id(ctx.ID().getText())
        
        param_lst = []
        #Get paramlist like vardecl
        if ctx.paramlst():
            temp_lst = self.visit(ctx.paramlst())
            
            param_lst = [VarDecl(*param) for param in temp_lst]
                    
        returntype  = self.visit(ctx.mptype())

        local = self.visit(ctx.vardecl()) if ctx.vardecl() else []

        body = self.visit(ctx.compstmt())
        
        #name: Id
        #param: list(VarDecl)
        #returnType: Type => VoidType for Procedure
        #local:list(VarDecl)
        #body: list(Stmt)
        return FuncDecl(name,param_lst,local,body,returntype)
    
    # procdecl : PROCEDURE ID LB paramlst? RB SEMI vardecl? compstmt ;
    def visitProcdecl(self,ctx:MPParser.ProcdeclContext):
        name = Id(ctx.ID().getText())
        
        param_lst = []
        if ctx.paramlst():
            temp_lst = self.visit(ctx.paramlst())

            param_lst = [VarDecl(*param) for param in temp_lst]

        local = self.visit(ctx.vardecl()) if ctx.vardecl() else []

        body = self.visit(ctx.compstmt())
        
        #name: Id
        #param: list(VarDecl)
        #returnType: Type => VoidType for Procedure
        #local:list(VarDecl)
        #body: list(Stmt)
        return FuncDecl(name,param_lst,local,body)
    
    # exp : exp (ANDOP THEN| OROP ELSE) exp1 | exp1;
    def visitExp(self,ctx:MPParser.ExpContext):
        if ctx.getChildCount() == 1 :
            return self.visit(ctx.exp1())
        else:
            if ctx.ANDOP() :
                op = "andthen"
            else:
                op = "orelse"
            
            return BinaryOp(op,self.visit(ctx.exp()),self.visit(ctx.exp1()))
            
    # exp1: exp2 (EQOP|NEOP|LTOP|LEOP|GTOP|GEOP) exp2 | exp2;
    def visitExp1(self,ctx:MPParser.Exp1Context):
        if ctx.getChildCount() == 1 :
            return self.visit(ctx.exp2(0))
        else:
            op = ctx.getChild(1).getText()

            return BinaryOp(op,self.visit(ctx.exp2(0)),self.visit(ctx.exp2(1)))

    # exp2: exp2 (ADDOP|SUBOP|OROP) exp3 | exp3;
    def visitExp2(self,ctx:MPParser.Exp2Context):
        if ctx.getChildCount() == 1 :
            return self.visit(ctx.exp3())
        else:
            op = ctx.getChild(1).getText()

            return BinaryOp(op,self.visit(ctx.exp2()),self.visit(ctx.exp3()))

    # exp3: exp3 (DIVOP|MULOP|MODOP|ANDOP|DIVIDEOP) exp4 | exp4;
    def visitExp3(self,ctx:MPParser.Exp3Context):
        if ctx.getChildCount() == 1 :
            return self.visit(ctx.exp4())
        else:
            op = ctx.getChild(1).getText()

            return BinaryOp(op,self.visit(ctx.exp3()),self.visit(ctx.exp4()))

    # exp4: <assoc = right> (SUBOP | NOTOP) exp4 | exp5;
    def visitExp4(self,ctx:MPParser.Exp4Context):
        if ctx.getChildCount() == 1 :
            return self.visit(ctx.exp5())
        else:
            op = ctx.getChild(0).getText()

            return UnaryOp(op,self.visit(ctx.exp4()))

    # exp5: LB exp RB | ID | INTLIT | BOOLIT | REALIT | STRINGLIT | invocastmt | idxexp ;
    def visitExp5(self,ctx:MPParser.Exp5Context):
        if ctx.getChildCount() == 1 : #Term,callstmt,index exp
            if ctx.ID():
                return Id(ctx.ID().getText())
                
            elif ctx.INTLIT():
                return IntLiteral(int(ctx.INTLIT().getText()))

            elif ctx.BOOLIT():
                return BooleanLiteral(self.toBool(ctx.BOOLIT().getText()))

            elif ctx.REALIT():
                return FloatLiteral(float(ctx.REALIT().getText()))

            elif ctx.STRINGLIT():
                return StringLiteral(ctx.STRINGLIT().getText())

            elif ctx.invocastmt():
                return self.visit(ctx.invocastmt())

            elif ctx.idxexp():
                return self.visit(ctx.idxexp())

        else: #LB exp RB
                return self.visit(ctx.exp())

 
    # arglst : exp (COMMA exp)* ;
    # return list of exp
    def visitArglst(self,ctx:MPParser.ArglstContext):
        return [self.visit(x) for x in ctx.exp()]
    
    # invocastmt : ID LB arglst? RB ; 
    def visitInvocastmt(self,ctx:MPParser.InvocastmtContext):
        id = Id(ctx.ID().getText())
        exp_lst = self.visit(ctx.arglst()) if ctx.arglst() else []

        return CallExpr(id,exp_lst)
    
    # idxexp: (ID | invocastmt) LSB exp RSB ;
    def visitIdxexp(self,ctx:MPParser.IdxexpContext):
        if ctx.ID():
            exp1 = Id(ctx.ID().getText())
        else:
            exp1 = self.visit(ctx.invocastmt())

        return ArrayCell(exp1,self.visit(ctx.exp()))
    
    # stmt 
    # : assignstmt 
    # | ifstmt 
    # | whilestmt 
    # | forstmt 
    # | breakstmt 
    # | continuestmt
    # | returnstmt
    # | compstmt
    # | withstmt
    # | callstmt 
    # ;
    # Because assignstmt and compstmt return a list,if we cast list,we might flatten that
    def visitStmt(self,ctx:MPParser.StmtContext):
        return self.flatten([self.visit(ctx.getChild(0))])
    
    # stmtlst : stmt+;
    # flatten because ctx.stmt() is a list,and each element of those return a list,so we got list of list when call visit stmt()
    def visitStmtlst(self,ctx:MPParser.StmtlstContext):
        return self.flatten([self.visit(x) for x in ctx.stmt()])
    
    # scavar : idxexp | ID ;
    def visitScavar(self,ctx:MPParser.ScavarContext):
        if ctx.ID():
            return Id(ctx.ID().getText())
        else:
            return self.visit(ctx.idxexp())  
    
    # assignstmt : (scavar ASSIGN)+ exp SEMI ;
    def visitAssignstmt(self,ctx:MPParser.AssignstmtContext):
        scavar_lst = [self.visit(x) for x in ctx.scavar()]
        
        scavar_lst.append(self.visit(ctx.exp()))

        scavar_lst = list(zip(scavar_lst,scavar_lst[1:]))
        
        assigstmt_lst = [Assign(*x) for x in scavar_lst]

        assigstmt_lst.reverse()

        return assigstmt_lst
    
    # callstmt : ID LB arglst? RB SEMI; 
    def visitCallstmt(self,ctx:MPParser.CallstmtContext):
        id = Id(ctx.ID().getText())

        arg_lst = self.visit(ctx.arglst()) if ctx.arglst() else []

        return CallStmt(id,arg_lst)
    
    # ifstmt : IF exp THEN stmt (ELSE stmt)? ;
    def visitIfstmt(self,ctx:MPParser.IfstmtContext):
        exp = self.visit(ctx.exp())

        thenStmt = self.visit(ctx.stmt(0))

        elseStmt = self.visit(ctx.stmt(1)) if ctx.stmt(1) else []
    
        return If(exp,thenStmt,elseStmt)
    
    # whilestmt : WHILE exp DO stmt ;
    def visitWhilestmt(self,ctx:MPParser.WhilestmtContext):
        exp = self.visit(ctx.exp())

        stmt = self.visit(ctx.stmt())

        return While(exp,stmt)
    
    # forstmt : FOR ID ASSIGN exp (TO|DOWNTO) exp DO stmt ; 
    def visitForstmt(self,ctx:MPParser.ForstmtContext):
        id = Id(ctx.ID().getText())

        exp1,exp2 = [self.visit(x) for x in ctx.exp()]

        up = True if ctx.TO() else False

        loop = self.visit(ctx.stmt())
        
        return For(id, exp1, exp2, up, loop)
    
    # breakstmt : BREAK SEMI ;
    def visitBreakstmt(self,ctx:MPParser.BreakstmtContext):
        return Break()

    # continuestmt : CONTINUE SEMI ;
    def visitContinuestmt(self,ctx:MPParser.ContinuestmtContext):
        return Continue()
    
    #returnstmt : RETURN exp? SEMI ;
    def visitReturnstmt(self,ctx:MPParser.ReturnstmtContext):

        exp = self.visit(ctx.exp()) if ctx.exp() else None
        
        return Return(exp)
    
    # compstmt : BEGIN stmtlst? END ;
    def visitCompstmt(self,ctx:MPParser.CompstmtContext):
        return self.visit(ctx.stmtlst()) if ctx.stmtlst() else []
    
    # withstmt : WITH paramlst SEMI DO stmtlst ;
    def visitWithstmt(self,ctx:MPParser.WithstmtContext):
        stmt = self.visit(ctx.stmt())
        
        param_lst = self.visit(ctx.paramlst())

        vardecl = [VarDecl(*param) for param in param_lst]

        return With(vardecl,stmt)