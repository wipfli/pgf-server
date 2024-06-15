# pgf-server
HTTP server to encode strings to a positioned glyph font for MapLibre GL JS and MapLibre Native

## Requirements

- Python3
- `pip3 install fastapi uvicorn`
- `apt install libharfbuzz-bin`

## Usage

Get the [wipfli/pgf-encoding](https://github.com/wipfli/pgf-encoding) submodule with:

```
git submodule update --init
```

Start the server with:

```
python3 server.py
```

This will listen on `http://locahost:3000` for requests of the form `/{font_name}/{version}/{text}`, where 

- `font_name` is the name of the font without suffix in the `vendor/pgf-encoding/fonts/` folder.
- `version` is the encoding version which has to be present in the `vendor/pgf-encoding/encoding/` folder.
- `text` is the text to be encoded.

### `wget` Example 

From CLI you can encode the string `नेपाल` (Nepal) with the font `NotoSansDevanagari-Regular` version 1 with the following command

```
wget -O encoded.txt http://localhost:3000/NotoSansDevanagari-Regular/1/नेपाल
```

The file `encoded.txt` should now contain the pgf-encoded string for `नेपाल`.

### Python `requests` Example

With python you can achieve the same with:

```
python3 get.py
```

Make sure that you have the `requests` package installed.

### Remarks

- Text with whitespaces cannot be encoded.
- Only characters that match a given script can be encoded, e.g., for NotoSansDevanagari-Regular-v1 use only text in the Devanagari script.

## License

The code in this repository is published under the [MIT License](./LICENSE).
