// name_generator.js - Генератор имён на JavaScript (Node.js CLI и браузер)
// Для CLI: node name_generator.js --count 5 --culture ru --full
// Для браузера: вставьте код в HTML или используйте как модуль.

// ========== БАЗА ДАННЫХ ==========
const NAMES = {
    en: {
        male: ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles"],
        female: ["Mary", "Patricia", "Jennifer", "Linda", "Barbara", "Elizabeth", "Susan", "Jessica", "Sarah", "Karen"],
        surname: ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
    },
    ru: {
        male: ["Александр", "Дмитрий", "Максим", "Сергей", "Андрей", "Алексей", "Иван", "Евгений", "Михаил", "Николай"],
        female: ["Анна", "Мария", "Екатерина", "Ольга", "Татьяна", "Наталья", "Ирина", "Елена", "Светлана", "Юлия"],
        surname: ["Иванов", "Петров", "Сидоров", "Кузнецов", "Смирнов", "Волков", "Морозов", "Новиков", "Козлов", "Лебедев"]
    },
    es: {
        male: ["Alejandro", "Carlos", "David", "Francisco", "Javier", "José", "Juan", "Luis", "Manuel", "Miguel"],
        female: ["Ana", "Carmen", "Elena", "Isabel", "Laura", "Lucía", "María", "Marta", "Paula", "Sara"],
        surname: ["García", "López", "Martínez", "Rodríguez", "González", "Pérez", "Sánchez", "Ramírez", "Torres", "Rivera"]
    },
    de: {
        male: ["Hans", "Peter", "Michael", "Klaus", "Andreas", "Thomas", "Stefan", "Jürgen", "Wolfgang", "Heinz"],
        female: ["Anna", "Maria", "Andrea", "Susanne", "Karin", "Petra", "Monika", "Margarete", "Ursula", "Sabine"],
        surname: ["Müller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer", "Wagner", "Becker", "Schulz", "Hoffmann"]
    },
    fr: {
        male: ["Jean", "Pierre", "Michel", "Philippe", "André", "Jacques", "François", "Paul", "Daniel", "Louis"],
        female: ["Marie", "Jeanne", "Françoise", "Catherine", "Nathalie", "Isabelle", "Sophie", "Anne", "Élisabeth", "Christine"],
        surname: ["Martin", "Bernard", "Dubois", "Thomas", "Robert", "Richard", "Petit", "Durand", "Leroy", "Moreau"]
    },
    it: {
        male: ["Giuseppe", "Antonio", "Giovanni", "Francesco", "Luigi", "Angelo", "Pietro", "Salvatore", "Vincenzo", "Mario"],
        female: ["Maria", "Anna", "Giuseppa", "Antonia", "Rosa", "Teresa", "Lucia", "Francesca", "Angela", "Caterina"],
        surname: ["Rossi", "Russo", "Ferrari", "Esposito", "Bianchi", "Romano", "Colombo", "Ricci", "Marino", "Greco"]
    }
};

const ADJECTIVES = {
    en: ["Brave", "Clever", "Swift", "Bold", "Wise", "Fierce", "Gentle", "Loyal", "Valiant", "Bright"],
    ru: ["Храбрый", "Умный", "Быстрый", "Смелый", "Мудрый", "Свирепый", "Нежный", "Верный", "Доблестный", "Светлый"],
    es: ["Valiente", "Inteligente", "Rápido", "Audaz", "Sabio", "Feroz", "Gentil", "Leal", "Valeroso", "Brillante"],
    de: ["Tapfer", "Klug", "Schnell", "Kühn", "Weise", "Wild", "Sanft", "Treu", "Mutig", "Hell"],
    fr: ["Brave", "Intelligent", "Rapide", "Audacieux", "Sage", "Féroce", "Doux", "Loyal", "Vaillant", "Brillant"],
    it: ["Coraggioso", "Intelligente", "Veloce", "Audace", "Saggio", "Feroce", "Gentile", "Leale", "Valoroso", "Brillante"]
};

const NOUNS = {
    en: ["Wolf", "Eagle", "Lion", "Tiger", "Bear", "Hawk", "Dragon", "Phoenix", "Raven", "Falcon"],
    ru: ["Волк", "Орёл", "Лев", "Тигр", "Медведь", "Ястреб", "Дракон", "Феникс", "Ворон", "Сокол"],
    es: ["Lobo", "Águila", "León", "Tigre", "Oso", "Halcón", "Dragón", "Fénix", "Cuervo", "Halcón"],
    de: ["Wolf", "Adler", "Löwe", "Tiger", "Bär", "Falke", "Drache", "Phönix", "Rabe", "Falke"],
    fr: ["Loup", "Aigle", "Lion", "Tigre", "Ours", "Faucon", "Dragon", "Phénix", "Corbeau", "Faucon"],
    it: ["Lupo", "Aquila", "Leone", "Tigre", "Orso", "Falco", "Drago", "Fenice", "Corvo", "Falco"]
};

// ========== КЛАСС ==========
class NameGenerator {
    constructor(culture = "en", gender = "any", seed = null) {
        this.culture = culture;
        this.gender = gender;
        if (seed !== null) {
            this._seed = seed;
            // Для воспроизводимости в JS используем seedrandom, но для простоты пропустим.
        }
        this.data = NAMES[culture] || NAMES["en"];
        this.adj = ADJECTIVES[culture] || ADJECTIVES["en"];
        this.nouns = NOUNS[culture] || NOUNS["en"];
    }

    getNames(gender = null) {
        const g = gender || this.gender;
        if (g === "male") return this.data.male;
        if (g === "female") return this.data.female;
        return this.data.male.concat(this.data.female);
    }

    getSurnames() {
        return this.data.surname;
    }

    generateName(full = false, nickname = false, gender = null) {
        if (nickname) {
            const adj = this.adj[Math.floor(Math.random() * this.adj.length)];
            const noun = this.nouns[Math.floor(Math.random() * this.nouns.length)];
            return `${adj} ${noun}`;
        }
        const pool = this.getNames(gender);
        const first = pool[Math.floor(Math.random() * pool.length)];
        if (full) {
            const surname = this.getSurnames()[Math.floor(Math.random() * this.getSurnames().length)];
            return `${first} ${surname}`;
        }
        return first;
    }

    generateBatch(count = 1, full = false, nickname = false, gender = null) {
        const result = [];
        for (let i = 0; i < count; i++) {
            result.push(this.generateName(full, nickname, gender));
        }
        return result;
    }
}

// ========== CLI (Node.js) ==========
if (typeof require !== 'undefined' && require.main === module) {
    const args = process.argv.slice(2);
    let count = 1, culture = "en", gender = "any", full = false, nickname = false, output = null;
    for (let i = 0; i < args.length; i++) {
        switch (args[i]) {
            case "--count": count = parseInt(args[++i]) || 1; break;
            case "--culture": culture = args[++i] || "en"; break;
            case "--gender": gender = args[++i] || "any"; break;
            case "--full": full = true; break;
            case "--nickname": nickname = true; break;
            case "--output": output = args[++i]; break;
        }
    }
    const gen = new NameGenerator(culture, gender);
    const names = gen.generateBatch(count, full, nickname, gender);
    names.forEach(n => console.log(n));
    if (output) {
        const fs = require('fs');
        fs.writeFileSync(output, names.join('\n'), 'utf8');
        console.log(`Сохранено в ${output}`);
    }
}

// ========== Браузерный экспорт ==========
if (typeof window !== 'undefined') {
    window.NameGenerator = NameGenerator;
    window.NAMES = NAMES;
    // Можно добавить функцию для HTML-интерфейса
}
