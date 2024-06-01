# pvp_task0805
тестовое задание. разработка реферальной платформы.

## инструменты:
- python 3.10
- django 3.2

## о структуре. реализованы следующие страницы:
- /register # страница регистрации
- /login # страница авторизации
- /profile # страниа профиля пользователя. содержит реферальную ссылку пользователя. генерируется автоматически при создании профиля.

### на странице профиля доступны следующие ссылки:
- /my_refs/ # страничка содержит список с информацией о всех пользователях зарегистрировавашихся по реферальной ссылке из профиля пользователя. информация включает в себя имя реферррала, количество покупок сделанных реферралом и общая потраченная сумма реферралом.

- /all_refs/ # страничка содержит информацию о всех пользователях зарегистрировавшихся по реферальным ссылкам. информация включает в себя имя реферрера и имя реферрала.

- /buy_page/ # страница покупок. содержит:
* информацию о балансе пользователя.
* ссылку, активирующую получение денег /give_money/
* форму покупки, где вводится сумма покупки.

### реализована функция вознаграждения для реферрера.
когда покупки совершают приглашенные им пользователи. реферрер получает %5 процентов от суммы покупки.

## тесты для основных случаев.
### внутринние. без использования http запросов к тестовому серверу. test_inner.py:

- test_create_user
- test_create_user_with_ref_code
- test_get_user_by_id
- test_get_referals_from_user
- test_get_all_referals
- test_get_money
- test_can_buy_thin
- test_can_get_referral
- test_can_control_buy_from_refl

### http-тесты. test_base_http.py:

- test_redirect_after_register_user
- test_can_get_ref_code
- test_can_reg_from_ref_code
- test_ref_code_in_profile_page
- test_myrefs_link_in_profile_page
- test_can_view_own_referals
- test_allrefs_link_in_profile_page
- test_can_view_all_referals
- test_buypage_link_in_profile_page
- test_can_view_buy_page
- test_buy_page_have_balance
- test_give_money
- test_can_buy_thing
- test_pay_to_referrer
- test_can_view_refs_purchases