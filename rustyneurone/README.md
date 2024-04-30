# A challenge simulating a neuron, written in Rust.

This challenge is written in Rust, but it uses unsafe constructs.
For this reason, it is possible to solve it with traditional exploitation techniques.
I am not including a Makefile, since re-compiling the binary can break the exploit.
I am including the pre-compiled binary (`src/rustyneurone`) and a compilation script (`src/compile.sh`).

# Writeup

## Introduction
`rustyneurone` is a challenge written in Rust. The challenge simulates how a classical neuron used by a neural network operates.

The challenge is exploitable since it contains some unsafe usage of Rust (marked `unsafe` in the Rust source code).
The unsafe code leads both to memory on the stack being leaked and to stack memory being overwritten, enabling standard ROP-chain-based exploitation.


## Challenge analysis
The challenge asks for a list of weights, a list of inputs, a bias, one hyperbias, and an activation function (to be chosen among `tanh`, `sigmoid`, and `GELU`).

After the neuron's configuration is provided, the challenge prints out the provided weights and the final computed value, performing standard neural network math (check here for a [tutorial](https://medium.com/coinmonks/the-mathematics-of-neural-network-60a112dd3e05)). The code operates in a loop, allowing the user to simulate a neuron's behavior multiple times.

By manual testing and reverse engineering, one can notice that:
1. The weights printed back to the user do not always match what provided. Upon further inspection one can realize that weights printed back can leak values from the stack (encoded as floating point numbers).
2. The hyperbias is not really used in the computation of the final results (indeed, there is no such thing as a hyperbias in standard neurons). However, it is used to determine where the final results of the neuron simulation is written on the stack.

## Exploitation

Exploiting point 1, it is possible to leak part of the content of the stack. In particular the value printed as Weight #6 leaks the location of the main binary in memory.

Exploiting point 2, it is possible to write a ROP-chain on the stack. Specifically, for each neuron simulation we can write 8 bytes on the stack, controlling the location on the stack using different values for the hyperbias.

In particular, the values written on the stack are the results of each neuron simulation. Hence, to control them, we need to provide proper values to the neuron so that its output is what we desire. This is not particularly hard. In fact, we can provide a list of zeros for both the inputs and the weights effectively making the input of the neuron's activation function equal to only the neuron's bias. Then, we can choose an activation function that does not modify its input, so that the provided value for the bias will be equal to the output of the neuron and directly written to the stack.

To this aim, when we need to write to the stack small values (i.e., 8-byte sequences that, when encoded as a floating point number, translate to a small value), we can use the `tanh` activation function. On the contrary, when we need to write to the stack large values, we can use the `GELU` activation function. Mathematically, this works because these two functions can be approximated to the identify function for values near 0 and for values near to plus infinitive, respectively.

By exploiting the method explained above, we can corrupt the saved return address and write an entire ROP-chain on the stack (e.g., a ROP-chain opening a shell). The ROP-chain will be triggered by making the program exit the main neuron simulation loop and return from its `main` function.


