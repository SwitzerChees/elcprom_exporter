# ELCprom Exporter

## Description

> This project can be used to create a stateful connection between logstash (or other streaming pipelines) and prometheus.

## Getting Started

### Dependencies

* \>= python 3.8.x
* All packages installed from the **requirements.txt** file

### Installing

* Pull this repository
* Configure youre needed states in the **stytes.yml** file
* Run the **gunicorn** in the root folder with the command
    - ``gunicorn -w 1 wsgi:app --bind 0.0.0.0:9000``
* Alternative build the container with the **DOCKERFILE**
    - ``docker build <name-of-container-image> .``

### States

The states can be used to implement a state between an event stream for example from logstash and prometheus.

```yaml
- name: bgp_state #The name as prometheus metric
  decription: State that holds information about bgp state errors
  type: increment #Increment means 
  parse_fields: #Which fields to parse from 
    - errorcode
  label_fields: #Labels to use for grouping the counter
    - edge
    - host
  inc_pattern: 30902 #If this regex pattern appears the state increases
  dec_pattern: 30901 #If this regex pattern appears the state decreases
```

### API

The exporter provides a very simple HTTP API with the follwoing endpoints.

> **/states** (POST): Accepts JSON Payloads these payloads can be used to manipulate the state of a defined state.

> **/metrics** (GET): The scrape endpoint for prometheus. 

## License

This project is licensed under the Apache Version 2.0 License - see the LICENSE file for details.

## Acknowledgments

Inspiration, code snippets, etc.
* [stream-exporter](https://github.com/carlpett/stream_exporter)