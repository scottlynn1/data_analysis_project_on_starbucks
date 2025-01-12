#!/bin/bash


grep -n "$1" abstracted_links_2.txt | cut -d':' -f 1


