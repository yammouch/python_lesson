// make -C /usr/src/linux-headers-4.18.0-10-generic M=`pwd` modules
// sudo insmod ./hello.ko
// sudo rmmod hello

#include <linux/init.h>
#include <linux/module.h>
MODULE_LICENSE("Dual BSD/GPL");

static int hello_init(void) {
  printk(KERN_ALERT "Hello, world\n");
  return 0;
}

static void hello_exit(void) {
  printk(KERN_ALERT "Goodbye, cruel world\n");
  return;
}

module_init(hello_init);
module_exit(hello_exit);
