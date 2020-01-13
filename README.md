# Lenssort

Using facial recognition and pixelsorting on images to create glitched, Snapchat-like lenses.

Utilizes [pixelsort](https://github.com/satyarth/pixelsort), another project I am involved in. Make sure to check it out!

## Usage

With Docker:

```bash
# Make sure to include the -o flag, previews won't show up in the container.
docker-compose up
docker-compose run lenssort python -m lenssort examples/example.jpg -m face -o example_result.png
```

Manually:

Requires Python 3.6 >=.

Make sure you have [dlib Python bindings](https://gist.github.com/ageitgey/629d75c1baac34dfa5ca2a1928a7aeaf) installed: 

```bash
git clone https://github.com/BernardZhao/lenssort.git
cd lenssort

# Can skip virtual environment if desired
python -m venv venv 
source venv/bin/activate

pip install -r requirements.txt

python -m lenssort %PathToImage% [mask_type] [params]
```

### Mask types:

Mask name | Description
----------|------------
`eyes`    | Sort the eyes.
`face`    | Sort the face, within the brows and chin.
`shuffle` | Sort a polygon randomly generated over facial features.
`censored`| Sort the eye area with a thick bar.
`facemask`| Sort the area of the face under the eyes.
`tears`   | Sort tear-like lines below the eyes.

### Parameters:

Parameter   | Flag 	| Description
------------|-------|------------
Invert      | `-i`	| Inverts the mask. May produce cool results.
Angle       | `-a`	| Sorting angle. Overrides internal default for the mask.
Output path | `-o`	| File output path. Previews image if not provided.


## Examples

`python -m lenssort examples/example1.jpg -m face`

![example1_face_i_a90](/examples/results/example1_face.png)


`python -m lenssort examples/example1.jpg -m face -i -a 90`

![example1_face_i_a90](/examples/results/example1_face_i_a90.png)


`python -m lenssort examples/example1.jpg -m eyes -i`

![example1_eyes_i](/examples/results/example1_eyes_i.png)


`python -m lenssort examples/example3.jpg -m facemask`

![example1_eyes_i](/examples/results/example3_facemask.png)


`python -m lenssort examples/example3.jpg -m shuffle`

![example1_eyes_i](/examples/results/example3_shuffle.png)


`python -m lenssort examples/example2.jpg -m censored`

![example1_eyes_i](/examples/results/example2_censored.png)

### Todo
- [ ] Expose pixelsort args: sorting function, interval function, etc.
- [ ] Validate mask: No out of bounds
- [ ] Mask compositions: Ex: (face - eyes + ...)

And more masks ofc 😪