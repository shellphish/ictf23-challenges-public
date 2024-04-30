# AI Lock

*Can you break the smartest Arduino Uno lock protected with AI?*

### Not sure how to reverse AVR?
1. Use Ghidra to load the hex file or use objcopy to convert to a hex file

### Want to dynamically execute and don't have an Arduino Uno around?

1. I got you!
   Use [simavr](https://github.com/buserror/simavr) install required dependencies (avr-gcc/libc/avr-gdb/picocom)

2. Build everything using `make`

3. Go to `examples/board_simduino`, spawn 3 different terminals
    - `./obj-x86_64-pc-linux-gnu/simduino.elf -d <path to>/ai_lock.hex` 
    - `picocom -b 115200 /tmp/simavr-uart0 --omap crlf --echo`
    - `avr-gdb -nh -ex 'target remote :1234'`
