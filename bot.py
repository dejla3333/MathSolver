from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from sympy import *


TOKEN = ""

keyboard = [
    [" Calculator"],
    [" Help"]
]


menu = ReplyKeyboardMarkup(
    keyboard,
    resize_keyboard=True
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        """
 Welcome to Math Solver Bot

Send any math expression.

Examples:

5+10

20/4

2^5

sqrt(81)

x^2-9=0
        """,
        reply_markup=menu
    )


def solve_math(expression):

    try:

        expression = expression.replace("^", "**")


        if "=" in expression:

            x = symbols("x")

            left, right = expression.split("=")

            result = solve(
                Eq(
                    sympify(left),
                    sympify(right)
                ),
                x
            )

            return result


        else:

            result = sympify(expression)

            return simplify(result)


    except:

        return None



async def calculator(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text


    result = solve_math(text)


    if result is not None:


        await update.message.reply_text(
            f"""
 Math Solver

📌 Problem:
{text}

 Answer:
{result}
"""
        )


    else:


        await update.message.reply_text(
            """
❌ Cannot solve.

Examples:

10+20

5^3

sqrt(100)

x^2-4=0
"""
        )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text


    if text == " Calculator":

        await update.message.reply_text(
            " Send your math expression."
        )


    elif text == " Help":

        await update.message.reply_text(
            """
 Supported:

+  Addition
-  Subtraction
*  Multiplication
/  Division
^  Power
sqrt() Root

Example:

sqrt(144)
2^10
x^2-9=0
"""
        )



app = Application.builder().token(TOKEN).build()


app.add_handler(
    CommandHandler(
        "start",
        start
    )
)


app.add_handler(
    MessageHandler(
        filters.Regex(r".*(\+|\-|\*|/|\^|sqrt|=).*"),
        calculator
    )
)


app.add_handler(
    MessageHandler(
        filters.TEXT,
        buttons
    )
)



print(" Math Solver Bot is running...")


app.run_polling()