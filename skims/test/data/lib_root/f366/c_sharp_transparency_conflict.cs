using System;
using System.Security;

namespace MyLibrary
{
    // Should fail pointing to lines 12 and 19
    [FilterOne]
    [SecurityCritical]
    [LastFilter]
    public class HaveFails
    {
        [SecuritySafeCritical]
        [Fone]
        [Hello]
        public void FailsFirsFilter()
        {
        }

        [SecuritySafeCritical]
        public void MethodWhithOneFilter()
        {
        }

        public void MethodWithoutFilters()
        {
        }

        [FilterOne]
        [OtherFilter]
        public void MethodWithSomeSafeFilters()
        {
        }

    }

    // Must not fail cause class has no insecure filter
    [FilterOne]
    [LastFilter]
    public class MustNotFail
    {
        [Fone]
        [SecuritySafeCritical]
        [Hello]
        public void Bar()
        {
        }

        [SecuritySafeCritical]
        public void MethodWhithoutFilters()
        {
        }

    }

    // Chacks having no filters is not an issue
    public class ControlClass
    {
        public void Bar()
        {
        }
    }
}
