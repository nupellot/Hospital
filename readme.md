# Госпиталь
Сервис предназначен для помощи в организации работы госпиталя. Рабочий прототип находится по адресу
https://hospital-production.up.railway.app/auth/
Система построена на микрофреймворке Flask с использованием jinja2, html, css и ванильного JavaScript.


## Сайт
Система реализована в виде сайта, дающего пользователям возможность взаимодействия с базой данных, хранящей информацию о пациентах, врачах, палатах и отделениях.
##### Демонстрация внешнего вида сайта
https://github.com/nupellot/Hospital/assets/54524404/cf1612ff-aea6-4bd6-8389-ea8bc57fa15a

### Доктор
После авторизации доктору открывается панель инструментов. Она предоставляет возможность проведения осмотров - как для собственных пациентов, для которых врач является лечащим, так и для сторонних. Также реализована возможность выписки приписанных к нему пациентов.
##### Демонстрация пользовательского пути доктора
https://github.com/nupellot/Hospital/assets/54524404/604b54c6-724f-433f-aaf4-2e9a6ca820ea

### Пациент
При входе на сайт пользователь может увидеть все свои истории болезни с подробным описанием каждой из них. Имеются записи о лечащих врачах, всех проведенных ими или приглашенными врачами осмотрах, времени поступления в госпиталь, времени выписки из него и другая важная информация. Ввиду особенностей организации госпиталя у больного нет доступа к информации о других палатах, отделениях, палатах или пациентах.
##### Демонстрация пользовательского пути пациента
https://github.com/nupellot/Hospital/assets/54524404/55b947a5-a7fc-43b4-9586-3bb9aa593dfc

### Регистратор
Регистратор - человек, работающий в регистратуре и занимающийся внесением новых пациентов в базу. Для этого ему доступна информация о структуре госиталя - общая страница с инфорацией обо всех отделениях и страницы каждой конкретной палаты. Также у него есть доступ ко всем страницам пациентов и врачей, на которых он может узнать дополнительную важную информацию. 
#### Демонстрация пользовательского пути регистратора
https://github.com/nupellot/Hospital/assets/54524404/f68dd29c-f213-44d1-92e3-fa4deb704fa7


## База данных
Для корректной работы сервиса на вашей локальной машине нужно изменить параметры подключения к БД, хранящиеся в конфиге по адресу /configs/db.json, а также обеспечить следующую структуру базы данных.
##### Инфологическая модель БД
![db_scheme](https://github.com/nupellot/Hospital/assets/54524404/c68ce158-1746-4c62-be95-8c679217e480)

## Более подробное описание предметной области
Госпиталь состоит из отделений. Известно сколько палат в каждом отделении, этаж, где оно расположено, фамилия заведующего. В каждом отделении работают врачи. При этом каждый врач по основной специальности работает только в одном отделении. Каждому врачу присвоен уникальный номер, известны его фамилия, паспортные данные, адрес, год рождения, специализация, дата поступления на работу в госпиталь. В каждом отделении находится несколько палат. Каждая палата имеет номер, тип (обычная или VIP) и характеризуется количеством мест. При поступлении пациента в госпиталь его направляют в конкретное отделение и определенную палату. О каждом пациенте известны его паспортные данные, адрес, дата рождения. Каждому пациенту при поступлении назначается один лечащий врач из числа врачей отделения. Но каждый лечащий врач может вести нескольких пациентов. На каждого больного ведется история болезни. История болезни открывается при поступлении пациента в госпиталь и закрывается при выписке пациента, т.е. известны даты поступления и выписки пациента. Если пациент поступает в госпиталь повторно, то на него открывается новая история болезни. Каждая история болезни имеет уникальный номер, в нее при поступлении заносится основный диагноз, дата поступления пациента и в дальнейшем дата выписки из госпиталя. Для консультаций пациентов в случае необходимости могут приглашаться врачи из других отделений. Кажлый осмотр пациента врачом заканчивается записью в истории болезни. Каждая запись содержит сведения о враче, сделавшим запись, дату, основные наблюдения и назначения, сделанные в результате осмотра.
