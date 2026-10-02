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
PARTS = [
    ('BASE',       'css',  'parts/base.css'),
    ('RAIL_HEAD',  'html', 'parts/rail_head.html'),
    ('RAIL_FOOT',  'html', 'parts/rail_foot.html'),
    ('RAIL_INTRO', 'html', {'index.html': 'parts/rail_intro.html'}),
]
PAGES = ['index.html', 'realdeal.html']


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
        for name, kind, src in PARTS:
            path = src.get(page) if isinstance(src, dict) else src
            body = (HERE / path).read_text(encoding='utf8') if path else ''
            t, ok = inject(t, name, kind, body)
            if ok:
                hits.append(name if path else name + '(пусто)')
        f.write_text(t, encoding='utf8')
        print(f'{page:12} ← {", ".join(hits) or "нет маркеров"}')


if __name__ == '__main__':
    main()
