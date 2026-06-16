// name_generator.rs - Генератор случайных имён на Rust (CLI)
// Используйте: cargo run -- --count 5 --culture ru --full
use std::collections::HashMap;
use rand::seq::SliceRandom;
use rand::SeedableRng;
use rand::rngs::StdRng;
use clap::{Arg, App};

// ========== БАЗА ДАННЫХ ==========
type NameMap = HashMap<String, HashMap<String, Vec<String>>>;
lazy_static! {
    static ref NAMES: NameMap = {
        let mut m = HashMap::new();
        // en
        let mut en = HashMap::new();
        en.insert("male".to_string(), vec!["James".to_string(), "John".to_string(), "Robert".to_string(), "Michael".to_string(), "William".to_string(), "David".to_string(), "Richard".to_string(), "Joseph".to_string(), "Thomas".to_string(), "Charles".to_string()]);
        en.insert("female".to_string(), vec!["Mary".to_string(), "Patricia".to_string(), "Jennifer".to_string(), "Linda".to_string(), "Barbara".to_string(), "Elizabeth".to_string(), "Susan".to_string(), "Jessica".to_string(), "Sarah".to_string(), "Karen".to_string()]);
        en.insert("surname".to_string(), vec!["Smith".to_string(), "Johnson".to_string(), "Williams".to_string(), "Brown".to_string(), "Jones".to_string(), "Garcia".to_string(), "Miller".to_string(), "Davis".to_string(), "Rodriguez".to_string(), "Martinez".to_string()]);
        m.insert("en".to_string(), en);
        // ru
        let mut ru = HashMap::new();
        ru.insert("male".to_string(), vec!["Александр".to_string(), "Дмитрий".to_string(), "Максим".to_string(), "Сергей".to_string(), "Андрей".to_string(), "Алексей".to_string(), "Иван".to_string(), "Евгений".to_string(), "Михаил".to_string(), "Николай".to_string()]);
        ru.insert("female".to_string(), vec!["Анна".to_string(), "Мария".to_string(), "Екатерина".to_string(), "Ольга".to_string(), "Татьяна".to_string(), "Наталья".to_string(), "Ирина".to_string(), "Елена".to_string(), "Светлана".to_string(), "Юлия".to_string()]);
        ru.insert("surname".to_string(), vec!["Иванов".to_string(), "Петров".to_string(), "Сидоров".to_string(), "Кузнецов".to_string(), "Смирнов".to_string(), "Волков".to_string(), "Морозов".to_string(), "Новиков".to_string(), "Козлов".to_string(), "Лебедев".to_string()]);
        m.insert("ru".to_string(), ru);
        // es, de, fr, it - аналогично, сокращённо для примера
        // ...
        m
    };
    static ref ADJECTIVES: HashMap<String, Vec<String>> = {
        let mut m = HashMap::new();
        m.insert("en".to_string(), vec!["Brave".to_string(), "Clever".to_string(), "Swift".to_string(), "Bold".to_string(), "Wise".to_string(), "Fierce".to_string(), "Gentle".to_string(), "Loyal".to_string(), "Valiant".to_string(), "Bright".to_string()]);
        m.insert("ru".to_string(), vec!["Храбрый".to_string(), "Умный".to_string(), "Быстрый".to_string(), "Смелый".to_string(), "Мудрый".to_string(), "Свирепый".to_string(), "Нежный".to_string(), "Верный".to_string(), "Доблестный".to_string(), "Светлый".to_string()]);
        // ...
        m
    };
    static ref NOUNS: HashMap<String, Vec<String>> = {
        let mut m = HashMap::new();
        m.insert("en".to_string(), vec!["Wolf".to_string(), "Eagle".to_string(), "Lion".to_string(), "Tiger".to_string(), "Bear".to_string(), "Hawk".to_string(), "Dragon".to_string(), "Phoenix".to_string(), "Raven".to_string(), "Falcon".to_string()]);
        m.insert("ru".to_string(), vec!["Волк".to_string(), "Орёл".to_string(), "Лев".to_string(), "Тигр".to_string(), "Медведь".to_string(), "Ястреб".to_string(), "Дракон".to_string(), "Феникс".to_string(), "Ворон".to_string(), "Сокол".to_string()]);
        // ...
        m
    };
}

// ========== ГЕНЕРАТОР ==========
pub struct NameGenerator {
    culture: String,
    gender: String,
    rng: StdRng,
}

impl NameGenerator {
    pub fn new(culture: &str, gender: &str, seed: u64) -> Self {
        let rng = if seed == 0 {
            StdRng::from_entropy()
        } else {
            StdRng::seed_from_u64(seed)
        };
        NameGenerator {
            culture: culture.to_string(),
            gender: gender.to_string(),
            rng,
        }
    }

    fn get_names(&self, gender: Option<&str>) -> Vec<String> {
        let data = NAMES.get(&self.culture).unwrap_or_else(|| NAMES.get("en").unwrap());
        let g = gender.unwrap_or(&self.gender);
        if g == "male" {
            data.get("male").unwrap().clone()
        } else if g == "female" {
            data.get("female").unwrap().clone()
        } else {
            let mut v = data.get("male").unwrap().clone();
            v.extend(data.get("female").unwrap().clone());
            v
        }
    }

    fn get_surnames(&self) -> Vec<String> {
        let data = NAMES.get(&self.culture).unwrap_or_else(|| NAMES.get("en").unwrap());
        data.get("surname").unwrap().clone()
    }

    pub fn generate_name(&mut self, full: bool, nickname: bool, gender: Option<&str>) -> String {
        if nickname {
            let adj_list = ADJECTIVES.get(&self.culture).unwrap_or_else(|| ADJECTIVES.get("en").unwrap());
            let noun_list = NOUNS.get(&self.culture).unwrap_or_else(|| NOUNS.get("en").unwrap());
            let adj = adj_list.choose(&mut self.rng).unwrap();
            let noun = noun_list.choose(&mut self.rng).unwrap();
            return format!("{} {}", adj, noun);
        }
        let pool = self.get_names(gender);
        let first = pool.choose(&mut self.rng).unwrap().clone();
        if full {
            let surnames = self.get_surnames();
            let surname = surnames.choose(&mut self.rng).unwrap().clone();
            return format!("{} {}", first, surname);
        }
        first
    }

    pub fn generate_batch(&mut self, count: usize, full: bool, nickname: bool, gender: Option<&str>) -> Vec<String> {
        (0..count).map(|_| self.generate_name(full, nickname, gender)).collect()
    }
}

// ========== MAIN ==========
fn main() {
    let matches = App::new("Name Generator")
        .arg(Arg::with_name("count").short("c").long("count").default_value("1").help("Количество имён"))
        .arg(Arg::with_name("culture").short("u").long("culture").default_value("en").help("Культура"))
        .arg(Arg::with_name("gender").short("g").long("gender").default_value("any").help("Пол"))
        .arg(Arg::with_name("full").long("full").help("Добавить фамилию"))
        .arg(Arg::with_name("nickname").long("nickname").help("Никнейм"))
        .arg(Arg::with_name("output").short("o").long("output").help("Файл для сохранения"))
        .arg(Arg::with_name("seed").long("seed").help("Seed"))
        .get_matches();

    let count: usize = matches.value_of("count").unwrap().parse().unwrap();
    let culture = matches.value_of("culture").unwrap();
    let gender = matches.value_of("gender").unwrap();
    let full = matches.is_present("full");
    let nickname = matches.is_present("nickname");
    let seed: u64 = matches.value_of("seed").unwrap_or("0").parse().unwrap();

    let mut gen = NameGenerator::new(culture, gender, seed);
    let names = gen.generate_batch(count, full, nickname, Some(gender));
    for name in &names {
        println!("{}", name);
    }
    if let Some(path) = matches.value_of("output") {
        use std::fs::File;
        use std::io::Write;
        let mut file = File::create(path).expect("Не удалось создать файл");
        for name in names {
            writeln!(file, "{}", name).expect("Ошибка записи");
        }
        println!("Сохранено в {}", path);
    }
}
