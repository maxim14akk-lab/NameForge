<?php
// name_generator.php - Генератор случайных имён на PHP (CLI + веб)
// CLI: php name_generator.php --count=5 --culture=ru --full
// Веб: запустите сервер и откройте в браузере.

// ========== БАЗА ДАННЫХ ==========
$NAMES = [
    "en" => [
        "male" => ["James","John","Robert","Michael","William","David","Richard","Joseph","Thomas","Charles"],
        "female" => ["Mary","Patricia","Jennifer","Linda","Barbara","Elizabeth","Susan","Jessica","Sarah","Karen"],
        "surname" => ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez"]
    ],
    "ru" => [
        "male" => ["Александр","Дмитрий","Максим","Сергей","Андрей","Алексей","Иван","Евгений","Михаил","Николай"],
        "female" => ["Анна","Мария","Екатерина","Ольга","Татьяна","Наталья","Ирина","Елена","Светлана","Юлия"],
        "surname" => ["Иванов","Петров","Сидоров","Кузнецов","Смирнов","Волков","Морозов","Новиков","Козлов","Лебедев"]
    ],
    "es" => [
        "male" => ["Alejandro","Carlos","David","Francisco","Javier","José","Juan","Luis","Manuel","Miguel"],
        "female" => ["Ana","Carmen","Elena","Isabel","Laura","Lucía","María","Marta","Paula","Sara"],
        "surname" => ["García","López","Martínez","Rodríguez","González","Pérez","Sánchez","Ramírez","Torres","Rivera"]
    ],
    "de" => [
        "male" => ["Hans","Peter","Michael","Klaus","Andreas","Thomas","Stefan","Jürgen","Wolfgang","Heinz"],
        "female" => ["Anna","Maria","Andrea","Susanne","Karin","Petra","Monika","Margarete","Ursula","Sabine"],
        "surname" => ["Müller","Schmidt","Schneider","Fischer","Weber","Meyer","Wagner","Becker","Schulz","Hoffmann"]
    ],
    "fr" => [
        "male" => ["Jean","Pierre","Michel","Philippe","André","Jacques","François","Paul","Daniel","Louis"],
        "female" => ["Marie","Jeanne","Françoise","Catherine","Nathalie","Isabelle","Sophie","Anne","Élisabeth","Christine"],
        "surname" => ["Martin","Bernard","Dubois","Thomas","Robert","Richard","Petit","Durand","Leroy","Moreau"]
    ],
    "it" => [
        "male" => ["Giuseppe","Antonio","Giovanni","Francesco","Luigi","Angelo","Pietro","Salvatore","Vincenzo","Mario"],
        "female" => ["Maria","Anna","Giuseppa","Antonia","Rosa","Teresa","Lucia","Francesca","Angela","Caterina"],
        "surname" => ["Rossi","Russo","Ferrari","Esposito","Bianchi","Romano","Colombo","Ricci","Marino","Greco"]
    ]
];

$ADJECTIVES = [
    "en" => ["Brave","Clever","Swift","Bold","Wise","Fierce","Gentle","Loyal","Valiant","Bright"],
    "ru" => ["Храбрый","Умный","Быстрый","Смелый","Мудрый","Свирепый","Нежный","Верный","Доблестный","Светлый"],
    "es" => ["Valiente","Inteligente","Rápido","Audaz","Sabio","Feroz","Gentil","Leal","Valeroso","Brillante"],
    "de" => ["Tapfer","Klug","Schnell","Kühn","Weise","Wild","Sanft","Treu","Mutig","Hell"],
    "fr" => ["Brave","Intelligent","Rapide","Audacieux","Sage","Féroce","Doux","Loyal","Vaillant","Brillant"],
    "it" => ["Coraggioso","Intelligente","Veloce","Audace","Saggio","Feroce","Gentile","Leale","Valoroso","Brillante"]
];

$NOUNS = [
    "en" => ["Wolf","Eagle","Lion","Tiger","Bear","Hawk","Dragon","Phoenix","Raven","Falcon"],
    "ru" => ["Волк","Орёл","Лев","Тигр","Медведь","Ястреб","Дракон","Феникс","Ворон","Сокол"],
    "es" => ["Lobo","Águila","León","Tigre","Oso","Halcón","Dragón","Fénix","Cuervo","Halcón"],
    "de" => ["Wolf","Adler","Löwe","Tiger","Bär","Falke","Drache","Phönix","Rabe","Falke"],
    "fr" => ["Loup","Aigle","Lion","Tigre","Ours","Faucon","Dragon","Phénix","Corbeau","Faucon"],
    "it" => ["Lupo","Aquila","Leone","Tigre","Orso","Falco","Drago","Fenice","Corvo","Falco"]
];

// ========== ЛОГИКА ==========
class NameGenerator {
    private $culture;
    private $gender;
    private $seed;

    public function __construct($culture = "en", $gender = "any", $seed = null) {
        $this->culture = $culture;
        $this->gender = $gender;
        if ($seed !== null) {
            mt_srand($seed);
        }
    }

    private function getNames($gender) {
        global $NAMES;
        $data = isset($NAMES[$this->culture]) ? $NAMES[$this->culture] : $NAMES["en"];
        if ($gender === "male") return $data["male"];
        if ($gender === "female") return $data["female"];
        return array_merge($data["male"], $data["female"]);
    }

    private function getSurnames() {
        global $NAMES;
        $data = isset($NAMES[$this->culture]) ? $NAMES[$this->culture] : $NAMES["en"];
        return $data["surname"];
    }

    public function generateName($full = false, $nickname = false, $gender = null) {
        global $ADJECTIVES, $NOUNS;
        if ($nickname) {
            $adjList = isset($ADJECTIVES[$this->culture]) ? $ADJECTIVES[$this->culture] : $ADJECTIVES["en"];
            $nounList = isset($NOUNS[$this->culture]) ? $NOUNS[$this->culture] : $NOUNS["en"];
            $adj = $adjList[mt_rand(0, count($adjList)-1)];
            $noun = $nounList[mt_rand(0, count($nounList)-1)];
            return "$adj $noun";
        }
        $pool = $this->getNames($gender ?: $this->gender);
        $first = $pool[mt_rand(0, count($pool)-1)];
        if ($full) {
            $surnames = $this->getSurnames();
            $surname = $surnames[mt_rand(0, count($surnames)-1)];
            return "$first $surname";
        }
        return $first;
    }

    public function generateBatch($count = 1, $full = false, $nickname = false, $gender = null) {
        $result = [];
        for ($i = 0; $i < $count; $i++) {
            $result[] = $this->generateName($full, $nickname, $gender);
        }
        return $result;
    }
}

// ========== ОБРАБОТКА ЗАПРОСОВ ==========
if (php_sapi_name() === 'cli') {
    // CLI
    $options = getopt("", ["count:", "culture:", "gender:", "full", "nickname", "output:"]);
    $count = isset($options['count']) ? (int)$options['count'] : 1;
    $culture = $options['culture'] ?? "en";
    $gender = $options['gender'] ?? "any";
    $full = isset($options['full']);
    $nickname = isset($options['nickname']);
    $output = $options['output'] ?? null;

    $gen = new NameGenerator($culture, $gender);
    $names = $gen->generateBatch($count, $full, $nickname, $gender);
    foreach ($names as $name) echo $name . "\n";
    if ($output) {
        file_put_contents($output, implode("\n", $names));
        echo "Сохранено в $output\n";
    }
    exit;
}

// ========== ВЕБ-ИНТЕРФЕЙС ==========
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Генератор имён (PHP)</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #f4f7fb; margin: 40px; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 20px; border-radius: 16px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        label { display: inline-block; width: 100px; }
        input, select, button { margin: 8px 0; padding: 6px; }
        button { background: #3498db; color: white; border: none; padding: 8px 20px; border-radius: 4px; cursor: pointer; }
        textarea { width: 100%; height: 200px; margin-top: 10px; }
    </style>
</head>
<body>
<div class="container">
    <h1>🏷️ Генератор случайных имён</h1>
    <form method="GET">
        <label>Культура:</label>
        <select name="culture">
            <option value="en" <?= isset($_GET['culture']) && $_GET['culture']=='en' ? 'selected' : '' ?>>English</option>
            <option value="ru" <?= isset($_GET['culture']) && $_GET['culture']=='ru' ? 'selected' : '' ?>>Русский</option>
            <option value="es" <?= isset($_GET['culture']) && $_GET['culture']=='es' ? 'selected' : '' ?>>Español</option>
            <option value="de" <?= isset($_GET['culture']) && $_GET['culture']=='de' ? 'selected' : '' ?>>Deutsch</option>
            <option value="fr" <?= isset($_GET['culture']) && $_GET['culture']=='fr' ? 'selected' : '' ?>>Français</option>
            <option value="it" <?= isset($_GET['culture']) && $_GET['culture']=='it' ? 'selected' : '' ?>>Italiano</option>
        </select><br>
        <label>Пол:</label>
        <select name="gender">
            <option value="any" <?= isset($_GET['gender']) && $_GET['gender']=='any' ? 'selected' : '' ?>>Любой</option>
            <option value="male" <?= isset($_GET['gender']) && $_GET['gender']=='male' ? 'selected' : '' ?>>Мужской</option>
            <option value="female" <?= isset($_GET['gender']) && $_GET['gender']=='female' ? 'selected' : '' ?>>Женский</option>
        </select><br>
        <label>Количество:</label>
        <input type="number" name="count" value="<?= isset($_GET['count']) ? $_GET['count'] : 5 ?>" min="1" max="100"><br>
        <label>Опции:</label>
        <input type="checkbox" name="full" value="1" <?= isset($_GET['full']) ? 'checked' : '' ?>> Имя + фамилия
        <input type="checkbox" name="nickname" value="1" <?= isset($_GET['nickname']) ? 'checked' : '' ?>> Никнейм<br>
        <button type="submit">Сгенерировать</button>
        <button type="button" onclick="document.getElementById('result').select(); document.execCommand('copy');">Копировать</button>
    </form>
    <?php
    if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['culture'])) {
        $culture = $_GET['culture'];
        $gender = $_GET['gender'] ?? 'any';
        $count = (int)($_GET['count'] ?? 5);
        $full = isset($_GET['full']);
        $nickname = isset($_GET['nickname']);
        $gen = new NameGenerator($culture, $gender);
        $names = $gen->generateBatch($count, $full, $nickname, $gender);
        echo '<textarea id="result" readonly>' . htmlspecialchars(implode("\n", $names)) . '</textarea>';
        echo '<button onclick="downloadTxt()">Скачать как .txt</button>';
    }
    ?>
    <script>
        function downloadTxt() {
            var text = document.getElementById('result').value;
            if (!text) return;
            var blob = new Blob([text], {type: 'text/plain'});
            var a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = 'names.txt';
            a.click();
            URL.revokeObjectURL(a.href);
        }
    </script>
</div>
</body>
</html>
