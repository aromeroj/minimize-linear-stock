## About

Python script to minimize the number of linear stock required for a given number of cuts of different lengths *(usually required lumber purchase)*.

## Usage

Run the `optimize-linear-stock-cuts.py` with the following options:

- `-s` or `--stock_length` followed by the stock length.
- `-c` or `--cut_list` followed by the cut list, each cut must by separated by colon, each cut contains the length and quantity separated by a comma. Example `4,2:8,5:2,3`.

### Example:

`python3 optimize-linear-stock-cuts.py -s 18 -c 10,2:8,3`

## License

Distributed under the MIT License.