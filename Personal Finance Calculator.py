# -*- coding: utf-8 -*-


"""
Program : Personal Finance Calculator
Author  : Debasmita Ghosh
Date    : February 2026
Purpose : Track monthly income, expenses, and savings using the 50/20/30 rule.
          Supports multiple months, saves reports to a file, and gives analysis.
"""


import datetime

# ─────────────────────────────────────────────
#  CONSTANTS  (50 / 20 / 30 rule targets)
# ─────────────────────────────────────────────
FUNDAMENTALS_TARGET = 0.50
FUN_TARGET          = 0.20
FUTURE_TARGET       = 0.30

REPORT_FILE = "finance_report.txt"

# ─────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────

def get_float_input(prompt, allow_zero=True):
    """
    Asks the user for a number.
    Keeps asking (while loop) until a valid non-negative number is entered.
    """
    while True:
        try:
            value = float(input(prompt))
            if not allow_zero and value <= 0:
                print("  ⚠  Value must be greater than 0. Please try again.")
            elif value < 0:
                print("  ⚠  Value cannot be negative. Please try again.")
            else:
                return value
        except ValueError:
            print("  ⚠  Invalid input. Please enter a number.")


def collect_expenses(category_name, items):
    """
    Uses a FOR LOOP to collect expense amounts for a list of items.
    Returns a dictionary {item_name: amount} and the total.
    """
    print(f"\n  {'─'*36}")
    print(f"  {category_name}")
    print(f"  {'─'*36}")

    expenses = {}
    for item in items:                          # ← FOR LOOP
        amount = get_float_input(f"  {item} (Rs): ")
        expenses[item] = amount

    total = sum(expenses.values())
    print(f"\n  Total {category_name}: Rs {total:,.2f}")
    return expenses, total


def evaluate_category(label, actual, target_amount, target_pct):
    """
    Compares actual spending against the 50/20/30 target.
    Returns a result string and a status emoji.
    """
    diff = actual - target_amount
    pct_used = (actual / target_amount * 100) if target_amount > 0 else 0

    if actual == target_amount:
        status = "✅  Goal met exactly!"
    elif actual > target_amount:
        status = f"🔴  Over by Rs {diff:,.2f}  ({pct_used:.1f}% of target used)"
    else:
        status = f"🟢  Under by Rs {abs(diff):,.2f}  ({pct_used:.1f}% of target used)"

    return status


def save_report(name, month_label, monthly_income,
                fund_expenses, fund_total,
                fun_expenses,  fun_total,
                fut_expenses,  fut_total,
                savings):
    """
    Saves a formatted text report to finance_report.txt.
    Appends so previous months are preserved.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = []
    lines.append("\n" + "=" * 52)
    lines.append(f"  FINANCE REPORT — {name.upper()}  |  {month_label}")
    lines.append(f"  Generated: {timestamp}")
    lines.append("=" * 52)
    lines.append(f"  Monthly Income : Rs {monthly_income:,.2f}")
    lines.append("")

    # Write each category using a for loop over the expense dicts
    for section, exp_dict, total in [
        ("FUNDAMENTALS (50%)", fund_expenses, fund_total),
        ("FUN (20%)",          fun_expenses,  fun_total),
        ("FUTURE YOU (30%)",   fut_expenses,  fut_total),
    ]:
        lines.append(f"  {section}")
        for item, amount in exp_dict.items():   # ← FOR LOOP over dictionary
            lines.append(f"    {item:<30} Rs {amount:>10,.2f}")
        lines.append(f"    {'TOTAL':<30} Rs {total:>10,.2f}")
        lines.append("")

    lines.append(f"  NET SAVINGS    : Rs {savings:,.2f}")
    lines.append("=" * 52)

    # FILE HANDLING — append to file
    with open(REPORT_FILE, "a") as f:
        f.write("\n".join(lines) + "\n")

    print(f"\n  📄  Report saved to '{REPORT_FILE}'")


def show_summary(name, monthly_income,
                 fund_total, fun_total, fut_total):
    """Prints the final analysis to the terminal."""

    total_expenses = fund_total + fun_total + fut_total
    savings        = monthly_income - total_expenses

    fund_target = monthly_income * FUNDAMENTALS_TARGET
    fun_target  = monthly_income * FUN_TARGET
    fut_target  = monthly_income * FUTURE_TARGET

    print("\n" + "=" * 52)
    print(f"  SUMMARY FOR {name.upper()}")
    print("=" * 52)
    print(f"  Monthly Income   : Rs {monthly_income:,.2f}")
    print(f"  Total Expenses   : Rs {total_expenses:,.2f}")
    print(f"  Net Savings      : Rs {savings:,.2f}")
    print("─" * 52)
    print("  50/20/30 ANALYSIS")
    print("─" * 52)

    categories = [
        ("Fundamentals (50%)", fund_total, fund_target),
        ("Fun         (20%)", fun_total,  fun_target),
        ("Future You  (30%)", fut_total,  fut_target),
    ]

    for label, actual, target in categories:    # ← FOR LOOP
        status = evaluate_category(label, actual, target,
                                   target / monthly_income)
        print(f"\n  {label}")
        print(f"    Spent  : Rs {actual:,.2f}  /  Target: Rs {target:,.2f}")
        print(f"    Status : {status}")

    print("\n" + "=" * 52)
    return savings


# ─────────────────────────────────────────────
#  EXPENSE ITEM LISTS
# ─────────────────────────────────────────────

FUNDAMENTAL_ITEMS = ["Rent", "Groceries", "Credit Card Bill",
                     "Transport", "Miscellaneous"]

FUN_ITEMS = ["Netflix Subscription", "Spotify Subscription",
             "Shopping", "Eating Out"]

FUTURE_ITEMS = ["Equity Stocks", "Bonds", "Mutual Funds",
                "Index Funds", "Gold ETF", "Emergency Fund Deposit"]


# ─────────────────────────────────────────────
#  MAIN PROGRAM
# ─────────────────────────────────────────────

def main():
    print("\n" + "=" * 52)
    print("        PERSONAL FINANCE CALCULATOR")
    print("         — 50 / 20 / 30 Rule Tracker —")
    print("=" * 52)

    name = input("\n  Enter your name: ").strip() or "User"

    # ── WHILE LOOP: lets user track multiple months ──────────────────
    while True:
        month_label = input("\n  Enter month (e.g. March 2026): ").strip()
        if not month_label:
            month_label = datetime.datetime.now().strftime("%B %Y")

        # Income
        print()
        monthly_income = get_float_input(
            "  Enter monthly income (Rs): ", allow_zero=False
        )

        # Expenses — each uses a for loop internally
        fund_expenses, fund_total = collect_expenses(
            "FUNDAMENTALS (Needs)", FUNDAMENTAL_ITEMS
        )
        fun_expenses,  fun_total  = collect_expenses(
            "FUN (Wants)", FUN_ITEMS
        )
        fut_expenses,  fut_total  = collect_expenses(
            "FUTURE YOU (Investments)", FUTURE_ITEMS
        )

        # Summary
        savings = show_summary(name, monthly_income,
                               fund_total, fun_total, fut_total)

        # Save to file
        save_report(name, month_label, monthly_income,
                    fund_expenses, fund_total,
                    fun_expenses,  fun_total,
                    fut_expenses,  fut_total,
                    savings)

        # ── Ask if user wants to add another month ───────────────────
        print("\n  Would you like to track another month?")
        again = input("  Enter 'yes' to continue or any key to exit: ").strip().lower()
        if again != "yes":
            break   # exits the while loop

    print("\n  Thanks for using the Finance Calculator. Goodbye! 👋\n")


# ─────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()
