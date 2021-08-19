using System;
using System.Security;

namespace MyLibrary
{

    [SecurityCritical]
    public class Foo
    {
        [SecuritySafeCritical]
        public void Bar()
        {
        }

        public void Testeo()
        {
        }
    }
}
