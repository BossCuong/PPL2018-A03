import unittest
from TestUtils import TestChecker
from AST import *

class CheckerSuite(unittest.TestCase):
    # def test_undeclared_function(self):
    #     """Simple program: int main() {} """
    #     input = """procedure main(); begin foo();end"""
    #     expect = "Undeclared Procedure: foo"
    #     self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_redeclare1(self):
        """Simple program: int main() {} """
        input = """
                   procedure main(); begin end 
                   procedure foo(); begin end
                   procedure PutLn(); begin end"""
        expect = "Redeclared Procedure: PutLn"
        self.assertTrue(TestChecker.test(input,expect,400))

    def test_redeclare2(self):
        """Simple program: int main() {} """
        input = """
                   procedure main(); begin end 
                   var main:integer;"""
        expect = "Redeclared Variable: main"
        self.assertTrue(TestChecker.test(input,expect,401))


    def test_redeclare3(self):
        """Simple program: int main() {} """
        input = """
                   procedure main(); begin end 
                   function main():integer; begin end """
        expect = "Redeclared Function: main"
        self.assertTrue(TestChecker.test(input,expect,402))

    
    def test_redeclare4(self):
        """Simple program: int main() {} """
        input = """
                   var foo:integer;
                   procedure main(); begin end 
                   function foo():integer; begin end """
        expect = "Redeclared Function: foo"
        self.assertTrue(TestChecker.test(input,expect,403))


    def test_redeclare5(self):
        """Simple program: int main() {} """
        input = """
                   function foo(a:integer;a:integer):real; begin end 
                   procedure main(); begin end"""
        expect = "Redeclared Parameter: a"
        self.assertTrue(TestChecker.test(input,expect,404))

    def test_redeclare6(self):
        """Simple program: int main() {} """
        input = """procedure main();
                   var a,a:integer;
                   begin end """
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input,expect,405))

    def test_redeclare7(self):
        """Simple program: int main() {} """
        input = """procedure main(a:string);
                   var a:integer;
                   begin end """
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input,expect,406))

    def test_redeclare8(self):
        """Simple program: int main() {} """
        input = """var d:string;c:real;e:boolean;
                   function foo():integer; begin return integer; end
                   procedure k(a:integer;b:real); begin end
                   procedure main(f:string);
                   var a,b:integer;
                   begin
                   with
                       a:string;
                       a:real;
                       f:integer;
                   do
                       begin 
                       with
                           a:string;
                           b:string;
                           f:string;
                           l:integer;
                           c:ARRAY [1 .. 2] OF integeR;
                       do
                           begin end
                       end
                   end """
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input,expect,407))

    def test_redeclare9(self):
        """Simple program: int main() {} """
        input = """var d:string;c:real;e:boolean;
                   function foo():integer; begin end
                   procedure k(a:integer;b:real); begin end
                   procedure main(f:string);
                   var a,b:integer;
                   begin
                   with
                       a:string;
                       b:real;
                       f:integer;
                   do
                       begin 
                       with
                           a:string;
                           b:string;
                           b:string;
                           l:integer;
                           c:ARRAY [1 .. 2] OF integeR;
                       do
                           begin end
                       end
                   end """
        expect = "Redeclared Variable: b"
        self.assertTrue(TestChecker.test(input,expect,408))


    def test_undeclare1(self):
        """Simple program: int main() {} """
        input = """procedure main();
                   var a,b:integer;
                   begin
                       k(); 
                   end """
        expect = "Undeclared Procedure: k"
        self.assertTrue(TestChecker.test(input,expect,409))

    def test_undeclare2(self):
        """Simple program: int main() {} """
        input = """var k : integer;
                   procedure main();
                   var a,b:integer;
                   begin
                       k(); 
                   end """
        expect = "Undeclared Procedure: k"
        self.assertTrue(TestChecker.test(input,expect,410))

    def test_undeclare3(self):
        """Simple program: int main() {} """
        input = """function k() : integer; begin end
                   procedure main();
                   var a,b:integer;
                   begin
                       k(); 
                   end """
        expect = "Undeclared Procedure: k"
        self.assertTrue(TestChecker.test(input,expect,411))

    def test_undeclare4(self):
        """Simple program: int main() {} """
        input = """
                   procedure main();
                   var k,b:integer;
                   begin
                       k(); 
                   end """
        expect = "Undeclared Procedure: k"
        self.assertTrue(TestChecker.test(input,expect,412))

    def test_undeclare5(self):
        """Simple program: int main() {} """
        input = """function k() : integer; begin return k(); end
                   procedure main();
                   var a,b:integer;
                   begin
                       x();
                   end """
        expect = "Undeclared Procedure: x"
        self.assertTrue(TestChecker.test(input,expect,413))

    def test_undeclare6(self):
        """Simple program: int main() {} """
        input = """procedure K(); begin end
                   procedure main();
                   var a,b:integer;
                   begin
                       a := k();
                   end """
        expect = "Undeclared Function: k"
        self.assertTrue(TestChecker.test(input,expect,414))

    def test_undeclare7(self):
        """Simple program: int main() {} """
        input = """procedure K(); begin end
                   procedure main();
                   var a,b:integer;
                   begin
                       if k() then begin end
                   end """
        expect = "Undeclared Function: k"
        self.assertTrue(TestChecker.test(input,expect,415))

    def test_undeclare8(self):
        """Simple program: int main() {} """
        input = """procedure K(); begin end
                   procedure main();
                   var a,b:integer;
                   begin
                       if l then begin end
                   end """
        expect = "Undeclared Identifier: l"
        self.assertTrue(TestChecker.test(input,expect,416))


    def test_undeclare9(self):
        """Simple program: int main() {} """
        input = """function x():integer; begin return x();; end
                   function y():integer; begin  return x();end
                   function z():integer; begin return x(); end
                   procedure main();
                   var a,b,c,d,e,f,g,h:integer;
                   begin
                       a := (a+b)/(c*d)*(x()*y()) + (y()/z())+(l div b * c);
                   end """
        expect = "Undeclared Identifier: l"
        self.assertTrue(TestChecker.test(input,expect,417))

    def test_typeStmt1(self):
        """Simple program: int main() {} """
        input = """var x,y : real;
                   procedure main(c : boolean; k :string);
                   var a,b:integer;
                   begin
                       if k then begin end
                   end """
        expect = "Type Mismatch In Statement: If(Id(k),[],[])"
        self.assertTrue(TestChecker.test(input,expect,418))

    def test_typeStmt2(self):
        """Simple program: int main() {} """
        input = """var x,y : real;
                   procedure main(c : boolean; k :string);
                   var a,b:integer;
                   begin
                       if (x + y) / (a * b) then begin end
                   end """
        expect = "Type Mismatch In Statement: If(BinaryOp(/,BinaryOp(+,Id(x),Id(y)),BinaryOp(*,Id(a),Id(b))),[],[])"
        self.assertTrue(TestChecker.test(input,expect,419))

    def test_typeStmt3(self):
        """Simple program: int main() {} """
        input = """var x,y : real;
                   procedure main(c : boolean; k :string);
                   var a,b:integer;
                   begin
                       if (a >= b) and c then 
                           for x := a to b do begin end
                   end """
        expect = "Type Mismatch In Statement: For(Id(x)Id(a),Id(b),True,[])"
        self.assertTrue(TestChecker.test(input,expect,420))

    def test_typeStmt4(self):
        """Simple program: int main() {} """
        input = """var x,y : real;
                   procedure main(c : boolean; k :string);
                   var a,b:integer;
                   begin
                       if c and c begin end
                       with
                           c : integer;
                       do
                           if c then begin end
                   end """
        expect = "Type Mismatch In Statement: If(Id(c),[],[])"
        self.assertTrue(TestChecker.test(input,expect,421))


    def test_typeStmt5(self):
        """Simple program: int main() {} """
        input = """var x,y : real;
                   procedure main(c : boolean; k :string);
                   var a,b:integer;
                   begin
                       if (a >= b) and c then 
                           for a := a + b to (a * b) * (b+a div a) do
                               for a := a + b to (a * b) / (b+a div a) do begin end
                   end """
        expect = "Type Mismatch In Statement: For(Id(a)BinaryOp(+,Id(a),Id(b)),BinaryOp(/,BinaryOp(*,Id(a),Id(b)),BinaryOp(+,Id(b),BinaryOp(div,Id(a),Id(a)))),True,[])"
        self.assertTrue(TestChecker.test(input,expect,422))


    def test_typeStmt6(self):
        """Simple program: int main() {} """
        input = """var x,y : real;
                   procedure main(c : boolean; k :string);
                   var a,b:integer;
                   begin
                       if (a >= b) and c then 
                           for a := a + b to (a * b) * (b+a div a) do begin
                               for a := a / b to (a * b) * (b+a div a) do begin end 
                            end
                   end """
        expect = "Type Mismatch In Statement: For(Id(a)BinaryOp(/,Id(a),Id(b)),BinaryOp(*,BinaryOp(*,Id(a),Id(b)),BinaryOp(+,Id(b),BinaryOp(div,Id(a),Id(a)))),True,[])"
        self.assertTrue(TestChecker.test(input,expect,423))

    def test_typeStmt7(self):
        """Simple program: int main() {} """
        input = """var x,y : real;
                   procedure main(c : boolean; k :string);
                   var a,b,e:integer;
                   for e := 2 * b to (a * b) * (b+a div a) do begin end
                   begin
                       with
                       e :real;
                       do
                           begin
                               if (a >= b) and c then begin end
                               for a := a + b to (a * b) * (b+a div a) do begin end
                               for e := a + b to (a * b) * (b+a div a) do begin end
                        end
                   end """
        expect = "Type Mismatch In Statement: For(Id(e)BinaryOp(+,Id(a),Id(b)),BinaryOp(*,BinaryOp(*,Id(a),Id(b)),BinaryOp(+,Id(b),BinaryOp(div,Id(a),Id(a)))),True,[])"
        self.assertTrue(TestChecker.test(input,expect,424))

    def test_typeStmt8(self):
        """Simple program: int main() {} """
        input = """var x,y : real;
                   procedure main(c : boolean; k :string);
                   var a,b,e:integer;
                   for e := 2 * b to (a * b) * (b+a div a) do begin end
                   begin
                       with
                       e :real;
                       do
                           begin
                               while a + b do begin end
                        end
                   end """
        expect = "Type Mismatch In Statement: While(BinaryOp(+,Id(a),Id(b)),[])"
        self.assertTrue(TestChecker.test(input,expect,425))


    def test_typeStmt9(self):
        """Simple program: int main() {} """
        input = """var x, y : array[1 .. 3] of integer;
            a, b: integer;
            c, d: real;
            e, f: boolean;
            m, n : string;
        procedure main();
        begin

           with
           k : integer;
           do
           begin
           return c;
           with
           a : real;
           return a
           do begin end
           end
        end

        """
        expect = "Type Mismatch In Statement: Return(Some(Id(a)))"
        self.assertTrue(TestChecker.test(input,expect,426))

    # def test_undeclare5(self):
    #     """Simple program: int main() {} """
    #     input = """procedure K(); begin end
    #                procedure main();
    #                var a,b:integer;
    #                f : boolean;
    #                c,d:string;
    #                e: array [1 .. 2] of integer;
    #                begin
    #                    if f then return;
    #                    else
    #                    if f then return;
    #                    else 
    #                    if f then return;
    #                 end
                
    #             procedure doo();
    #                var a,b:integer;
    #                f : boolean;
    #                c,d:string;
    #                e: array [1 .. 2] of integer;
    #                begin
    #                    if f then return a ;
    #                    else
    #                    if f then return a ;
    #                    else 
    #                    if f then return a;
    #                end 

    #                procedure koo();
    #                var a,b:integer;
    #                f : boolean;
    #                c,d:string;
    #                e: array [1 .. 2] of integer;
    #                begin
    #                   return;
    #                   return;
    #                   return;
    #                end
    #                 """
    #     expect = "Undeclared Procedure: k"
    #     self.assertTrue(TestChecker.test(input,expect,414))


    # def test_redeclare6(self):
    #     """Simple program: int main() {} """
    #     input = """var d:string;c:real;e:boolean;
    #                procedure k(); begin end
    #                procedure main(f:string);
    #                var a,b:integer;
    #                begin
    #                with
    #                    a:string;
    #                    b:real;
    #                    f:integer;
    #                do
    #                    begin end
    #                    with
    #                        a:string;
    #                        b:string;
    #                        f:string;
    #                        l:integer;
    #                        c:ARRAY [1 .. 2] OF integeR;
    #                    do
    #                        begin end
    #                end """
    #     expect = "Redeclared Variable: a"
    #     self.assertTrue(TestChecker.test(input,expect,405))

    # def test_redeclare7(self):
    #     """Simple program: int main() {} """
    #     input = """procedure main(x:integer;y:integer);
    #                var a:integer;b:string;c:real;
    #                begin
    #                main(a+a,a+a);
    #                end"""
    #     expect = "Redeclared Variable: a"
    #     self.assertTrue(TestChecker.test(input,expect,406))

    # def test_diff_numofparam_stmt(self):
    #     """More complex program"""
    #     input = """procedure main (); begin
    #         putIntLn();
    #     end"""
    #     expect = "Type Mismatch In Statement: CallStmt(Id(putIntLn),[])"
    #     self.assertTrue(TestChecker.test(input,expect,401))

    # def test_undeclared_function_use_ast(self):
    #     """Simple program: int main() {} """
    #     input = Program([FuncDecl(Id("main"),[],[],[
    #         CallStmt(Id("foo"),[])])])
    #     expect = "Undeclared Procedure: foo"
    #     self.assertTrue(TestChecker.test(input,expect,402))

    # def test_diff_numofparam_expr_use_ast(self):
    #     """More complex program"""
    #     input = Program([
    #             FuncDecl(Id("main"),[],[],[
    #                 CallStmt(Id("putIntLn"),[])])])
                        
    #     expect = "Type Mismatch In Statement: CallStmt(Id(putIntLn),[])"
    #     self.assertTrue(TestChecker.test(input,expect,403))

    
    