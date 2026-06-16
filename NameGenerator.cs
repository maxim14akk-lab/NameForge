// NameGenerator.cs - Генератор случайных имён на C# (CLI + WinForms)
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace NameGenerator
{
    public static class Data
    {
        public static Dictionary<string, Dictionary<string, List<string>>> Names = new Dictionary<string, Dictionary<string, List<string>>>();
        public static Dictionary<string, List<string>> Adjectives = new Dictionary<string, List<string>>();
        public static Dictionary<string, List<string>> Nouns = new Dictionary<string, List<string>>();

        static Data()
        {
            // en
            var en = new Dictionary<string, List<string>>();
            en["male"] = new List<string> { "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles" };
            en["female"] = new List<string> { "Mary", "Patricia", "Jennifer", "Linda", "Barbara", "Elizabeth", "Susan", "Jessica", "Sarah", "Karen" };
            en["surname"] = new List<string> { "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez" };
            Names["en"] = en;
            // ru
            var ru = new Dictionary<string, List<string>>();
            ru["male"] = new List<string> { "Александр", "Дмитрий", "Максим", "Сергей", "Андрей", "Алексей", "Иван", "Евгений", "Михаил", "Николай" };
            ru["female"] = new List<string> { "Анна", "Мария", "Екатерина", "Ольга", "Татьяна", "Наталья", "Ирина", "Елена", "Светлана", "Юлия" };
            ru["surname"] = new List<string> { "Иванов", "Петров", "Сидоров", "Кузнецов", "Смирнов", "Волков", "Морозов", "Новиков", "Козлов", "Лебедев" };
            Names["ru"] = ru;
            // ... остальные культуры
            Adjectives["en"] = new List<string> { "Brave", "Clever", "Swift", "Bold", "Wise", "Fierce", "Gentle", "Loyal", "Valiant", "Bright" };
            Adjectives["ru"] = new List<string> { "Храбрый", "Умный", "Быстрый", "Смелый", "Мудрый", "Свирепый", "Нежный", "Верный", "Доблестный", "Светлый" };
            Nouns["en"] = new List<string> { "Wolf", "Eagle", "Lion", "Tiger", "Bear", "Hawk", "Dragon", "Phoenix", "Raven", "Falcon" };
            Nouns["ru"] = new List<string> { "Волк", "Орёл", "Лев", "Тигр", "Медведь", "Ястреб", "Дракон", "Феникс", "Ворон", "Сокол" };
        }
    }

    public class NameGenerator
    {
        private string culture;
        private string gender;
        private Random random;

        public NameGenerator(string culture, string gender, int? seed = null)
        {
            this.culture = culture;
            this.gender = gender;
            this.random = seed.HasValue ? new Random(seed.Value) : new Random();
        }

        private List<string> GetNames(string gender)
        {
            var data = Data.Names.ContainsKey(culture) ? Data.Names[culture] : Data.Names["en"];
            if (gender == "male") return data["male"];
            if (gender == "female") return data["female"];
            var combined = new List<string>(data["male"]);
            combined.AddRange(data["female"]);
            return combined;
        }

        private List<string> GetSurnames()
        {
            var data = Data.Names.ContainsKey(culture) ? Data.Names[culture] : Data.Names["en"];
            return data["surname"];
        }

        public string GenerateName(bool full, bool nickname, string gender)
        {
            if (nickname)
            {
                var adjList = Data.Adjectives.ContainsKey(culture) ? Data.Adjectives[culture] : Data.Adjectives["en"];
                var nounList = Data.Nouns.ContainsKey(culture) ? Data.Nouns[culture] : Data.Nouns["en"];
                string adj = adjList[random.Next(adjList.Count)];
                string noun = nounList[random.Next(nounList.Count)];
                return adj + " " + noun;
            }
            var pool = GetNames(gender);
            string first = pool[random.Next(pool.Count)];
            if (full)
            {
                var surnames = GetSurnames();
                string surname = surnames[random.Next(surnames.Count)];
                return first + " " + surname;
            }
            return first;
        }

        public List<string> GenerateBatch(int count, bool full, bool nickname, string gender)
        {
            var result = new List<string>();
            for (int i = 0; i < count; i++)
            {
                result.Add(GenerateName(full, nickname, gender));
            }
            return result;
        }
    }

    class Program
    {
        [STAThread]
        static void Main(string[] args)
        {
            if (args.Length > 0)
            {
                // CLI режим
                RunCLI(args);
            }
            else
            {
                // GUI режим (WinForms)
                Application.EnableVisualStyles();
                Application.Run(new MainForm());
            }
        }

        static void RunCLI(string[] args)
        {
            // Простейший разбор аргументов (можно использовать библиотеку)
            int count = 1; string culture = "en"; string gender = "any"; bool full = false, nickname = false; string output = null;
            for (int i = 0; i < args.Length; i++)
            {
                switch (args[i])
                {
                    case "--count": count = int.Parse(args[++i]); break;
                    case "--culture": culture = args[++i]; break;
                    case "--gender": gender = args[++i]; break;
                    case "--full": full = true; break;
                    case "--nickname": nickname = true; break;
                    case "--output": output = args[++i]; break;
                }
            }
            var gen = new NameGenerator(culture, gender);
            var names = gen.GenerateBatch(count, full, nickname, gender);
            foreach (var n in names) Console.WriteLine(n);
            if (!string.IsNullOrEmpty(output))
            {
                File.WriteAllLines(output, names);
                Console.WriteLine($"Сохранено в {output}");
            }
        }
    }

    public class MainForm : Form
    {
        private ComboBox cultureBox, genderBox;
        private NumericUpDown countBox;
        private CheckBox fullCheck, nickCheck;
        private TextBox resultBox;
        private Button generateBtn, saveBtn;

        public MainForm()
        {
            this.Text = "Генератор имён";
            this.Size = new System.Drawing.Size(500, 400);
            this.StartPosition = FormStartPosition.CenterScreen;

            var panel = new TableLayoutPanel { Dock = DockStyle.Fill, ColumnCount = 2, RowCount = 6, Padding = new Padding(10) };
            panel.RowStyles.Add(new RowStyle(SizeType.AutoSize));
            panel.RowStyles.Add(new RowStyle(SizeType.AutoSize));
            panel.RowStyles.Add(new RowStyle(SizeType.AutoSize));
            panel.RowStyles.Add(new RowStyle(SizeType.AutoSize));
            panel.RowStyles.Add(new RowStyle(SizeType.AutoSize));
            panel.RowStyles.Add(new RowStyle(SizeType.Percent, 100));

            panel.Controls.Add(new Label { Text = "Культура:", AutoSize = true }, 0, 0);
            cultureBox = new ComboBox { DropDownStyle = ComboBoxStyle.DropDownList, Items = { "en", "ru", "es", "de", "fr", "it" }, SelectedIndex = 0 };
            panel.Controls.Add(cultureBox, 1, 0);

            panel.Controls.Add(new Label { Text = "Пол:", AutoSize = true }, 0, 1);
            genderBox = new ComboBox { DropDownStyle = ComboBoxStyle.DropDownList, Items = { "any", "male", "female" }, SelectedIndex = 0 };
            panel.Controls.Add(genderBox, 1, 1);

            panel.Controls.Add(new Label { Text = "Количество:", AutoSize = true }, 0, 2);
            countBox = new NumericUpDown { Minimum = 1, Maximum = 100, Value = 1 };
            panel.Controls.Add(countBox, 1, 2);

            fullCheck = new CheckBox { Text = "Имя + фамилия", AutoSize = true };
            panel.Controls.Add(fullCheck, 1, 3);
            nickCheck = new CheckBox { Text = "Никнейм", AutoSize = true };
            panel.Controls.Add(nickCheck, 1, 4);

            generateBtn = new Button { Text = "Сгенерировать", AutoSize = true };
            generateBtn.Click += Generate;
            panel.Controls.Add(generateBtn, 0, 5);
            saveBtn = new Button { Text = "Сохранить в файл", AutoSize = true };
            saveBtn.Click += Save;
            panel.Controls.Add(saveBtn, 1, 5);

            resultBox = new TextBox { Multiline = true, Dock = DockStyle.Fill, ReadOnly = true, ScrollBars = ScrollBars.Vertical };
            panel.Controls.Add(resultBox, 0, 6);
            panel.SetColumnSpan(resultBox, 2);
            this.Controls.Add(panel);
        }

        private void Generate(object sender, EventArgs e)
        {
            string culture = cultureBox.SelectedItem.ToString();
            string gender = genderBox.SelectedItem.ToString();
            int count = (int)countBox.Value;
            bool full = fullCheck.Checked;
            bool nickname = nickCheck.Checked;
            var gen = new NameGenerator(culture, gender);
            var names = gen.GenerateBatch(count, full, nickname, gender);
            resultBox.Text = string.Join("\n", names);
        }

        private void Save(object sender, EventArgs e)
        {
            if (string.IsNullOrEmpty(resultBox.Text)) return;
            var saveDialog = new SaveFileDialog { Filter = "Text files|*.txt|CSV files|*.csv", DefaultExt = "txt" };
            if (saveDialog.ShowDialog() == DialogResult.OK)
            {
                File.WriteAllText(saveDialog.FileName, resultBox.Text);
                MessageBox.Show($"Сохранено в {saveDialog.FileName}");
            }
        }
    }
}
