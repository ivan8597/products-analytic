from config import OUTPUT_DIR
from data_loader import load_data
from tasks.task1_category_sales import run as run_task1
from tasks.task2_subcategories import run as run_task2
from tasks.task3_average_check import run as run_task3
from tasks.task4_promo_share import run as run_task4
from tasks.task5_margin import run as run_task5
from tasks.task6_abc_analysis import run as run_task6

TASKS = [
    ("1. Продажи по категориям", run_task1),
    ("2. Распределение по подкатегориям", run_task2),
    ("3. Средний чек", run_task3),
    ("4. Доля промо в «Сыры»", run_task4),
    ("5. Маржа по категориям", run_task5),
    ("6. ABC-анализ", run_task6),
]


def run_all() -> dict:
    bundle = load_data()
    results = {}

    for name, task_fn in TASKS:
        print(f"→ {name}")
        results[name] = task_fn(bundle)

    return results


def print_summary(results: dict) -> None:
    task1 = results["1. Продажи по категориям"]
    task3 = results["3. Средний чек"]
    task4 = results["4. Доля промо в «Сыры»"]

    print("\n=== РЕЗУЛЬТАТЫ ===")
    print(f"\n1. Лидер по штукам: {task1['leader']} — {task1['leader_qty']} шт.")
    print(f"\n3. Средний чек: {task3['avg_check']:.2f} руб. ({task3['check_count']} чеков)")
    print(
        f"\n4. Доля промо в «Сыры»: {task4['promo_share']:.2f}% "
        f"({task4['promo_qty']} из {task4['total_qty']} шт.)"
    )
    print(f"\nФайлы сохранены в: {OUTPUT_DIR}")


def main() -> None:
    results = run_all()
    print_summary(results)


if __name__ == "__main__":
    main()
