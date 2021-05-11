# elcprom Exporter

## Description

> This app can be used as a state manager between tools which follow a push logic like *logstash* or other pipeline/streaming tools and the monitoring tool prometheus. It allows to define custom states which can be updated with increment and decrement patterns on various fields in the incoming data.

## Getting Started

### Dependencies

* \>= python 3.8.x
* All packages installed from the **requirements.txt** file

### Installing

* Pull this repository
* Configure youre needed states in the **STATE_FILE** file
* Run the **gunicorn** in the root folder with the command
    - ``gunicorn -w 1 wsgi:app --bind 0.0.0.0:9000``
* Alternative build the container with the **DOCKERFILE**
    - ``docker build <name-of-container-image> .``

### States

The states can be used to achieve a managed state which can be scraped by prometheus. The mappings are located in the **STATE_FILE**.

```yaml
- name: bgp_state # The name as prometheus metric
  decription: State that holds information about bgp state errors
  type: increment # increment means int number, binary means 0 or 1
  parse_fields: # Which fields to parse from 
    - errorcode
  label_fields: # Labels to use for grouping the counter
    - edge
    - host
  inc_pattern: 30902 # If this regex pattern appears the state increases
  dec_pattern: 30901 # If this regex pattern appears the state decreases
```
### Matchings

These configs can be used to enrich incoming data with local mapping files located in the **MAPPING_FOLDER**.

```yaml
- file: nsx_edges.json # The file to search the mapping
  from: # Which fields in the mapping file and the incoming data must match
  - edge_id
  - host
  to: edge_name # The field of the mapping file to enrich the data with
```

### Environment Variables

| Name        | Type           | Default  | Description |
| ------------- |:-------------:| -----:| -----:| 
| MAPPING_FILE      | string | mappings.yml | The mappings configuration file |
| MAPPING_FOLDER      | string      |   mappings | The folder with the mapping files |
| OUTPUT_FILE | string      |    "" | The output file for all logs. If empty then no log file will be written |
| STATE_FILE | string      |    states.yml | The states configuration file |
| CURRENT_STATE_FILE | string      |    current_states.json | The persistent state of the actual states |

### Logs

If the env variable **OUTPUT_FILE** is set, the log will be written into this file. Otherwise the default output is always stdout.

### API

The exporter provides a very simple HTTP API with the follwoing endpoints.

> **/states** (POST): Accepts JSON Payloads these payloads can be used to manipulate the state of a defined state.

> **/metrics** (GET): The scrape endpoint for prometheus. 

## License

This project is licensed under the Apache Version 2.0 License - see the LICENSE file for details.

## Acknowledgments

Inspiration, code snippets, etc.
* [stream-exporter](https://github.com/carlpett/stream_exporter)