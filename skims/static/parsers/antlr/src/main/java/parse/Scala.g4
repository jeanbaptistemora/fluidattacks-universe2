/*
 [The "BSD licence"]
 Copyright (c) 2014 Leonardo Lucena
 Copyright (c) 2018 Andrey Stolyarov
 All rights reserved.

 Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions
 are met:
 1. Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.
 2. Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.
 3. The name of the author may not be used to endorse or promote products
    derived from this software without specific prior written permission.

 THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
 IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
 INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
 THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/
/*
   Derived from https://github.com/scala/scala/blob/2.12.x/spec/13-syntax-summary.md
 */

grammar Scala;

literal
   : '-'? IntegerLiteral
   | '-'? FloatingPointLiteral
   | BooleanLiteral
   | CharacterLiteral
   | StringLiteral
   | SymbolLiteral
   | 'null'
   ;

qualId
   : Id ('.' Id)*
   ;

ids
   : Id (',' Id)*
   ;

stableId
   : Id
   | stableId '.' Id
   | (Id '.')? ('this' | 'super' classQualifier? '.' Id)
   ;

classQualifier
   : '[' Id ']'
   ;

type_
   : functionArgTypes '=>' type_
   | infixType existentialClause?
   ;

functionArgTypes
   : infixType
   | '(' (paramType (',' paramType)*)? ')'
   ;

existentialClause
   : 'forSome' '{' existentialDcl+ '}'
   ;

existentialDcl
   : 'type' typeDcl
   | 'val' valDcl
   ;

infixType
   : compoundType (Id compoundType)*
   ;

compoundType
   : annotType ('with' annotType)* refinement?
   | refinement
   ;

annotType
   : simpleType annotation*
   ;

simpleType
   : simpleType typeArgs
   | simpleType '#' Id
   | stableId ('.' 'type')?
   | '(' types ')'
   ;

typeArgs
   : '[' types ']'
   ;

types
   : type_ (',' type_)*
   ;

refinement
   : NL? '{' refineStat+ '}'
   ;

refineStat
   : dcl
   | 'type' typeDef
   ;

typePat
   : type_
   ;

ascription
   : ':' infixType
   | ':' annotation +
   | ':' '_' '*'
   ;

expr
   : (bindings | 'implicit'? Id | '_') '=>' expr
   | expr1
   ;

expr1
   : 'if' '(' expr ')' NL* expr ('else' expr)?
   | 'while' '(' expr ')' NL* expr
   | 'try' expr ('catch' expr)? ('finally' expr)?
   | 'do' expr 'while' '(' expr ')'
   | 'for' ('(' enumerators ')' | '{' enumerators '}') 'yield'? expr
   | 'throw' expr
   | 'return' expr?
   | ((simpleExpr | simpleExpr1 '_'?) '.')? Id '=' expr
   | simpleExpr1 argumentExprs '=' expr
   | postfixExpr ascription?
   | postfixExpr 'match' '{' caseClauses '}'
   ;

prefixDef
   : '-' | '+' | '~' | '!'
   ;

postfixExpr
   : infixExpr Id? (prefixDef simpleExpr1)* NL?
   ;

infixExpr
   : prefixExpr
   | infixExpr Id NL? infixExpr
   ;

prefixExpr
   : prefixDef? (simpleExpr | simpleExpr1 '_'?)
   ;

simpleExpr
   : 'new' (classTemplate | templateBody)
   | blockExpr
   ;

// Dublicate lines to prevent left-recursive code.
// can't use (simpleExpr|simpleExpr1) '.' Id
simpleExpr1
   : literal
   | stableId
   | '_'
   | '(' exprs? ')'
   | simpleExpr '.' Id
   | simpleExpr1 '_'?  '.' Id
   | simpleExpr  typeArgs
   | simpleExpr1 '_'? typeArgs
   | simpleExpr1 argumentExprs
   ;

exprs
   : expr (',' expr)*
   ;

argumentExprs
   : '(' exprs? ')'
   | '(' (exprs ',')? postfixExpr ':' '_' '*' ')'
   | NL? blockExpr
   ;

blockExpr
   : '{' caseClauses '}'
   | '{' block '}'
   ;

block
   : blockStat+ resultExpr?
   ;

blockStat
   : import_
   | annotation* ('implicit' | 'lazy')? def
   | annotation* localModifier* tmplDef
   | expr1
   ;

resultExpr
   : expr1
   | (bindings | ('implicit'? Id | '_') ':' compoundType) '=>' block
   ;

enumerators
   : generator+
   ;

generator
   : pattern1 '<-' expr (guard | pattern1 '=' expr)*
   ;

caseClauses
   : caseClause +
   ;

caseClause
   : 'case' pattern guard? '=>' block
   ;

guard
   : 'if' postfixExpr
   ;

pattern
   : pattern1 ('|' pattern1)*
   ;

pattern1
   : (BoundVarid| '_' | Id) ':' typePat
   | pattern2
   ;

pattern2
   : Id ('@' pattern3)?
   | pattern3
   ;

pattern3
   : simplePattern
   | simplePattern (Id NL? simplePattern)*
   ;

simplePattern
   : '_'
   | Varid
   | literal
   | stableId ('(' patterns? ')')?
   | stableId '(' (patterns ',')? (Id '@')? '_' '*' ')'
   | '(' patterns? ')'
   ;

patterns
   : pattern (',' patterns)?
   | '_' '*'
   ;

typeParamClause
   : '[' variantTypeParam (',' variantTypeParam)* ']'
   ;

funTypeParamClause
   : '[' typeParam (',' typeParam)* ']'
   ;

variantTypeParam
   : annotation* ('+' | '-')? typeParam
   ;

typeParam
   : (Id | '_') typeParamClause? ('>:' type_)? ('<:' type_)? ('<%' type_)* (':' type_)*
   ;

paramClauses
   : paramClause* (NL? '(' 'implicit' params ')')?
   ;

paramClause
   : NL? '(' params? ')'
   ;

params
   : param (',' param)*
   ;

param
   : annotation* Id (':' paramType)? ('=' expr)?
   ;

paramType
   : type_
   | '=>' type_
   | type_ '*'
   ;

classParamClauses
   : classParamClause* (NL? '(' 'implicit' classParams ')')?
   ;

classParamClause
   : NL? '(' classParams? ')'
   ;

classParams
   : classParam (',' classParam)*
   ;

classParam
   : annotation* modifier* ('val' | 'var')? Id ':' paramType ('=' expr)?
   ;

bindings
   : '(' binding (',' binding)* ')'
   ;

binding
   : (Id | '_') (':' type_)?
   ;

modifier
   : localModifier
   | accessModifier
   | 'override'
   ;

localModifier
   : 'abstract'
   | 'final'
   | 'sealed'
   | 'implicit'
   | 'lazy'
   ;

accessModifier
   : ('private' | 'protected') accessQualifier?
   ;

accessQualifier
   : '[' (Id | 'this') ']'
   ;

annotation
   : '@' simpleType argumentExprs*
   ;

constrAnnotation
   : '@' simpleType argumentExprs
   ;

templateBody
   : NL? '{' selfType? templateStat+ '}'
   ;

templateStat
   : import_
   | (annotation NL?)* modifier* def
   | (annotation NL?)* modifier* dcl
   | expr
   ;

selfType
   : Id (':' type_)? '=>'
   | 'this' ':' type_ '=>'
   ;

import_
   : 'import' importExpr (',' importExpr)*
   ;

importExpr
   : stableId ('.' (Id | '_' | importSelectors))?
   ;

importSelectors
   : '{' (importSelector ',')* (importSelector | '_') '}'
   ;

importSelector
   : Id ('=>' (Id | '_'))?
   ;

dcl
   : 'val' valDcl
   | 'var' varDcl
   | 'def' funDcl
   | 'type' NL* typeDcl
   ;

valDcl
   : ids ':' type_
   ;

varDcl
   : ids ':' type_
   ;

funDcl
   : funSig (':' type_)?
   ;

funSig
   : Id funTypeParamClause? paramClauses
   ;

typeDcl
   : Id typeParamClause? ('>:' type_)? ('<:' type_)?
   ;

patVarDef
   : 'val' patDef
   | 'var' varDef
   ;

def
   : patVarDef
   | 'def' funDef
   | 'type' NL* typeDef
   | tmplDef
   ;

patDef
   : pattern2 (',' pattern2)* (':' type_)? '=' expr
   ;

varDef
   : patDef
   | ids ':' type_ '=' '_'
   ;

funDef
   : funSig (':' type_)? '=' expr
   | funSig NL? '{' block '}'
   | 'this' paramClause paramClauses ('=' constrExpr | NL? constrBlock)
   ;

typeDef
   : Id typeParamClause? '=' type_
   ;

tmplDef
   : 'case'? 'class' classDef
   | 'case'? 'object' objectDef
   | 'trait' traitDef
   ;

classDef
   : Id typeParamClause? constrAnnotation* accessModifier? classParamClauses classTemplateOpt
   ;

traitDef
   : Id typeParamClause? traitTemplateOpt
   ;

objectDef
   : Id classTemplateOpt
   ;

classTemplateOpt
   : 'extends' classTemplate
   | ('extends'? templateBody)?
   ;

traitTemplateOpt
   : 'extends' traitTemplate
   | ('extends'? templateBody)?
   ;

classTemplate
   : earlyDefs? classParents templateBody?
   ;

traitTemplate
   : earlyDefs? traitParents templateBody?
   ;

classParents
   : constr ('with' annotType)*
   ;

traitParents
   : annotType ('with' annotType)*
   ;

constr
   : annotType argumentExprs*
   ;

earlyDefs
   : '{' earlyDef+ '}' 'with'
   ;

earlyDef
   : (annotation NL?)* modifier* patVarDef
   ;

constrExpr
   : selfInvocation
   | constrBlock
   ;

constrBlock
   : '{' selfInvocation (blockStat)* '}'
   ;

selfInvocation
   : 'this' argumentExprs +
   ;

topStatSeq
   : topStat+
   ;

topStat
   : (annotation NL?)* modifier* tmplDef
   | import_
   | packaging
   | packageObject
   ;

packaging
   : 'package' qualId  NL? '{' topStatSeq '}'
   ;

packageObject
   : 'package' 'object' objectDef
   ;


compilationUnit
   : ('package' qualId)* topStatSeq
   ;

// Lexer


Id
   : Plainid
   | '`' (CharNoBackQuoteOrNewline | UnicodeEscape | CharEscapeSeq )+ '`'
   ;


BooleanLiteral
   : 'true' | 'false'
   ;


CharacterLiteral
   : '\'' (PrintableChar | CharEscapeSeq) '\''
   ;


SymbolLiteral
   : '\'' Plainid
   ;


IntegerLiteral
   : (DecimalNumeral | HexNumeral) ('L' | 'l')?
   ;


StringLiteral
   : '"' StringElement* '"' | '"""' MultiLineChars '"""'
   ;

FloatingPointLiteral
   : Digit + '.' Digit + ExponentPart? FloatType? | '.' Digit + ExponentPart? FloatType? | Digit ExponentPart FloatType? | Digit + ExponentPart? FloatType
   ;


Varid
   : Lower Idrest
   ;

BoundVarid
   : Varid
   | '`' Varid '`'
   ;
Paren
   : '(' | ')' | '[' | ']' | '{' | '}'
   ;


Delim
   : '`' | '\'' | '"' | '.' | ';' | ','
   ;

Semi
   : (';' | (NL)+) -> skip
   ;

NL
   : '\n'
   | '\r' '\n'?
   ;


// \u0020-\u0026 """ !"#$%"""
// \u0028-\u007E """()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"""
fragment CharNoBackQuoteOrNewline
   : [\u0020-\u0026\u0028-\u007E]
   ;

// fragments

fragment UnicodeEscape
   : '\\' 'u' 'u'? HexDigit HexDigit HexDigit HexDigit
   ;


fragment WhiteSpace
   : '\u0020' | '\u0009' | '\u000D' | '\u000A'
   ;


fragment Opchar
   : '!' | '#' | '%' | '&' | '*' | '+' | '-' | ':' | '<' | '=' | '>' | '?' | '@' | '\\' | '^' | '|' | '~'
   ;


fragment Op
   : '/'? Opchar +
   ;


fragment Idrest
   : (Letter | Digit)* ('_' Op)?
   ;


fragment StringElement
   : '\u0020' | '\u0021' | '\u0023' .. '\u007F' | CharEscapeSeq
   ;


fragment MultiLineChars
   : (StringElement | NL) *
   ;


fragment HexDigit
   : '0' .. '9' | 'A' .. 'F' | 'a' .. 'f'
   ;


fragment FloatType
   : 'F' | 'f' | 'D' | 'd'
   ;


fragment Upper
   : 'A' .. 'Z' | '$' | '_' | UnicodeClass_LU
   ;


fragment Lower
   : 'a' .. 'z' | UnicodeClass_LL
   ;


fragment Letter
   : Upper | Lower | UnicodeClass_LO | UnicodeClass_LT // TODO Add category Nl
   ;

// and Unicode categories Lo, Lt, Nl

fragment ExponentPart
   : ('E' | 'e') ('+' | '-')? Digit +
   ;


fragment PrintableChar
   : '\u0020' .. '\u007F'
   ;

fragment PrintableCharExceptWhitespace
   : '\u0021' .. '\u007F'
   ;


fragment CharEscapeSeq
   : '\\' ('b' | 't' | 'n' | 'f' | 'r' | '"' | '\'' | '\\')
   ;


fragment DecimalNumeral
   : '0' | NonZeroDigit Digit*
   ;


fragment HexNumeral
   : '0' 'x' HexDigit HexDigit +
   ;


fragment Digit
   : '0' | NonZeroDigit
   ;


fragment NonZeroDigit
   : '1' .. '9'
   ;


fragment VaridFragment
   : Varid
   ;


fragment Plainid
   : Upper Idrest | Lower Idrest | Op
   ;


//
// Unicode categories
// https://github.com/antlr/grammars-v4/blob/master/stringtemplate/LexUnicode.g4
//

fragment UnicodeLetter
   : UnicodeClass_LU
   | UnicodeClass_LL
   | UnicodeClass_LT
   | UnicodeClass_LM
   | UnicodeClass_LO
   ;

fragment UnicodeClass_LU
   : '\u0041'..'\u005a'
   | '\u00c0'..'\u00d6'
   | '\u00d8'..'\u00de'
   | '\u0100'..'\u0136'
   | '\u0139'..'\u0147'
   | '\u014a'..'\u0178'
   | '\u0179'..'\u017d'
   | '\u0181'..'\u0182'
   | '\u0184'..'\u0186'
   | '\u0187'..'\u0189'
   | '\u018a'..'\u018b'
   | '\u018e'..'\u0191'
   | '\u0193'..'\u0194'
   | '\u0196'..'\u0198'
   | '\u019c'..'\u019d'
   | '\u019f'..'\u01a0'
   | '\u01a2'..'\u01a6'
   | '\u01a7'..'\u01a9'
   | '\u01ac'..'\u01ae'
   | '\u01af'..'\u01b1'
   | '\u01b2'..'\u01b3'
   | '\u01b5'..'\u01b7'
   | '\u01b8'..'\u01bc'
   | '\u01c4'..'\u01cd'
   | '\u01cf'..'\u01db'
   | '\u01de'..'\u01ee'
   | '\u01f1'..'\u01f4'
   | '\u01f6'..'\u01f8'
   | '\u01fa'..'\u0232'
   | '\u023a'..'\u023b'
   | '\u023d'..'\u023e'
   | '\u0241'..'\u0243'
   | '\u0244'..'\u0246'
   | '\u0248'..'\u024e'
   | '\u0370'..'\u0372'
   | '\u0376'..'\u037f'
   | '\u0386'..'\u0388'
   | '\u0389'..'\u038a'
   | '\u038c'..'\u038e'
   | '\u038f'..'\u0391'
   | '\u0392'..'\u03a1'
   | '\u03a3'..'\u03ab'
   | '\u03cf'..'\u03d2'
   | '\u03d3'..'\u03d4'
   | '\u03d8'..'\u03ee'
   | '\u03f4'..'\u03f7'
   | '\u03f9'..'\u03fa'
   | '\u03fd'..'\u042f'
   | '\u0460'..'\u0480'
   | '\u048a'..'\u04c0'
   | '\u04c1'..'\u04cd'
   | '\u04d0'..'\u052e'
   | '\u0531'..'\u0556'
   | '\u10a0'..'\u10c5'
   | '\u10c7'..'\u10cd'
   | '\u1e00'..'\u1e94'
   | '\u1e9e'..'\u1efe'
   | '\u1f08'..'\u1f0f'
   | '\u1f18'..'\u1f1d'
   | '\u1f28'..'\u1f2f'
   | '\u1f38'..'\u1f3f'
   | '\u1f48'..'\u1f4d'
   | '\u1f59'..'\u1f5f'
   | '\u1f68'..'\u1f6f'
   | '\u1fb8'..'\u1fbb'
   | '\u1fc8'..'\u1fcb'
   | '\u1fd8'..'\u1fdb'
   | '\u1fe8'..'\u1fec'
   | '\u1ff8'..'\u1ffb'
   | '\u2102'..'\u2107'
   | '\u210b'..'\u210d'
   | '\u2110'..'\u2112'
   | '\u2115'..'\u2119'
   | '\u211a'..'\u211d'
   | '\u2124'..'\u212a'
   | '\u212b'..'\u212d'
   | '\u2130'..'\u2133'
   | '\u213e'..'\u213f'
   | '\u2145'..'\u2183'
   | '\u2c00'..'\u2c2e'
   | '\u2c60'..'\u2c62'
   | '\u2c63'..'\u2c64'
   | '\u2c67'..'\u2c6d'
   | '\u2c6e'..'\u2c70'
   | '\u2c72'..'\u2c75'
   | '\u2c7e'..'\u2c80'
   | '\u2c82'..'\u2ce2'
   | '\u2ceb'..'\u2ced'
   | '\u2cf2'..'\ua640'
   | '\ua642'..'\ua66c'
   | '\ua680'..'\ua69a'
   | '\ua722'..'\ua72e'
   | '\ua732'..'\ua76e'
   | '\ua779'..'\ua77d'
   | '\ua77e'..'\ua786'
   | '\ua78b'..'\ua78d'
   | '\ua790'..'\ua792'
   | '\ua796'..'\ua7aa'
   | '\ua7ab'..'\ua7ad'
   | '\ua7b0'..'\ua7b1'
   | '\uff21'..'\uff3a'
   ;

fragment UnicodeClass_LL
   : '\u0061'..'\u007A'
   | '\u00b5'..'\u00df'
   | '\u00e0'..'\u00f6'
   | '\u00f8'..'\u00ff'
   | '\u0101'..'\u0137'
   | '\u0138'..'\u0148'
   | '\u0149'..'\u0177'
   | '\u017a'..'\u017e'
   | '\u017f'..'\u0180'
   | '\u0183'..'\u0185'
   | '\u0188'..'\u018c'
   | '\u018d'..'\u0192'
   | '\u0195'..'\u0199'
   | '\u019a'..'\u019b'
   | '\u019e'..'\u01a1'
   | '\u01a3'..'\u01a5'
   | '\u01a8'..'\u01aa'
   | '\u01ab'..'\u01ad'
   | '\u01b0'..'\u01b4'
   | '\u01b6'..'\u01b9'
   | '\u01ba'..'\u01bd'
   | '\u01be'..'\u01bf'
   | '\u01c6'..'\u01cc'
   | '\u01ce'..'\u01dc'
   | '\u01dd'..'\u01ef'
   | '\u01f0'..'\u01f3'
   | '\u01f5'..'\u01f9'
   | '\u01fb'..'\u0233'
   | '\u0234'..'\u0239'
   | '\u023c'..'\u023f'
   | '\u0240'..'\u0242'
   | '\u0247'..'\u024f'
   | '\u0250'..'\u0293'
   | '\u0295'..'\u02af'
   | '\u0371'..'\u0373'
   | '\u0377'..'\u037b'
   | '\u037c'..'\u037d'
   | '\u0390'..'\u03ac'
   | '\u03ad'..'\u03ce'
   | '\u03d0'..'\u03d1'
   | '\u03d5'..'\u03d7'
   | '\u03d9'..'\u03ef'
   | '\u03f0'..'\u03f3'
   | '\u03f5'..'\u03fb'
   | '\u03fc'..'\u0430'
   | '\u0431'..'\u045f'
   | '\u0461'..'\u0481'
   | '\u048b'..'\u04bf'
   | '\u04c2'..'\u04ce'
   | '\u04cf'..'\u052f'
   | '\u0561'..'\u0587'
   | '\u1d00'..'\u1d2b'
   | '\u1d6b'..'\u1d77'
   | '\u1d79'..'\u1d9a'
   | '\u1e01'..'\u1e95'
   | '\u1e96'..'\u1e9d'
   | '\u1e9f'..'\u1eff'
   | '\u1f00'..'\u1f07'
   | '\u1f10'..'\u1f15'
   | '\u1f20'..'\u1f27'
   | '\u1f30'..'\u1f37'
   | '\u1f40'..'\u1f45'
   | '\u1f50'..'\u1f57'
   | '\u1f60'..'\u1f67'
   | '\u1f70'..'\u1f7d'
   | '\u1f80'..'\u1f87'
   | '\u1f90'..'\u1f97'
   | '\u1fa0'..'\u1fa7'
   | '\u1fb0'..'\u1fb4'
   | '\u1fb6'..'\u1fb7'
   | '\u1fbe'..'\u1fc2'
   | '\u1fc3'..'\u1fc4'
   | '\u1fc6'..'\u1fc7'
   | '\u1fd0'..'\u1fd3'
   | '\u1fd6'..'\u1fd7'
   | '\u1fe0'..'\u1fe7'
   | '\u1ff2'..'\u1ff4'
   | '\u1ff6'..'\u1ff7'
   | '\u210a'..'\u210e'
   | '\u210f'..'\u2113'
   | '\u212f'..'\u2139'
   | '\u213c'..'\u213d'
   | '\u2146'..'\u2149'
   | '\u214e'..'\u2184'
   | '\u2c30'..'\u2c5e'
   | '\u2c61'..'\u2c65'
   | '\u2c66'..'\u2c6c'
   | '\u2c71'..'\u2c73'
   | '\u2c74'..'\u2c76'
   | '\u2c77'..'\u2c7b'
   | '\u2c81'..'\u2ce3'
   | '\u2ce4'..'\u2cec'
   | '\u2cee'..'\u2cf3'
   | '\u2d00'..'\u2d25'
   | '\u2d27'..'\u2d2d'
   | '\ua641'..'\ua66d'
   | '\ua681'..'\ua69b'
   | '\ua723'..'\ua72f'
   | '\ua730'..'\ua731'
   | '\ua733'..'\ua771'
   | '\ua772'..'\ua778'
   | '\ua77a'..'\ua77c'
   | '\ua77f'..'\ua787'
   | '\ua78c'..'\ua78e'
   | '\ua791'..'\ua793'
   | '\ua794'..'\ua795'
   | '\ua797'..'\ua7a9'
   | '\ua7fa'..'\uab30'
   | '\uab31'..'\uab5a'
   | '\uab64'..'\uab65'
   | '\ufb00'..'\ufb06'
   | '\ufb13'..'\ufb17'
   | '\uff41'..'\uff5a'
   ;

fragment UnicodeClass_LT
   : '\u01c5'..'\u01cb'
   | '\u01f2'..'\u1f88'
   | '\u1f89'..'\u1f8f'
   | '\u1f98'..'\u1f9f'
   | '\u1fa8'..'\u1faf'
   | '\u1fbc'..'\u1fcc'
   | '\u1ffc'..'\u1ffc'
   ;

fragment UnicodeClass_LM
   : '\u02b0'..'\u02c1'
   | '\u02c6'..'\u02d1'
   | '\u02e0'..'\u02e4'
   | '\u02ec'..'\u02ee'
   | '\u0374'..'\u037a'
   | '\u0559'..'\u0640'
   | '\u06e5'..'\u06e6'
   | '\u07f4'..'\u07f5'
   | '\u07fa'..'\u081a'
   | '\u0824'..'\u0828'
   | '\u0971'..'\u0e46'
   | '\u0ec6'..'\u10fc'
   | '\u17d7'..'\u1843'
   | '\u1aa7'..'\u1c78'
   | '\u1c79'..'\u1c7d'
   | '\u1d2c'..'\u1d6a'
   | '\u1d78'..'\u1d9b'
   | '\u1d9c'..'\u1dbf'
   | '\u2071'..'\u207f'
   | '\u2090'..'\u209c'
   | '\u2c7c'..'\u2c7d'
   | '\u2d6f'..'\u2e2f'
   | '\u3005'..'\u3031'
   | '\u3032'..'\u3035'
   | '\u303b'..'\u309d'
   | '\u309e'..'\u30fc'
   | '\u30fd'..'\u30fe'
   | '\ua015'..'\ua4f8'
   | '\ua4f9'..'\ua4fd'
   | '\ua60c'..'\ua67f'
   | '\ua69c'..'\ua69d'
   | '\ua717'..'\ua71f'
   | '\ua770'..'\ua788'
   | '\ua7f8'..'\ua7f9'
   | '\ua9cf'..'\ua9e6'
   | '\uaa70'..'\uaadd'
   | '\uaaf3'..'\uaaf4'
   | '\uab5c'..'\uab5f'
   | '\uff70'..'\uff9e'
   | '\uff9f'..'\uff9f'
   ;

fragment UnicodeClass_LO
   : '\u00aa'..'\u00ba'
   | '\u01bb'..'\u01c0'
   | '\u01c1'..'\u01c3'
   | '\u0294'..'\u05d0'
   | '\u05d1'..'\u05ea'
   | '\u05f0'..'\u05f2'
   | '\u0620'..'\u063f'
   | '\u0641'..'\u064a'
   | '\u066e'..'\u066f'
   | '\u0671'..'\u06d3'
   | '\u06d5'..'\u06ee'
   | '\u06ef'..'\u06fa'
   | '\u06fb'..'\u06fc'
   | '\u06ff'..'\u0710'
   | '\u0712'..'\u072f'
   | '\u074d'..'\u07a5'
   | '\u07b1'..'\u07ca'
   | '\u07cb'..'\u07ea'
   | '\u0800'..'\u0815'
   | '\u0840'..'\u0858'
   | '\u08a0'..'\u08b2'
   | '\u0904'..'\u0939'
   | '\u093d'..'\u0950'
   | '\u0958'..'\u0961'
   | '\u0972'..'\u0980'
   | '\u0985'..'\u098c'
   | '\u098f'..'\u0990'
   | '\u0993'..'\u09a8'
   | '\u09aa'..'\u09b0'
   | '\u09b2'..'\u09b6'
   | '\u09b7'..'\u09b9'
   | '\u09bd'..'\u09ce'
   | '\u09dc'..'\u09dd'
   | '\u09df'..'\u09e1'
   | '\u09f0'..'\u09f1'
   | '\u0a05'..'\u0a0a'
   | '\u0a0f'..'\u0a10'
   | '\u0a13'..'\u0a28'
   | '\u0a2a'..'\u0a30'
   | '\u0a32'..'\u0a33'
   | '\u0a35'..'\u0a36'
   | '\u0a38'..'\u0a39'
   | '\u0a59'..'\u0a5c'
   | '\u0a5e'..'\u0a72'
   | '\u0a73'..'\u0a74'
   | '\u0a85'..'\u0a8d'
   | '\u0a8f'..'\u0a91'
   | '\u0a93'..'\u0aa8'
   | '\u0aaa'..'\u0ab0'
   | '\u0ab2'..'\u0ab3'
   | '\u0ab5'..'\u0ab9'
   | '\u0abd'..'\u0ad0'
   | '\u0ae0'..'\u0ae1'
   | '\u0b05'..'\u0b0c'
   | '\u0b0f'..'\u0b10'
   | '\u0b13'..'\u0b28'
   | '\u0b2a'..'\u0b30'
   | '\u0b32'..'\u0b33'
   | '\u0b35'..'\u0b39'
   | '\u0b3d'..'\u0b5c'
   | '\u0b5d'..'\u0b5f'
   | '\u0b60'..'\u0b61'
   | '\u0b71'..'\u0b83'
   | '\u0b85'..'\u0b8a'
   | '\u0b8e'..'\u0b90'
   | '\u0b92'..'\u0b95'
   | '\u0b99'..'\u0b9a'
   | '\u0b9c'..'\u0b9e'
   | '\u0b9f'..'\u0ba3'
   | '\u0ba4'..'\u0ba8'
   | '\u0ba9'..'\u0baa'
   | '\u0bae'..'\u0bb9'
   | '\u0bd0'..'\u0c05'
   | '\u0c06'..'\u0c0c'
   | '\u0c0e'..'\u0c10'
   | '\u0c12'..'\u0c28'
   | '\u0c2a'..'\u0c39'
   | '\u0c3d'..'\u0c58'
   | '\u0c59'..'\u0c60'
   | '\u0c61'..'\u0c85'
   | '\u0c86'..'\u0c8c'
   | '\u0c8e'..'\u0c90'
   | '\u0c92'..'\u0ca8'
   | '\u0caa'..'\u0cb3'
   | '\u0cb5'..'\u0cb9'
   | '\u0cbd'..'\u0cde'
   | '\u0ce0'..'\u0ce1'
   | '\u0cf1'..'\u0cf2'
   | '\u0d05'..'\u0d0c'
   | '\u0d0e'..'\u0d10'
   | '\u0d12'..'\u0d3a'
   | '\u0d3d'..'\u0d4e'
   | '\u0d60'..'\u0d61'
   | '\u0d7a'..'\u0d7f'
   | '\u0d85'..'\u0d96'
   | '\u0d9a'..'\u0db1'
   | '\u0db3'..'\u0dbb'
   | '\u0dbd'..'\u0dc0'
   | '\u0dc1'..'\u0dc6'
   | '\u0e01'..'\u0e30'
   | '\u0e32'..'\u0e33'
   | '\u0e40'..'\u0e45'
   | '\u0e81'..'\u0e82'
   | '\u0e84'..'\u0e87'
   | '\u0e88'..'\u0e8a'
   | '\u0e8d'..'\u0e94'
   | '\u0e95'..'\u0e97'
   | '\u0e99'..'\u0e9f'
   | '\u0ea1'..'\u0ea3'
   | '\u0ea5'..'\u0ea7'
   | '\u0eaa'..'\u0eab'
   | '\u0ead'..'\u0eb0'
   | '\u0eb2'..'\u0eb3'
   | '\u0ebd'..'\u0ec0'
   | '\u0ec1'..'\u0ec4'
   | '\u0edc'..'\u0edf'
   | '\u0f00'..'\u0f40'
   | '\u0f41'..'\u0f47'
   | '\u0f49'..'\u0f6c'
   | '\u0f88'..'\u0f8c'
   | '\u1000'..'\u102a'
   | '\u103f'..'\u1050'
   | '\u1051'..'\u1055'
   | '\u105a'..'\u105d'
   | '\u1061'..'\u1065'
   | '\u1066'..'\u106e'
   | '\u106f'..'\u1070'
   | '\u1075'..'\u1081'
   | '\u108e'..'\u10d0'
   | '\u10d1'..'\u10fa'
   | '\u10fd'..'\u1248'
   | '\u124a'..'\u124d'
   | '\u1250'..'\u1256'
   | '\u1258'..'\u125a'
   | '\u125b'..'\u125d'
   | '\u1260'..'\u1288'
   | '\u128a'..'\u128d'
   | '\u1290'..'\u12b0'
   | '\u12b2'..'\u12b5'
   | '\u12b8'..'\u12be'
   | '\u12c0'..'\u12c2'
   | '\u12c3'..'\u12c5'
   | '\u12c8'..'\u12d6'
   | '\u12d8'..'\u1310'
   | '\u1312'..'\u1315'
   | '\u1318'..'\u135a'
   | '\u1380'..'\u138f'
   | '\u13a0'..'\u13f4'
   | '\u1401'..'\u166c'
   | '\u166f'..'\u167f'
   | '\u1681'..'\u169a'
   | '\u16a0'..'\u16ea'
   | '\u16f1'..'\u16f8'
   | '\u1700'..'\u170c'
   | '\u170e'..'\u1711'
   | '\u1720'..'\u1731'
   | '\u1740'..'\u1751'
   | '\u1760'..'\u176c'
   | '\u176e'..'\u1770'
   | '\u1780'..'\u17b3'
   | '\u17dc'..'\u1820'
   | '\u1821'..'\u1842'
   | '\u1844'..'\u1877'
   | '\u1880'..'\u18a8'
   | '\u18aa'..'\u18b0'
   | '\u18b1'..'\u18f5'
   | '\u1900'..'\u191e'
   | '\u1950'..'\u196d'
   | '\u1970'..'\u1974'
   | '\u1980'..'\u19ab'
   | '\u19c1'..'\u19c7'
   | '\u1a00'..'\u1a16'
   | '\u1a20'..'\u1a54'
   | '\u1b05'..'\u1b33'
   | '\u1b45'..'\u1b4b'
   | '\u1b83'..'\u1ba0'
   | '\u1bae'..'\u1baf'
   | '\u1bba'..'\u1be5'
   | '\u1c00'..'\u1c23'
   | '\u1c4d'..'\u1c4f'
   | '\u1c5a'..'\u1c77'
   | '\u1ce9'..'\u1cec'
   | '\u1cee'..'\u1cf1'
   | '\u1cf5'..'\u1cf6'
   | '\u2135'..'\u2138'
   | '\u2d30'..'\u2d67'
   | '\u2d80'..'\u2d96'
   | '\u2da0'..'\u2da6'
   | '\u2da8'..'\u2dae'
   | '\u2db0'..'\u2db6'
   | '\u2db8'..'\u2dbe'
   | '\u2dc0'..'\u2dc6'
   | '\u2dc8'..'\u2dce'
   | '\u2dd0'..'\u2dd6'
   | '\u2dd8'..'\u2dde'
   | '\u3006'..'\u303c'
   | '\u3041'..'\u3096'
   | '\u309f'..'\u30a1'
   | '\u30a2'..'\u30fa'
   | '\u30ff'..'\u3105'
   | '\u3106'..'\u312d'
   | '\u3131'..'\u318e'
   | '\u31a0'..'\u31ba'
   | '\u31f0'..'\u31ff'
   | '\u3400'..'\u4db5'
   | '\u4e00'..'\u9fcc'
   | '\ua000'..'\ua014'
   | '\ua016'..'\ua48c'
   | '\ua4d0'..'\ua4f7'
   | '\ua500'..'\ua60b'
   | '\ua610'..'\ua61f'
   | '\ua62a'..'\ua62b'
   | '\ua66e'..'\ua6a0'
   | '\ua6a1'..'\ua6e5'
   | '\ua7f7'..'\ua7fb'
   | '\ua7fc'..'\ua801'
   | '\ua803'..'\ua805'
   | '\ua807'..'\ua80a'
   | '\ua80c'..'\ua822'
   | '\ua840'..'\ua873'
   | '\ua882'..'\ua8b3'
   | '\ua8f2'..'\ua8f7'
   | '\ua8fb'..'\ua90a'
   | '\ua90b'..'\ua925'
   | '\ua930'..'\ua946'
   | '\ua960'..'\ua97c'
   | '\ua984'..'\ua9b2'
   | '\ua9e0'..'\ua9e4'
   | '\ua9e7'..'\ua9ef'
   | '\ua9fa'..'\ua9fe'
   | '\uaa00'..'\uaa28'
   | '\uaa40'..'\uaa42'
   | '\uaa44'..'\uaa4b'
   | '\uaa60'..'\uaa6f'
   | '\uaa71'..'\uaa76'
   | '\uaa7a'..'\uaa7e'
   | '\uaa7f'..'\uaaaf'
   | '\uaab1'..'\uaab5'
   | '\uaab6'..'\uaab9'
   | '\uaaba'..'\uaabd'
   | '\uaac0'..'\uaac2'
   | '\uaadb'..'\uaadc'
   | '\uaae0'..'\uaaea'
   | '\uaaf2'..'\uab01'
   | '\uab02'..'\uab06'
   | '\uab09'..'\uab0e'
   | '\uab11'..'\uab16'
   | '\uab20'..'\uab26'
   | '\uab28'..'\uab2e'
   | '\uabc0'..'\uabe2'
   | '\uac00'..'\ud7a3'
   | '\ud7b0'..'\ud7c6'
   | '\ud7cb'..'\ud7fb'
   | '\uf900'..'\ufa6d'
   | '\ufa70'..'\ufad9'
   | '\ufb1d'..'\ufb1f'
   | '\ufb20'..'\ufb28'
   | '\ufb2a'..'\ufb36'
   | '\ufb38'..'\ufb3c'
   | '\ufb3e'..'\ufb40'
   | '\ufb41'..'\ufb43'
   | '\ufb44'..'\ufb46'
   | '\ufb47'..'\ufbb1'
   | '\ufbd3'..'\ufd3d'
   | '\ufd50'..'\ufd8f'
   | '\ufd92'..'\ufdc7'
   | '\ufdf0'..'\ufdfb'
   | '\ufe70'..'\ufe74'
   | '\ufe76'..'\ufefc'
   | '\uff66'..'\uff6f'
   | '\uff71'..'\uff9d'
   | '\uffa0'..'\uffbe'
   | '\uffc2'..'\uffc7'
   | '\uffca'..'\uffcf'
   | '\uffd2'..'\uffd7'
   | '\uffda'..'\uffdc'
   ;

fragment UnicodeDigit // UnicodeClass_ND
   : '\u0030'..'\u0039'
   | '\u0660'..'\u0669'
   | '\u06f0'..'\u06f9'
   | '\u07c0'..'\u07c9'
   | '\u0966'..'\u096f'
   | '\u09e6'..'\u09ef'
   | '\u0a66'..'\u0a6f'
   | '\u0ae6'..'\u0aef'
   | '\u0b66'..'\u0b6f'
   | '\u0be6'..'\u0bef'
   | '\u0c66'..'\u0c6f'
   | '\u0ce6'..'\u0cef'
   | '\u0d66'..'\u0d6f'
   | '\u0de6'..'\u0def'
   | '\u0e50'..'\u0e59'
   | '\u0ed0'..'\u0ed9'
   | '\u0f20'..'\u0f29'
   | '\u1040'..'\u1049'
   | '\u1090'..'\u1099'
   | '\u17e0'..'\u17e9'
   | '\u1810'..'\u1819'
   | '\u1946'..'\u194f'
   | '\u19d0'..'\u19d9'
   | '\u1a80'..'\u1a89'
   | '\u1a90'..'\u1a99'
   | '\u1b50'..'\u1b59'
   | '\u1bb0'..'\u1bb9'
   | '\u1c40'..'\u1c49'
   | '\u1c50'..'\u1c59'
   | '\ua620'..'\ua629'
   | '\ua8d0'..'\ua8d9'
   | '\ua900'..'\ua909'
   | '\ua9d0'..'\ua9d9'
   | '\ua9f0'..'\ua9f9'
   | '\uaa50'..'\uaa59'
   | '\uabf0'..'\uabf9'
   | '\uff10'..'\uff19'
   ;


//
// Whitespace and comments
//
NEWLINE
   : NL+ -> skip
   ;

WS
   :  WhiteSpace+ -> skip
   ;

COMMENT
   :   '/*' .*? '*/' -> skip
   ;


LINE_COMMENT
   :   '//' (~[\r\n])* -> skip
   ;
