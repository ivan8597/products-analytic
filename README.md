# Аналитика продаж
## Как запустить на другом компьютере
### 1. Скопировать проект

Передайте папку `products analytic` (или склонируйте с GitHub):
```bash
git clone https://github.com/<username>/products-analytic.git
cd products-analytic
```

### 2. Установить Python и зависимости

Нужен Python 3.10+.

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Запустить анализ

```bash
python main.py
```

Результаты появятся в папке `output/`.

### Открыть дашборд
```bash
python -m dashboard
```

