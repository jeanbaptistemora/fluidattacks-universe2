/*
Hyper-V -> DirectX Interaction Sample Code

Author: Andres Roldan <aroldan@fluidattacks.com>
LinkedIn: https://www.linkedin.com/in/andres-roldan/
Twitter: @andresroldan
*/

#define _GNU_SOURCE 1
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include "/home/aroldan/WSL2-Linux-Kernel-linux-msft-wsl-5.15.y/include/uapi/misc/d3dkmthk.h"

int open_device() {
    int fd;
    fd = open("/dev/dxg", O_RDWR);
    if (fd < 0) {
        printf("Cannot open device file...\n");
        exit(1);
    }
    printf("Opened /dev/dxg: 0x%x\n", fd);
    return fd;
}

void create_device(int fd) {
    int ret;
    struct d3dkmt_createdevice ddd = { 0 };
    struct d3dkmt_adapterinfo adapterinfo = { 0 };
    struct d3dkmt_enumadapters3 enumada = { 0 };

    enumada.adapter_count = 0xff;
    enumada.adapters = &adapterinfo;
    ret = ioctl(fd, LX_DXENUMADAPTERS3, &enumada);
    if (ret) {
        printf("Error calling LX_DXENUMADAPTERS3: %d: %s\n", ret, strerror(errno));
        exit(1);
    }
    printf("Adapters found: %d\n", enumada.adapter_count);

    ddd.adapter = adapterinfo.adapter_handle;
    printf("Adapter handle: 0x%x\n", ddd.adapter.v);
    printf("Creating device\n");
    ret = ioctl(fd, LX_DXCREATEDEVICE, &ddd);
    if (ret) {
        printf("Error calling LX_DXCREATEDEVICE: %d: %s\n", ret, strerror(errno));
        exit(1);
    }
    printf("Device created: 0x%x\n", ddd.device);
}

int main() {
    int fd;
    struct d3dkmthandle device;

    fd = open_device();
    create_device(fd);
    close(fd);
}