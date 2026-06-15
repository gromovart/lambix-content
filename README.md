# lambix-content

Шаблоны и инфографика для Telegram-каналов Lambix.

## Каналы

| Канал | Описание |
|-------|----------|
| [@lambix_ai](https://t.me/lambix_ai) | Lambix: AI-автоматизация для малого бизнеса |
| [@pro_crypto_trading](https://t.me/pro_crypto_trading) | PRO. Криптотрейдинг — торговый путь с нуля |

## Структура

```
lambix-content/
├── logos/                        — логотипы каналов (PNG 512×512)
├── templates/
│   ├── lambix-trade/             — бриф для инфлюенсера (PDF), логотипы HTML
│   └── pro-crypto/               — шаблон текстового поста, сигнала для входа
└── output/
    ├── lambix-trade/             — готовые PDF
    └── pro-crypto/               — готовые PNG для публикации
```

## Генерация PNG из HTML-шаблона

Требуется: Node.js + Playwright или Python-сервер.

```bash
# Локальный сервер для просмотра шаблонов
python3 -m http.server 8080 --directory .
# Открыть: http://localhost:8080/templates/pro-crypto/signal_template.html
```

## Шаблоны

### PRO. Криптотрейдинг

| Файл | Назначение |
|------|-----------|
| `templates/pro-crypto/pro_post1.html` | Заголовочная картинка для текстового поста |
| `templates/pro-crypto/signal_template.html` | Карточка сигнала для входа в сделку |

### LambixTrade

| Файл | Назначение |
|------|-----------|
| `templates/lambix-trade/gen_brief.py` | Генератор PDF-брифа для инфлюенсера |
| `templates/lambix-trade/logo_render.html` | Логотип LambixTrade |
| `templates/lambix-trade/lambix_ai_logo.html` | Логотип Lambix AI |
