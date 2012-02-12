#!/bin/bash
(echo; echo -n "("; cat dragon.scm; echo " ${1:-10})") | python run.py
