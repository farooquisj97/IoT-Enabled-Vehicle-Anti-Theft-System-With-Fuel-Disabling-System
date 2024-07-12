import requests

def main(message):
	# Telegram Bot API token (from BotFather)
	telegram_token = '6766930316:AAGUDAJzTdCvdnzLLzjEsk3wuD5rMZsOhgQ' # Replace with you telegram token


	# Your chat ID (from your bot or other method)
	chat_id = '6771796827'  # Replace with your chat ID

	# URL for sending a message
	telegram_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"

	# Data to send with the request
	data = {
		'chat_id': chat_id,
		'text': message,
	}

	# Send the message
	response = requests.post(telegram_url, data=data)

	# Check if the message was sent successfully
	if response.status_code == 200:
		print("Message sent successfully!")
	else:
		print("Failed to send message.")

if __name__ == '__main__':
	# The message you want to send
	message = "Hello from Python!!"
	main(message)
