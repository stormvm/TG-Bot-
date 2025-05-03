from aiogram import Router, types, F

router = Router()

@router.message(F.text & F.command("buy"))
async def process_buy_command(message: types.Message):
    await message.answer("Please provide the details of your purchase.")