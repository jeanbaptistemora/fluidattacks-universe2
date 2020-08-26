#include <stdio.h>

int main()
{
    // char buf[5];
    char a[] = "something" /* ignore this */; strncpy(buf, /* ignore this */"but not this", 4);

    /*
        A multi line comment

        // a line comment
    */ printf(buf); // a line comment

    /*  A multi line comment
    */

    /*
        A multi line comment*/

    return 0;
}
