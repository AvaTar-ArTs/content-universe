use std::io::{self, Read};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).expect("read stdin");
    let bytes = input.as_bytes().len();
    println!(r#"{{"service":"creativeos-indexer","status":"ready","input_bytes":{}}}"#, bytes);
}
