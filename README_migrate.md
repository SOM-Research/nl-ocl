# 

# Commands:

+ To migrate Spider from /data/spider:
    - Download content to /data/spider
    - Exec: python manage.py migrateFromSpider migrateTables
    - Exec: python manage.py migrateFromSpider migrateQuestions
    - Exec: python manage.py migrateFromSpider migrateAssociations

+ To migrate WikiSQL from /data:
    - Download a copy to /data
    - Exec: python manage.py migrateFromWikiSQL migrate