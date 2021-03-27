# Image-ETL

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [Image-ETL](#image-etl)
  - [Overview](#overview)
  - [Usage](#usage)
    - [Examples](#examples)
  - [Development](#development)

<!-- /code_chunk_output -->


## Overview

Image-ETL is a simple ETL tool to extract image data, transform and load results in a format that can be leveraged by instance segmentation models. 

The format of the transformed data is inspired by [COCO dataset](https://cocodataset.org/#home).

## Usage

Install the distribution with following commands:

```sh
conda create -n etl python=3.8 pip
cd /path/to/image-etl/
make local-dist
```

To verify installation:

```sh
`$etl --version`
```

For help options:

```sh
`$etl --help`
```

### Examples

Run the following commands to try `image-etl` on the toy dataset included in `examples`.

```sh
$etl start example/tiny_data.zip examples
```

The output `json` file will have the following format:

```json
{
  "loc_id_date": [
    {
      "categoory": {
        "loc_id": "<location id>",
        "category": "<class of object>",
        "size": "<[pixel height, pixel width]>",
        "corner": "<coordinates of bottom left>",
        "height": "<height from corner>",
        "width": "<width from corner>",
      }
    }
  ]
}
```

## Development

To run tests:
```sh
make test
```