#!/usr/bin/env python3
"""
Вклеивает общие части в index.html, realdeal.html, kino-i-tv.html и design-system.html.

Левая колонка живёт в одном месте — parts/. Раньше она существовала
в двух копиях и разъехалась сама: на главной оказалась чёрная кнопка
без аватара, внутри — аватар и серый чип. Никто этого не решал,
расхождение накопилось за двадцать версий.

С 2026-10-12 колонка одна на обеих страницах (макеты «Главная-v2», «Кейс-v2»):
«кто я» с интро, список кейсов по центру, внизу резюме и контакты.

Часть может быть общей (одна строка-путь) или разной по страницам
(словарь: страница → путь; страницы без записи получают пустоту).

Запуск:  python3 build.py
"""
import pathlib

HERE = pathlib.Path(__file__).parent

# fmt=True — в части есть {поля}, они подставляются из META[страница]
PARTS = [
    ('HEAD',       'html', 'parts/head.html', True),
    ('BASE',       'css',  'parts/base.css'),
    # шапка телефона и меню (≤800): шапка одна для всех, меню — кодом (текущий кейс)
    ('MBAR',       'html', 'parts/mbar.html'),
    ('MENU',       'html', None),
    ('RAIL_HEAD',  'html', 'parts/rail_head.html', True),
    ('RAIL_FOOT',  'html', 'parts/rail_foot.html'),
    # правила и скрипт страницы кейса — общие для всех внутренних страниц
    # (realdeal, kino-i-tv…); на главной маркеров нет, там часть пропускается
    ('CASE',       'css',  'parts/case.css'),
    ('CASE_JS',    'html', 'parts/case.js'),
    # собираются кодом из CASES, файла нет: содержимое зависит от страницы
    ('CASE_TREE',  'html', None),
    ('CASE_MORE',  'html', None),
]
PAGES = ['index.html', 'realdeal.html', 'kino-i-tv.html', 'design-system.html', 'second-screen.html']

# Порядок — как в ленте на главной: по силе кейса, не по дате.
# brand: значение атрибута data-brand, по нему CSS берёт цвет продукта.
# anchors: якоря разделов кейса; у всех внутренних страниц они одинаковы.
CASES = [
    dict(slug='realdeal',      name='Real Deal',           domain='B2B SaaS · PropTech',        brand='realdeal'),
    dict(slug='kino-i-tv',     name='Кино и ТВ',          domain='B2C · Streaming TV',         brand='kino-i-tv'),
    dict(slug='second-screen', name='Второй экран',       domain='B2C · TV &amp; Media',       brand='second-screen'),
    dict(slug='design-system', name='DREAMPlatform',      domain='B2B SaaS · Design system',   brand='design-system'),
    # в работе: карточка без ссылки на 30% (soon=True), страницы нет
    dict(slug='smart-home',    name='Умный дом',          domain='B2C · TV',                   brand='smart-home', soon=True),
]
ANCHORS = [('#problem', 'Проблема'), ('#work', 'Мой вклад'), ('#result', 'Результат')]

# Шапка у страниц одна, различаются только значения. Копий parts/head_*.html
# не делаем специально: две копии расходятся — так уже было с левой колонкой.
# Имя в колонке: на главной это просто текст (ссылка вела бы сама на себя),
# на внутренней странице — ссылка на главную.
WHO = 'Задорожная Екатерина —<br>Senior Product Designer.'
META = {
    'index.html': dict(
        who=WHO,
        title='Задорожная Екатерина — Senior Product Designer',
        description='Senior Product Designer, 9+ лет в B2B SaaS и B2C: PropTech, '
                    'Streaming TV, дизайн-системы. $7.5M инвестиций и рост аудитории '
                    '100% YoY на продуктах, которые я вела.',
        url='https://codedesign.ru/',
        og_type='profile',
        og_title='Задорожная Екатерина — Senior Product Designer',
        og_description='9+ лет в B2B SaaS и B2C. Сложные интерфейсы, дизайн-системы, запуск продуктов с нуля. $7.5M на Демо + MVP, ×2 аудитории на редизайне.',
        og_image='og/og.png',
    ),
    'realdeal.html': dict(
        who=f'<a href="/">{WHO}</a>',
        title='Real Deal — Екатерина Задорожная',
        description='Кейс Real Deal: первая в ОАЭ платформа онлайн-сделок с коммерческой '
                    'недвижимостью. Роль Lead Product Designer, путь от аналитического '
                    'демо до коммерческого MVP.',
        url='https://codedesign.ru/realdeal',
        og_type='article',
        og_title='Демо + MVP, поднявшие $7.5M',
        og_description='Первая в ОАЭ платформа онлайн-сделок с коммерческой недвижимостью. Аналитика на данных земельного департамента Дубая.',
        og_image='og/og_realdeal.png',
    ),
    'kino-i-tv.html': dict(
        who=f'<a href="/">{WHO}</a>',
        title='Триколор Кино и ТВ — Екатерина Задорожная',
        description='Кейс «Триколор Кино и ТВ»: редизайн онлайн-кинотеатра для базы 12 млн '
                    'абонентов. Product Designer: доступ к контенту, вход, навигация, '
                    'единые принципы Smart TV и Apple TV. Аудитория выросла до 1,7 млн.',
        url='https://codedesign.ru/kino-i-tv',
        og_type='article',
        og_title='×2 аудитории до 1,7 млн',
        og_description='Онлайн-кинотеатр для базы 12 млн абонентов. 95% не доходили до подписки — аудитория удвоилась за год.',
        og_image='og/og_kino.png',
    ),
    'design-system.html': dict(
        who=f'<a href="/">{WHO}</a>',
        title='Дизайн-система DREAMPlatform — Екатерина Задорожная',
        description='Кейс «Дизайн-система DREAMPlatform»: первая в платформе цифрового ТВ '
                    'дизайн-система для шести сервисов. Senior Product Designer: чистка '
                    'десятилетнего легаси, процесс согласования, 40+ компонентов с документацией.',
        url='https://codedesign.ru/design-system',
        og_type='article',
        og_title='Дизайн-система для 6 сервисов',
        og_description='Корпоративная дизайн-система для GS Group. 40+ компонентов, ускорила релизы ×2, работает без автора.',
        og_image='og/og_ds.png',
    ),
    'second-screen.html': dict(
        who=f'<a href="/">{WHO}</a>',
        title='Второй экран — Екатерина Задорожная',
        description='Кейс «Второй экран» для Триколора: MVP за 4 месяца, два релиза за год, '
                    'разворот оттока с 198K до 236K активных пользователей.',
        url='https://codedesign.ru/second-screen',
        og_type='article',
        og_title='Триколор терял активных пользователей. Два релиза за год развернули отток в рост',
        og_description='Кейс «Второй экран». Senior Product Designer: MVP на двух платформах, связь телефона с приставкой, 198K → 236K активных пользователей.',
        og_image='og/og_ss.png',
    ),
}


def dom(s):
    """Разделитель «роль · сфера» — своим элементом, чтобы CSS дал ему воздух."""
    return s.replace(' · ', ' <span class="sep">·</span> ')


def row(c):
    """Свёрнутый кейс — ссылка-карточка. Одна разметка на все места.
    Кейс «в работе» (soon) — та же карточка, но блоком без ссылки."""
    inner = (f'<span class="row__id"><span class="logo" aria-hidden="true"></span>'
             f'<span><span class="row__name">{c["name"]}</span><em>{dom(c["domain"])}</em></span>'
             f'</span>')
    if c.get('soon'):
        return (f'<div class="row row--flat row--soon" data-brand="{c["brand"]}" '
                f'aria-disabled="true">{inner}</div>')
    return f'<a class="row row--flat" href="/{c["slug"]}" data-brand="{c["brand"]}">{inner}</a>'


ALL_ICON = ('<svg viewBox="0 0 12 12" aria-hidden="true" fill="currentColor">'
            + ''.join(f'<circle cx="{x}" cy="{y}" r="1.1"/>' for y in (1.5, 6, 10.5) for x in (1.5, 6, 10.5))
            + '</svg>')


def case_tree(page):
    """Список кейсов в левой колонке — на обеих страницах.
    Первый пункт «Все»: на главной текущий (без плашки), на странице кейса —
    белая ссылка на главную. Текущий кейс — без подложки и с якорями разделов,
    остальные — карточками."""
    cur = page.replace('.html', '')
    out = ['    <nav class="tree" aria-label="Кейсы">']
    if cur == 'index':
        out.append(f'      <span class="all" aria-current="page">{ALL_ICON}Все</span>')
    else:
        out.append(f'      <a class="all" href="/">{ALL_ICON}Все</a>')
    for c in CASES:
        if c['slug'] == cur:
            toc = ''.join(f'<a href="{h}">{t}</a>' for h, t in ANCHORS)
            out += [f'      <div class="row row--open" data-brand="{c["brand"]}" aria-current="page">',
                    '        <span class="row__id"><span class="logo" aria-hidden="true"></span>',
                    f'        <span><span class="row__name">{c["name"]}</span><em>{dom(c["domain"])}</em></span></span>',
                    f'        <span class="toc">{toc}</span>',
                    '      </div>']
        else:
            out.append('      ' + row(c))
    out.append('    </nav>')
    return '\n'.join(out)


def case_more(page):
    """«Другие кейсы» в конце внутренней страницы — только ниже 1140."""
    cur = page.replace('.html', '')
    if cur == 'index':
        return ''
    rows = '\n'.join('        ' + row(c) for c in CASES if c['slug'] != cur)
    return ('    <nav class="more" aria-label="Другие кейсы">\n'
            '      <p class="more__t">Другие кейсы</p>\n'
            f'      <div class="tree">\n{rows}\n      </div>\n'
            '    </nav>')


def menu(page):
    """Меню телефона: кейсы карточками, резюме, контакты. Низ берётся из
    parts/rail_foot.html — контакты живут в одном месте. «В работе» не показываем."""
    cur = page.replace('.html', '')
    cards = []
    for c in CASES:
        if c.get('soon'):
            continue
        r = row(c)
        if c['slug'] == cur:
            r = r.replace('<a class="row row--flat"', '<a class="row row--flat" aria-current="page"', 1)
        cards.append('      ' + r)
    foot = (HERE / 'parts/rail_foot.html').read_text(encoding='utf8')
    foot = foot[foot.index('<div class="rail__foot">'):foot.index('<button class="prefs__theme"')].rstrip() + '\n      </div>'
    foot = foot.replace('rail__foot', 'menu__foot')
    mod = ' menu--home' if cur == 'index' else ''
    return (f'<div class="menu{mod}" id="menu">\n'
            '  <nav class="menu__panel" aria-label="Меню">\n'
            '    <div class="tree">\n' + '\n'.join(cards) + '\n    </div>\n'
            f'    {foot}\n  </nav>\n</div>')


GENERATED = {'CASE_TREE': case_tree, 'CASE_MORE': case_more, 'MENU': menu}


def tags(name, kind):
    if kind == 'css':
        return f'/* <<{name}>> */', f'/* <</{name}>> */'
    return f'<!-- <<{name}>> -->', f'<!-- <</{name}>> -->'


def inject(text, name, kind, body):
    o, c = tags(name, kind)
    i, j = text.find(o), text.find(c)
    if i < 0 or j < 0:
        return text, False
    return text[:i + len(o)] + ('\n' + body.rstrip() + '\n' if body.strip() else '\n') + text[j:], True


def main():
    for page in PAGES:
        f = HERE / page
        t = f.read_text(encoding='utf8')
        hits = []
        for name, kind, src, *rest in PARTS:
            fmt = bool(rest and rest[0])
            if name in GENERATED:
                body = GENERATED[name](page)
            else:
                path = src.get(page) if isinstance(src, dict) else src
                body = (HERE / path).read_text(encoding='utf8') if path else ''
                if fmt and body:
                    body = body.format(**META[page])
            t, ok = inject(t, name, kind, body)
            if ok:
                hits.append(name if body.strip() else name + '(пусто)')
        f.write_text(t, encoding='utf8')
        print(f'{page:12} ← {", ".join(hits) or "нет маркеров"}')


if __name__ == '__main__':
    main()
