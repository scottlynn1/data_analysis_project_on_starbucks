#!/bin/bash


grep -n "$1" abstracted_links.txt | cut -d':' -f 1


