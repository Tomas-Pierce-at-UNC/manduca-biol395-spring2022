
const BINS :usize = 256;

pub struct Histogram {
    value_counts :[u32;BINS],
    total_count :u32,
}

impl Histogram {

    pub fn new() -> Histogram {
        Histogram {
            value_counts : [0;BINS],
            total_count : 0,
        }
    }

    pub fn update(&mut self, value :u8) {
        self.total_count += 1;
        self.value_counts[value as usize] += 1;
    }

    pub fn median(&self) -> u8 {
        let mid :u32 = self.total_count / 2;
        let mut index :u32 = 0;
        let mut output :u8 = 0;
        'vals: for i in 0..BINS {
            output = i as u8;
            let value_count = self.value_counts[i];
            if index + value_count <= mid {
                index += value_count;
                continue;
            } else {
                break 'vals;
            }
        }

        return output;
    }
}
