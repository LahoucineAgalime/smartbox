Database: mysql, Redis

1. Installation dependencies, see requirements.txt
2. Create mysql database: monitor, character set: utf8mb4, collation: utf8mb4_general_ci
3. Modify the database information in smartbox/smartbox/settings.py
4. Enter the smartbox path, enter python manage.py make migrations; python manage.py migrate to create a data table
5. Double-click the start.bat file to start the service
6. Open localhost:8000/admin to configure camera information
7. Open localhost:8000 to view the page
