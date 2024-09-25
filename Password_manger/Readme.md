# Python Password Manager ---PassWe

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Project Structure](#project-structure)
7. [Security Considerations](#security-considerations)
8. [Contributing](#contributing)
9. [License](#license)

## Introduction

This Python Password Manager is a command-line application born out of a common struggle: the challenge of managing numerous passwords securely. Like many, I found myself reusing similar passwords across different services and rarely updating them, which left me vulnerable to security breaches. This project addresses these issues by providing a secure way to store, retrieve, and generate strong, unique passwords for various services.

Key features include:
- Secure storage of passwords paired with their corresponding services
- Strong password generation to encourage unique passwords for each service
- Easy retrieval of stored passwords
- Encouragement to regularly update passwords, enhancing overall security

By implementing industry-standard practices for password hashing and encryption, this tool aims to provide a robust solution for personal password management, making it easier to maintain good password hygiene without compromising on security.

**Note:** !!  This project is still under active development and has not yet reached its full potential. There are known issues and areas for improvement. Contributions and feedback are welcome as we work towards a more complete and robust solution. !!

## Development Approach

This project was developed with a focus on writing clean, maintainable, and extensible code. We adhered to several key software engineering principles:

1. **SOLID Principles:** We have leveraged on SOLID principles to improve the quality of software.

2. **Modular Architecture:** The project is organized into distinct modules (auth, password, storage) to separate concerns and improve maintainability.

3. **Design Patterns:** We've implemented patterns like Dependency Injection (e.g., injecting the DataStore into the PasswordManager) to reduce coupling between components.

4. **Code Structure and Organization:** The codebase follows a clear, logical structure with meaningful file and directory names, adhering to Python's PEP 8 style guide.

5. **Error Handling and Logging:** Robust error handling is implemented throughout the application to improve reliability and user experience.

6. **Security Best Practices:** We've implemented secure password hashing, encryption for stored passwords, and input validation to prevent common security vulnerabilities.

While I've made efforts to follow these principles, I acknowledge that there's always room for improvement. As the project evolves, I continue to refine my approach and welcome contributions that align with these principles.

## Features

- A simple user authentication system
- Secure password storage
- Password retrieval
- Password generation
- Password strength checking
- Command-line interface for easy interaction

## Requirements

- Python 3.120
- pip (Python package installer)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/mathew-star/python-password-manager.git
   cd python-password-manager
   ```

2. (Optional) Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the Password Manager, use the following command:

```
python main.py
```

Follow the on-screen prompts to:
1. Register a new user
2. Log in
3. Add a new password
4. Retrieve a stored password
5. Generate a new password



## Project Structure

```
password_manager/
├── main.py
├── auth/
│   ├── __init__.py
│   ├── user.py
│   └── session.py
├── password/
│   ├── __init__.py
│   ├── password_manager.py
│   ├── password_generator.py
│   └── strength_checker.py
├── storage/
│   ├── __init__.py
│   └── data_store.py
├── utils/
│   ├── __init__.py
│   └── encryption.py
└── tests/

```

## Security Considerations

- User authentication passwords are hashed using PBKDF2 with SHA256, which is resistant to rainbow table and brute-force attacks.
- Stored passwords are encrypted before being saved to the JSON file.
- The application uses strong random number generation for password creation.


Note: While we've implemented several security measures, this project is for educational purposes. For a production environment, additional security measures and a more secure storage solution would be necessary.



## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
