// NameGenerator.java - Генератор случайных имён на Java (CLI с меню)
import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.stream.Collectors;

public class NameGenerator {
    private static final Map<String, Map<String, List<String>>> NAMES = new HashMap<>();
    private static final Map<String, List<String>> ADJECTIVES = new HashMap<>();
    private static final Map<String, List<String>> NOUNS = new HashMap<>();

    static {
        // Инициализация баз данных (сокращённо для примера)
        // en
        Map<String, List<String>> en = new HashMap<>();
        en.put("male", Arrays.asList("James","John","Robert","Michael","William","David","Richard","Joseph","Thomas","Charles"));
        en.put("female", Arrays.asList("Mary","Patricia","Jennifer","Linda","Barbara","Elizabeth","Susan","Jessica","Sarah","Karen"));
        en.put("surname", Arrays.asList("Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez"));
        NAMES.put("en", en);
        // ru
        Map<String, List<String>> ru = new HashMap<>();
        ru.put("male", Arrays.asList("Александр","Дмитрий","Максим","Сергей","Андрей","Алексей","Иван","Евгений","Михаил","Николай"));
        ru.put("female", Arrays.asList("Анна","Мария","Екатерина","Ольга","Татьяна","Наталья","Ирина","Елена","Светлана","Юлия"));
        ru.put("surname", Arrays.asList("Иванов","Петров","Сидоров","Кузнецов","Смирнов","Волков","Морозов","Новиков","Козлов","Лебедев"));
        NAMES.put("ru", ru);
        // es, de, fr, it - аналогично (сокращённо)
        // ...
        // Прилагательные и существительные
        ADJECTIVES.put("en", Arrays.asList("Brave","Clever","Swift","Bold","Wise","Fierce","Gentle","Loyal","Valiant","Bright"));
        ADJECTIVES.put("ru", Arrays.asList("Храбрый","Умный","Быстрый","Смелый","Мудрый","Свирепый","Нежный","Верный","Доблестный","Светлый"));
        NOUNS.put("en", Arrays.asList("Wolf","Eagle","Lion","Tiger","Bear","Hawk","Dragon","Phoenix","Raven","Falcon"));
        NOUNS.put("ru", Arrays.asList("Волк","Орёл","Лев","Тигр","Медведь","Ястреб","Дракон","Феникс","Ворон","Сокол"));
    }

    private String culture;
    private String gender;
    private Random random;

    public NameGenerator(String culture, String gender, Long seed) {
        this.culture = culture;
        this.gender = gender;
        this.random = (seed != null) ? new Random(seed) : new Random();
    }

    private List<String> getNames(String gender) {
        Map<String, List<String>> data = NAMES.getOrDefault(culture, NAMES.get("en"));
        if ("male".equals(gender)) return data.get("male");
        if ("female".equals(gender)) return data.get("female");
        List<String> combined = new ArrayList<>(data.get("male"));
        combined.addAll(data.get("female"));
        return combined;
    }

    private List<String> getSurnames() {
        Map<String, List<String>> data = NAMES.getOrDefault(culture, NAMES.get("en"));
        return data.get("surname");
    }

    public String generateName(boolean full, boolean nickname, String gender) {
        if (nickname) {
            List<String> adjList = ADJECTIVES.getOrDefault(culture, ADJECTIVES.get("en"));
            List<String> nounList = NOUNS.getOrDefault(culture, NOUNS.get("en"));
            String adj = adjList.get(random.nextInt(adjList.size()));
            String noun = nounList.get(random.nextInt(nounList.size()));
            return adj + " " + noun;
        }
        List<String> pool = getNames(gender);
        String first = pool.get(random.nextInt(pool.size()));
        if (full) {
            List<String> surnames = getSurnames();
            String surname = surnames.get(random.nextInt(surnames.size()));
            return first + " " + surname;
        }
        return first;
    }

    public List<String> generateBatch(int count, boolean full, boolean nickname, String gender) {
        List<String> result = new ArrayList<>();
        for (int i = 0; i < count; i++) {
            result.add(generateName(full, nickname, gender));
        }
        return result;
    }

    public static void main(String[] args) throws IOException {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Генератор случайных имён (Java)");
        System.out.print("Культура (en/ru/es/de/fr/it) [en]: ");
        String culture = scanner.nextLine().trim();
        if (culture.isEmpty()) culture = "en";
        System.out.print("Пол (male/female/any) [any]: ");
        String gender = scanner.nextLine().trim();
        if (gender.isEmpty()) gender = "any";
        System.out.print("Количество [1]: ");
        String countStr = scanner.nextLine().trim();
        int count = countStr.isEmpty() ? 1 : Integer.parseInt(countStr);
        System.out.print("Добавить фамилию? (y/n) [n]: ");
        boolean full = scanner.nextLine().trim().equalsIgnoreCase("y");
        System.out.print("Никнейм? (y/n) [n]: ");
        boolean nickname = scanner.nextLine().trim().equalsIgnoreCase("y");
        System.out.print("Seed (число, или пусто): ");
        String seedStr = scanner.nextLine().trim();
        Long seed = seedStr.isEmpty() ? null : Long.parseLong(seedStr);

        NameGenerator gen = new NameGenerator(culture, gender, seed);
        List<String> names = gen.generateBatch(count, full, nickname, gender);
        for (String name : names) {
            System.out.println(name);
        }
        System.out.print("Сохранить в файл? (y/n) [n]: ");
        if (scanner.nextLine().trim().equalsIgnoreCase("y")) {
            System.out.print("Имя файла: ");
            String filename = scanner.nextLine().trim();
            Files.write(Paths.get(filename), names.stream().collect(Collectors.joining("\n")).getBytes());
            System.out.println("Сохранено в " + filename);
        }
    }
}
