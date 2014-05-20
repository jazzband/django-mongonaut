=========
CHANGELOG
=========

* 0.2.21 (05/19/2014)

    * Backwards compatible templates so things work in Django 1.4 again. (@ashishsingh2205)

* 0.2.20 (26/03/2014)

    * Python 3.3 compatibility (@haard)
    * Working test harness (@j1z0)
    * Fixed missing url function call in documentation (@JAORMX)

* 0.2.19 (18/07/2013)

    * Use Select widget if choices defined for a field (@jeff-ogmento )
    * Use ordering if defined in MongoAdmin class (@jeff-ogmento )
    * Respect order of list_fields in admin class (@jeff-ogmento )
    * Fixed "django.conf.urls.defaults is deprecated" (@swaroopch)
    * Fix search (@swaroopch)
    * Make index page also password-protected (@swaroopch)

* 0.2.18 Various things

* 0.2.17 Can now add, and modify ListFields and Embedded document fields @garrypolley

* 0.2.16 ListFields can be added and updated @garrypolley

* 0.2.15 Editing or Adding a document does not require all fields to be filled out @garrypolley

* 0.2.14 Fixed pymongo version thanks to @marsam and pagination fixes thanks to @jerzyk

* 0.2.13 Fields validation and type conversion thanks to @jerzyk

* 0.2.12 Bump to mongoengine 0.6.2, PEP-8, and fixing the is_authenticated problem in default permission controls.

* 0.2.11 Change style over to Twitter Bootstrap 2.0.0, Add templates to manifest

* 0.2.10 Proper Reference field saves, more permission fixes

* 0.2.9 Permissions correction - Do remember this is in ALPHA!!!

* 0.2.8 Test components, permission controls in the views, first pass on deletes, Reference field display and some really bad SELECT widget implementations on it.

* authenticated Permissions refactor, list_fields implementation, and ability to add new documents

* 0.2.6 Major performance enhancement of the DocumentListView

* 0.2.5 Added EmbeddedDocument to form views

* 0.2.4 Installation fix

* 0.2.3 Installation fix

* 0.2.2 Supporting of Boolean and Datetime fields and search to boot

* 0.2.1 Project description fix

* 0.2.0 basic form saves, pagination, and formatting

* 0.1.0 Inception and fundamentals
