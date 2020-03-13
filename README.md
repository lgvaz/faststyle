# Welcome to faststyle
> This is still in early development, expect lots of API changes.  


Faststyle aims to provide an easy and modular interface to Image to Image problems based on [feature loss](https://arxiv.org/abs/1603.08155).

Start by taking a look at [simple.ipynb](https://github.com/lgvaz/faststyle/blob/master/examples/simple.ipynb) for a high level view of the library. If you want a more low level approach take a look at [hats_on_cats.ipynb](https://github.com/lgvaz/faststyle/blob/master/examples/hats_on_cats.ipynb) were with few lines of modification we can change our task completely to put hats on cats!


## Installing
Making sure you have a working installation of [fastai2](https://github.com/fastai/fastai2). You can then install the library by doing:
```
pip install faststyle
```

You can instead use a editable install, which is more recommended since the lib is chaging a lot:
```
git clone https://github.com/lgvaz/faststyle.git
cd faststyle
pip install -e .
```

## Contributing
There are still tons of things to do in the library, you're welcome to contribute. Some of the tasks are listed in the issues, feel free to contact me directly for more info =)  .

The library is build with [nbdev](https://github.com/fastai/nbdev), I'm following the coding style used by fastai (the only difference being that I use 2 spaces for indentation instead of 4), take a look at the cotribution guideline [here](https://github.com/fastai/nbdev/blob/master/CONTRIBUTING.md).
