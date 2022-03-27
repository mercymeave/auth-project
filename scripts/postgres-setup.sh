sudo -u postgres createdb authy
sudo -u postgres psql -c "CREATE USER jerimkaura WITH PASSWORD '@Admin_Authy';";
sudo -u postgres psql -c "ALTER ROLE jerimkaura SET client_encoding TO 'utf8';";
sudo -u postgres psql -c "ALTER ROLE jerimkaura SET default_transaction_isolation TO 'read committed';";
sudo -u postgres psql -c "ALTER ROLE jerimkaura SET timezone TO 'UTC';";
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE authy TO jerimkaura;"
./manage.py migrate
