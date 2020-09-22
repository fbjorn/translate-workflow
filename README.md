# translate-workflow

Alfred workflow for translating text and making dictionary lookup.

Built on top of Yandex Dictionary API and Yandex Translate API.

## Features

- Automatic translation from Russian to English and vice versa
- Show synonyms and examples when translating a word
- Triggered both by `t` (eng) and `е` (rus) prefix
- Global hotkey for translation of the selected text

## Installation

[Download](https://github.com/fbjorn/translate-workflow/releases/) Alfred
workflow and open it

## Configuration

Before start using this awesome workflow, you need to proceed with following
steps:

#### To enable words translation:

1. Obtain Dictionary [API key](https://yandex.ru/dev/dictionary/keys/get/). It's
   free
2. Invoke Alfred and type `tset <API_KEY>`. Choose _Save as Dictionary Api Key_

#### To enable text translation:

1. This step requires paid account on
   [Yandex.Cloud](https://cloud.yandex.ru/docs/translate/). It's extremely cheap
   for amateur usage of Translate API though.
2. Go to cloud console and create a service account with `editor` role.
3. Generate
   [API Token](https://cloud.yandex.com/docs/iam/operations/api-key/create) for
   this service account
4. Invoke Alfred and type `tset <Token>`. Choose _Save as Translate Api Token_

> Note: All your keys and tokens are stored in the OSX Keychain securely

## Usage

Just type `t <word>` or `t <phrase>` and you'll get the input translated

## Local development

```bash
make
```

It will create a `translate-workflow` folder in your default Alfred installation
and add all required source files as symlinks.

Then just open Alfred on Workflows tab and you'll find it.

### TODO:

- Store desired languages in local settings
- Auto detect source language
- Add spell checks
- Cache API Keys to not access OSX Keychain every time
- Cache API responses locally

---

Icons made by
<a href="https://www.flaticon.com/authors/photo3idea-studio" title="photo3idea_studio">photo3idea_studio</a>
from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
