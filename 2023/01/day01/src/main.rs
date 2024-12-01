use std::fs::File;
use std::io::{self, prelude::*, BufReader};

fn main() -> io::Result<()> {
    use std::time::Instant;
    let now = Instant::now();

    let file = File::open("../input")?;
    let reader = BufReader::new(file);

    // for line in reader.lines() {
    //     println!("{}", line?);
    // }
    let answer: i32 = reader
        .lines()
        .map(|line| line_to_value(line.unwrap()))
        .sum();
    println!("{:?}", answer);

    let elapsed = now.elapsed();
    println!("Elapsed: {:.2?}", elapsed);

    Ok(())
}

fn line_to_value(line: String) -> i32 {
    let mut total = 0;
    for c in line.chars() {
        match c {
            '0'..='9' => {
                total += 10 * c.to_string().parse::<i32>().unwrap();
                break;
            }
            _ => {}
        }
    }

    for c in line.chars().rev() {
        match c {
            '0'..='9' => {
                total += c.to_string().parse::<i32>().unwrap();
                break;
            }
            _ => {}
        }
    }
    return total;
}
