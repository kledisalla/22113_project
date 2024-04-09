
# MEDLINE Abstract Mining

This project aims to mine MEDLINE abstracts to discover word associations within the biomedical literature. The process involves identifying informative words that co-occur frequently with each other in abstracts. This is achieved through several steps including identifying non-informative words, parsing abstracts to extract informative words, and creating co-occurrence tables for analysis.

# Method

1) Abstract extraction: Abstracts are extracted from a file containing Medline articles

2) Identifying Non-Informative Words: Words with high average occurrence per abstract are considered non-informative. A first pass parsing of abstracts is done to create a word blacklist. This is typically achieved by random sampling of a portion of abstracts (e.g., 10%) to create the blacklist.

3) Parsing Abstracts for Informative Words: Abstracts are parsed again, disregarding blacklisted words and non-words. This results in a list of informative words. Duplicate occurrences of words within an abstract are collapsed into one occurrence.

4) Creating Occurrence and Co-Occurrence Tables: Occurrence tables are generated for single informative words as well as co-occurring word pairs. The log-likelihood (LLH) score is calculated for each word pair, indicating the strength of association between them.




## Installation

Install my-project with npm

```bash
  npm install my-project
  cd my-project
```
    
## Dependencies
- Python 3.x
- NetworkX
- Matplotlib
- Random
- NLTK
- Regular expressions (re)

## Usage/Examples

```Python3
python3 main.py <medline_articles file>
```


## Authors

- @kledisalla (https://github.com/kledisalla)
- @Dilancifci (https://github.com/Dilancifci)


## Appendix

This project was undertaken as part of a course at the Technical University of Denmark.


## Notes
The pipeline uses the file acquired from https://teaching.healthtech.dtu.dk/22113/index.php/22113/22163_-_Unix_%26_Python_Programming_for_Bioinformaticians
and as such, it was designed with that file format in mind.