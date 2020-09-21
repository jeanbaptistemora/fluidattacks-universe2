#import <Foundation/Foundation.h>

int main(){
NSInteger nota = 4;
switch(nota){
  case '5' :
    NSLog(@"Excelente!\n" );
    break;

  case '4' :
    NSLog(@"Bien hecho!\n" );
    break;

  case '3' :
    NSLog(@"Pasaste!\n" );
    break;

  case '2' :
    NSLog(@"Intentalo de nuevo!\n" );
    break;

  case '1' :
    NSLog(@"Perdiste!\n" );
    break;

  default :
    NSLog(@"Nota Invalida\n" );
  }
return 0;
}
