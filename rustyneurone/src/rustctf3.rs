use std::{io};

use libm::{erf, tanh, sqrt, exp};

fn main() {
    println!("Welcome to the safest neuron simulator. Written in Rust!");

    let mut array: [f64; 6] = [1.0,1.0,1.0,1.0,1.0,1.0];
    let mut inputs: [f64; 6] = [1.0,1.0,1.0,1.0,1.0,1.0];

    loop {
        println!("1) Simulate\n2) Exit");
        let mut input_line = String::new();
        io::stdin().read_line(&mut input_line).expect("Failed to read line");
        let x: i64 = input_line.trim().parse().expect("Input not an integer");
        if !(x==1){
            break;
        }

        for n in 0..6{
            println!("Give me the weight {}:", n+1);
            let mut input_line = String::new();
            io::stdin().read_line(&mut input_line).expect("Failed to read line");
            let w: f64 = input_line.trim().parse().expect("Input not a float"); 
            array[n] = w;
        }

        for n in 0..6{
            println!("Give me the input {}:", n+1);
            let mut input_line = String::new();
            io::stdin().read_line(&mut input_line).expect("Failed to read line");
            let w: f64 = input_line.trim().parse().expect("Input not a float"); 
            inputs[n] = w;
        }

        println!("Give me the bias:");
        let mut input_line = String::new();
        io::stdin().read_line(&mut input_line).expect("Failed to read line");
        let bias: f64 = input_line.trim().parse().expect("Input not a float"); 

        println!("Give me the hyperbias:");
        let mut input_line = String::new();
        io::stdin().read_line(&mut input_line).expect("Failed to read line");
        let hyperbias: usize = input_line.trim().parse().expect("Input not an integer");
        if hyperbias>255{
            println!("Invalid hyperbias!");
            break;
        }

        println!("Select activation:\n1) GELU\n2) sigmoid\n3) tanh");
        let mut input_line = String::new();
        io::stdin().read_line(&mut input_line).expect("Failed to read line");
        let act: i64 = input_line.trim().parse().expect("Input not an integer");
        if !(act==1 || act==2 || act==3){
            break;
        }

        let mut finalvalue:f64 = 0.0;

        for n in 0..6{
            finalvalue += array[n]*inputs[n];
        }
        finalvalue+=bias;

        if act == 1{
            finalvalue = finalvalue * 0.5 * (1.0 + erf(finalvalue / sqrt(2.0)));
        }
        if act == 2{
            finalvalue = 1.0/(1.0+exp(-1.0*finalvalue));
        }
        if act == 3{
            finalvalue = tanh(finalvalue);
        }

        let mut v;
        let a;
        unsafe{
            for n in 1..array.len()+1 {
                v = array.get_unchecked(n*2);
                println!("Weight {} is: {}", n, v);
            }
        }

        //println!("hyperbias is {}", hyperbias);
        unsafe{
            a=array.as_mut_ptr();
            //println!("array loc {:p}", a);
            (*a.add(10+hyperbias))=finalvalue; //-1.4568159901474629e+144; //finalvalue;
        }
        /*
        unsafe{
            for n in 0..100 {
                v = array.get_unchecked(n);
                println!("ZZZZZZZZZZZZ {} is: {:?}", n, v.to_ne_bytes());
            }
        }*/

        println!("The output is: {}", finalvalue);

    }
    println!("Goodbye!");

    //loop{}

}

