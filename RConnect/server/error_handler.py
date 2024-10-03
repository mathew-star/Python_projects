class ErrorHandler:
    def handle_error(self, error_message, log=False):
        if log:
            print(f"Logged Error: {error_message}")
        else:
            print(f"Error: {error_message}")
