# laravel-ai
<img src="data/laravel-terminator.png" height=256>

This repository supplies tools to explore a set of github repositories as a dataset in a Artificial Inteligense model. The following components are provided

* [x] Github scrape module
* [ ] Pytorch Dataset
* [ ] Pytorch Dataloader
* [ ] Example analysis. As the name implies I will focus on applications built with the PHP framework Laravel.

## Installation
* install anaconda
* install pygithub
* install pytorch
* copy Env.Example.py to Env.py and set your GITHUB_ACCESS_TOKEN
* run ```python src/examples/migration-analysis/01_scrape.py```

## Todo
- [x] Make a Env class
- [x] Make a Print class
- [x] Make 'main' into 'analysis-x'
- [x] Move everything to a src folder
- [x] Rename 'scraped' to 'data/raw'
- [x] Code example Transformer-X
- [ ] Deploy more scrapers
- [ ] Transform 'data/raw' into 'data/processed/transformer-x'
- [ ] Find online storage for harvested dumps (33K files -> 83,8 MB )

## License
MIT