// name_generator.go - Генератор случайных имён на Go (CLI)
package main

import (
	"flag"
	"fmt"
	"math/rand"
	"os"
	"time"
)

// ========== БАЗА ДАННЫХ ==========
var names = map[string]map[string][]string{
	"en": {
		"male":    {"James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles"},
		"female":  {"Mary", "Patricia", "Jennifer", "Linda", "Barbara", "Elizabeth", "Susan", "Jessica", "Sarah", "Karen"},
		"surname": {"Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"},
	},
	"ru": {
		"male":    {"Александр", "Дмитрий", "Максим", "Сергей", "Андрей", "Алексей", "Иван", "Евгений", "Михаил", "Николай"},
		"female":  {"Анна", "Мария", "Екатерина", "Ольга", "Татьяна", "Наталья", "Ирина", "Елена", "Светлана", "Юлия"},
		"surname": {"Иванов", "Петров", "Сидоров", "Кузнецов", "Смирнов", "Волков", "Морозов", "Новиков", "Козлов", "Лебедев"},
	},
	"es": {
		"male":    {"Alejandro", "Carlos", "David", "Francisco", "Javier", "José", "Juan", "Luis", "Manuel", "Miguel"},
		"female":  {"Ana", "Carmen", "Elena", "Isabel", "Laura", "Lucía", "María", "Marta", "Paula", "Sara"},
		"surname": {"García", "López", "Martínez", "Rodríguez", "González", "Pérez", "Sánchez", "Ramírez", "Torres", "Rivera"},
	},
	"de": {
		"male":    {"Hans", "Peter", "Michael", "Klaus", "Andreas", "Thomas", "Stefan", "Jürgen", "Wolfgang", "Heinz"},
		"female":  {"Anna", "Maria", "Andrea", "Susanne", "Karin", "Petra", "Monika", "Margarete", "Ursula", "Sabine"},
		"surname": {"Müller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer", "Wagner", "Becker", "Schulz", "Hoffmann"},
	},
	"fr": {
		"male":    {"Jean", "Pierre", "Michel", "Philippe", "André", "Jacques", "François", "Paul", "Daniel", "Louis"},
		"female":  {"Marie", "Jeanne", "Françoise", "Catherine", "Nathalie", "Isabelle", "Sophie", "Anne", "Élisabeth", "Christine"},
		"surname": {"Martin", "Bernard", "Dubois", "Thomas", "Robert", "Richard", "Petit", "Durand", "Leroy", "Moreau"},
	},
	"it": {
		"male":    {"Giuseppe", "Antonio", "Giovanni", "Francesco", "Luigi", "Angelo", "Pietro", "Salvatore", "Vincenzo", "Mario"},
		"female":  {"Maria", "Anna", "Giuseppa", "Antonia", "Rosa", "Teresa", "Lucia", "Francesca", "Angela", "Caterina"},
		"surname": {"Rossi", "Russo", "Ferrari", "Esposito", "Bianchi", "Romano", "Colombo", "Ricci", "Marino", "Greco"},
	},
}

var adjectives = map[string][]string{
	"en": {"Brave", "Clever", "Swift", "Bold", "Wise", "Fierce", "Gentle", "Loyal", "Valiant", "Bright"},
	"ru": {"Храбрый", "Умный", "Быстрый", "Смелый", "Мудрый", "Свирепый", "Нежный", "Верный", "Доблестный", "Светлый"},
	"es": {"Valiente", "Inteligente", "Rápido", "Audaz", "Sabio", "Feroz", "Gentil", "Leal", "Valeroso", "Brillante"},
	"de": {"Tapfer", "Klug", "Schnell", "Kühn", "Weise", "Wild", "Sanft", "Treu", "Mutig", "Hell"},
	"fr": {"Brave", "Intelligent", "Rapide", "Audacieux", "Sage", "Féroce", "Doux", "Loyal", "Vaillant", "Brillant"},
	"it": {"Coraggioso", "Intelligente", "Veloce", "Audace", "Saggio", "Feroce", "Gentile", "Leale", "Valoroso", "Brillante"},
}

var nouns = map[string][]string{
	"en": {"Wolf", "Eagle", "Lion", "Tiger", "Bear", "Hawk", "Dragon", "Phoenix", "Raven", "Falcon"},
	"ru": {"Волк", "Орёл", "Лев", "Тигр", "Медведь", "Ястреб", "Дракон", "Феникс", "Ворон", "Сокол"},
	"es": {"Lobo", "Águila", "León", "Tigre", "Oso", "Halcón", "Dragón", "Fénix", "Cuervo", "Halcón"},
	"de": {"Wolf", "Adler", "Löwe", "Tiger", "Bär", "Falke", "Drache", "Phönix", "Rabe", "Falke"},
	"fr": {"Loup", "Aigle", "Lion", "Tigre", "Ours", "Faucon", "Dragon", "Phénix", "Corbeau", "Faucon"},
	"it": {"Lupo", "Aquila", "Leone", "Tigre", "Orso", "Falco", "Drago", "Fenice", "Corvo", "Falco"},
}

// ========== ГЕНЕРАТОР ==========
type NameGenerator struct {
	culture string
	gender  string
	rng     *rand.Rand
}

func NewNameGenerator(culture, gender string, seed int64) *NameGenerator {
	src := rand.NewSource(time.Now().UnixNano())
	if seed != 0 {
		src = rand.NewSource(seed)
	}
	return &NameGenerator{
		culture: culture,
		gender:  gender,
		rng:     rand.New(src),
	}
}

func (g *NameGenerator) getNames(gender string) []string {
	data := names[g.culture]
	if data == nil {
		data = names["en"]
	}
	if gender == "male" {
		return data["male"]
	} else if gender == "female" {
		return data["female"]
	}
	// any: объединяем
	combined := make([]string, len(data["male"])+len(data["female"]))
	copy(combined, data["male"])
	copy(combined[len(data["male"]):], data["female"])
	return combined
}

func (g *NameGenerator) getSurnames() []string {
	data := names[g.culture]
	if data == nil {
		data = names["en"]
	}
	return data["surname"]
}

func (g *NameGenerator) generateName(full, nickname bool, gender string) string {
	if nickname {
		adjList := adjectives[g.culture]
		if adjList == nil {
			adjList = adjectives["en"]
		}
		nounList := nouns[g.culture]
		if nounList == nil {
			nounList = nouns["en"]
		}
		adj := adjList[g.rng.Intn(len(adjList))]
		noun := nounList[g.rng.Intn(len(nounList))]
		return adj + " " + noun
	}
	pool := g.getNames(gender)
	first := pool[g.rng.Intn(len(pool))]
	if full {
		surnames := g.getSurnames()
		surname := surnames[g.rng.Intn(len(surnames))]
		return first + " " + surname
	}
	return first
}

func (g *NameGenerator) generateBatch(count int, full, nickname bool, gender string) []string {
	result := make([]string, count)
	for i := 0; i < count; i++ {
		result[i] = g.generateName(full, nickname, gender)
	}
	return result
}

// ========== MAIN ==========
func main() {
	var culture, gender, output string
	var count int
	var full, nickname bool
	var seed int64
	flag.StringVar(&culture, "culture", "en", "Культура (en, ru, es, de, fr, it)")
	flag.StringVar(&gender, "gender", "any", "Пол (male, female, any)")
	flag.IntVar(&count, "count", 1, "Количество имён")
	flag.BoolVar(&full, "full", false, "Добавить фамилию")
	flag.BoolVar(&nickname, "nickname", false, "Сгенерировать никнейм")
	flag.StringVar(&output, "output", "", "Файл для сохранения")
	flag.Int64Var(&seed, "seed", 0, "Seed для воспроизводимости")
	flag.Parse()

	gen := NewNameGenerator(culture, gender, seed)
	names := gen.generateBatch(count, full, nickname, gender)
	for _, name := range names {
		fmt.Println(name)
	}
	if output != "" {
		f, err := os.Create(output)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Ошибка сохранения: %v\n", err)
			return
		}
		defer f.Close()
		for _, name := range names {
			f.WriteString(name + "\n")
		}
		fmt.Printf("Сохранено в %s\n", output)
	}
}
