import unittest
from TestUtils import TestChecker
from AST import *
from StaticError import *

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
        expect = str(Redeclared(Procedure(),'PutLn'))
        self.assertTrue(TestChecker.test(input,expect,400))

    def test_redeclare2(self):
        """Simple program: int main() {} """
        input = """
                   procedure main(); begin end 
                   var main:integer;"""
        expect = str(Redeclared(Variable(),'main'))
        self.assertTrue(TestChecker.test(input,expect,401))


    def test_redeclare3(self):
        """Simple program: int main() {} """
        input = """
                   procedure main(); begin end 
                   function main():integer; begin end """
        expect = str(Redeclared(Function(),'main'))
        self.assertTrue(TestChecker.test(input,expect,402))

    
    def test_redeclare4(self):
        """Simple program: int main() {} """
        input = """
                   var foo:integer;
                   procedure main(); begin end 
                   function foo():integer; begin end """
        expect = str(Redeclared(Function(),'foo'))
        self.assertTrue(TestChecker.test(input,expect,403))


    def test_redeclare5(self):
        """Simple program: int main() {} """
        input = """
                   function foo(a:integer;a:integer):real; begin end 
                   procedure main(); begin end"""
        expect = str(Redeclared(Parameter(),'a'))
        self.assertTrue(TestChecker.test(input,expect,404))

    def test_redeclare6(self):
        """Simple program: int main() {} """
        input = """procedure main();
                   var a,a:integer;
                   begin end """
        expect = str(Redeclared(Variable(),'a'))
        self.assertTrue(TestChecker.test(input,expect,405))

    def test_redeclare7(self):
        """Simple program: int main() {} """
        input = """procedure main();
                   var a:integer;
                       a:string;
                   begin end """
        expect = str(Redeclared(Variable(),'a'))
        self.assertTrue(TestChecker.test(input,expect,406))

    def test_redeclare8(self):
        """Simple program: int main() {} """
        input = """var d:string;c:real;e:boolean;
                   function foo():integer; begin return foo(); end
                   procedure k(a:integer;b:real); begin end
                   procedure main();
                   var a,b:integer;
                       f:string;
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
        expect = str(Redeclared(Variable(),'a'))
        self.assertTrue(TestChecker.test(input,expect,407))

    def test_redeclare9(self):
        """Simple program: int main() {} """
        input = """var d:string;c:real;e:boolean;
                   function foo():integer; begin return foo(); end
                   procedure k(a:integer;b:real); begin end
                   procedure main();
                   var a,b:integer;
                       f:string;
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
        expect = str(Redeclared(Variable(),'b'))
        self.assertTrue(TestChecker.test(input,expect,408))


    def test_undeclare1(self):
        """Simple program: int main() {} """
        input = """procedure main();
                   var a,b:integer;
                   begin
                       k(); 
                   end """
        expect = str(Undeclared(Procedure(),'k'))
        self.assertTrue(TestChecker.test(input,expect,409))

    def test_undeclare2(self):
        """Simple program: int main() {} """
        input = """var k : integer;
                   procedure main();
                   var a,b:integer;
                   begin
                       k(); 
                   end """
        expect = str(Undeclared(Procedure(),'k'))
        self.assertTrue(TestChecker.test(input,expect,410))

    def test_undeclare3(self):
        """Simple program: int main() {} """
        input = """function k() : integer; begin return k(); end
                   procedure main();
                   var a,b:integer;
                   begin
                       k(); 
                   end """
        expect = str(Undeclared(Procedure(),'k'))
        self.assertTrue(TestChecker.test(input,expect,411))

    def test_undeclare4(self):
        """Simple program: int main() {} """
        input = """
                   procedure main();
                   var k,b:integer;
                   begin
                       k(); 
                   end """
        expect = str(Undeclared(Procedure(),'k'))
        self.assertTrue(TestChecker.test(input,expect,412))

    def test_undeclare5(self):
        """Simple program: int main() {} """
        input = """function k() : integer; begin return k(); end
                   procedure main();
                   var a,b:integer;
                   begin
                       x();
                   end """
        expect = str(Undeclared(Procedure(),'x'))
        self.assertTrue(TestChecker.test(input,expect,413))

    def test_undeclare6(self):
        """Simple program: int main() {} """
        input = """procedure K(); begin end
                   procedure main();
                   var a,b:integer;
                   begin
                       a := k();
                   end """
        expect = str(Undeclared(Function(),'k'))
        self.assertTrue(TestChecker.test(input,expect,414))

    def test_undeclare7(self):
        """Simple program: int main() {} """
        input = """procedure K(); begin end
                   procedure main();
                   var a,b:integer;
                   begin
                       if k() then begin end
                   end """
        expect = str(Undeclared(Function(),'k'))
        self.assertTrue(TestChecker.test(input,expect,415))

    def test_undeclare8(self):
        """Simple program: int main() {} """
        input = """procedure K(); begin end
                   procedure main();
                   var a,b:integer;
                   begin
                       if l then begin end
                   end """
        expect = str(Undeclared(Identifier(),'l'))
        self.assertTrue(TestChecker.test(input,expect,416))


    def test_undeclare9(self):
        """Simple program: int main() {} """
        input = """function x():integer; begin return x(); end
                   function y():integer; begin  return x(); end
                   function z():integer; begin return x(); end
                   procedure main();
                   var a,b,c,d,e,f,g,h:integer;
                   begin
                       a := (a+b)/(c*d)*(x()*y()) + (y()/z())+(l div b * c);
                   end """
        expect = str(Undeclared(Identifier(),'l'))
        self.assertTrue(TestChecker.test(input,expect,417))

    def test_typeStmt1(self):
        """Simple program: int main() {} """
        input = """var x,y : real;
                   procedure main();
                   var a,b:integer;
                       c : boolean; k :string;
                   begin
                       if k then begin end
                   end """
        expect = str(TypeMismatchInStatement(If(Id('k'),[],[])))
        self.assertTrue(TestChecker.test(input,expect,418))

    def test_typeStmt2(self):
        """Simple program: int main() {} """
        input = """var x,y : real;
                   procedure main();
                   var a,b:integer;
                    c : boolean; k :string;
                   begin
                       if (x + y) / (a * b) then begin end
                   end """
        expect = str(TypeMismatchInStatement(If(BinaryOp("/",BinaryOp("+",Id("x"),Id("y")),BinaryOp("*",Id("a"),Id("b"))),
		[],

		[])))
        self.assertTrue(TestChecker.test(input,expect,419))

    def test_typeStmt3(self):
        """Simple program: int main() {} """
        input = """var x,y : real;
                   procedure main();
                   var a,b:integer;
                       c : boolean; k :string;
                   begin
                       if (a >= b) and c then 
                           for x := a to b do begin end
                   end """
        expect = str(TypeMismatchInStatement(For(Id("x"),Id("a"),Id("b"),True,
		[])))
        self.assertTrue(TestChecker.test(input,expect,420))

    def test_typeStmt4(self):
        """Simple program: int main() {} """
        input = """var x,y : real;
                   procedure main();
                   var a,b:integer;
                       c : boolean; k :string;
                   begin
                       if c and c then begin end
                       with
                           c : integer;
                       do
                           if c then begin end
                   end """
        expect = str(TypeMismatchInStatement(If(Id("c"),
		[],

		[])))
        self.assertTrue(TestChecker.test(input,expect,421))


    def test_typeStmt5(self):
        """Simple program: int main() {} """
        input = """var x,y : real;
                   procedure main();
                   var a,b:integer;
                       c : boolean; k :string;
                   begin
                       if (a >= b) and c then 
                           for a := a + b to (a * b) * (b+a div a) do
                               for a := a + b to (a * b) / (b+a div a) do begin end
                   end """
        expect = str(TypeMismatchInStatement(For(Id("a"),BinaryOp("+",Id("a"),Id("b")),BinaryOp("/",BinaryOp("*",Id("a"),Id("b")),BinaryOp("+",Id("b"),BinaryOp("div",Id("a"),Id("a")))),True,
		[])))
        self.assertTrue(TestChecker.test(input,expect,422))


    def test_typeStmt6(self):
        """Simple program: int main() {} """
        input = """var x,y : real;
                   procedure main();
                   var a,b:integer;
                       c : boolean; k :string;
                   begin
                       if (a >= b) and c then 
                           for a := a + b to (a * b) * (b+a div a) do begin
                               for a := a / b to (a * b) * (b+a div a) do begin end 
                            end
         
                   end """
        expect = str(TypeMismatchInStatement(For(Id("a"),BinaryOp("/",Id("a"),Id("b")),BinaryOp("*",BinaryOp("*",Id("a"),Id("b")),BinaryOp("+",Id("b"),BinaryOp("div",Id("a"),Id("a")))),True,
		[])))
        self.assertTrue(TestChecker.test(input,expect,423))

    def test_typeStmt7(self):
        """Simple program: int main() {} """
        input = """var x,y : real;
                   procedure main();
                   var a,b,e:integer;
                       c : boolean; k :string;
                   begin
                   for e := 2 * b to (a * b) * (b+a div a) do begin end
                       with
                       e :real;
                       do
                           begin
                               if (a >= b) and c then begin end
                               for a := a + b to (a * b) * (b+a div a) do begin end
                               for e := a + b to (a * b) * (b+a div a) do begin end
                            end
                   end """
        expect = str(TypeMismatchInStatement(For(Id("e"),BinaryOp("+",Id("a"),Id("b")),BinaryOp("*",BinaryOp("*",Id("a"),Id("b")),BinaryOp("+",Id("b"),BinaryOp("div",Id("a"),Id("a")))),True,
		[])))
        self.assertTrue(TestChecker.test(input,expect,424))

    def test_typeStmt8(self):
        """Simple program: int main() {} """
        input = """var x,y : real;
                   procedure main();
                   var a,b,e:integer;
                       c : boolean; k :string;
                   begin
                   for e := 2 * b to (a * b) * (b+a div a) do begin end
                       with
                       e :real;
                       do
                        begin
                               while a + b do begin end
                        end
                   end """
        expect = str(TypeMismatchInStatement(While(BinaryOp("+",Id("a"),Id("b")),
		[])))
        self.assertTrue(TestChecker.test(input,expect,425))

    def test_typeStmt9(self):
        """Simple program: int main() {} """
        input = """
                   var x,y : real;
                   procedure main();
                   var a,b,e:integer;
                       c : boolean; k :string;
                   begin
                   for e := 2 * b to (a * b) * (b+a div a) do begin end
                       with
                       e :real;
                       do
                        begin
                               while a > b do begin while (a + b) do begin end end
                        end
                   end
        """
        expect = str(TypeMismatchInStatement(While(BinaryOp("+",Id("a"),Id("b")),
		[])))
        self.assertTrue(TestChecker.test(input,expect,426))

    def test_typeStmt10(self):
        """Simple program: int main() {} """
        input = """
                   var x,y : real;
                   procedure main();
                   var a,b,e:integer;
                       c : boolean; k :string;
                   begin
                   a := a / b;
                   end
        """
        expect = str(TypeMismatchInStatement(Assign(Id("a"),BinaryOp("/",Id("a"),Id("b")))))
        self.assertTrue(TestChecker.test(input,expect,427))

    def test_typeStmt11(self):
        """Simple program: int main() {} """
        input = """
                   var x,y : real;
                   procedure main();
                   var a,b,e:integer;
                       c : boolean; k :string;
                   begin
                   a := a + (b*a)*(a-b)*(a*a*a/a);
                   end
        """
        expect = str(TypeMismatchInStatement(Assign(Id("a"),BinaryOp("+",Id("a"),BinaryOp("*",BinaryOp("*",BinaryOp("*",Id("b"),Id("a")),BinaryOp("-",Id("a"),Id("b"))),BinaryOp("/",BinaryOp("*",BinaryOp("*",Id("a"),Id("a")),Id("a")),Id("a")))))))
        self.assertTrue(TestChecker.test(input,expect,428))


    def test_typeStmt12(self):
        """Simple program: int main() {} """
        input = """
                   var x,y : real;
                   procedure main();
                   var a,b,e:integer;
                       c : boolean; k :string;
                        l:string;
                   begin
                   l := c;
                   end
        """
        expect = str(TypeMismatchInStatement(Assign(Id("l"),Id("c"))))
        self.assertTrue(TestChecker.test(input,expect,429))

    def test_typeStmt13(self):
        """Simple program: int main() {} """
        input = """
                   var x,y : real;
                       koo : array [1 .. 2] of integer;
                   procedure main();
                   var a,b,e:integer;
                       c : boolean; k :string;
                        l:string;
                        arr : array [1 .. 2] of integer;
                   begin
                   koo[1] := arr[2];
                   a := a+b*b;
                   x := (a/b*y) + (b+a div a);
                   koo := arr;
                   end
        """
        expect = str(TypeMismatchInStatement(Assign(Id("koo"),Id("arr"))))
        self.assertTrue(TestChecker.test(input,expect,430))


    def test_typeStmt14(self):
        """Simple program: int main() {} """
        input = """
                   var x,y : real;
                       d : boolean;
                       koo : array [1 .. 2] of integer;
                   procedure main();
                   var a,b,e:integer;
                        l:string;
                        arr : array [1 .. 2] of integer;
                   begin
                   koo[1] := arr[2];
                   
                   with
                       l: boolean;
                    do
                       if l then
                           return;
                        else if l then if l then if l then return a;
                    end

        """
        expect = str(TypeMismatchInStatement(Return(Id("a"))))
        self.assertTrue(TestChecker.test(input,expect,431))


    def test_typeStmt15(self):
        """Simple program: int main() {} """
        input = """
                   var x,y : real;
                       d : boolean;
                       koo : array [1 .. 2] of integer;
                   procedure main();
                   var a,b,e:integer;
                        l:string;
                        arr : array [1 .. 2] of integer;
                   begin
                   koo[1] := arr[2];
                   
                   with
                       l: boolean;
                    do
                       if l then
                           return;
                       else
                           return;
                    end

                   function foo() : real;
                   var a,b,e:integer;
                        l:string;
                        arr : array [1 .. 2] of integer;
                   begin
                   koo[1] := arr[2];
                   
                   with
                       l: boolean;
                    do
                       if l then
                           return;
                       else
                           return;
                    end

        """
        expect = str(TypeMismatchInStatement(Return(None)))
        self.assertTrue(TestChecker.test(input,expect,432))


    def test_typeStmt16(self):
        """Simple program: int main() {} """
        input = """
                   var x,y : real;
                       d : boolean;
                       koo : array [1 .. 2] of integer;
                   procedure main();
                   var a,b,e:integer;
                        l:string;
                        arr : array [1 .. 2] of integer;
                   begin
                   koo[1] := arr[2];
                   
                   with
                       l: boolean;
                    do
                       if l then
                           return;
                       else
                           return;
                    end

                   function foo() : real;
                   var a,b,e:integer;
                        l:string;
                        arr : array [1 .. 2] of integer;
                   begin
                   koo[1] := arr[2];
                   
                   with
                       l: boolean;
                    do
                       if l then
                           return a;
                       else if l then
                           return a/b;
                       else
                           return l;
                    end

        """
        expect = str(TypeMismatchInStatement(Return(Id('l'))))
        self.assertTrue(TestChecker.test(input,expect,433))


    def test_typeStmt17(self):
        """Simple program: int main() {} """
        input = """
                   var x,y : real;
                       d : boolean;
                       koo : array [1 .. 2] of integer;
                   procedure main();
                   var a,b,e:integer;
                        l:string;
                        arr : array [1 .. 2] of integer;
                   begin
                   koo[1] := arr[2];
                   
                   with
                       l: boolean;
                    do
                       if l then
                           return;
                       else
                           return;
                    end

                   function foo() : string;
                   var a,b,e:integer;
                        l:string;
                        arr : array [1 .. 2] of integer;
                   begin
                   koo[1] := arr[2];
                   
                   with
                       l: boolean;
                       a:string;
                    do
                       if l then
                           return a;
                       else if l then
                           return l;
                       else
                           return a;
                    end

        """
        expect = str(TypeMismatchInStatement(Return(Id('l'))))
        self.assertTrue(TestChecker.test(input,expect,434))


    def test_typeStmt18(self):
        """Simple program: int main() {} """
        input = """
                   var x,y : real;
                       d : boolean;
                       koo : array [1 .. 2] of integer;
                   procedure main();
                   begin
                   end

                   function foo() : array [1 .. 3] of integer;
                   var a,b,e:integer;
                        l:string;
                        arr : array [1 .. 2] of integer;
                   begin
                   koo[1] := arr[2];
                   
                   with
                       l: boolean;
                       a:string;
                    do
                           return arr;
                    end

        """
        expect = str(TypeMismatchInStatement(Return(Id("arr"))))
        self.assertTrue(TestChecker.test(input,expect,435))


    def test_typeStmt19(self):
        """Simple program: int main() {} """
        input = """
                   var x,y : real;
                       d : boolean;
                       koo : array [1 .. 2] of integer;
                   procedure main();
                   begin
                   end

                   function foo() : array [1 .. 2] of real;
                   var a,b,e:integer;
                        l:string;
                        arr : array [1 .. 2] of integer;
                   begin
                   koo[1] := arr[2];
                   
                   with
                       l: boolean;
                       a:string;
                    do
                           return arr;
                    end

        """
        expect = str(TypeMismatchInStatement(Return(Id("arr"))))
        self.assertTrue(TestChecker.test(input,expect,436))


    def test_typeStmt20(self):
        """Simple program: int main() {} """
        input = """
                   var x,y : real;
                       d : boolean;
                       koo : array [1 .. 2] of integer;
                   procedure main();
                   begin
                   end

                   function foo() : array [2 .. 2] of real;
                   var a,b,e:integer;
                        l:string;
                        arr : array [1 .. 2] of integer;
                   begin
                   koo[1] := arr[2];
                   
                   with
                       l: boolean;
                       a:string;
                    do
                           return arr;
                    end

        """
        expect = str(TypeMismatchInStatement(Return(Id("arr"))))
        self.assertTrue(TestChecker.test(input,expect,437))


    def test_typeStmt21(self):
        """Simple program: int main() {} """
        input = """
                   var x,y : real;
                       d : boolean;
                       koo : array [1 .. 2] of integer;
                   procedure main();
                   begin
                       x := foo(x);
                   end

                   function foo() : real;
                   var a,b,e:integer;
                        l:string;
                        arr : array [1 .. 2] of integer;
                   begin
                   koo[1] := arr[2];
                   
                   with
                       l: boolean;
                       a:string;
                    do
                       if l then
                           return a;
                    end

        """
        expect = str(TypeMismatchInExpression(CallExpr(Id("foo"),
			[Id("x")])))
        self.assertTrue(TestChecker.test(input,expect,438))


    def test_typeStmt22(self):
        """Simple program: int main() {} """
        input = """
                   var x,y : real;
                       a,b :integer;
                       d : boolean;
                       koo : array [1 .. 2] of integer;
                   procedure main();
                   begin
                       x := foo(a/b);
                   end

                   function foo(x :integer) : real;
                   var a,b,e:integer;
                        l:string;
                        arr : array [1 .. 2] of integer;
                   begin
                   koo[1] := arr[2];
                   
                   with
                       l: boolean;
                       a:real;
                    do
                       if l then
                           return a;
                    end

        """
        expect = str(TypeMismatchInExpression(CallExpr(Id("foo"),
			[BinaryOp("/",Id("a"),Id("b"))])))
        self.assertTrue(TestChecker.test(input,expect,439))


    def test_typeStmt23(self):
        """Simple program: int main() {} """
        input = """
                   var x,y : real;
                       a,b :integer;
                       d : boolean;
                       koo : array [1 .. 2] of integer;
                   procedure main();
                   begin
                       x := foo(koo,a,a);
                   end

                   function foo(x :array[1 .. 3] of integer;loo:integer;phic:real) : real;
                   var a,b,e:integer;
                        l:string;
                        arr : array [1 .. 2] of integer;
                   begin
                   koo[1] := arr[2];
                   
                   with
                       l: boolean;
                       a:real;
                    do
                       if l then
                           return a;
                    end

        """
        expect = str(TypeMismatchInExpression(CallExpr(Id("foo"),
			[Id("koo"),
			Id("a"),
			Id("a")])))
        self.assertTrue(TestChecker.test(input,expect,440))


    def test_notReturn1(self):
        """Simple program: int main() {} """
        input = """
                   var x,y : real;
                       a,b :integer;
                       d : boolean;
                       koo : array [1 .. 2] of integer;
                   procedure main();
                   begin
                   end

                   function foo(x :array[1 .. 3] of integer;loo:integer;phic:real) : real;
                   var a,b,e:integer;
                        l:string;
                        arr : array [1 .. 2] of integer;
                   begin
                   
                   
                   with
                       l: boolean;
                       a:real;
                   do
                       if l then return a/b;
                       else a := b;
                    end

        """
        expect = str(FunctionNotReturn('foo'))
        self.assertTrue(TestChecker.test(input,expect,441))


    def test_notReturn2(self):
        """Simple program: int main() {} """
        input = """
                   var x,y : real;
                       a,b :integer;
                       d : boolean;
                       koo : array [1 .. 2] of integer;
                   procedure main();
                   begin
                   end

                   function foo(x :array[1 .. 3] of integer;loo:integer;phic:real) : real;
                   var a,b,e:integer;
                        l:string;
                        arr : array [1 .. 2] of integer;
                   begin
                   
                   
                   with
                       l: boolean;
                       a:real;
                   do
                       if l then 
                           if a >= b then
                               return a/b;
                           else
                               return a+b;
                       else a := b;
                    end

        """
        expect = str(FunctionNotReturn('foo'))
        self.assertTrue(TestChecker.test(input,expect,442))


    def test_notReturn3(self):
        """Simple program: int main() {} """
        input = """
                   var x,y : real;
                       a,b :integer;
                       d : boolean;
                       koo : array [1 .. 2] of integer;
                   procedure main();
                   begin
                   end

                   function foo(x :array[1 .. 3] of integer;loo:integer;phic:real) : real;
                   var a,b,e:integer;
                        l:string;
                        arr : array [1 .. 2] of integer;
                   begin
                   
                   
                   with
                       l: boolean;
                       a:real;
                   do
                       if l then 
                           if a >= b then
                               return a/b;
                           else
                               return a+b;
                       else 
                       while l do return a/b;
                    end

        """
        expect = str(FunctionNotReturn('foo'))
        self.assertTrue(TestChecker.test(input,expect,443))


    def test_notReturn4(self):
        """Simple program: int main() {} """
        input = """
                   var x,y : real;
                       a,b :integer;
                       d : boolean;
                       koo : array [1 .. 2] of integer;
                   procedure main();
                   begin
                   end

                   function foo(x :array[1 .. 3] of integer;loo:integer;phic:real) : real;
                   var a,b,e:integer;
                        l:string;
                        arr : array [1 .. 2] of integer;
                   begin
                   
                   
                   with
                       l: boolean;
                       a:real;
                   do
                       if l then 
                           if a >= b then
                               return a/b;
                           else
                               return a+b;
                       else 
                       while l do return a/b;

                    for a:= b to a do return a/b;
                    end

        """
        expect = str(FunctionNotReturn('foo'))
        self.assertTrue(TestChecker.test(input,expect,444))


    def test_notReturn5(self):
        """Simple program: int main() {} """
        input = """
                   var x,y : real;
                       a,b :integer;
                       d : boolean;
                       koo : array [1 .. 2] of integer;
                   procedure main();
                   begin
                   end

                   function foo(x :array[1 .. 3] of integer;loo:integer;phic:real) : real;
                   var a,b,e:integer;
                        l:string;
                        arr : array [1 .. 2] of integer;
                   begin
                   
                   
                   with
                       l: boolean;
                       a:real;
                   do
                       if l then 
                           if a >= b then
                               return a/b;
                           else
                               return a+b;
                       else 
                           if l then 
                               if a >= b then
                                   return a/b;
                               else
                                   a := a+b;
                           

                    for a:= b to a do return a/b;
                    end

        """
        expect = str(FunctionNotReturn('foo'))
        self.assertTrue(TestChecker.test(input,expect,445))

    def test_notReturn6(self):
        """Simple program: int main() {} """
        input = """
                   var x,y : real;
                       a,b :integer;
                       d : boolean;
                       koo : array [1 .. 2] of integer;
                   procedure main();
                   begin
                   end

                   function foo(x :array[1 .. 3] of integer;loo:integer;phic:real) : real;
                   var a,b,e:integer;
                        l:string;
                        arr : array [1 .. 2] of integer;
                   begin
                   
                   
                   with
                       l: boolean;
                       a:real;
                   do
                       if l then 
                           if a >= b then
                               return a/b;
                           else
                               return a+b;
                       else 
                           if l then 
                               if a >= b then
                                   return a/b;
                               else
                                   if a >= b then
                                       return a/b;
                                    else
                                       while l do  return a;
                           

                    for a:= b to a do return a/b;
                    end

        """
        expect = str(FunctionNotReturn('foo'))
        self.assertTrue(TestChecker.test(input,expect,446))



    def test_loop1(self):
        """Simple program: int main() {} """
        input = """
                   var x,y : real;
                       a,b :integer;
                       d : boolean;
                       koo : array [1 .. 2] of integer;
                   procedure main();
                   begin
                   end

                   function foo(x :array[1 .. 3] of integer;loo:integer;phic:real) : real;
                   var a,b,e:integer;
                        l:string;
                        arr : array [1 .. 2] of integer;
                   begin
                   
                   
                   with
                       l: boolean;
                       a:real;
                   do
                       if l then 
                           if a >= b then
                               return a/b;
                           else
                               return a+b;
                       else 
                           if l then 
                               if a >= b then
                                   return a/b;
                               else
                                   if a >= b then
                                       return a/b;
                                   else
                                    begin
                                    return a/b;
                                    break;
                                    end
                    for a:= b to a do return a/b;
                    end

        """
        expect = str(BreakNotInLoop())
        self.assertTrue(TestChecker.test(input,expect,447))


    def test_notReturn7(self):
        """Simple program: int main() {} """
        input = """
                   var x,y : real;
                       a,b :integer;
                       d : boolean;
                       koo : array [1 .. 2] of integer;
                   procedure main();
                   begin
                   end

                   function foo(x :array[1 .. 3] of integer;loo:integer;phic:real) : real;
                   var a,b,e:integer;
                        l:string;
                        arr : array [1 .. 2] of integer;
                   begin
                   
                   
                   with
                       l: boolean;
                       a:real;
                   do

                   for b := b to b do begin
                       if l then 
                           if a >= b then
                               return a/b;
                           else
                               return a+b;
                       else 
                           if l then 
                               if a >= b then
                                   return a/b;
                               else
                                   if a >= b then return a;
                        break;
                        end
                    for a:= b to a do return a/b;
                    end

        """
        expect = str(FunctionNotReturn('foo'))
        self.assertTrue(TestChecker.test(input,expect,448))

    def test_loop2(self):
        """Simple program: int main() {} """
        input = """
                   var x,y : real;
                       a,b :integer;
                       d : boolean;
                       koo : array [1 .. 2] of integer;
                   procedure main();
                   begin
                   end

                   function foo(x :array[1 .. 3] of integer;loo:integer;phic:real) : real;
                   var a,b,e:integer;
                        l:string;
                        arr : array [1 .. 2] of integer;
                   begin
                   
                   
                   with
                       l: boolean;
                       a:real;
                   do
                   while l do begin
                       if l then 
                           if a >= b then
                               return a/b;
                           else
                               return a+b;
                       else 
                           if l then 
                               if a >= b then
                                   return a/b;
                               else
                                   if a >= b then
                                       return a/b;
                    break;
                    end
                    continue;
                    return a/b
                    for a:= b to a do return a/b;
                    end

        """
        expect = str(ContinueNotInLoop())
        self.assertTrue(TestChecker.test(input,expect,449))

    def test_noentry1(self):
        """Simple program: int main() {} """
        input = """
                   var x,y : real;
                       a,b :integer;
                       d : boolean;
                       koo : array [1 .. 2] of integer;
                   procedure mainnu();
                   begin
                   end

                   function foo(x :array[1 .. 3] of integer;loo:integer;phic:real) : real;
                   var a,b,e:integer;
                        l:string;
                        arr : array [1 .. 2] of integer;
                   begin
                   return a;
                    end

        """
        expect = str(NoEntryPoint())
        self.assertTrue(TestChecker.test(input,expect,450))

    def test_noentry2(self):
        """Simple program: int main() {} """
        input = """
                   var x,y : real;
                       a,b :integer;
                       d : boolean;
                       koo : array [1 .. 2] of integer;
                   procedure main(a:integer;b:real);
                   begin
                   end

                   function foo(x :array[1 .. 3] of integer;loo:integer;phic:real) : real;
                   var a,b,e:integer;
                        l:string;
                        arr : array [1 .. 2] of integer;
                   begin
                   return a;
                    end

        """
        expect = str(NoEntryPoint())
        self.assertTrue(TestChecker.test(input,expect,451))

    def test_noentry3(self):
        """Simple program: int main() {} """
        input = """
                   var x,y : real;
                       a,b :integer;
                       d : boolean;
                       koo : array [1 .. 2] of integer;
                   function main():real; begin return x; end
                   begin
                   end

                   function foo(x :array[1 .. 3] of integer;loo:integer;phic:real) : real;
                   var a,b,e:integer;
                        l:string;
                        arr : array [1 .. 2] of integer;
                   begin
                   return a;
                    end

        """
        expect = str(NoEntryPoint())
        self.assertTrue(TestChecker.test(input,expect,452))

    def test_some1(self):
        """Simple program: int main() {} """
        input = """
                   var x,y : real;
                       a,b :integer;
                       d : boolean;
                       koo : array [1 .. 2] of integer;
                   function main():real; begin return x; end
                   begin
                   end

                   function foo(x :array[1 .. 3] of integer;loo:integer;phic:real) : real;
                   var a,b,e:integer;
                        l:string;
                        arr : array [1 .. 2] of integer;
                   begin
                   return a;
                    end

        """
        expect = str(NoEntryPoint())
        self.assertTrue(TestChecker.test(input,expect,453))
    
    def test_some2(self):
        """Simple program: int main() {} """
        input = """
                   var x,y : real;
                       a,b :integer;
                       d : boolean;
                       koo : array [1 .. 2] of integer;
                   procedure main(); begin return; end
                   begin
                   end

                   function foo(i:integer):string;
                        var ret: array [1 .. 2] of string;
                        begin
                            for i :=1 to 4836 do
                                begin
                                    while i <> 1 do
                                    begin
                                        if i < 463 then return "hehe";
                                        else return "4168";
                                    end
                                    return ret[i];
                                end
                        end

        """
        expect = str(FunctionNotReturn('foo'))
        self.assertTrue(TestChecker.test(input,expect,454))

    def test_some3(self):
        """Simple program: int main() {} """
        input = """
                   var x,y : real;
                       a,b :integer;
                       d : boolean;
                       koo : array [1 .. 2] of integer;
                   procedure main(); begin return; end
                   begin
                   end

                   function foo(i:integer):string;
                        var ret: array [1 .. 2] of string;
                        begin
                            for i :=1 to 4836 do
                                begin
                                    while i <> 1 do
                                    begin
                                        while i <> 1 do
                                            begin
                                                if i < 463 then return "hehe";
                                                else return "4168";
                                            end
                                        return ret[i];
                                    end
                                    return ret[i];
                                end
                        end

        """
        expect = str(FunctionNotReturn('foo'))
        self.assertTrue(TestChecker.test(input,expect,455))
    
    def test_some4(self):
        input = """procedure main();
        begin
            with x,y,z: real;
                i,j: integer;
            do
                begin
                    for i:=1 to 10 do
                        begin
                            y := foo();
                        end
                    break;
                    while j <> 10 do
                    begin
                    end
                end
        end
        function foo():integer;
        var a,b,c: integer;
        begin
            return a + b mod c;
        end"""
        expect = str(BreakNotInLoop())
        self.assertTrue(TestChecker.test(input, expect, 456))

    def test_some5(self):
        input = """procedure main();
        begin
            with x,y,z: real;
                i,j: integer;
            do
                begin
                    for i:=1 to 10 do
                        begin
                            y := foo();
                        end
                    continue;
                    while j <> 10 do
                    begin
                    end
                end
        end
        function foo():integer;
        var a,b,c: integer;
        begin
            return a + b mod c;
        end"""
        expect = str(ContinueNotInLoop())
        self.assertTrue(TestChecker.test(input, expect, 457))

    def test_some6(self):
        input = """procedure main();
        begin
            with x,y,z: real;
                i,j: integer;
            do
                begin
                    for i:=1 to 10 do
                        begin
                            y := foo();
                        end
                    while not j <> 10 do
                    begin
                    end
                end
        end
        function foo():integer;
        var a,b,c: integer;
        begin
            return a + b mod c;
        end"""
        expect = str(TypeMismatchInExpression(UnaryOp('not', Id('j'))))
        self.assertTrue(TestChecker.test(input, expect, 458))

    def test_some7(self):
        input = """procedure main();
        begin
            with x,y,z: real;
                i,j: integer;
            do
                begin
                    for i:=1 to 10 do
                        begin
                            y := foo();
                        end
                    while j and Then 10 do
                    begin
                    end
                end
        end
        function foo():integer;
        var a,b,c: integer;
        begin
            return a + b mod c;
        end"""
        expect = str(
            TypeMismatchInExpression(
                BinaryOp('andthen', Id('j'), IntLiteral(10))))
        self.assertTrue(TestChecker.test(input, expect, 459))

    def test_some8(self):
        input = """procedure main();
        begin
            with x,y,z: real;
                i,j: integer;
            do
                begin
                    for i:=1 to 10 do
                        begin
                            y := foo();
                        end
                    while j <> foo(10) do
                    begin
                    end
                end
        end
        function foo():integer;
        var a,b,c: integer;
        begin
            return a + b mod c;
        end"""
        expect = str(
            TypeMismatchInExpression(CallExpr(Id('foo'), [IntLiteral(10)])))
        self.assertTrue(TestChecker.test(input, expect, 460))

    def test_some9(self):
        input = """procedure main();
        begin
        end
        function foo():string;
        var a,b,c: integer;
        begin
            return a + b mod c;
        end"""
        expect = str(
            TypeMismatchInStatement(
                Return(
                    BinaryOp('+', Id('a'), BinaryOp('mod', Id('b'),
                                                    Id('c'))))))
        self.assertTrue(TestChecker.test(input, expect, 461))

    def test_some10(self):
        input = """procedure main();
        begin
            foo("hehehe");
        end
        function foo(x: string):real;
        var a,b,c: string;
        begin
        end"""
        expect = str(Undeclared(Procedure(), 'foo'))
        self.assertTrue(TestChecker.test(input, expect, 462))

    def test_some11(self):
        input = """
        var x, y : array[1 .. 3] of boolean;
            a, b: integer;
            c, d: real;
            e, f: boolean;
            m, n : string;

        function foo() : integer ;
        begin
            return a;
        end

        procedure main();
        begin
            x[foo()] := f or b;
        end

        procedure foo2 (n: string; m : array[2 .. 3] of real);
        begin
        end
        """
        expect = str(TypeMismatchInExpression(BinaryOp("or",Id("f"),Id("b"))))
        self.assertTrue(TestChecker.test(input, expect, 463))

    def test_some12(self):
        input = """var x,y: real;
        procedure main();
        begin
            foo(x * y - x / 2);
        end
        procedure foo(x: real);
        var a,b,c: boolean;
        begin
            a := x or else c;
        end"""
        expect = str(
            TypeMismatchInExpression(BinaryOp('orelse', Id('x'), Id('c'))))
        self.assertTrue(TestChecker.test(input, expect, 464))

    def test_some13(self):
        input = """
        function foo(i:integer):integer;
        begin
            with a:integer; do
                if 2>1 then
                        if true then 
                            return i;
                        else return 0;
                else
                    begin
                        if a=i then 
                        begin
                            if false then return 1;
                            else return 2;
                        end
                        else return 0;
                    end
        end
        procedure main();
        var a:integer;b:integer;i:integer;
        begin
            while(a>=b) do
            begin   
                foo(i);
            end
        end
        """
        expect = str(Undeclared(Procedure(), 'foo'))
        self.assertTrue(TestChecker.test(input, expect, 465))

    def test_some14(self):
        input = """
        function foo(i:integer):integer;
        begin
            with a:integer; do
                if 2>1 then
                        if true then 
                            return i;
                        else return 0;
                else
                    begin
                        if a=i then 
                        begin
                            if false then return 1;
                            else return 2;
                        end
                    end
        end
        procedure main();
        var a:integer;b:integer;i:integer;
        begin
            while(a>=b) do
            begin   
                a := foo(i);
            end
        end
        """
        expect = str(FunctionNotReturn('foo'))
        self.assertTrue(TestChecker.test(input, expect, 466))

    def test_some15(self):
        input = """
        procedure main (); 
        begin
        end
        function BichNu(Thino: array[-1 .. -2] of integer): real;
        var dau: real; loan:string; nu:boolean; mam:boolean;
            chipheo: array[-1 .. -2] of integer;
        begin
            dau:= 2.2+1;
            if (not nu) 
                then 
                    dau:= BichNu(Thino);
                    dau:= BichNu(chipheo);
        end
        """
        expect = str(FunctionNotReturn('BichNu'))

        self.assertTrue(TestChecker.test(input,expect,467))

    def test_some16(self):
        input = """
        procedure main (); 
        begin
        end
        function foo(n: integer; m:integer): integer;
        BEGIN           
        END"""
        expect = str(FunctionNotReturn('foo'))
        self.assertTrue(TestChecker.test(input, expect, 468))

    def test_some17(self):
        input = """
        procedure main (); 
        begin
        end
        function BichNu(Thino: array[-1 .. -2] of integer): real;
        var dau: real; loan:string; nu:boolean; mam:boolean;
            chipheo: array[-1 .. -2] of integer;
        begin
            dau:= 2.2+1;
            if (not nu) 
                then 
                    return dau;
        end
        """
        expect = str(FunctionNotReturn('BichNu'))

        self.assertTrue(TestChecker.test(input,expect,469))
    def test_some18(self):
        input = """
        procedure main (); 
        begin
        end
        function BichNu(Thino: array[-1 .. -2] of integer): real;
        var dau: real; loan:string; nu:boolean; mam:boolean;
            chipheo: array[-1 .. -2] of integer;
            nhi: integer;
        begin
            dau:= 2.2+1;
            if (not nu) 
                then 
                    for nhi:=0 to 69 do
                    begin
                        dau:= BichNu(Thino);
                        dau:= BichNu(chipheo);
                        return dau;
                    end
                else
                    return dau;
        end
        """
        expect = str(FunctionNotReturn('BichNu'))

        self.assertTrue(TestChecker.test(input,expect,470))
    def test_some19(self):
        input = """
        procedure main (); 
        begin
        end
        function BichNu(Thino: array[-1 .. -2] of integer): real;
        var dau: real; loan:string; nu:boolean; mam:boolean;
            chipheo: array[-1 .. -2] of integer;
            nhi: integer;
        begin
            dau:= 2.2+1;
            if (not nu) 
                then
                dau:=dau+0;
                else
                    return dau;
        end
        """
        expect = str(FunctionNotReturn('BichNu'))

        self.assertTrue(TestChecker.test(input,expect,471))

    def test_some20(self):
        input = """
        procedure main (); 
        begin
        end
        function BichNu(Thino: array[-1 .. -2] of integer): real;
        var dau: real; loan:string; nu:boolean; mam:boolean;
            chipheo: array[-1 .. -2] of integer;
            nhi: integer;
        begin
            for nhi:=0 to 69 do
            begin
                dau:= BichNu(Thino);
                dau:= BichNu(chipheo);
            end
        end
        """
        expect = str(FunctionNotReturn('BichNu'))

        self.assertTrue(TestChecker.test(input,expect,472))

    def test_some21(self):
        input = """
        procedure main (); 
        begin
        end
        function BichNu(Thino: array[-1 .. -2] of integer): real;
        var dau: real; loan:string; nu:boolean; mam:boolean;
            chipheo: array[-1 .. -2] of integer;
            nhi: integer;
        begin
            for nhi:=0 to 69 do
            begin
                dau:= BichNu(Thino);
                dau:= BichNu(chipheo);
                return dau;
            end
        end
        """
        expect = str(FunctionNotReturn('BichNu'))

        self.assertTrue(TestChecker.test(input,expect,473))

    def test_some22(self):
        input = """
        procedure main (); 
        begin
        end
        
        function BichNu(Thino: array[-1 .. -2] of integer): real;
        var dau: real; loan:string; nu:boolean; mam:boolean;
            chipheo: array[-1 .. -2] of integer;
            nhi: integer;
        begin
            for nhi:=0 to 69 do
            begin
                dau:= BichNu(Thino);
                dau:= BichNu(chipheo);
                return dau;
            end
            return dau;
        end
        function BichMam(): real;
        begin
        end
        """
        expect = str(FunctionNotReturn('BichMam'))

        self.assertTrue(TestChecker.test(input,expect,474))

    def test_some23(self):
        """Test invocation"""
        input = """procedure main (); 
        begin
        end
        
        function BichNu(Thino: array[-1 .. -2] of integer): real;
        var dau: real; loan:string; nu:boolean; mam:boolean;
            chipheo: array[-1 .. -2] of integer;
            nhi: integer;
        begin
            while nhi>0  do
            begin
                dau:=0;
            end
        end
        function BichMam(): real;
        begin
            return 1.2;
        end"""
        expect = str(FunctionNotReturn('BichNu'))
        self.assertTrue(TestChecker.test(input,expect,475))

    def test_some24(self):
        """Test integer literal"""
        input = """procedure main (); 
        begin
        end
        
        function BichNu(Thino: array[-1 .. -2] of integer): real;
        var dau: real; loan:string; nu:boolean; mam:boolean;
            chipheo: array[-1 .. -2] of integer;
            nhi: integer;
        begin
            while nhi>0 do
            begin
                return dau;
            end
        end
        function BichMam(): real;
        begin
            return 6.9;
        end"""
        expect = str(FunctionNotReturn('BichNu'))
        self.assertTrue(TestChecker.test(input,expect,476))

    def test_some25(self):
        input = """
        procedure main(a:integer);
        begin
            a:=1;
        end"""
        expect = str(NoEntryPoint())
        self.assertTrue(TestChecker.test(input,expect,477))

    def test_some26(self):
        input = """
        procedure main (); 
        begin
        end
        
        function BichNu(Thino: array[-1 .. -2] of integer): real;
        var dau: real; loan:string; nu:boolean; mam:boolean;
            chipheo: array[-1 .. -2] of integer;
            nhi: integer;
        begin
            with
                dau:real; 
                doanxem:integer;
            do
            begin
                if nhi>1 
                    then
                        return nhi;

            end
        end
        function BichMam(): real;
        begin
            return 2;
        end"""
        expect = str(FunctionNotReturn('BichNu'))
        self.assertTrue(TestChecker.test(input,expect,478))

    def test_some27(self):
        input = """
        procedure main (); 
        begin
            break;
        end"""
        expect = str(BreakNotInLoop())
        self.assertTrue(TestChecker.test(input,expect,479))
    def test_some28(self):
        input = """
        procedure main (); 
        begin
        end
        function gt(i : integer): integer;
        begin
            if i <= 1 then 
                break;
        return 1;
        end"""
        expect = str(BreakNotInLoop())
        self.assertTrue(TestChecker.test(input,expect,480))
    def test_some29(self):
        input = """
        procedure main (); 
        begin
            continue;
        end"""
        expect = str(ContinueNotInLoop())
        self.assertTrue(TestChecker.test(input,expect,481))

    def test_some30(self):
        input = """
        procedure main (); 
        begin
        end
        function gt(i : integer): integer;
        begin
            if i <= 1 then 
            begin
                continue;
                return 1;
            end
            else
                retuRn i*gt(i-1);
        end"""
        expect = str(ContinueNotInLoop())

        self.assertTrue(TestChecker.test(input,expect,482))

    def test_some31(self):
        input = """
        function aaa():integer;
		begin
			return 0;
		end
		function foo():integer;
		var i:real;
		begin
			i:=aaa()*2.1*foo();
			return i;
		end
		procedure main();
		var i:integer;
		a:array [1 .. 2] of integer; 
		begin
			while(2>1)do
				return;
		end"""
        expect = str(TypeMismatchInStatement(Return(Id("i"))))
        self.assertTrue(TestChecker.test(input,expect,483))

    def test_some32(self):
        input = """
        function foo(): array [1 .. 2] of real;
               var a,x:REAl;
                    b:array [1 .. 2] of real;
                begin
                    return b;
                end
                procedure main();
                var a,x:REAl;
                    b:array [1 .. 2] of real;
                    c:integer;

                Begin
                    a := b[10] := foo ()[3] := x := 1 ;
                   
                    c := 2/2;
                    return ;
                end
                """       
        expect = str(TypeMismatchInStatement(Assign(Id("c"),BinaryOp("/",IntLiteral(2),IntLiteral(2)))))

        self.assertTrue(TestChecker.test(input, expect, 484))

    def test_some33(self):
        input = """
		function call1(i:integer): array[1 .. -4] of real;
		var a: array[1 .. -4] of real;
		begin
			return a;
		end
		procedure gt(x:boolean);
		begin
			if call1(1)[2] <> 2 then
			begin
				if((call1(1)[1] = 2) and x) then 
					while(call1(1)[1] >= 2 and then call1(1)[2] <= 3) do
					beGin
						with a,b:string; do
							break;
					end
			eND
		end
		procedure main();
		begin
			gt(True);
			gt();
		end
		"""
        expect = str(TypeMismatchInStatement(CallStmt(Id("gt"),
		[])))
        self.assertTrue(TestChecker.test(input, expect, 485))

    def test_some34(self):
        input = """
        procedure Main( ) ;    //1    
         var c: integer;
        begin  c:=1.4; end
        
        function Main1( c: integer) :real;    //1    
        begin   
           if true then 
           begin  
            return 1;
            while true do break;
            end
            return 1;
        end
        """
        expect = str(TypeMismatchInStatement(Assign(Id("c"),FloatLiteral(1.4))))

        self.assertTrue(TestChecker.test(input, expect, 486))

    def test_some35(self):
        input = """
        procedure main();
        begin
        end
        procedure a();
        begin
        end
        function foo(a, b: integer ; c: real): integer ;
        BEGIN
            a();
        return 1;
        END"""
        expect = str(Undeclared(Procedure(),'a'))

        self.assertTrue(TestChecker.test(input, expect, 487))

    def test_some36(self):
	    """Simple program: int main() {} """
	    input = """
                    function foo(i:integer):real;
                    begin
                        for i:=1 to 2 do
                        begin
                            return i;
                        end
                        return i;
                    end
                    procedure main();
                                var i:integer;
                                begin
                                    i:=foo(i);
                                    while(2>1)do
                                        return;
                                end
				"""
	    expect = str(TypeMismatchInStatement(Assign(Id("i"),CallExpr(Id("foo"),
			[Id("i")]))))
	    self.assertTrue(TestChecker.test(input,expect,488))

    def test_some37(self):
        input = """
        var a, b: integer; c: real;
        var f: array [1 .. 5] of integer;
        function foo(x: integer; c: real): real;
            var a, b: integer; n: real;
            begin
                with s:boolean; do 
                    return 5;
            end
        procedure main(); 
            begin
                for a:=1 to 5 do
                    for b:=8 downto 2 do
                        a:=2;
                        for b:=1 to 9 do
                            begin
                            end
                foo(a, b);
            end
        """
        expect = str(Undeclared(Procedure(),'foo'))
        self.assertTrue(TestChecker.test(input,expect,489))

    def test_some38(self):
        input = """procedure main();
        var a: real;
            b: integer;
        begin
            if a + b then return;
        end"""
        expect = str(TypeMismatchInStatement(If(BinaryOp("+",Id("a"),Id("b")),[Return()],[])))
        self.assertTrue(TestChecker.test(input, expect, 490))

    def test_some39(self):
        input = """procedure main();
        var a: real;
        begin
            for a := 2.2 to 5.5 do
                a := a + 1; 
        end"""
        ast = For(Id("a"),FloatLiteral(2.2),FloatLiteral(5.5),True,[Assign(Id("a"),BinaryOp("+",Id("a"),IntLiteral(1)))])

        expect = str(TypeMismatchInStatement(For(Id("a"),FloatLiteral(2.2),FloatLiteral(5.5),True,[Assign(Id("a"),BinaryOp("+",Id("a"),IntLiteral(1)))])))
        self.assertTrue(TestChecker.test(input, expect, 491))

    def test_some40(self):
        input = """procedure main();
        var a: integer;
        begin
            while a do
                a := a + 1;
        end"""
        expect = str(TypeMismatchInStatement(While(Id("a"),[Assign(Id("a"),BinaryOp("+",Id("a"),IntLiteral(1)))])))
        self.assertTrue(TestChecker.test(input, expect, 492))

    def test_some41(self):
        input = """procedure foo(a: integer; b:real);
        begin
        end
        procedure main();
        var x,y: real;
        begin
            foo(x,y);
        end"""
        expect = str(TypeMismatchInStatement(CallStmt(Id("foo"),[Id("x"),Id("y")])))
        self.assertTrue(TestChecker.test(input, expect, 493))

    def test_some42(self):
        input = """procedure main();
        var a: integer;
            b: real;
        begin
            for a := 1 to b do
                a := a + 1; 
        end"""
        ast = For(Id("a"),IntLiteral(1),Id("b"),True,[Assign(Id("a"),BinaryOp("+",Id("a"),IntLiteral(1)))])

        expect =str(TypeMismatchInStatement(ast))
        self.assertTrue(TestChecker.test(input, expect, 494))

    def test_some43(self):
        input = """procedure main();
        var arr: array [1 .. 5] of real;
            a, b: real;
        begin
            a := b + arr[1.2];
        end"""
        expect = str(TypeMismatchInExpression(ArrayCell(Id("arr"),FloatLiteral(1.2))))
        self.assertTrue(TestChecker.test(input, expect, 495))

    def test_some44(self):
        input = """procedure main();
        var a,b,c:real;
        begin
            a := b + c[1];
        end"""
        expect = str(TypeMismatchInExpression(ArrayCell(Id("c"),IntLiteral(1))))
        self.assertTrue(TestChecker.test(input, expect, 496))

    def test_some45(self):
        input = """procedure main();
        var a: boolean;
            b,c: real;
            d: integer;
        begin
            b := c + d + a;
        end"""
        expect = str(TypeMismatchInExpression(BinaryOp("+",BinaryOp("+",Id("c"),Id("d")),Id("a"))))
        self.assertTrue(TestChecker.test(input, expect, 497))

    def test_some46(self):
        input = """procedure main();
        var a,b,c:integer;
        begin
            a := b mod not c;
        end"""
        expect = str(TypeMismatchInExpression(UnaryOp("not",Id("c"))))
        self.assertTrue(TestChecker.test(input, expect, 498))

    def test_some47(self):
        input = """procedure main();
        var a: boolean;
            b,c: integer;
        begin
            b := c div -a;
        end"""
        expect = str(TypeMismatchInExpression(UnaryOp("-",Id("a"))))
        self.assertTrue(TestChecker.test(input, expect, 499))
   
