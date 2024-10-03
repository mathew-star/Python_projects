class MessageFormat:
    @staticmethod
    def format_message(sender, message):
        return f"[{sender}]: {message}"

    @staticmethod
    def parse_message(formatted_message):
        parts = formatted_message.split(": ", 1)
        return parts[0], parts[1] if len(parts) > 1 else ""
