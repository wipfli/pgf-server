import sys
import os
import json

from fastapi import FastAPI, HTTPException
import uvicorn
from fastapi.responses import HTMLResponse

folder = os.path.dirname(os.path.abspath(__file__))
folder = os.path.join(folder, 'vendor')
folder = os.path.join(folder, 'pgf-encoding')

sys.path.append(folder)

from shape import shape

encodings = {}

def read_encoding(font_name, version):
    encoding = {}
    filename = f'vendor/pgf-encoding/encoding/{font_name}-v{version}.csv'
    if not os.path.exists(filename):
        raise HTTPException(status_code=400, detail=f"Encoding not found at {filename}")
    with open(filename) as f:
        # skip csv header
        line = f.readline()
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip()
            index, x_offset, y_offset, x_advance, y_advance, codepoint = [int(num) for num in line.split(',')]
            glyph_tuple = (index, x_offset, y_offset, x_advance, y_advance)
            encoding[glyph_tuple] = codepoint
    return encoding

app = FastAPI()

deltas = [
    [0, 0],

    [1, 0],
    [0, 1],
    [-1, 0],
    [0, -1],

    [2, 0],
    [0, 2],
    [-2, 0],
    [0, -2],

    [3, 0],
    [0, 3],
    [-3, 0],
    [0, -3]
]

@app.get("/{font_name}/{version}/{text}", response_class=HTMLResponse)
async def root(font_name:str, version:str, text: str):
    result = ''

    encoding_key = f'{font_name}-v{version}'
    if encoding_key not in encodings:
        encodings[encoding_key] = read_encoding(font_name, version)
    
    font_path = f'vendor/pgf-encoding/fonts/{font_name}.ttf'
    try:
        glyph_vector = shape(font_path, text)
    except json.decoder.JSONDecodeError:
        raise HTTPException(status_code=400, detail=f"Unable to run HarfBuzz. You may want to check the font path: {font_path}")

    if not glyph_vector:
        raise HTTPException(status_code=400, detail="Glyph vector empty")
    
    for glyph in glyph_vector:
        index = glyph['index']

        if index == 0:
            raise HTTPException(status_code=400, detail="Glyph vector contains glyphs with index 0")

        x_offset = int(round(glyph['x_offset'] / 64.0))
        y_offset = int(round(glyph['y_offset'] / 64.0))
        x_advance = int(round(glyph['x_advance'] / 64.0))
        y_advance = int(round(glyph['y_advance'] / 64.0))

        codepoint = None
        for delta in deltas:
            glyph_tuple = (
                index, 
                x_offset + delta[0], 
                y_offset, 
                x_advance + delta[1], 
                y_advance
            )
            if glyph_tuple in encodings[encoding_key]:
                codepoint = encodings[encoding_key][glyph_tuple]
                break
        
        if codepoint is None:
            raise HTTPException(status_code=400, detail=f"No matching positioned glyph found for {glyph}")
        
        result += chr(codepoint)

    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
