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
import html
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
    dict(slug='realdeal',      name='Real Deal', name_en='Real Deal',           domain='B2B SaaS · PropTech',        brand='realdeal'),
    dict(slug='kino-i-tv',     name='Кино и ТВ', name_en='Cinema &amp; TV',          domain='B2C · Streaming TV',         brand='kino-i-tv'),
    dict(slug='second-screen', name='Второй экран', name_en='Second Screen',       domain='B2C · TV &amp; Media',       brand='second-screen'),
    dict(slug='design-system', name='DREAMPlatform', name_en='DREAMPlatform',      domain='B2B SaaS · Design system',   brand='design-system'),
    # в работе: карточка без ссылки на 30% (soon=True), страницы нет
    dict(slug='smart-home',    name='Умный дом', name_en='Smart Home',          domain='B2C · TV',                   brand='smart-home', soon=True),
]
ANCHORS = {'ru': [('#problem', 'Проблема'), ('#work', 'Мой вклад'), ('#result', 'Результат')],
           'en': [('#problem', 'Problem'), ('#work', 'My contribution'), ('#result', 'Result')]}

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


# Английская версия лежит в en/ (/en/, /en/realdeal …): те же страницы и тот же дизайн.
# Тексты страниц переведены в самих en/*.html; общие части (parts/) берут язык отсюда.
# Страница попадает в сборку, когда есть файл en/<страница>.html.
EN_WHO = 'Ekaterina Zadorozhnaya —<br>Senior Product Designer.'
CV_HREF = {
    'ru': 'https://codedesign.ru/%D0%97%D0%B0%D0%B4%D0%BE%D1%80%D0%BE%D0%B6%D0%BD%D0%B0%D1%8F_%D0%95%D0%BA%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%BD%D0%B0_Product_Designer.pdf',
    'en': 'https://codedesign.ru/Zadorozhnaya_Ekaterina_Product_Designer.pdf',
}
# @@ключ@@ в parts/ заменяется значениями отсюда; alt_* считаются в main() (ссылка на ту же страницу в другом языке)
I18N = {
    'ru': dict(
        home='/', to_home='На главную', cv_href=CV_HREF['ru'], cv_label='Резюме — PDF', cv_aria='Резюме, PDF',
        theme_dark='Тёмная тема', theme_light='Светлая тема', menu='Меню', menu_close='Закрыть меню', linkedin='Linkedin',
        me_span='9+ лет в <b>B2B&nbsp;SaaS</b> и <b>B2C:</b> PropTech, <br class="br-m">Streaming&nbsp;TV, дизайн-системы.',
        me_sum='<b>$7.5M</b> инвестиций и рост аудитории <br class="br-m"><b>100%&nbsp;YoY</b> — на продуктах, которые я&nbsp;вела.',
        alt_code='en', alt_label='Eng', alt_aria='English version',
    ),
    'en': dict(
        home='/en/', to_home='Home', cv_href=CV_HREF['en'], cv_label='Resume — PDF', cv_aria='Resume, PDF',
        theme_dark='Dark theme', theme_light='Light theme', menu='Menu', menu_close='Close menu', linkedin='Linkedin',
        me_span='9+ years in <b>B2B&nbsp;SaaS</b> and <b>B2C:</b> PropTech, <br class="br-m">Streaming&nbsp;TV, design systems.',
        me_sum='<b>$7.5M</b> raised and <b>100%&nbsp;YoY</b> audience growth <br class="br-m">— on products I&nbsp;led.',
        alt_code='ru', alt_label='Рус', alt_aria='Русская версия',
    ),
}
META_EN = {
    'index.html': dict(
        who=EN_WHO,
        title='Ekaterina Zadorozhnaya — Senior Product Designer',
        description='Senior Product Designer with 9+ years in B2B SaaS and B2C: PropTech, '
                    'Streaming TV, design systems. $7.5M raised and 100% YoY audience '
                    'growth on products I led.',
        url='https://codedesign.ru/en/',
        og_type='profile',
        og_title='Ekaterina Zadorozhnaya — Senior Product Designer',
        og_description='9+ years in B2B SaaS and B2C. Complex interfaces, design systems, products from zero to launch. $7.5M raised on the Demo + MVP, 2× audience on the redesign.',
        og_image='og/og_eng.png',
    ),
    'realdeal.html': dict(
        who=f'<a href="/en/">{EN_WHO}</a>',
        title='Real Deal — Ekaterina Zadorozhnaya',
        description='Real Deal case study: the first platform for online commercial real estate '
                    'deals in the UAE. Lead Product Designer, from an analytics demo to a '
                    'commercial MVP.',
        url='https://codedesign.ru/en/realdeal',
        og_type='article',
        og_title='The Demo + MVP that raised $7.5M',
        og_description='The first platform for online commercial real estate deals in the UAE. Analytics built on Dubai Land Department data.',
        og_image='og/og_realdeal.png',
    ),
    'kino-i-tv.html': dict(
        who=f'<a href="/en/">{EN_WHO}</a>',
        title='Tricolor Cinema & TV — Ekaterina Zadorozhnaya',
        description='Tricolor Cinema & TV case study: an online cinema redesign for a base of '
                    '12M subscribers. Product Designer: content access, sign-in, navigation, '
                    'shared principles for Smart TV and Apple TV. The audience grew to 1.7M.',
        url='https://codedesign.ru/en/kino-i-tv',
        og_type='article',
        og_title='2× audience, up to 1.7M',
        og_description='An online cinema for a base of 12M subscribers. 95% never reached a subscription — the audience doubled in a year.',
        og_image='og/og_kino.png',
    ),
    'design-system.html': dict(
        who=f'<a href="/en/">{EN_WHO}</a>',
        title='DREAMPlatform Design System — Ekaterina Zadorozhnaya',
        description='DREAMPlatform design system case study: the first design system for six '
                    'services of a digital TV platform. Senior Product Designer: cleaning up '
                    'ten years of legacy, an approval process, 40+ documented components.',
        url='https://codedesign.ru/en/design-system',
        og_type='article',
        og_title='A design system for 6 services',
        og_description='A corporate design system for GS Group. 40+ components, releases 2× faster, runs without its author.',
        og_image='og/og_ds.png',
    ),
    'second-screen.html': dict(
        who=f'<a href="/en/">{EN_WHO}</a>',
        title='Second Screen — Ekaterina Zadorozhnaya',
        description='Second Screen case study for Tricolor: MVP in 4 months, two releases in a '
                    'year, a turnaround from 198K to 236K active users.',
        url='https://codedesign.ru/en/second-screen',
        og_type='article',
        og_title='Tricolor was losing active users. Two releases in a year turned the decline into growth',
        og_description='Second Screen case study. Senior Product Designer: an MVP on two platforms, a link between phone and set-top box, 198K → 236K active users.',
        og_image='og/og_ss.png',
    ),
}


def dom(s):
    """Разделитель «роль · сфера» — своим элементом, чтобы CSS дал ему воздух."""
    return s.replace(' · ', ' <span class="sep">·</span> ')


def row(c, lang='ru'):
    """Свёрнутый кейс — ссылка-карточка. Одна разметка на все места.
    Кейс «в работе» (soon) — та же карточка, но блоком без ссылки."""
    name = c['name_en'] if lang == 'en' else c['name']
    pre = '/en' if lang == 'en' else ''
    inner = (f'<span class="row__id"><span class="logo" aria-hidden="true"></span>'
             f'<span><span class="row__name">{name}</span><em>{dom(c["domain"])}</em></span>'
             f'</span>')
    if c.get('soon'):
        return (f'<div class="row row--flat row--soon" data-brand="{c["brand"]}" '
                f'aria-disabled="true">{inner}</div>')
    return f'<a class="row row--flat" href="{pre}/{c["slug"]}" data-brand="{c["brand"]}">{inner}</a>'


ALL_ICON = ('<svg viewBox="0 0 12 12" aria-hidden="true" fill="currentColor">'
            + ''.join(f'<circle cx="{x}" cy="{y}" r="1.1"/>' for y in (1.5, 6, 10.5) for x in (1.5, 6, 10.5))
            + '</svg>')


def case_tree(page, lang='ru'):
    """Список кейсов в левой колонке — на обеих страницах.
    Первый пункт «Все»: на главной текущий (без плашки), на странице кейса —
    белая ссылка на главную. Текущий кейс — без подложки и с якорями разделов,
    остальные — карточками."""
    cur = page.replace('.html', '')
    en = lang == 'en'
    home = '/en/' if en else '/'
    out = [f'    <nav class="tree" aria-label="{"Cases" if en else "Кейсы"}">']
    if cur == 'index':
        out.append(f'      <span class="all" aria-current="page">{ALL_ICON}{"All" if en else "Все"}</span>')
    else:
        out.append(f'      <a class="all" href="{home}">{ALL_ICON}{"All" if en else "Все"}</a>')
    for c in CASES:
        if c['slug'] == cur:
            toc = ''.join(f'<a href="{h}">{t}</a>' for h, t in ANCHORS[lang])
            out += [f'      <div class="row row--open" data-brand="{c["brand"]}" aria-current="page">',
                    '        <span class="row__id"><span class="logo" aria-hidden="true"></span>',
                    f'        <span><span class="row__name">{c["name_en"] if en else c["name"]}</span><em>{dom(c["domain"])}</em></span></span>',
                    f'        <span class="toc">{toc}</span>',
                    '      </div>']
        else:
            out.append('      ' + row(c, lang))
    out.append('    </nav>')
    return '\n'.join(out)


def case_more(page, lang='ru'):
    """«Другие кейсы» в конце внутренней страницы — только ниже 1140."""
    cur = page.replace('.html', '')
    if cur == 'index':
        return ''
    rows = '\n'.join('        ' + row(c, lang) for c in CASES if c['slug'] != cur)
    other = 'Other cases' if lang == 'en' else 'Другие кейсы'
    return (f'    <nav class="more" aria-label="{other}">\n'
            f'      <p class="more__t">{other}</p>\n'
            f'      <div class="tree">\n{rows}\n      </div>\n'
            '    </nav>')


def menu(page, lang='ru'):
    """Меню телефона: кейсы карточками, резюме, контакты. Низ берётся из
    parts/rail_foot.html — контакты живут в одном месте. «В работе» не показываем."""
    cur = page.replace('.html', '')
    cards = []
    for c in CASES:
        if c.get('soon'):
            continue
        r = row(c, lang)
        if c['slug'] == cur:
            r = r.replace('<a class="row row--flat"', '<a class="row row--flat" aria-current="page"', 1)
        cards.append('      ' + r)
    foot = (HERE / 'parts/rail_foot.html').read_text(encoding='utf8')
    foot = foot[foot.index('<div class="rail__foot">'):foot.index('<div class="prefs">')].rstrip() + '\n      </div>'
    foot = foot.replace('rail__foot', 'menu__foot')
    # язык в меню телефона — третьей строкой под Telegram и Linkedin (макет 2026-10-28);
    # на странице кейса колонки с переключателем нет
    link = ('\n          <a href="@@alt_href@@" hreflang="@@alt_code@@" lang="@@alt_code@@" '
            'aria-label="@@alt_aria@@">@@alt_label@@</a>')
    k = foot.index('</a>', foot.index('linkedin.com')) + len('</a>')
    foot = foot[:k] + link + foot[k:]
    mod = ' menu--home' if cur == 'index' else ''
    return (f'<div class="menu{mod}" id="menu">\n'
            f'  <nav class="menu__panel" aria-label="{"Menu" if lang == "en" else "Меню"}">\n'
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


def lang_pages(lang):
    """Страницы языка: русские — все, английские — те, у которых есть en/<страница>."""
    return PAGES if lang == 'ru' else [p for p in PAGES if (HERE / 'en' / p).exists()]


def page_url(lang, page):
    slug = '' if page == 'index.html' else page.replace('.html', '')
    return ('/en/' if lang == 'en' else '/') + slug if slug or lang == 'en' else '/'


def page_path(lang, page):
    return HERE / 'en' / page if lang == 'en' else HERE / page


def main():
    for lang in ('ru', 'en'):
        other = 'en' if lang == 'ru' else 'ru'
        for page in lang_pages(lang):
            f = page_path(lang, page)
            t = f.read_text(encoding='utf8')
            if lang == 'en':
                # CSS страницы один на два языка: английская копия берёт его у русской
                ru = page_path('ru', page).read_text(encoding='utf8')
                a, b = ru.index('<style>'), ru.index('</style>')
                t = t[:t.index('<style>')] + ru[a:b] + t[t.index('</style>'):]
            vals = dict(I18N[lang])
            vals['alt_href'] = page_url(other, page)
            meta = dict((META if lang == 'ru' else META_EN)[page])
            for k_ in ('title', 'description', 'og_title', 'og_description'):
                meta[k_] = html.escape(meta[k_], quote=True)   # «&» в названиях (Cinema & TV) — в атрибуте и тексте только сущностью
            meta['og_locale'] = 'ru_RU' if lang == 'ru' else 'en_US'
            alts = []
            if page in lang_pages('en'):
                u = {l: 'https://codedesign.ru' + page_url(l, page) for l in ('ru', 'en')}
                alts = [f'<link rel="alternate" hreflang="ru" href="{u["ru"]}">',
                        f'<link rel="alternate" hreflang="en" href="{u["en"]}">',
                        f'<link rel="alternate" hreflang="x-default" href="{u["ru"]}">']
            meta['alternates'] = '\n'.join(alts)
            hits = []
            for name, kind, src, *rest in PARTS:
                fmt = bool(rest and rest[0])
                if name in GENERATED:
                    body = GENERATED[name](page, lang)
                else:
                    path = src.get(page) if isinstance(src, dict) else src
                    body = (HERE / path).read_text(encoding='utf8') if path else ''
                    if fmt and body:
                        body = body.format(**meta)
                for k_, v_ in vals.items():
                    body = body.replace(f'@@{k_}@@', v_)
                t, ok = inject(t, name, kind, body)
                if ok:
                    hits.append(name if body.strip() else name + '(пусто)')
            f.write_text(t, encoding='utf8')
            print(f'{lang} {page:20} ← {", ".join(hits) or "нет маркеров"}')


if __name__ == '__main__':
    main()
