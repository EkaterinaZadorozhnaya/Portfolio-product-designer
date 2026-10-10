#!/usr/bin/env python3
"""
Вклеивает общие части в index.html и realdeal.html.

Левая колонка живёт в одном месте — parts/. Раньше она существовала
в двух копиях и разъехалась сама: на главной оказалась чёрная кнопка
без аватара, внутри — аватар и серый чип. Никто этого не решал,
расхождение накопилось за двадцать версий.

Часть может быть общей (одна строка-путь) или разной по страницам
(словарь: страница → путь; страницы без записи получают пустоту).

Запуск:  python3 build.py
"""
import pathlib

HERE = pathlib.Path(__file__).parent

# порядок важен: RAIL_INTRO лежит ВНУТРИ RAIL_HEAD и вклеивается после него
# fmt=True — в части есть {поля}, они подставляются из META[страница]
PARTS = [
    ('HEAD',       'html', 'parts/head.html', True),
    ('BASE',       'css',  'parts/base.css'),
    ('RAIL_HEAD',  'html', 'parts/rail_head.html'),
    ('RAIL_FOOT',  'html', 'parts/rail_foot.html'),
    ('RAIL_INTRO', 'html', {'index.html': 'parts/rail_intro.html'}),
    # собираются кодом из CASES, файла нет: содержимое зависит от страницы
    ('CASE_TREE',  'html', None),
    ('CASE_MORE',  'html', None),
]
PAGES = ['index.html', 'realdeal.html']

# Порядок — как в ленте на главной: по силе кейса, не по дате.
# brand: значение атрибута data-brand, по нему CSS берёт цвет продукта.
# anchors: якоря разделов кейса; у всех внутренних страниц они одинаковы.
CASES = [
    dict(slug='realdeal',      name='RealDeal',           domain='B2B SaaS · PropTech',        brand='realdeal'),
    dict(slug='kino-i-tv',     name='Кино и ТВ',          domain='B2C · Streaming TV',         brand='kino-i-tv'),
    dict(slug='design-system', name='DREAMPlatform',      domain='B2B SaaS · Design system',   brand='design-system'),
    dict(slug='second-screen', name='Второй экран',       domain='B2C · TV &amp; Media',       brand='second-screen'),
    # в работе: карточка без ссылки на 30% (soon=True), страницы нет
    dict(slug='smart-home',    name='Умный дом',          domain='B2C · TV',                   brand='smart-home', soon=True),
]
ANCHORS = [('#problem', 'Проблема'), ('#work', 'Мой вклад'), ('#result', 'Результат')]

# Шапка у страниц одна, различаются только значения. Копий parts/head_*.html
# не делаем специально: две копии расходятся — так уже было с левой колонкой.
META = {
    'index.html': dict(
        title='Задорожная Екатерина — Senior Product Designer',
        description='Senior Product Designer, 8 лет в B2B SaaS и B2C: PropTech, '
                    'Streaming TV, дизайн-системы. $7.5M инвестиций и рост аудитории '
                    '100% YoY на продуктах, которые я вела.',
        url='https://codedesign.ru/',
        og_type='profile',
        og_title='Задорожная Екатерина — Senior Product Designer',
        og_description='8 лет в B2B SaaS и B2C: PropTech, Streaming TV, дизайн-системы.',
        og_image='og.png',
    ),
    'realdeal.html': dict(
        title='RealDeal — Екатерина Задорожная',
        description='Кейс RealDeal: первая в ОАЭ платформа онлайн-сделок с коммерческой '
                    'недвижимостью. Роль Lead Product Designer, путь от аналитического '
                    'демо до коммерческого MVP.',
        url='https://codedesign.ru/realdeal',
        og_type='article',
        og_title='Первая в ОАЭ платформа онлайн-сделок с коммерческой недвижимостью',
        og_description='Кейс RealDeal. Lead Product Designer: стратегия, карта на данных '
                       'DLD, онлайн-сделка на UAE PASS.',
        og_image='og-realdeal.png',
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


def case_tree(page):
    """Список кейсов в левой колонке внутренней страницы.
    Текущий — без подложки и с якорями разделов, остальные — карточками."""
    cur = page.replace('.html', '')
    out = ['    <nav class="tree" aria-label="Кейсы">']
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
    rows = '\n'.join('        ' + row(c) for c in CASES if c['slug'] != cur)
    return ('    <nav class="more" aria-label="Другие кейсы">\n'
            '      <p class="more__t">Другие кейсы</p>\n'
            f'      <div class="tree">\n{rows}\n      </div>\n'
            '    </nav>')


GENERATED = {'CASE_TREE': case_tree, 'CASE_MORE': case_more}


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
                body = GENERATED[name](page) if page != 'index.html' else ''
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
