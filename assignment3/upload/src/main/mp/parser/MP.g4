//1610342
//Bui Bao Cuong

grammar MP;

@lexer::header {
from lexererr import *
}

options{
	language=Python3;
}

//Program entry point

program  : decl+ EOF;

//
decl : vardecl | funcdecl | procdecl;

//------------------------------------------Main entry point-------------------------------

//entry_decl : PROCEDURE MAIN LB RB SEMI compstmt ;

//-------------------------------------------Type------------------------------------------

mptype: primtype | comptype ;

primtype : INTEGER | BOOLEAN | REAL | STRING ;

signint : SUBOP? INTLIT ;

comptype : ARRAY LSB signint DDOT signint RSB OF primtype ;

// // [ x..y ]  space ??
// type_decl: primtype | comptype  //Fix this to integer exp

//--------------------------------------------Var declaration----------------------------------

idlst : ID (COMMA ID)* ;

param : idlst COLON mptype ;

vardecl : VAR paramlst SEMI;

//---------------------------------------------Function declaration----------------------------
paramlst : param (SEMI param)* ;

funcdecl : FUNCTION ID LB paramlst? RB COLON mptype SEMI vardecl? compstmt ;

//Procedure

procdecl : PROCEDURE ID LB paramlst? RB SEMI vardecl? compstmt ;

WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines

//---------------------------------------------Expression----------------------------
exp : exp (ANDOP THEN| OROP ELSE) exp1 | exp1;
exp1: exp2 (EQOP|NEOP|LTOP|LEOP|GTOP|GEOP) exp2 | exp2;
exp2: exp2 (ADDOP|SUBOP|OROP) exp3 | exp3;
exp3: exp3 (DIVOP|MULOP|MODOP|ANDOP|DIVIDEOP) exp4 | exp4;
exp4: <assoc = right> (SUBOP | NOTOP) exp4 | exp5;
exp5: LB exp RB | ID | INTLIT | BOOLIT | REALIT | STRINGLIT | invocastmt | idxexp ;

arglst : exp (COMMA exp)* ;

invocastmt : ID LB arglst? RB ; 

idxexp: (ID | invocastmt) LSB exp RSB ;
//---------------------------------------------Statement----------------------------
stmt 
    : assignstmt 
    | ifstmt 
    | whilestmt 
    | forstmt 
    | breakstmt 
    | continuestmt
    | returnstmt
    | compstmt
    | withstmt
    | callstmt 
    ;

stmtlst : stmt+;

scavar : idxexp | ID ;

assignstmt : (scavar ASSIGN)+ exp SEMI ; 

callstmt : ID LB arglst? RB SEMI;

ifstmt : IF exp THEN stmt (ELSE stmt)? ;

whilestmt : WHILE exp DO stmt ;

forstmt : FOR ID ASSIGN exp (TO|DOWNTO) exp DO stmt ; 

breakstmt : BREAK SEMI ;

continuestmt : CONTINUE SEMI ;

returnstmt : RETURN exp? SEMI ;

compstmt : BEGIN stmtlst? END ;

withstmt : WITH paramlst SEMI DO stmt ;


//Comment
// .*? matches anything until the first */
fragment COMMENT1 : '(*' .*? '*)' ; 
fragment COMMENT2 : '{' .*? '}' ;
fragment COMMENT3 : '//' ~[\r\n]* ; 

//Note nested comment

COMMENT: (COMMENT1|COMMENT2|COMMENT3) -> skip ;


//Fragment to use case-insensitive
fragment A : [aA]; // match either an 'a' or 'A'
fragment B : [bB];
fragment C : [cC];
fragment D : [dD];
fragment E : [eE];
fragment F : [fF];
fragment G : [gG];
fragment H : [hH];
fragment I : [iI];
fragment J : [jJ];
fragment K : [kK];
fragment L : [lL];
fragment M : [mM];
fragment N : [nN];
fragment O : [oO];
fragment P : [pP];
fragment Q : [qQ];
fragment R : [rR];
fragment S : [sS];
fragment T : [tT];
fragment U : [uU];
fragment V : [vV];
fragment W : [wW];
fragment X : [xX];
fragment Y : [yY];
fragment Z : [zZ];

//Keywords

WITH : W I T H ;

BREAK : B R E A K ;

CONTINUE : C O N T I N U E ;

FOR : F O R ;

TO : T O ;

DOWNTO : D O W N T O ;

DO : D O ;

IF : I F ;

THEN : T H E N ;

ELSE : E L S E ;

RETURN : R E T U R N ;

WHILE : W H I L E ;

BEGIN : B E G I N ;

END : E N D ;

FUNCTION : F U N C T I O N ;

PROCEDURE : P R O C E D U R E ;

VAR : V A R ;

ARRAY : A R R A Y ;

OF : O F ;

REAL : R E A L ;

BOOLEAN : B O O L E A N ;

INTEGER : I N T E G E R ;

STRING : S T R I N G ;

//MAIN : M A I N ;
//Operator
ADDOP : '+' ;

MULOP : '*' ;

SUBOP : '-' ;

DIVIDEOP : '/';

NOTOP : N O T ;

ANDOP : A N D ;

OROP : O R ;

DIVOP : D I V ;

MODOP : M O D ;

NEOP : '<>' ;

LTOP : '<' ;

LEOP : '<=' ;

EQOP : '=' ;

GTOP : '>' ;

GEOP : '>=' ;

ASSIGN : ':=' ;
//Separator

LSB : '[' ;

RSB : ']' ;

COLON : ':' ;

COMMA : ',' ;

DDOT : '..' ;

LB: '(' ;

RB: ')' ;

SEMI: ';' ;

//Literials

INTLIT: [0-9]+;

fragment TRUE : T R U E ;

fragment FALSE : F A L S E ;

BOOLIT : TRUE | FALSE ;

//Identifiers
fragment Char : (A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z) ;
ID : ('_'|Char)('_'|Char|[0-9])* ;

fragment EXP : E '-'?[0-9]+ ;

REALIT 
    : ([0-9]+)( EXP | '.'([0-9]*EXP?)? ) 
    | '.'[0-9]+EXP?  ;


fragment EscapeSequence : '\\' [btnfr"'\\] ;

STRINGLIT
    : '"' (~[\b\t\r\n\f\\'"] | EscapeSequence)* '"'
    {self.text = self.text[1:-1]}
    ;

UNCLOSE_STRING
    : '"' (EscapeSequence | ~[\b\t\r\n\f\\'"])*  
    {raise UncloseString(self.text[1:])}
    ;

//Get from the internet,fix the output
ILLEGAL_ESCAPE
    : UNCLOSE_STRING '\\' ~[btnfr"'\\] 
    //'"' .*? ('\\' ~[btnfr"'\\])* .*? '"'
    {    
        temp=Lexer.text.fget(self)
        temp1=temp[1:len(temp)]
        temp2=temp1[0:temp1.find("\\")+2]
        raise IllegalEscape(temp2)
    }
    ;

// ILLEGAL_ESCAPE
//     : UNCLOSE_STRING '\\' ~[btnfr"'\\]
//     {raise IllegalEscape(self.text[1:])}
//     ;

ERROR_CHAR: .{raise ErrorToken(self.text)};
