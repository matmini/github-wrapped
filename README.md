# 1. Clone the repository
git clone [<your-repo-url>]

# 2. Duplicate the example template into a real .env file
cp .env.example .env

# 3. Open the new .env file and type in your actual passwords!
nano .env  # Or open it in your code editor

# 4. Spin up Docker normally
docker-compose up -d --build
docker-compose run app