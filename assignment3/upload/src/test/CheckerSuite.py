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
                   procedure main(); begin end"""
        expect = "Redeclared Procedure: main"
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
                   function foo():integer; begin end
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

    def test_undeclare2(self):
        """Simple program: int main() {} """
        input = """function k() : integer; begin end
                   procedure main();
                   var a,b:integer;
                   begin
                       k(); 
                   end """
        expect = "Undeclared Procedure: k"
        self.assertTrue(TestChecker.test(input,expect,411))

    def test_undeclare3(self):
        """Simple program: int main() {} """
        input = """
                   procedure main();
                   var k,b:integer;
                   begin
                       k(); 
                   end """
        expect = "Undeclared Procedure: k"
        self.assertTrue(TestChecker.test(input,expect,412))

    def test_undeclare4(self):
        """Simple program: int main() {} """
        input = """procedure K(); begin end
                   procedure main();
                   var a,b:integer;
                   begin
                       x();
                   end """
        expect = "Undeclared Procedure: x"
        self.assertTrue(TestChecker.test(input,expect,413))

    def test_undeclare5(self):
        """Simple program: int main() {} """
        input = """procedure K(); begin end
                   procedure main();
                   var a,b:integer;
                   f : real;
                   c,d:string;
                   e: array [1 .. 2] of integer;
                   begin
                       f := a -- f;
                   end """
        expect = "Undeclared Procedure: k"
        self.assertTrue(TestChecker.test(input,expect,414))


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

    
    