from modules.mailbot.mailbot import MailBot

# entry point for mailbot
mail_bot = MailBot()
mail_bot.poll_inbox()
