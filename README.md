# RoMiner (Server)

RoMiner was a live service developed and managed by a high school senior in early 2022, which allowed users to mine cryptocurrency and earn Robux, the virtual currency for the popular online game Roblox. The service successfully attracted around 100 users before it was shut down in late 2022 due to the declining profitability of small-scale cryptocurrency mining.

This repository contains the Python-based server-side code for the RoMiner service. It handled user accounts, tracked mining contributions, converted earnings to Robux, and processed payout requests initiated by users through a separate .exe client application (not included in this repository).

The project demonstrates practical backend development, API integration with mining pools, user data management, and the creation of a functional client-server application that served a live user base.

## Key Features

The RoMiner service provided several key features to its users via a dedicated .exe client application:

*   **Client-Server User Interaction:**
    *   Users interacted with the service primarily through a Windows .exe client application (not included in this repository).
    *   The client handled user registration, login, mining control, balance viewing, and payout requests, communicating with this backend server.

*   **User Account Management (Server-Side):**
    *   The server managed new user signups initiated from the client.
    *   It maintained user-specific data for balances and authentication tokens.
    *   Token-based authentication was used to secure client-server communication for operations like payouts.

*   **Dual Cryptocurrency Mining Support:**
    *   The service enabled users to mine Monero (XMR) and Ethereum (ETH).
    *   This server-side component integrated with Nanopool, MineXMR (for XMR), and Ethermine (for ETH) APIs to fetch mining data.
    *   The actual mining was performed by the user's own mining software, configured via the .exe client to report under their RoMiner username.

*   **Automated Balance Tracking & Conversion (Server-Side):**
    *   The server regularly polled mining pool APIs to retrieve mining contributions attributed to its users.
    *   It calculated individual earnings in USD (based on live XMR/ETH prices) and converted them to Robux using a defined exchange rate (`buxrate`).

*   **Robux Withdrawal System:**
    *   Users could request withdrawal of their accumulated Robux via the .exe client.
    *   The server processed these requests, with `payout.py` handling the backend logic for Robux disbursement.

### User Workflow

1.  **Download & Signup:** A user downloaded the RoMiner .exe client. Using the client, they registered for the service. The client sent signup information to this server, which created an account and an authentication token.
2.  **Login & Mining Configuration:** The user logged in via the .exe client. The client allowed them to configure their mining software (e.g., XMRig, T-Rex) to mine to the service's specified pool addresses, using their RoMiner username as the worker/wallet identifier.
3.  **Mining & Earning:** The user ran their mining software.
    *   This server periodically fetched overall mining statistics from the public pool APIs.
    *   It identified contributions linked to RoMiner users (based on their worker names/IDs) and updated individual Robux balances in its database.
4.  **Balance Check & Payout:** Through the .exe client, the user could check their Robux balance (which queried this server) and request a payout.
5.  **Payout Processing:** Upon receiving a payout request from the client, this server (specifically `payout.py`) handled the backend process of transferring Robux to the user's Roblox account.

## Technical Implementation

The RoMiner service operated on a client-server architecture. This repository contains the **server-side component**, which was built entirely in Python and leveraged several built-in modules. The client-side was a separate .exe application (not included here) that users installed on their machines.

**Server-Side Details:**

*   **Core Technologies:**
    *   **Python 3:** The primary programming language for all server logic.
    *   **`socketserver` Module:** Used to create a multi-threaded TCP server for handling HTTP-like requests from the RoMiner client application. The `BaseHTTPRequestHandler` class was customized to parse these requests.
    *   **`threading` Module:** Enabled concurrent execution of background tasks, notably the `balupdate.py` (XMR) and `ethearn.py` (ETH) scripts responsible for fetching mining data and updating user balances from public pool APIs.

*   **Server Architecture:**
    *   This server listened on a specific port (1003 as per `main.py`) for connections from RoMiner clients.
    *   A custom handler (`MyHandler`) processed incoming client requests by inspecting the request path (e.g., `/connect`, `/balance`, `/payout`) and HTTP method.
    *   Server-side functions in `main.py` handled client requests for user signup, balance inquiries, and payout initiations.

*   **Data Management (Server-Side):**
    *   User data, including authentication tokens (`pw.txt`) and Robux balances (`balance.txt`), was stored in plain text files within a server-side directory structure (`users/<username>/`).
    *   A template directory (`users/userbase/`) was used for initializing new user data.
    *   Files like `passid.txt`, `robloxuser.txt`, `cookie.txt`, and `proxies.txt` supported various server operations including payouts and API interactions.

*   **Security Aspects (Server-Side):**
    *   **Token-Based Authentication:** Client requests for sensitive operations like payouts required a unique token (generated by the server during signup and stored user-side, then validated by the server).
    *   **Proxy Usage:** The `balupdate.py` script utilized a list of proxies (`proxies.txt`) for requests to XMR mining pool APIs, aiding in network load distribution or mitigating rate limits.

*(Note: The security measures were appropriate for the project's scale and context. For larger, commercial applications, more comprehensive security infrastructure would be essential.)*

## Project Structure

The repository is organized into several key Python scripts and data files:

*   **Python Scripts:**
    *   `main.py`: The core server application. It initializes the HTTP server, handles incoming user requests (signup, balance checks, payout requests), and manages user sessions. It also launches the balance update scripts in separate threads.
    *   `balupdate.py`: A script dedicated to fetching Monero (XMR) mining statistics from Nanopool and MineXMR APIs. It calculates user earnings based on their hash contributions and updates their respective balance files.
    *   `ethearn.py`: Similar to `balupdate.py`, but for Ethereum (ETH). It connects to the Ethermine API to get ETH mining data and updates user balances accordingly.
    *   `payout.py`: This script is responsible for handling the Robux payout process. It's triggered by `main.py` upon a user's withdrawal request and likely contains the logic to interact with external systems or APIs for Robux transfer. (The exact mechanics are not fully detailed in the script and would depend on specific Roblox API interaction methods).

*   **Data Files and Directories:**
    *   `README.md`: This file, providing information about the project.
    *   `users/`: A directory containing subdirectories for each registered user.
        *   `users/<username>/balance.txt`: Stores the user's current Robux balance (after conversion from crypto).
        *   `users/<username>/pw.txt`: Stores the user's authentication token.
        *   `users/<username>/lastshares.txt` (for XMR): Stores the last recorded hash count for a user from the XMR mining pool, used to calculate new earnings.
    *   `users/userbase/`: Likely a template directory copied when a new user signs up.
    *   `cookie.txt`: Potentially used to store session cookies for interacting with web services, possibly related to the payout process.
    *   `history.txt`: Could be used for logging transactions or significant server events (though its usage is not explicitly detailed in `main.py`).
    *   `passid.txt`: Seems to temporarily store an identifier (possibly a Roblox user ID or an asset ID) during the payout process.
    *   `proxies.txt`: A list of proxy servers (IP:port:user:pass format) used by `balupdate.py` to make requests to XMR mining pool APIs.
    *   `robloxuser.txt`: Temporarily stores the Roblox username of the user requesting a payout.

## Showcasing Skills

The RoMiner service, particularly this server-side component, demonstrates a range of valuable skills and experiences:

*   **Entrepreneurial Initiative & Project Management:**
    *   Conceptualizing, developing, and launching a complete service (client application and this server) as a high school senior.
    *   Managing a live service with approximately 100 active users, including user support and operational maintenance until its shutdown.

*   **Client-Server Architecture:**
    *   Designing and implementing a client-server application, where this Python server formed the backend.
    *   Handling API-like requests from a separate client application.

*   **Backend Development (Python):**
    *   Proficient Python programming for server-side logic.
    *   Building a custom TCP server using the `socketserver` module to handle client communications.
    *   Implementing request handling, parsing, and routing logic.

*   **API Integration:**
    *   Interacting with multiple third-party REST APIs (Nanopool, MineXMR, Ethermine for mining data; CryptoCompare for price feeds) to fetch and utilize external data.
    *   Parsing JSON responses and integrating them into the service's operations.

*   **Concurrent Programming:**
    *   Using the `threading` module for concurrent background tasks, ensuring the server remained responsive while performing periodic updates (e.g., fetching balances).

*   **User Account Management (Backend):**
    *   Implementing server-side logic for user registration.
    *   Managing user data (profiles, balances, authentication tokens) through file-based storage.
    *   Implementing a token-based authentication system for client-server communication.

*   **System Design (Server-Side):**
    *   Developing a modular server with distinct scripts for core functions (main server logic, XMR updates, ETH updates, payouts).

*   **File I/O & Data Manipulation:**
    *   Utilizing file operations for data persistence and configuration.
    *   Manipulating data for calculations (e.g., currency conversion, mining share calculations).

*   **Problem Solving & Adaptation:**
    *   Creating a system to automate cryptocurrency earnings and their conversion to Robux.
    *   Implementing proxy rotation for API interactions.
    *   Making the decision to shut down the service due to changing external factors (mining profitability).

This project is a testament to the ability to take an idea from conception to a functional, user-facing service, combining technical development with practical operational management.

## Disclaimer

**Important Information about RoMiner:**

The RoMiner service was operational in 2022 and was shut down in late 2022 primarily due to the declining profitability of small-scale cryptocurrency mining, which was its core reward mechanism.

This repository contains the **server-side code** for the RoMiner service. While it demonstrates the backend logic and architecture, **this server code is not directly runnable or deployable in its current state.** It requires:
*   The original client-side `.exe` application (not included in this repository) for user interaction.
*   The specific production environment, configurations, and credentials (e.g., for mining pool APIs, Robux payout mechanisms) that were used when the service was live. These are not provided.

The primary purpose of sharing this server code is to **showcase the software development, backend engineering, and project management skills** demonstrated in its creation and operation. It serves as a portfolio piece illustrating a real-world application that was designed, built, and managed for a user base.
